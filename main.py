import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QHBoxLayout, QLineEdit, QPushButton, QFileDialog

class app(QApplication):
    text = ""

    def __init__(self):
        super().__init__(sys.argv)
        self.fereastra = QWidget()
        self.fereastra.setWindowTitle("Aplicatie smechera")
        self.fereastra.resize(400, 300)

        self.text_box = QLineEdit()
        self.text_box.setPlaceholderText("/home/constantin/PP/")
        self.text_box.returnPressed.connect(self.path_text_box)

        self.button = QPushButton("Browse")
        self.button.clicked.connect(self.button_browse)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.text_box)
        self.layout.addWidget(self.button)
        self.fereastra.setLayout(self.layout)

    def open(self):
        self.fereastra.show()
        sys.exit(app.exec_())


    def button_browse(self):
        path, _ = QFileDialog.getOpenFileName(None, "Selecteaza fisier", "")
        self.text = str(path)
        print(self.text)

    def path_text_box(self):
        self.text = self.text_box.text()
        self.text_box.clear()
        print(self.text)

x = app()
x.open()

