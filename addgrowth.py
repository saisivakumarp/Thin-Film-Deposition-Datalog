# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 15:05:10 2020

@author: saisi
"""

from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import Qt
import sqlite3
import sys
import os
from PIL import Image
from PyQt5 import QtCore, QtWidgets

con = sqlite3.connect("pecvd.db")
cur = con.cursor()

defaultImg = 'addgrowth.png'

class AddGrowth(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Growth")
        self.setWindowIcon(QIcon('icons/pecvdicon.png'))
        self.setGeometry(450, 150, 700, 700)
        self.setFixedSize(self.size())
        self.UI()
        self.show()
    
    def UI(self):
        self.widgets()
        self.layouts()
        
    
    def widgets(self):
        #####Creating widgets#####
        #Top Layout#
        self.addFilmImg = QLabel()
        self.img = QPixmap('')
        self.addFilmImg.setPixmap(self.img)
        self.addFilmImg.setAlignment(Qt.AlignCenter)

        #Bottom Layout#
        self.growthDateEntry = QtWidgets.QDateEdit(calendarPopup=True)
        self.growthDateEntry.setDateTime(QtCore.QDateTime.currentDateTime())
        self.growthDateEntry.setDisplayFormat("yyyy/MM/dd")
        self.growthTitleEntry = QLineEdit()
        self.growthTitleEntry.setPlaceholderText("Enter the growth title")
        self.growthSubstrateEntry = QLineEdit()
        self.growthSubstrateEntry.setPlaceholderText("Enter the substrate type")
        self.growthTemperatureEntry = QLineEdit()
        self.growthTemperatureEntry.setPlaceholderText("Enter the substrate temperature")
        self.growthPressureEntry = QLineEdit()
        self.growthPressureEntry.setPlaceholderText("Enter the chamber pressure")
        self.growthPowerEntry = QLineEdit()
        self.growthPowerEntry.setPlaceholderText("Enter the plasma power")
        self.growthFlowEntry = QLineEdit()
        self.growthFlowEntry.setPlaceholderText("Enter the precursor flow")
        self.growthRefIndexEntry = QLineEdit()
        self.growthRefIndexEntry.setPlaceholderText("Enter the refractive index of film")
        self.growthThicknessEntry = QLineEdit()
        self.growthThicknessEntry.setPlaceholderText("Enter the thickness of film")
        self.growthSiliconEntry = QLineEdit()
        self.growthSiliconEntry.setPlaceholderText("Enter the % Si composition")
        self.growthCarbonEntry = QLineEdit()
        self.growthCarbonEntry.setPlaceholderText("Enter the % C composition")
        self.growthNitrogenEntry = QLineEdit()
        self.growthNitrogenEntry.setPlaceholderText("Enter the % N composition")
        self.growthOxygenEntry = QLineEdit()
        self.growthOxygenEntry.setPlaceholderText("Enter the % O composition")
        self.growthNotesEntry = QTextEdit()
        self.uploadBtn = QPushButton('Upload')
        self.uploadBtn.clicked.connect(self.uploadImg)
        self.submitBtn = QPushButton('Submit')
        self.submitBtn.clicked.connect(self.addGrowth)
    
    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()
        self.bottomFrame = QFrame()
        self.topLayout = QVBoxLayout()
        self.topFrame = QFrame()
        
        #Adding widgets to Layouts#
        #Top Layout#
        self.topLayout.addWidget(self.addFilmImg)
        self.topFrame.setLayout(self.topLayout)
        
        #Bottom or Form Layout#
        self.bottomLayout.addRow(QLabel("Date: "), self.growthDateEntry)
        self.bottomLayout.addRow(QLabel("Growth title: "), self.growthTitleEntry)
        self.bottomLayout.addRow(QLabel("Substrate: "), self.growthSubstrateEntry)
        self.bottomLayout.addRow(QLabel("Temperature (C): "), self.growthTemperatureEntry)
        self.bottomLayout.addRow(QLabel("Pressure (Torr): "), self.growthPressureEntry)
        self.bottomLayout.addRow(QLabel("Power (W): "), self.growthPowerEntry)
        self.bottomLayout.addRow(QLabel("Flow (sccm): "), self.growthFlowEntry)
        self.bottomLayout.addRow(QLabel("Refractive index: "), self.growthRefIndexEntry)
        self.bottomLayout.addRow(QLabel("Thickness (nm) : "), self.growthThicknessEntry)
        self.bottomLayout.addRow(QLabel("% Si: "), self.growthSiliconEntry)
        self.bottomLayout.addRow(QLabel("% C: "), self.growthCarbonEntry)
        self.bottomLayout.addRow(QLabel("% N: "), self.growthNitrogenEntry)
        self.bottomLayout.addRow(QLabel("% O: "), self.growthOxygenEntry)
        self.bottomLayout.addRow(QLabel("Notes "), self.growthNotesEntry)
        self.bottomLayout.addRow(QLabel(""), self.uploadBtn)
        self.bottomLayout.addRow(QLabel(""), self.submitBtn)
        self.bottomFrame.setLayout(self.bottomLayout)
        
        self.mainLayout.addWidget(self.topFrame, 20)
        self.mainLayout.addWidget(self.bottomFrame, 80)
        self.setLayout(self.mainLayout)

    def uploadImg(self):
        global defaultImg
        size = (128,128)
        self.filename, ok = QFileDialog.getOpenFileName(self, "Upload Image", "", "Image File (*.jpg *.png)")
        if ok:
            defaultImg = os.path.basename(self.filename)
            img = Image.open(self.filename)
            img = img.resize(size)
            img.save("img/{0}".format(defaultImg))
    
    def addGrowth(self):
        global defaultImg
        date = self.growthDateEntry.text()
        title = self.growthTitleEntry.text()
        substrate = self.growthSubstrateEntry.text()
        temperature = self.growthTemperatureEntry.text()
        pressure = self.growthPressureEntry.text()
        power = self.growthPowerEntry.text()
        flow = self.growthFlowEntry.text()
        refIndex = self.growthRefIndexEntry.text()
        thickness = self.growthThicknessEntry.text()
        percentSilicon = self.growthSiliconEntry.text()
        percentCarbon = self.growthCarbonEntry.text()
        percentNitrogen = self.growthNitrogenEntry.text()
        percentOxygen = self.growthOxygenEntry.text()
        notes = self.growthNotesEntry.toPlainText()
        
        if (date and title and substrate and temperature and pressure and power and flow != ""):
            try:
                query = ("INSERT INTO 'pecvd' (growth_date, growth_name, growth_substrate, growth_temperature, growth_pressure, growth_power, growth_flow, growth_refindex, growth_thickness, growth_si, growth_c, growth_n, growth_o, growth_notes, growth_img) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)")
                cur.execute(query, (date, title, substrate, temperature, pressure, power, flow, refIndex, thickness, percentSilicon, percentCarbon, percentNitrogen, percentOxygen, notes, defaultImg))
                con.commit()
                QMessageBox.information(self, "Info", "Growth has been added")
                self.close()
            except:
                QMessageBox.information(self, "Info", "Growth has not been added")
        else:
            QMessageBox.information(self, "Info", "Title, substrate and parameters cannot be empty")

def main():
    App = QApplication(sys.argv)
    window = AddGrowth()
    sys.exit(App.exec_())
    
if __name__ == '__main__':
    main()
