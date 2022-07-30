from PyQt5.uic.properties import QtWidgets
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import dload
from PyQt5 import *
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
import os
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
import chromedriver_autoinstaller
from os import environ


UI = uic.loadUiType("UI.ui")[0]

class MainWindow(QtWidgets.QMainWindow,UI):
    def __init__(self):
        super().__init__()
        self.setFixedSize(623, 681)
        self.initUI()
        self.setWindowTitle("DtoD")
        self.selectDir.clicked.connect(self.fileFunc)
        self.DirButtonIcon()
        self.setWindowIcon(QIcon('./imgs/logo.jpg'))
        self.startButton.clicked.connect(self.saveImg)
        self.minN = self.MIN.value()
        self.maxN = self.MAX.value()
        self.saveMM.clicked.connect(self.getmm)
        self.errorornotStyle()
        self.success = False
        self.Readme.clicked.connect(self.startReadme)

    def initUI(self):
        self.setupUi(self)

    def fileFunc(self):
        self.folder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.showDir.setText(f"Directory : {self.folder}")

    def DirButtonIcon(self):
        pixmap = QPixmap('./imgs/folder.png')
        pixmap = pixmap.scaled(31,31)
        icon = QIcon()
        icon.addPixmap(pixmap)
        self.selectDir.setIcon(icon)
        self.selectDir.setIconSize(QSize(31,31))

    def saveImg(self):
        try :
            chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
            try:
                driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe')
            except:
                chromedriver_autoinstaller.install(True)
                driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe')
            driver.get(self.URL.toPlainText())
            req = driver.page_source
            soup = BeautifulSoup(req, 'html.parser')
            for i in range(self.minN, self.maxN + 1) :
                imgs = soup.select(
                    f'#package_detail > div.pop_content.dccon_popinfo > div.dccon_list_wrap.clear > div > ul > li:nth-child({i}) > span > img')
                if imgs == []:
                    break
                for im in imgs:
                    img = im['src']
                    imgtitle = im['title']
                    imgtitle = imgtitle.replace("?","")
                    dload.save(img, f'{self.folder}/{imgtitle}')
                file = open(f'{self.folder}/{imgtitle}','rb')
                magic = file.read(11)
                file.close()
                if magic.hex() == '47494638396164006400f7' :
                    os.rename(f'{self.folder}/{imgtitle}',f'{self.folder}/{imgtitle}.gif')
                elif magic.hex() == '89504e470d0a1a0a000000' :
                    os.rename(f'{self.folder}/{imgtitle}',f'{self.folder}/{imgtitle}.jpg')
            driver.quit()
            self.errorornot.setStyleSheet(
                "color: #4D69E8; border-style: solid; border-width: 2px; border-color: #54A0FF; border-radius: 10px; ")
            self.errorornot.setText("SUCCESS !!")
        except:
            driver.quit()
            QMessageBox.critical(self, "Notice", "ERROR !!")
            self.errorornot.setStyleSheet(
                "color: #FF0000; border-style: solid; border-width: 2px; border-color: #FFC300; border-radius: 10px; ")
            self.errorornot.setText("ERROR !!")
    def getmm(self):
        self.minN = self.MIN.value()
        self.maxN = self.MAX.value()

    def errorornotStyle(self):
        self.errorornot.setStyleSheet("color: #00FF00; border-style: solid; border-width: 2px; border-color: #FFC300; border-radius: 10px; ")

    def startReadme(self):
        os.system('start ./Readme/ww.html')

def suppress_qt_warnings():   # 해상도별 글자크기 강제 고정하는 함수
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"

if __name__ == '__main__':
    suppress_qt_warnings()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())