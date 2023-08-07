import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
import pytesseract
# import cv2
import time
from pyaspeller import YandexSpeller
from pyaspeller import Word

speller = YandexSpeller(lang='ru')
speller_eng = YandexSpeller(lang='en')
language = 'rus'

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# def image_remake(image_path):
#     img = cv2.imread(image_path)
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     ret, thresh1 = cv2.threshold(
#         gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
#     cv2.imwrite(image_path, thresh1)


def to_string(file_path):
    global language
    return pytesseract.image_to_string(file_path, language)

def change_lang(text):
    global language
    if text == 'Русский':
        language = 'rus'
    elif text == 'English':
        language = 'eng'

def check_text(text):
    global language
    global speller
    global speller_eng
    if language == 'rus':
        return speller.spelled(text)
    elif language == 'eng':
        return speller_eng.spelled(text)
    
def check_words(text):
    global language
    global speller
    global speller_eng
    if language == 'rus':
        return speller.spell(text)
    elif language == 'eng':
        return speller_eng.spell(text)
    
    


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(840, 680)
        MainWindow.setMinimumSize(QtCore.QSize(840, 680))
        MainWindow.setStyleSheet("QMainWindow{\n"
                                 "    background-color:rgb(14, 22, 33);\n"
                                 "    color:rgb(245, 245, 245);\n"
                                 "}\n"
                                 "QProgressBar{\n"
                                 "    color:rgb(245, 245, 245);\n"
                                 "    background-color:rgb(24, 37, 51);\n"
                                 "}\n"
                                 "QLabel{\n"
                                 "    color:rgb(245, 245, 245)\n"
                                 "}\n"
                                 "QPlainTextEdit{\n"
                                 "    background-color:rgb(24, 37, 51);\n"
                                 "    color:rgb(245, 245, 245);\n"
                                 "    font-size: 24px;\n"
                                 "}\n"
                                 "QComboBox{\n"
                                 "    background-color:rgb(24, 37, 51);\n"
                                 "    color:rgb(245, 245, 245);\n"
                                 "}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.verticalLayout.addWidget(self.comboBox)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout.addWidget(self.plainTextEdit)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Design_checker"))
        self.label_2.setText(_translate(
            "MainWindow", "Для проверки текста на изображении выберите язык текста и  перетащите документ в окно программы."))
        self.comboBox.setItemText(0, _translate("MainWindow", "Русский"))
        self.comboBox.addItem('Русский')
        self.comboBox.setItemText(1, _translate("MainWindow", "English"))
        self.comboBox.activated[str].connect(change_lang)


class ExampleApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("design_check")
        self.setupUi(self)
        self.plainTextEdit.setReadOnly(True)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        # Тут выполняются проверки и дается (или нет) разрешение на Dr
        event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                ocr_text = to_string(file_path)
                ocr_text_wrong = check_words(ocr_text)
                self.plainTextEdit.clear()
                self.plainTextEdit.appendPlainText(ocr_text)
                self.plainTextEdit.appendPlainText(check_text(ocr_text))
                for elem in ocr_text_wrong:
                    self.plainTextEdit.appendPlainText('ошибка: ' + elem['word'] + " варианты: " + ' '.join(elem['s']))
                for i in range(100):
                    self.progressBar.setProperty('value', i)
                    time.sleep(0.01)
                self.progressBar.setProperty('value', 0)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
