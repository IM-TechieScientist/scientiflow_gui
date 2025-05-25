from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QFileDialog, QWidget
)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
import sys

# Try to import AuthService, show error if not available
try:
    from scientiflow_cli.services.auth_service import AuthService
except ImportError:
    AuthService = None

class LoginWindow:
    def __init__(self):
        loader = QUiLoader()
        ui_file = QFile("ui/beta.ui")
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
        ui_file = QFile("ui/gamma.ui")
        ui_file.open(QFile.ReadOnly)
        self.window = loader.load(ui_file)
        ui_file.close()
        self.window.pushButton.clicked.connect(self.handle_proceed)
        self.window.toolButton.clicked.connect(self.open_directory_dialog)
        self.window.checkBox.stateChanged.connect(self.handle_checkbox)

        self.base_directory = ""
        self.singularity_checked = False

    def open_directory_dialog(self):
        directory = QFileDialog.getExistingDirectory(self.window, "Select Base Directory")
        if directory:
            self.window.lineEdit.setText(directory)
            self.base_directory = directory
            self.dummy_set_base_directory(directory)

    def handle_checkbox(self, state):
        self.singularity_checked = bool(state)

    def handle_proceed(self):
        if self.singularity_checked:
            self.dummy_install_singularity()
        # Always go to main window after proceed
        self.main_window = MainWindow()
        self.main_window.window.show()
        self.window.close()

    def dummy_install_singularity(self):
        QMessageBox.information(self.window, "Install", "Dummy: Installing Singularity...")

    def dummy_set_base_directory(self, directory):
        QMessageBox.information(self.window, "Base Directory", f"Dummy: Set base directory to {directory}")

class MainWindow:
    def __init__(self):
        loader = QUiLoader()
        ui_file = QFile("ui/alpha.ui")
        ui_file.open(QFile.ReadOnly)
        self.window = loader.load(ui_file)
        ui_file.close()

        # Sidebar navigation
        self.window.btn_jobs.clicked.connect(lambda: self.window.stackedWidget.setCurrentWidget(self.window.page_jobs))
        self.window.btn_manage_containers.clicked.connect(lambda: self.window.stackedWidget.setCurrentWidget(self.window.page_manage_containers))
        self.window.btn_settings.clicked.connect(self.open_settings)
        self.window.btn_logout.clicked.connect(self.logout)

        # Default to jobs page
        self.window.stackedWidget.setCurrentWidget(self.window.page_jobs)

        self.settings_window = None

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
        ui_file = QFile("ui/delta.ui")
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
