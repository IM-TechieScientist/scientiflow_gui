from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QFileDialog, QWidget, QTableWidgetItem,
    QCheckBox, QHBoxLayout
)

import qdarkstyle
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtCore import Qt
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QPixmap
import sys, subprocess, platform
from pathlib import Path

# Try to import Scientiflow-cli services, show error if not available
try:
    from scientiflow_cli.services.auth_service import AuthService
    from scientiflow_cli.pipeline.get_jobs import get_jobs
    from scientiflow_cli.pipeline.container_manager import get_available_containers, delete_selected_containers
    from scientiflow_cli.services.base_directory import set_base_directory, get_base_directory #need to replace subprocess call with set_base_directory
except ImportError:
    AuthService = None

class LoginWindow:
    def __init__(self):
        loader = QUiLoader()
        ui_file = QFile("ui/login.ui")
        ui_file.open(QFile.ReadOnly)
        self.window = loader.load(ui_file)
        ui_file.close()
        self.window.pushButton.clicked.connect(self.handle_login)
        self.window.label.setPixmap(QPixmap("scientiflow.jpg"))

    def handle_login(self):
        if AuthService is None:
            QMessageBox.critical(self.window, "Error", "AuthService not found. Please install scientiflow_cli.")
            return
        email = self.window.lineEdit.text()
        password = self.window.lineEdit_2.text()
        auth_service = AuthService()
        result = auth_service.login(email, password)
        if result.get('success'):
            self.open_next_window()
        else:
            QMessageBox.critical(self.window, "Incorrect Credentials", "Incorrect credentials. Please try again.")

    def open_next_window(self):
        self.next_window = GammaWindow()
        self.next_window.window.show()
        self.window.close()

class SingularityInstallerThread(QThread):
    finished = Signal(str, bool)  # message, success
    def __init__(self, enable_gpu=False):
        super().__init__()
        self.enable_gpu = enable_gpu
    def run(self):
    
        if platform.system() == "Windows":
            self.finished.emit("Singularity installation is only supported on Linux", False)
            return
        
        cmd = ["scientiflow-cli", "--install-singularity"]
        if self.enable_gpu:
            cmd.append("--enable-gpu")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            self.finished.emit(result.stdout or "Singularity installed successfully.", True)
        except subprocess.CalledProcessError as e:
            self.finished.emit(e.stderr or str(e), False)

class GammaWindow:
    def __init__(self):
        loader = QUiLoader()
        ui_file = QFile("ui/setup.ui")
        ui_file.open(QFile.ReadOnly)
        self.window = loader.load(ui_file)
        ui_file.close()
        self.window.pushButton.clicked.connect(self.handle_proceed)
        self.window.toolButton.clicked.connect(self.open_directory_dialog)
        self.window.checkBox.stateChanged.connect(self.handle_singularity_checkbox)
        self.window.checkBox_2.setEnabled(False)
        self.window.label.setPixmap(QPixmap("scientiflow.jpg"))
        self.singularity_thread = None
        self.base_directory = ""
        self.singularity_checked = False

    def handle_singularity_checkbox(self, state):
        self.window.checkBox_2.setEnabled(state == 2)

    def open_directory_dialog(self):
        directory = QFileDialog.getExistingDirectory(self.window, "Select Base Directory")
        if directory:
            self.window.lineEdit.setText(directory)
            self.base_directory = directory

    def handle_proceed(self):
        directory = self.window.lineEdit.text().strip()
        hostname = self.window.lineEdit_2.text().strip()
        if not directory or not hostname:
            QMessageBox.warning(self.window, "Input Required", "Both base directory and host name are required.")
            return
        try:
            result = subprocess.run(
                ["scientiflow-cli", "--set-base-directory"],
                input=f"{hostname}\n",
                text=True,
                cwd=directory,
                capture_output=True,
                check=True
            )
            if "Successfully set base directory" in result.stdout:
                if self.window.checkBox.isChecked():
                    self.window.pushButton.setEnabled(False)
                    self.singularity_thread = SingularityInstallerThread(self.window.checkBox_2.isChecked())
                    self.singularity_thread.finished.connect(self.on_singularity_installed)
                    QMessageBox.information(self.window, "Singularity Installation", "Installing Singularity, please wait...")
                    self.singularity_thread.start()
                else:
                    QMessageBox.information(self.window, "Success", "Base directory and host name set successfully.")
                    self.main_window = MainWindow()
                    self.main_window.window.show()
                    self.window.close()
            else:
                QMessageBox.critical(self.window, "Error", f"Unexpected CLI output: {result.stdout}\n{result.stderr}")
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self.window, "Error", f"Failed to set base directory or host name:\n{e.stderr}")

    def on_singularity_installed(self, message, success):
        self.window.pushButton.setEnabled(True)
        if success:
            QMessageBox.information(self.window, "Singularity Installation", message)
            self.main_window = MainWindow()
            self.main_window.window.show()
            self.window.close()
        else:
            QMessageBox.critical(self.window, "Singularity Installation Failed", message)

