from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QFileDialog, QWidget, QTableWidgetItem,
    QCheckBox, QHBoxLayout
)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtCore import Qt
from PySide6.QtCore import QThread, Signal
import sys, subprocess

# Try to import AuthService, show error if not available
try:
    from scientiflow_cli.services.auth_service import AuthService
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

class GammaWindow:
    def __init__(self):
        loader = QUiLoader()
        ui_file = QFile("ui/setup.ui")
        ui_file.open(QFile.ReadOnly)
        self.window = loader.load(ui_file)
        ui_file.close()
        self.window.pushButton.clicked.connect(self.handle_proceed)
        self.window.toolButton.clicked.connect(self.open_directory_dialog)
        # self.window.checkBox.stateChanged.connect(self.handle_checkbox)  # Removed, no such method

        self.base_directory = ""
        self.singularity_checked = False

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
        import subprocess
        import sys
        try:
            # Run the CLI in the selected directory and provide hostname as input
            result = subprocess.run(
                ["scientiflow-cli", "--set-base-directory"],
                input=f"{hostname}\n",
                text=True,
                cwd=directory,
                capture_output=True,
                check=True
            )
            if "Successfully set base directory" in result.stdout:
                QMessageBox.information(self.window, "Success", "Base directory and host name set successfully.")
                self.main_window = MainWindow()
                self.main_window.window.show()
                self.window.close()
            else:
                QMessageBox.critical(self.window, "Error", f"Unexpected CLI output: {result.stdout}\n{result.stderr}")
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self.window, "Error", f"Failed to set base directory or host name:\n{e.stderr}")

class JobsLoaderThread(QThread):
    jobs_loaded = Signal(list, list)  # headers, rows
    error = Signal(str)

    def run(self):
        import subprocess
        try:
            result = subprocess.run(["scientiflow-cli", "--list-jobs"], capture_output=True, text=True, check=True)
            output = result.stdout.strip().splitlines()
            table_lines = [line for line in output if line.strip().startswith("|") and "|" in line]
            if not table_lines:
                self.jobs_loaded.emit(["Message"], [["No jobs found."]])
                return
            headers = [h.strip() for h in table_lines[0].split("|")[1:-1]]
            rows = []
            for row_line in table_lines[2:]:
                columns = [col.strip() for col in row_line.split("|")[1:-1]]
                rows.append(columns)
            self.jobs_loaded.emit(headers, rows)
        except Exception as e:
            self.error.emit(str(e))

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

        # Load jobs when landing on jobs page
        self.show_jobs_page()

    def show_jobs_page(self):
        self.window.stackedWidget.setCurrentWidget(self.window.page_jobs)
        self.load_jobs_async()
        # Disconnect all slots from the execute button to avoid RuntimeWarning
        try:
            self.window.btn_execute.clicked.disconnect()
        except Exception:
            pass
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
        synchronous = self.window.radio_synchronous.isChecked()
        # If parallel, collect checked jobs; if synchronous, execute all
        if parallel:
            for row in range(table.rowCount()):
                widget = table.cellWidget(row, 0)
                if widget:
                    cb = widget.findChild(QCheckBox)
                    if cb and cb.isChecked():
                        job_id = table.item(row, 1).text()
                        job_ids.append(job_id)
            if not job_ids:
                QMessageBox.warning(self.window, "No Jobs Selected", "Please select at least one job to execute in parallel mode.")
                return
        else:
            # Synchronous or async: execute all jobs
            job_ids = [table.item(row, 1).text() for row in range(table.rowCount()) if table.item(row, 1)]
        cmd = ["scientiflow-cli", "--execute-jobs"]
        cmd.extend(job_ids)
        if parallel:
            cmd.append("--parallel")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            QMessageBox.information(self.window, "Jobs Execution", result.stdout or "Jobs executed.")
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self.window, "Execution Failed", e.stderr or str(e))

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
    login = LoginWindow()
    login.window.show()
    sys.exit(app.exec())
