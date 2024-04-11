import icons_rc
from jendela_loading import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QApplication, QMainWindow
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import traceback
import keyboard
import pyperclip
import pyautogui
import time
import os


import openai
from openai import Completion



class Worker_Sinyal_Cari_Jawaban(QObject):
        finished = pyqtSignal()
        error = pyqtSignal(tuple)
        result = pyqtSignal(object)
        progress = pyqtSignal(int)


class Worker_Cari_Jawaban(QRunnable):
        def __init__(self, fn, *args, **kwargs):
                super(Worker_Cari_Jawaban, self).__init__()
                self.fn1 = fn
                self.args1 = args
                self.kwargs1 = kwargs
                self.signals1 = Worker_Sinyal_Cari_Jawaban()
                self.kwargs1['Kemajuan_Jawaban'] = self.signals1.progress

        @pyqtSlot()
        def run(self):
                try:
                        result1 = self.fn1(*self.args1, **self.kwargs1)
                except:
                        traceback.print_exc()
                        exctype, value = sys.exc_info()[:2]
                        self.signals1.error.emit((exctype, value, traceback.format_exc()))
                else:
                        self.signals1.result.emit(result1)
                finally:
                        self.signals1.finished.emit()


class SinyalWorkerHotkey(QObject):
        finished = pyqtSignal()
        error = pyqtSignal(tuple)
        result = pyqtSignal(object)
        progress = pyqtSignal(int)


class Worker_Hotkey(QRunnable):
        def __init__(self, fn, *args, **kwargs):
                super(Worker_Hotkey, self).__init__()
                self.fn10 = fn
                self.args10 = args
                self.kwargs10 = kwargs
                self.signals10 = SinyalWorkerHotkey()
                self.kwargs10['Kemajuan_Hotkey'] = self.signals10.progress

        @pyqtSlot()
        def run(self):
                try:
                        result10 = self.fn10(*self.args10, **self.kwargs10)
                except:
                        traceback.print_exc()
                        exctype, value = sys.exc_info()[:2]
                        self.signals10.error.emit((exctype, value, traceback.format_exc()))
                else:
                        self.signals10.result.emit(result10)
                finally:
                        self.signals10.finished.emit()




