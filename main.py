import sys
import sysv_ipc
from PyQt5.QtGui import QTextBlock
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QHBoxLayout, QLineEdit, QPushButton, \
    QFileDialog, QTextEdit, QFormLayout


class sender:

    def __init__(self):
        try:
            self.message_queue = sysv_ipc.MessageQueue(123321)
        except sysv_ipc.ExistentialError:
            print("Message queue not initialized. Please run the C program first")

    def send_message(self, message):
        self.message_queue.send(message)

    def trimite(self, content):
        self.message_queue.send(content)
        print("Mesajul a fost trimis cu succes in queue")




class convertor:
    def convert(self, nume_fisier):
        if self.check_type(nume_fisier) == False:
            print("Fisierul nu are formatul corespunzator")
            return
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

        print("Fisierul a fost convertit cu succes la HTML")
        return self.html

    def check_type(self, cale_fisier):
        if cale_fisier.endswith(".txt"):
            return True
        return False

class app(QApplication):
    text = ""
    conv = convertor()
    send_er = sender()

    def __init__(self):
        super().__init__(sys.argv)
        self.fereastra = QWidget()
        self.fereastra.setWindowTitle("Aplicatie smechera")
        self.fereastra.resize(400, 300)

        self.text_box = QLineEdit()
        self.text_box.setPlaceholderText("/home/constantin/PP/")
        self.text_box.returnPressed.connect(self.path_text_box)

        self.afisare = QTextEdit()
        self.afisare.setReadOnly(True)
        self.afisare.setPlaceholderText("Aici va aparea formatul HTML")

        self.button1 = QPushButton("Browse")
        self.button1.clicked.connect(self.button_browse)

        self.button2 = QPushButton("Convert to HTML")
        self.button2.clicked.connect(lambda: self.conv.convert(self.text))

        self.button3 = QPushButton("Send to C")
        self.button3.clicked.connect(lambda: self.send_er.trimite(self.conv.html))

        self.button4 = QPushButton("Afisare HTML")
        self.button4.clicked.connect(lambda: self.afisare_format_html("mesaj_salvat.html"))

        self.layout = QFormLayout()
        self.layout.addWidget(self.text_box)
        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.button2)
        self.layout.addWidget(self.button3)
        self.layout.addWidget(self.button4)
        self.layout.addWidget(self.afisare)
        self.fereastra.setLayout(self.layout)

    def open(self):
        self.fereastra.show()
        sys.exit(app.exec_())


    def button_browse(self):
        path, _ = QFileDialog.getOpenFileName(None, "Selecteaza fisier", "")
        self.text = str(path)
        print(self.text)
        #self.procesare()

    def path_text_box(self):
        self.text = self.text_box.text()
        self.text_box.clear()
        print(self.text)
        #self.procesare()

    def afisare_format_html(self, nume_fisier):
        with open(nume_fisier, "r", encoding='utf-8') as f:
            try:
                continut = f.read().strip()
            except:
                print("Fisierul nu este suportat")
                return
            self.afisare.setText(continut)

x = app()
x.open()
