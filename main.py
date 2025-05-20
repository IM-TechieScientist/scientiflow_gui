from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
import sys

app = QApplication(sys.argv)

loader = QUiLoader()
ui_file = QFile("ui/beta.ui")
ui_file.open(QFile.ReadOnly)

window = loader.load(ui_file)
ui_file.close()

window.show()
sys.exit(app.exec())
