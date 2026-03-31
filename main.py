import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QHBoxLayout, QLineEdit, QPushButton, QFileDialog

class convertor:
    def convert(self, nume_fisier):
        with open(nume_fisier, "r", encoding='utf-8') as f:
            try:
                self.continut = f.read().strip()
            except:
                print("Fisierul nu este suportat")
                return

        self.blocuri = self.continut.split('\n\n')

        titlu = self.blocuri[0].replace('\n', '').strip()
        paragrafe = self.blocuri[1:]

        self.html = f"""<!DOCTYPE html>
        <head>
            <meta charset="UTF-8">
            <title>{titlu}</title>
        </head>
        <body>
            <h1>{titlu}</h1>
        """

        for paragraf in paragrafe:
            paragraf = paragraf.replace('\n', '').strip()
            self.html += f"  <p>{paragraf}</p>\n"
        self.html += "</body>\n</html>"

    def salvare(self, fisier_iesire):
        with open(fisier_iesire, 'w', encoding='utf-8') as f:
            f.write(self.html)
            print(f"Fisierul a fost creat")

    def procesare(self, f_in, f_out):
        self.convert(f_in)
        self.salvare(f_out)

class app(QApplication):
    text = ""
    conv = convertor()

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
        self.procesare()

    def path_text_box(self):
        self.text = self.text_box.text()
        self.text_box.clear()
        print(self.text)
        self.procesare()

    def check_type(self):
        if self.text.endswith(".txt"):
            return True
        return False

    def procesare(self):
        if self.check_type():
            self.conv.salvare(self.text)
        else:
            print("Fisierul nu este suportat")


x = app()
x.open()

