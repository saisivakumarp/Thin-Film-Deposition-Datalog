# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 14:08:45 2020

@author: saisi
"""
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import Qt
import sqlite3
import sys, os
import addgrowth, style
from PIL import Image
from PyQt5 import QtCore, QtWidgets
import pandas as pd


con = sqlite3.connect("pecvd.db")
cur = con.cursor()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Thin Film Deposition Log")
        self.setWindowIcon(QIcon("icons/pecvdicon.png"))
        self.setGeometry(450, 150, 1400, 750)
        self.UI()
        self.show()
    
    
    def UI(self):
        self.toolBar()
        self.tabWidgets()
        self.widgets()
        self.layouts()
        self.displayGrowths()

    def toolBar(self):
        self.tb = self.addToolBar("Tool Bar")
        self.tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        #####Tool bar Buttons #####
        #Add Growth#
        self.addGrowth = QAction(QIcon('icons/add_simple.png'), "Add Growth", self)
        self.addGrowth.triggered.connect(self.funcAddGrowth)
        self.tb.addAction(self.addGrowth)
        self.tb.addSeparator()
            
    def tabWidgets(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.tab1 = QWidget()
        self.tabs.addTab(self.tab1, "Deposition Log Book")
    
    def widgets(self):
        #####Tab1 Widgets#####
        # Main Left Layout Widget#
        self.growthsTable = QTableWidget()
        self.growthsTable.setColumnCount(16)
        self.growthsTable.setColumnHidden(0, True)
        self.growthsTable.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.growthsTable.setHorizontalHeaderItem(1, QTableWidgetItem("Date"))
        self.growthsTable.setHorizontalHeaderItem(2, QTableWidgetItem("Title"))
        self.growthsTable.setHorizontalHeaderItem(3, QTableWidgetItem("Substrate"))
        self.growthsTable.setHorizontalHeaderItem(4, QTableWidgetItem("Temperature"))
        self.growthsTable.setHorizontalHeaderItem(5, QTableWidgetItem("Pressure"))
        self.growthsTable.setHorizontalHeaderItem(6, QTableWidgetItem("Power"))
        self.growthsTable.setHorizontalHeaderItem(7, QTableWidgetItem("Flow"))
        self.growthsTable.setHorizontalHeaderItem(8, QTableWidgetItem("Refractive Index"))
        self.growthsTable.setHorizontalHeaderItem(9, QTableWidgetItem("Thickness"))
        self.growthsTable.setHorizontalHeaderItem(10, QTableWidgetItem("%Si"))
        self.growthsTable.setHorizontalHeaderItem(11, QTableWidgetItem("%C"))
        self.growthsTable.setHorizontalHeaderItem(12, QTableWidgetItem("%N"))
        self.growthsTable.setHorizontalHeaderItem(13, QTableWidgetItem("%O"))
        self.growthsTable.setHorizontalHeaderItem(14, QTableWidgetItem("Status"))
        self.growthsTable.setHorizontalHeaderItem(15, QTableWidgetItem("Notes"))
        self.growthsTable.horizontalHeader().setSectionResizeMode(8, QHeaderView.Stretch)
        self.growthsTable.horizontalHeader().setSectionResizeMode(15, QHeaderView.Stretch)
        self.growthsTable.doubleClicked.connect(self.selectedGrowth)
        
        #Right Top Widgets#
        self.searchText = QLabel('Search')
        self.searchEntry = QLineEdit()
        self.searchEntry.setPlaceholderText("By title, substrate and deposition params")
        self.searchButton = QPushButton("Search")
        self.searchButton.setStyleSheet(style.searchButtonStyle())
        self.searchButton.clicked.connect(self.searchGrowths)
        
        #Right Middle Widgets#
        self.allGrowths = QRadioButton('All growths')
        self.goodGrowths = QRadioButton('Good')
        self.delaminatedGrowths = QRadioButton('Delaminated')
        self.usedGrowths = QRadioButton('Used')
        self.listButton = QPushButton('List')
        self.listButton.setStyleSheet(style.listButtonStyle())
        self.listButton.clicked.connect(self.listGrowths)
        
        #Right Bottom Widgets#
        self.csvFormat = QRadioButton('*.csv')
        self.csvFormat.setChecked(True)
        self.textFormat = QRadioButton('*.txt')
        self.exportButton = QPushButton('Export')
        self.exportButton.clicked.connect(self.funExportGrowths)
        
      
    def layouts(self):
        #####Creating Main Layouts#####
        self.mainLayout = QHBoxLayout()
        self.mainLeftLayout = QVBoxLayout()
        self.mainRightLayout = QVBoxLayout()
        self.rightTopLayout = QHBoxLayout()
        self.rightMiddleLayout = QHBoxLayout()
        self.rightBottomLayout = QHBoxLayout()
        self.topGroupBox = QGroupBox("Search Box")
        self.topGroupBox.setStyleSheet(style.searchBoxStyle())
        self.middleGroupBox = QGroupBox("List Box")
        self.middleGroupBox.setStyleSheet(style.listBoxStyle())
        self.bottomGroupBox = QGroupBox("Export Data to CSV")
        self.bottomGroupBox.setStyleSheet(style.exportBoxStyle())
        
        #####Adding widgets to layouts#####
        ###Tab1 Layouts###
        #Left Main Layout#
        self.mainLeftLayout.addWidget(self.growthsTable)
        #Right Top Layout#
        self.rightTopLayout.addWidget(self.searchText)
        self.rightTopLayout.addWidget(self.searchEntry)
        self.rightTopLayout.addWidget(self.searchButton)
        self.topGroupBox.setLayout(self.rightTopLayout)
        #Right Middle Layout#
        self.rightMiddleLayout.addWidget(self.allGrowths)
        self.rightMiddleLayout.addWidget(self.goodGrowths)
        self.rightMiddleLayout.addWidget(self.delaminatedGrowths)
        self.rightMiddleLayout.addWidget(self.usedGrowths)
        self.rightMiddleLayout.addWidget(self.listButton)
        self.middleGroupBox.setLayout(self.rightMiddleLayout)
        #Right Bottom Layout#
        # self.rightBottomLayout.addStretch()
        self.rightBottomLayout.addWidget(self.csvFormat)
        self.rightBottomLayout.addWidget(self.textFormat)
        self.rightBottomLayout.addWidget(self.exportButton)
        # self.rightBottomLayout.addStretch()
        self.bottomGroupBox.setLayout(self.rightBottomLayout)
        #Setting Layouts to Main Window#
        self.mainLayout.addLayout(self.mainLeftLayout, 80)
        self.mainLayout.addLayout(self.mainRightLayout, 20)
        self.mainRightLayout.addWidget(self.topGroupBox, 20)
        self.mainRightLayout.addWidget(self.middleGroupBox, 20)
        self.mainRightLayout.addWidget(self.bottomGroupBox, 20)
        self.tab1.setLayout(self.mainLayout)

    def funcAddGrowth(self):
        self.newGrowth = addgrowth.AddGrowth()
    
    def displayGrowths(self):
        self.growthsTable.setFont(QFont("Times", 12))
        for i in reversed(range(self.growthsTable.rowCount())):
            self.growthsTable.removeRow(i)
        
        query = cur.execute("SELECT growth_id, growth_date, growth_name, growth_substrate, growth_temperature, growth_pressure, growth_power, growth_flow, growth_refindex, growth_thickness, growth_si, growth_c, growth_n, growth_o, growth_status, growth_notes, growth_img FROM pecvd")
        for row_data in query:
            row_number = self.growthsTable.rowCount()
            self.growthsTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.growthsTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
            
            self.growthsTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
            
    def selectedGrowth(self):
        global growthId
        listGrowths = []
        for i in range(0,15):
            listGrowths.append(self.growthsTable.item(self.growthsTable.currentRow(), i).text())
        growthId = listGrowths[0]
        self.display = DisplayGrowth()
        self.display.show()

    def searchGrowths(self):
        value = self.searchEntry.text()
        
        if value == "":
            QMessageBox.information(self, "Warning", "Search query can't be empty!!!")
        else:
            self.searchEntry.setText("")
            
            query = ("SELECT * FROM pecvd WHERE growth_name LIKE ? or growth_substrate LIKE ? or growth_temperature LIKE ? or growth_pressure LIKE ? or growth_power LIKE ? or growth_flow LIKE ? or growth_refindex LIKE ?")
            results = cur.execute(query, ('%' + value + '%', '%' + value + '%', '%' + value + '%', '%' + value + '%', '%' + value + '%', '%' + value + '%', '%' + value + '%')).fetchall()
            
            if results == []:
                QMessageBox.information(self, "Warning", "There is no such a growth.")
            else:
                for i in reversed(range(self.growthsTable.rowCount())):
                    self.growthsTable.removeRow(i)
                
                for row_data in results:
                    row_number = self.growthsTable.rowCount()
                    self.growthsTable.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.growthsTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
    
    def listGrowths(self):
        if self.allGrowths.isChecked() == True:
            self.displayGrowths()
            
        elif self.goodGrowths.isChecked():
            query = ("SELECT * FROM pecvd WHERE growth_status = 'Good'")
            growths = cur.execute(query).fetchall()
            
            for i in reversed(range(self.growthsTable.rowCount())):
                    self.growthsTable.removeRow(i)
                
            for row_data in growths:
                row_number = self.growthsTable.rowCount()
                self.growthsTable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.growthsTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        
        elif self.delaminatedGrowths.isChecked():
            query = ("SELECT * FROM pecvd WHERE growth_status = 'Delaminated'")
            growths = cur.execute(query).fetchall()
            
            for i in reversed(range(self.growthsTable.rowCount())):
                    self.growthsTable.removeRow(i)
                
            for row_data in growths:
                row_number = self.growthsTable.rowCount()
                self.growthsTable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.growthsTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        
        elif self.usedGrowths.isChecked():
            query = ("SELECT * FROM pecvd WHERE growth_status = 'Used'")
            growths = cur.execute(query).fetchall()
            
            for i in reversed(range(self.growthsTable.rowCount())):
                    self.growthsTable.removeRow(i)
                
            for row_data in growths:
                row_number = self.growthsTable.rowCount()
                self.growthsTable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.growthsTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                    
    def funExportGrowths(self):
        if self.csvFormat.isChecked():  
            query = ("SELECT growth_date, growth_name, growth_substrate, growth_temperature, growth_pressure, growth_power, growth_flow, growth_refindex, growth_thickness, growth_si, growth_c, growth_n, growth_o, growth_status, growth_notes FROM pecvd")
            dataFrame = pd.read_sql_query(query,con)
            self.filename, ok = QFileDialog.getSaveFileName(self, 'Save data', "", "CSV(*.csv)")
            if ok:
                dataFrame.to_csv(self.filename)      
        elif self.textFormat.isChecked():
            query = ("SELECT growth_date, growth_name, growth_substrate, growth_temperature, growth_pressure, growth_power, growth_flow, growth_refindex, growth_thickness, growth_si, growth_c, growth_n, growth_o, growth_status, growth_notes FROM pecvd")
            dataFrame = pd.read_sql_query(query,con)
            self.filename, ok = QFileDialog.getSaveFileName(self, 'Save data', "", "text(*.txt)")
            if ok:
                dataFrame.to_csv(self.filename)  
        
class DisplayGrowth(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Growth Details")
        self.setWindowIcon(QIcon('icons/pecvdicon.png'))
        self.setGeometry(450, 150, 500, 800)
        self.setFixedSize(self.size())
        self.UI()
        self.show()
        
    def UI(self):
        self.growthDetails()
        self.widgets()
        self.layouts()
    
    def growthDetails(self):
        global growthId
        query = ("SELECT * FROM pecvd WHERE growth_id=?")
        growth = cur.execute(query,(growthId,)).fetchone() #single item tuple (1,)
        
        self.date = growth[1]
        print(self.date)
        self.title = growth[2]
        self.substrate = growth[3]
        self.temperature = growth[4]
        self.pressure = growth[5]
        self.power = growth[6]
        self.flow = growth[7]
        self.refIndex = growth[8]
        self.thickness = growth[9]
        self.silicon = growth[10]
        self.carbon = growth[11]
        self.nitrogen = growth[12]
        self.oxygen = growth[13]
        self.status = growth[14]
        self.notes = growth[15]
        self.growthImg = growth[16]
    
    def widgets(self):
          #####Creating widgets#####
        #Top Layout#
        self.addFilmImg = QLabel()
        self.img = QPixmap('img/{}'.format(self.growthImg))
        self.addFilmImg.setPixmap(self.img)
        self.addFilmImg.setAlignment(Qt.AlignCenter)
        #Bottom Layout#
        self.growthDate = QLineEdit()
        self.growthDate.setText(self.date)
        self.growthTitle = QLineEdit()
        self.growthTitle.setText(self.title)
        self.growthSubstrate = QLineEdit()
        self.growthSubstrate.setText(self.substrate)
        self.growthTemperature = QLineEdit()
        self.growthTemperature.setText(self.temperature)
        self.growthPressure = QLineEdit()
        self.growthPressure.setText(self.pressure)
        self.growthPower = QLineEdit()
        self.growthPower.setText(self.power)
        self.growthFlow = QLineEdit()
        self.growthFlow.setText(self.flow)
        self.growthRefIndex = QLineEdit()
        self.growthRefIndex.setText(self.refIndex)
        self.growthThickness = QLineEdit()
        self.growthThickness.setText(self.thickness)
        self.growthSilicon = QLineEdit()
        self.growthSilicon.setText(self.silicon)
        self.growthCarbon = QLineEdit()
        self.growthCarbon.setText(self.carbon)
        self.growthNitrogen = QLineEdit()
        self.growthNitrogen.setText(self.nitrogen)
        self.growthOxygen = QLineEdit()
        self.growthOxygen.setText(self.oxygen)
        self.growthStatusCombo = QComboBox()
        self.growthStatusCombo.addItems(["Good", "Delaminated", "Used"])
        self.growthNotes = QTextEdit()
        self.growthNotes.setText(self.notes)
        self.uploadBtn = QPushButton('Upload Image')
        self.uploadBtn.clicked.connect(self.uploadImg)
        self.deleteBtn = QPushButton('Delete Growth')
        self.deleteBtn.clicked.connect(self.deleteGrowth)
        self.updateBtn = QPushButton('Update Growth')
        self.updateBtn.clicked.connect(self.updateGrowth)
        
    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()
        self.bottomFrame = QFrame()
        # self.bottomFrame.setStyleSheet(style.growthBottomFrameStyle())
        self.topLayout = QVBoxLayout()
        self.topFrame = QFrame()
        
        #Adding widgets to Layouts#
        #Top Layout#
        self.topLayout.addWidget(self.addFilmImg)
        self.topFrame.setLayout(self.topLayout)
        
        #Bottom or Form Layout#
        self.bottomLayout.addRow(QLabel("Date: "), self.growthDate)
        self.bottomLayout.addRow(QLabel("Growth title: "), self.growthTitle)
        self.bottomLayout.addRow(QLabel("Substrate: "), self.growthSubstrate)
        self.bottomLayout.addRow(QLabel("Temperature (C): "), self.growthTemperature)
        self.bottomLayout.addRow(QLabel("Pressure (Torr): "), self.growthPressure)
        self.bottomLayout.addRow(QLabel("Power (W): "), self.growthPower)
        self.bottomLayout.addRow(QLabel("Flow (sccm): "), self.growthFlow)
        self.bottomLayout.addRow(QLabel("Refractive index: "), self.growthRefIndex)
        self.bottomLayout.addRow(QLabel("Thickness (nm) : "), self.growthThickness)
        self.bottomLayout.addRow(QLabel("% Si: "), self.growthSilicon)
        self.bottomLayout.addRow(QLabel("% C: "), self.growthCarbon)
        self.bottomLayout.addRow(QLabel("% N: "), self.growthNitrogen)
        self.bottomLayout.addRow(QLabel("% O: "), self.growthOxygen)
        self.bottomLayout.addRow(QLabel("Status: "), self.growthStatusCombo)
        self.bottomLayout.addRow(QLabel("Notes "), self.growthNotes)
        self.bottomLayout.addRow(QLabel(""), self.uploadBtn)
        self.bottomLayout.addRow(QLabel(""), self.deleteBtn)
        self.bottomLayout.addRow(QLabel(""), self.updateBtn)
        self.bottomFrame.setLayout(self.bottomLayout)
        
        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame,100)
        self.setLayout(self.mainLayout)
    
    def uploadImg(self):
        size = (64,64)
        self.filename, ok = QFileDialog.getOpenFileName(self, "Upload Image", "", "Image Files (*.jpg *.png)")
        if ok:
            self.growthImg = os.path.basename(self.filename)
            img = Image.open(self.filename)
            img = img.resize(size)
            img.save("img/{0}".format(self.growthImg))
        
    def updateGrowth(self):
        global growthId
        date = self.growthDate.text()
        title = self.growthTitle.text()
        substrate = self.growthSubstrate.text()
        temperature = self.growthTemperature.text()
        pressure = self.growthPressure.text()
        power = self.growthPower.text()
        flow = self.growthFlow.text()
        refIndex = self.growthRefIndex.text()
        thickness = self.growthThickness.text()
        percentSilicon = self.growthSilicon.text()
        percentCarbon = self.growthCarbon.text()
        percentNitrogen = self.growthNitrogen.text()
        percentOxygen = self.growthOxygen.text()
        status = self.growthStatusCombo.currentText()
        notes = self.growthNotes.toPlainText()
        defaultImg = self.growthImg
        
        if (date and title and substrate and temperature and pressure and power and flow != ""):
            try:
                query = "UPDATE pecvd set growth_date=?, growth_name=?, growth_substrate=?, growth_temperature=?, growth_pressure=?, growth_power=?, growth_flow=?, growth_refindex=?, growth_thickness=?, growth_si=?, growth_c=?, growth_n=?, growth_o=?, growth_status=?, growth_notes=?, growth_img=? WHERE growth_id=?"
                cur.execute(query,(date, title, substrate, temperature, pressure, power, flow, refIndex, thickness, percentSilicon, percentCarbon, percentNitrogen, percentOxygen, status, notes, defaultImg, growthId))
                con.commit()
                QMessageBox.information(self, "Info", "Growth has been updated!")
                self.close()
            except:
                QMessageBox.information(self, "Info", "Growth has not been updated!")
        else:
            QMessageBox.information(self, "Info", "Fields cannot be empty!")
    
    def deleteGrowth(self):
        global growthId
        
        mbox = QMessageBox.question(self, "Warning", "Are you sure to delete this product", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if (mbox == QMessageBox.Yes):
            try:
                cur.execute("DELETE FROM pecvd WHERE growth_id=?", (growthId,))
                con.commit()
                QMessageBox.information(self, "Info", "Growth has been deleted")
                con.commit()
                self.close()
            except:
                QMessageBox.information(self, "Info", "Growth has not been deleted")
        
def main():
    App = QApplication(sys.argv)
    window = Main()
    sys.exit(App.exec_())
    
if __name__ == '__main__':
    main()