class Jendela_Utama(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(Jendela_Utama, self).__init__(*args, **kwargs)
        self.setObjectName("LACIA")
        
        self.ThreadCariJawaban = QThreadPool()
        self.ThreadHotkey = QThreadPool()
        
        self.API_KEY = "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"
        
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.resize(466, 764)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.setFont(font)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setIconSize(QtCore.QSize(30, 30))
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setMovable(True)
        self.tabWidget.setObjectName("tabWidget")
        self.LACIA = QtWidgets.QWidget()
        self.LACIA.setObjectName("LACIA")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.LACIA)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.widget = QtWidgets.QWidget(self.LACIA)
        self.widget.setObjectName("widget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.TombolTanya = QtWidgets.QPushButton(self.widget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/codesandbox.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.TombolTanya.setIcon(icon)
        self.TombolTanya.setIconSize(QtCore.QSize(30, 30))
        self.TombolTanya.setFlat(True)
        self.TombolTanya.setObjectName("TombolTanya")
        self.TombolTanya.clicked.connect(self.Jawab)
        self.gridLayout_3.addWidget(self.TombolTanya, 1, 2, 1, 1)
        self.TombolBersihkan = QtWidgets.QPushButton(self.widget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/delete.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.TombolBersihkan.setIcon(icon1)
        self.TombolBersihkan.setIconSize(QtCore.QSize(30, 30))
        self.TombolBersihkan.setFlat(True)
        self.TombolBersihkan.setObjectName("TombolBersihkan")
        self.gridLayout_3.addWidget(self.TombolBersihkan, 1, 1, 1, 1)
        self.TombolRiwayat = QtWidgets.QPushButton(self.widget)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icons/layers.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.TombolRiwayat.setIcon(icon2)
        self.TombolRiwayat.setIconSize(QtCore.QSize(30, 30))
        self.TombolRiwayat.setFlat(True)
        self.TombolRiwayat.setObjectName("TombolRiwayat")
        self.gridLayout_3.addWidget(self.TombolRiwayat, 1, 0, 1, 1)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.TextTanya = QtWidgets.QPlainTextEdit(self.widget)
        self.TextTanya.setFont(font)
        self.TextTanya.setStyleSheet("background: transparent")
        self.TextTanya.setTabChangesFocus(False)
        self.TextTanya.setBackgroundVisible(False)
        self.TextTanya.setObjectName("TextTanya")
        self.gridLayout_3.addWidget(self.TextTanya, 3, 0, 1, 3)
        self.label_7 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 2, 0, 1, 3)
        self.gridLayout_2.addWidget(self.widget, 0, 0, 1, 1)
        self.widget_2 = QtWidgets.QWidget(self.LACIA)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.widget_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.TextJawab = QtWidgets.QPlainTextEdit(self.widget_2)
        self.TextJawab.setFont(font)
        self.TextJawab.setStyleSheet("background: transparent")
        self.TextJawab.setReadOnly(True)
        self.TextJawab.setObjectName("TextJawab")
        self.verticalLayout.addWidget(self.TextJawab)
        self.gridLayout_2.addWidget(self.widget_2, 1, 0, 1, 1)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/icons/codepen.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.LACIA, icon3, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.widget_3 = QtWidgets.QWidget(self.tab_2)
        self.widget_3.setObjectName("widget_3")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.widget_3)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_2 = QtWidgets.QLabel(self.widget_3)
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("icon.ico"))
        self.label_2.setScaledContents(False)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout_5.addWidget(self.label_2, 0, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.widget_3)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout_5.addWidget(self.label_4, 2, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.widget_3)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout_5.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.widget_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout_5.addWidget(self.label_5, 3, 0, 1, 1)
        self.gridLayout_4.addWidget(self.widget_3, 0, 0, 1, 1)
        self.widget_4 = QtWidgets.QWidget(self.tab_2)
        self.widget_4.setObjectName("widget_4")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.widget_4)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.TombolPenggunaan = QtWidgets.QPushButton(self.widget_4)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/icons/globe.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.TombolPenggunaan.setIcon(icon4)
        self.TombolPenggunaan.setIconSize(QtCore.QSize(30, 30))
        self.TombolPenggunaan.setFlat(True)
        self.TombolPenggunaan.setObjectName("TombolPenggunaan")
        self.TombolPenggunaan.clicked.connect(self.penggunaan)
        self.gridLayout_6.addWidget(self.TombolPenggunaan, 1, 1, 1, 1)
        self.TombolUpdate = QtWidgets.QPushButton(self.widget_4)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/icons/refresh-cw.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.TombolUpdate.setIcon(icon5)
        self.TombolUpdate.setIconSize(QtCore.QSize(30, 30))
        self.TombolUpdate.setFlat(True)
        self.TombolUpdate.setObjectName("TombolUpdate")
        self.TombolUpdate.clicked.connect(self.update)
        self.gridLayout_6.addWidget(self.TombolUpdate, 1, 0, 1, 1)
        self.LinkTelegram = QtWidgets.QLineEdit(self.widget_4)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.LinkTelegram.setFont(font)
        self.LinkTelegram.setStyleSheet("background-color: transparent")
        self.LinkTelegram.setFrame(False)
        self.LinkTelegram.setAlignment(QtCore.Qt.AlignCenter)
        self.LinkTelegram.setReadOnly(True)
        self.LinkTelegram.setClearButtonEnabled(False)
        self.LinkTelegram.setObjectName("LinkTelegram")
        self.gridLayout_6.addWidget(self.LinkTelegram, 0, 0, 1, 2)
        self.gridLayout_4.addWidget(self.widget_4, 2, 0, 1, 1)
        self.widget_5 = QtWidgets.QWidget(self.tab_2)
        self.widget_5.setObjectName("widget_5")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.widget_5)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.plainTextEdit_3 = QtWidgets.QPlainTextEdit(self.widget_5)
        self.plainTextEdit_3.setFont(font)
        self.plainTextEdit_3.setStyleSheet("background-color: transparent")
        self.plainTextEdit_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.plainTextEdit_3.setReadOnly(True)
        self.plainTextEdit_3.setBackgroundVisible(False)
        self.plainTextEdit_3.setCenterOnScroll(False)
        self.plainTextEdit_3.setObjectName("plainTextEdit_3")





        self.gridLayout_7.addWidget(self.plainTextEdit_3, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.widget_5, 1, 0, 1, 1)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/icons/info.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab_2, icon6, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 1, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.tabWidget.setCurrentIndex(0)

        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "L.A.I.C.I.A"))
        self.TombolTanya.setText(_translate("MainWindow", "Tanya"))
        self.TombolBersihkan.setText(_translate("MainWindow", "Bersihkan"))
        self.TombolRiwayat.setText(_translate("MainWindow", "Riwayat"))
        self.label_7.setText(_translate("MainWindow", "Apa yang dapat saya bantu ?"))
        self.label.setText(_translate("MainWindow", "Jawaban"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.LACIA), _translate("MainWindow", "L.A.I.C.I.A"))
        self.label_4.setText(_translate("MainWindow", "Learning Artificial Companion with Intelligent Abilities"))
        self.label_3.setText(_translate("MainWindow", "L.A.I.C.I.A"))
        self.label_5.setText(_translate("MainWindow", "Version 1.0 | Designed by Arif Maulana"))
        self.TombolPenggunaan.setText(_translate("MainWindow", "How to Use ?"))
        self.TombolUpdate.setText(_translate("MainWindow", "Update"))
        self.LinkTelegram.setText(_translate("MainWindow", "Link Telegram : "))
        self.plainTextEdit_3.setPlainText(_translate("MainWindow", ""))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "About"))
        self.label_6.setText(_translate("MainWindow", "Copyright Titan Digitalsoft 2023"))
        
        self.LinkTelegram.hide()
        self.TombolRiwayat.hide()
        
        self.TombolBersihkan.clicked.connect(self.TextTanya.clear)
        self.TombolBersihkan.clicked.connect(self.TextJawab.clear)
        QtCore.QMetaObject.connectSlotsByName(self)
        
        workerHotkey = Worker_Hotkey(self.Jalankan_Hotkey)
        self.ThreadHotkey.start(workerHotkey)
        
        
        
    
    def Thread_Jawab(self, Kemajuan_Jawaban):
        openai.api_key = self.API_KEY
        self.pertanyaan = self.TextTanya.toPlainText()
        
        self.jawaban = Completion.create(
        model="text-davinci-003",
        prompt= f"""Return answer into indonesian language {self.pertanyaan}""",
        temperature=0,
        max_tokens=1200,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
        )
        
        
        Kemajuan_Jawaban.emit(100)
        
        
    def CetakProsesJawab(self, Proses_Jawab):
        pass
    
    def SelesaiJawab(self):
        self.Jendela_Loading.close()
        self.TombolBersihkan.setEnabled(True)
        self.TombolPenggunaan.setEnabled(True)
        self.TombolRiwayat.setEnabled(True)
        self.TombolTanya.setEnabled(True)
        self.TombolUpdate.setEnabled(True)
        try:
            self.TextJawab.setPlainText(self.jawaban.choices[0].text)
        except:
            self.TextJawab.setPlainText("Mohon periksa koneksi internet anda")
            pass
        
    def ProsesMenjawab(self, Proses_Jawab):
        self.TombolBersihkan.setEnabled(False)
        self.TombolPenggunaan.setEnabled(False)
        self.TombolRiwayat.setEnabled(False)
        self.TombolTanya.setEnabled(False)
        self.TombolUpdate.setEnabled(False)
        pass

    def Jawab(self):
        self.TextJawab.clear()
        self.TombolBersihkan.setEnabled(False)
        self.TombolPenggunaan.setEnabled(False)
        self.TombolRiwayat.setEnabled(False)
        self.TombolTanya.setEnabled(False)
        self.TombolUpdate.setEnabled(False)
        workerjawab = Worker_Cari_Jawaban(self.Thread_Jawab)
        workerjawab.signals1.result.connect(self.CetakProsesJawab)
        workerjawab.signals1.finished.connect(self.SelesaiJawab)
        workerjawab.signals1.progress.connect(self.ProsesMenjawab)
        self.ThreadCariJawaban.start(workerjawab)
        try:
            loading_window = jendelaloading()
            self.Jendela_Loading = QDialog(self)
            self.Jendela_Loading.setWindowTitle("Sabar ya...")
            layout_loading = QVBoxLayout()
            layout_loading.addWidget(loading_window)
            self.Jendela_Loading.setLayout(layout_loading)
            self.Jendela_Loading.exec_()
        except:
            pass


    def Thread_jalankan_Hotkey(self):
        self.TextTanya.clear()
        self.TextJawab.clear()
        try:
            openai.api_key = self.API_KEY
            time.sleep(0.3)
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.3)
            tanya = pyperclip.paste()
            pyautogui.press('down', interval=0.01)
            time.sleep(0.1)
            pyautogui.press('enter', interval=0.01)
            time.sleep(0.1)
            pyautogui.write("Sabar ya", interval=0.01)
            text = f"""{tanya}"""
            self.response = Completion.create(
            model="text-davinci-003",
            prompt=f"""Return answer into indonesian language {text}""",
            temperature=0,
            max_tokens=1200,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
            )
            time.sleep(0.3)
            pyautogui.press('backspace', presses=8, interval=0.01)
            time.sleep(0.1)
            pyautogui.typewrite(self.response.choices[0].text, interval=0.01)
            self.TextTanya.setPlainText(str(text))
            self.TextJawab.setPlainText(self.response.choices[0].text)

        except:
            self.TextTanya.setPlainText("Mohon periksa koneksi internet anda")
            self.TextJawab.setPlainText("Mohon periksa koneksi internet anda")
            pass
    
    def Jalankan_Hotkey(self, Kemajuan_Hotkey):
        keyboard.add_hotkey('alt+x', self.Thread_jalankan_Hotkey)
        keyboard.wait()
        Kemajuan_Hotkey.emit(100)


    def penggunaan(self):
        try:
            os.system('start {}'.format('https://drive.google.com/drive/folders/1Bin3jmPg_SSeZkIKeLCOCM9mIJZ9bMwd?usp=share_link'))
        except:
            pass


    def update(self):
        try:
            os.system('start {}'.format('https://drive.google.com/drive/folders/1cfhWGWl8QGRgx3RWrhbe0x779riv_LGs?usp=share_link'))
        except:
            pass


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = Jendela_Utama()
    window.setWindowTitle("L.A.I.C.I.A")
    window.show()
    sys.exit(app.exec_())