class JobsLoaderThread(QThread):
    jobs_loaded = Signal(list, list)  # headers, rows
    error = Signal(str)

    def run(self):
        try:
            # Call the get_jobs function directly
            jobs = get_jobs()

            if not jobs:
                self.jobs_loaded.emit(["Message"], [["No jobs found."]])
                return

            # Extract headers and rows from the jobs data
            headers = ["Project Job ID", "Project Title", "Job Title"]
            rows = []
            for job in jobs:
                project_job_id = str(job['project_job']['id'])
                project_title = job['project']['project_title']
                job_title = job['project_job']['job_title']
                rows.append([project_job_id, project_title, job_title])

            self.jobs_loaded.emit(headers, rows)

        except Exception as e:
            self.error.emit(f"Unexpected error: {str(e)}")

class JobExecutionThread(QThread):
    finished = Signal(str, bool)  # message, success

    def __init__(self, job_ids, parallel):
        super().__init__()
        self.job_ids = job_ids
        self.parallel = parallel

    def run(self):
        # Construct the CLI command
        cmd = ["scientiflow-cli", "--execute-jobs"] + self.job_ids
        if self.parallel:
            cmd.append("--parallel")

        try:
            print(f"Executing command: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            stdout = result.stdout.strip()
            print(f"Command output: {stdout}")
            self.finished.emit(stdout if stdout else "Jobs executed successfully.", True)
        except subprocess.CalledProcessError as e:
            stderr = e.stderr.strip() if e.stderr else "An error occurred while executing the jobs."
            self.finished.emit(stderr, False)

class MainWindow:
    def __init__(self):
        loader = QUiLoader()
        ui_file = QFile("ui/main.ui")
        ui_file.open(QFile.ReadOnly)
        self.window = loader.load(ui_file)
        ui_file.close()

        # Sidebar navigation
        self.window.btn_jobs.clicked.connect(self.show_jobs_page)
        self.window.btn_manage_containers.clicked.connect(lambda: self.window.stackedWidget.setCurrentWidget(self.window.page_manage_containers))
        self.window.btn_settings.clicked.connect(self.open_settings)
        self.window.btn_logout.clicked.connect(self.logout)

        # Default to jobs page
        self.window.stackedWidget.setCurrentWidget(self.window.page_jobs)
        self.settings_window = None
        self.jobs_loader_thread = None

        self.window.label.setPixmap(QPixmap("scientiflow.jpg"))

        # Load jobs when landing on jobs page
        self.show_jobs_page()
        self.window.btn_delete_containers.clicked.connect(self.delete_selected_containers)
        self.show_containers_page()

    def show_jobs_page(self):
        self.window.stackedWidget.setCurrentWidget(self.window.page_jobs)
        self.load_jobs_async()
        # Disconnect all slots from the execute button to avoid RuntimeWarning
        # try:
        #     self.window.btn_execute.clicked.disconnect()
        # except Exception:
        #     pass
        self.window.btn_execute.clicked.connect(self.execute_selected_jobs)
        # Connect radio buttons to toggle checkboxes column
        self.window.radio_parallel.toggled.connect(self.toggle_select_column)
        self.window.radio_synchronous.toggled.connect(self.toggle_select_column)
        # Initial toggle
        self.toggle_select_column()

    def toggle_select_column(self):
        table = self.window.table_jobs
        # Hide select column if synchronous, show if parallel
        show_select = self.window.radio_parallel.isChecked()
        if table.columnCount() > 0 and table.horizontalHeaderItem(0).text() == "Select":
            table.setColumnHidden(0, not show_select)

    def load_jobs_async(self):
        table = self.window.table_jobs
        table.setRowCount(0)
        table.setColumnCount(1)
        table.setHorizontalHeaderLabels(["Loading..."])
        table.setRowCount(1)
        table.setItem(0, 0, QTableWidgetItem("Loading jobs, please wait..."))

        self.jobs_loader_thread = JobsLoaderThread()
        self.jobs_loader_thread.jobs_loaded.connect(self.on_jobs_loaded)
        self.jobs_loader_thread.error.connect(self.on_jobs_error)
        self.jobs_loader_thread.start()

    def on_jobs_loaded(self, headers, rows):
        table = self.window.table_jobs
        table.setRowCount(0)
        # Add a checkbox column at the start
        headers = ["Select"] + headers
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        for i, row in enumerate(rows):
            table.insertRow(i)
            # Add checkbox in the first column
            checkbox = QWidget()
            layout = QHBoxLayout(checkbox)
            layout.setAlignment(Qt.AlignCenter)
            cb = QCheckBox()
            layout.addWidget(cb)
            layout.setContentsMargins(0, 0, 0, 0)
            table.setCellWidget(i, 0, checkbox)
            # Fill the rest of the columns
            for j, col in enumerate(row):
                item = QTableWidgetItem(col)
                item.setTextAlignment(Qt.AlignCenter)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                table.setItem(i, j + 1, item)
        self.toggle_select_column()

    def on_jobs_error(self, error_msg):
        table = self.window.table_jobs
        table.setRowCount(0)
        table.setColumnCount(1)
        table.setHorizontalHeaderLabels(["Error"])
        table.setRowCount(1)
        table.setItem(0, 0, QTableWidgetItem(f"Error loading jobs: {error_msg}"))

    def execute_selected_jobs(self):
        table = self.window.table_jobs
        job_ids = []
        parallel = self.window.radio_parallel.isChecked()

        if parallel:
            # Collect only selected jobs via checkboxes
            for row in range(table.rowCount()):
                widget = table.cellWidget(row, 0)
                if widget:
                    cb = widget.findChild(QCheckBox)
                    if cb and cb.isChecked():
                        job_id_item = table.item(row, 1)
                        if job_id_item:
                            job_ids.append(job_id_item.text())
            if not job_ids:
                QMessageBox.warning(self.window, "No Jobs Selected", "Please select at least one job to execute in parallel mode.")
                return
        else:
            # Synchronous mode: execute all jobs
            for row in range(table.rowCount()):
                job_id_item = table.item(row, 1)
                if job_id_item:
                    job_ids.append(job_id_item.text())

        if not job_ids:
            QMessageBox.warning(self.window, "No Jobs Found", "No jobs to execute.")
            return

        # Show a message box indicating execution has started
        QMessageBox.information(self.window, "Execution Started", f"Execution of {len(job_ids)} job(s) has started.")
        print(f"Executing jobs: {job_ids} in {'parallel' if parallel else 'synchronous'} mode.")
        # Start the job execution thread
        self.job_execution_thread = JobExecutionThread(job_ids, parallel)
        self.job_execution_thread.finished.connect(self.on_job_execution_finished)
        self.job_execution_thread.start()

    def on_job_execution_finished(self, message, success):
        if success:
            QMessageBox.information(self.window, "Execution Completed", message)
        else:
            QMessageBox.critical(self.window, "Execution Failed", message)


    def open_settings(self):
        self.settings_window = SettingsWindow()
        self.settings_window.window.show()

    def logout(self):
        # Call CLI logout command and redirect to login page
        import subprocess
        try:
            subprocess.run(["scientiflow-cli", "--logout"], check=True)
        except Exception as e:
            QMessageBox.warning(self.window, "Logout", f"Logout failed: {e}")
        self.window.close()
        self.login_window = LoginWindow()
        self.login_window.window.show()

    def append_log(self, message):
        self.window.textBrowser_logs.append(message)

    def show_containers_page(self):
        containers_dir = Path(get_base_directory()) / "containers"
        if not containers_dir.exists():
            containers_dir.mkdir()  
        try:
            containers = get_available_containers(containers_dir)
            table = self.window.table_containers
            table.setRowCount(0)
            table.setColumnCount(2)
            table.setHorizontalHeaderLabels(["Select", "Container Name"])

            for i, container_name in enumerate(containers):
                table.insertRow(i)

                # Add checkbox in the first column
                checkbox = QWidget()
                layout = QHBoxLayout(checkbox)
                layout.setAlignment(Qt.AlignCenter)
                cb = QCheckBox()
                layout.addWidget(cb)
                layout.setContentsMargins(0, 0, 0, 0)
                table.setCellWidget(i, 0, checkbox)

                # Add container name in the second column
                table.setItem(i, 1, QTableWidgetItem(container_name))

        except Exception as e:
            QMessageBox.critical(self.window, "Error", f"Failed to load containers: {e}")

    def delete_selected_containers(self):
        containers_dir = Path(get_base_directory()) / "containers"
        table = self.window.table_containers
        selected_indices = []
        container_names = []

        # Collect selected containers
        for row in range(table.rowCount()):
            widget = table.cellWidget(row, 0)
            if widget:
                cb = widget.findChild(QCheckBox)
                if cb and cb.isChecked():
                    container_name_item = table.item(row, 1)
                    if container_name_item:
                        selected_indices.append(row)
                        container_names.append(container_name_item.text())

        if not container_names:
            QMessageBox.warning(self.window, "No Containers Selected", "Please select at least one container to delete.")
            return

        # Confirm deletion
        reply = QMessageBox.question(
            self.window,
            "Confirm Deletion",
            f"Are you sure you want to delete {len(container_names)} container(s)?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.No:
            return

        # Delete containers
        try:
            results = delete_selected_containers(containers_dir, container_names, list(range(1, len(container_names) + 1)))
            success_count = 0
            for res in results:
                if res["status"] == "success":
                    success_count += 1
                else:
                    QMessageBox.warning(self.window, "Error", res["message"])

            QMessageBox.information(self.window, "Deletion Complete", f"Successfully deleted {success_count} container(s).")
            self.show_containers_page()  # Refresh the table

        except Exception as e:
            QMessageBox.critical(self.window, "Error", f"Failed to delete containers: {e}")

class SettingsWindow:
    def __init__(self):
        loader = QUiLoader()
        ui_file = QFile("ui/settings.ui")
        ui_file.open(QFile.ReadOnly)
        self.window = loader.load(ui_file)
        ui_file.close()
        self.window.pushButton.clicked.connect(self.install_singularity)
        self.window.pushButton_2.clicked.connect(self.set_mode)
        self.window.toolButton.clicked.connect(self.browse_directory)

    def install_singularity(self):
        QMessageBox.information(self.window, "Install", "Install Singularity clicked (dummy).")

    def set_mode(self):
        if self.window.radioButton.isChecked():
            mode = "Dark"
        elif self.window.radioButton_2.isChecked():
            mode = "Light"
        else:
            mode = None
        if mode:
            QMessageBox.information(self.window, "Mode", f"{mode} mode set.")
        else:
            QMessageBox.warning(self.window, "Mode", "Please select a mode.")

    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self.window, "Select Base Directory")
        if directory:
            self.window.lineEdit.setText(directory)
            self.dummy_set_base_directory(directory)

    def dummy_set_base_directory(self, directory):
        QMessageBox.information(self.window, "Base Directory", f"Dummy: Set base directory to {directory}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(palette=qdarkstyle.LightPalette))
    login = LoginWindow()
    login.window.show()
    sys.exit(app.exec())
