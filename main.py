from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
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
        # Connect login button
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
        # Load settings page (delta.ui) as a class
        self.next_window = SettingsWindow()
        self.next_window.window.show()
        self.window.close()

class SettingsWindow:
    def __init__(self):
        loader = QUiLoader()
        ui_file = QFile("ui/delta.ui")
        ui_file.open(QFile.ReadOnly)
        self.window = loader.load(ui_file)
        ui_file.close()
        # Connect buttons to their respective methods
        self.window.pushButton.clicked.connect(self.install_singularity)
        self.window.pushButton_2.clicked.connect(self.set_mode)
        self.window.toolButton.clicked.connect(self.browse_directory)
        self.window.pushButton_3.clicked.connect(self.logout)

    def install_singularity(self):
        # TODO: Implement Singularity installation logic
        QMessageBox.information(self.window, "Install", "Install Singularity clicked.")

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
        # TODO: Implement directory browsing logic
        QMessageBox.information(self.window, "Browse", "Browse directory clicked.")

    def logout(self):
        # Call CLI logout command and redirect to login page
        import subprocess
        try:
            subprocess.run(["scientiflow-cli", "--logout"], check=True)
        except Exception as e:
            QMessageBox.warning(self.window, "Logout", f"Logout failed: {e}")
        # Show login window again
        self.window.close()
        self.login_window = LoginWindow()
        self.login_window.window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = LoginWindow()
    login.window.show()
    sys.exit(app.exec())
