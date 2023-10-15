import sys
from PyQt6 import QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from UiTancuri import *
from resource_rc import *
from resources.getdata import GetData
from resources.randdf import GetData2
from resources.calctanc import constanteTancuri as cT 
from TabelTanc import Ui_TabelTanc
from datetime import date
import os 

class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = Qt.AlignmentFlag.AlignCenter

class WorkerThread(QThread):
    update_signal = pyqtSignal(object)

    def run(self):
        def dataFunction():
            self.dF = GetData2()
            self.update_signal.emit(self.dF)
            print('dF was emitted')

        self.timer = QTimer()
        self.timer.timeout.connect(dataFunction)
        self.timer.start(5000)

        self.exec()

class AnotherWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.w2 = Ui_TabelTanc()
        self.w2.setupUi(self)
        self.clip = QtGui.QGuiApplication.clipboard()
    
    def keyPressEvent(self, event):
        if (event.modifiers() & QtCore.Qt.KeyboardModifier.ControlModifier):
            selected = self.w2.TabelDate.selectedRanges()

            if event.key() == QtCore.Qt.Key.Key_C:
                print('Data copied')
                copied = '\t'+"\t".join([str(self.w2.TabelDate.horizontalHeaderItem(i).text()) 
                                            for i in range(selected[0].leftColumn(), selected[0].rightColumn()+1)])
                copied = copied + '\n'

                for row in range(selected[0].topRow(), selected[0].bottomRow()+1):
                    copied += self.w2.TabelDate.verticalHeaderItem(row).text() + '\t'
                    for column in range(selected[0].leftColumn(), selected[0].rightColumn()+1):
                        try:
                            copied += str(self.w2.TabelDate.item(row,column).text()) + "\t"
                        except AttributeError:
                            copied += "\t"
                    copied = copied[:-1] + "\n" #eliminate last '\t'
                self.clip.setText(copied)
    
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window dimensions
        width = 1200;
        height = 700;
          
        
        # Make ui object
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


        #Start setttings
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)  # Set Window Title 
        self.setFixedSize(width, height) #Make window not resizeable
        self.ui.iconWidget.hide() #Load app with iconWidget hidden
        self.ui.dmp1_button_1.setChecked(True)
        self.ui.stackedWidget.setCurrentIndex(3)

        #SHORTCUTS#
        QShortcut('Esc',self,self.close)
  
        
        #BUTTONS#
        self.ui.dmp1_button_1.toggled.connect(self.changePage)
        self.ui.dmp2_button_1.toggled.connect(self.changePage)
        self.ui.coa_button_1.toggled.connect(self.changePage)
        self.ui.db_button_1.toggled.connect(self.changePage)
        self.ui.change_button.toggled.connect(self.slideSideMenu)

        

        #Make second window object
        self.window = AnotherWindow()
        # self.w2 = Ui_TabelTanc()
        # self.w2.setupUi(self.window)
        #Second window settings
        self.window.setWindowTitle("Raport cantitati")
        self.window.setFixedSize(480,515)
        delegate = AlignDelegate(self.window.w2.TabelDate)
        self.window.w2.TabelDate.setItemDelegate(delegate)
        self.window.w2.TabelDate.resizeColumnsToContents()

        #SHORTCUTS#
        QShortcut('Esc',self.window,self.window.close)
        self.window.w2.Copiere.clicked.connect(self.copyTabel)

        #BUTTONS#
        self.ui.butonTabel.clicked.connect(self.window.show)

        #SEPARATE THREAD FOR THE DATA AQUISITION
        self.thread = WorkerThread(self)
        self.thread.update_signal.connect(self.tancProcent)
        self.thread.update_signal.connect(self.showNewWindow)
        self.thread.start()

    # CHANGE THE PAGE INDEX BASED ON BUTTON PRESSED#
    def changePage(self):
            if self.ui.dmp1_button_1.isChecked()==True:
                self.ui.stackedWidget.setCurrentIndex(3)
            elif self.ui.dmp2_button_1.isChecked()==True:
                self.ui.stackedWidget.setCurrentIndex(1)
            elif self.ui.coa_button_1.isChecked()==True:
                self.ui.stackedWidget.setCurrentIndex(0)
            elif self.ui.db_button_1.isChecked()==True:
                self.ui.stackedWidget.setCurrentIndex(2)   
        # CHANGE THE PAGE INDEX BASED ON BUTTON PRESSED#
    
    # # GETS THE % FROM THE GETDATA FUNCTION FOR EACH TANK #

    def tancProcent(self,dF):
        try:
            if self.ui.dmp1_button_1.isChecked()==True: ##RUN FUNCTION ONLY IF THE BUTTON IS CHECKED
                # self.dF=GetData2() # SCHIMBA AICI IN GetData()


                #TDI TANKS#
                pTT1 = round(dF['Procent'][0])    
                pTT2 = round(dF['Procent'][1])
                pTT3 = round(dF['Procent'][5])
                pTT4 = round(dF['Procent'][4])
                
                self.ui.TancTT1.setProperty("value", pTT1)
                self.ui.TancTT2.setProperty("value", pTT2)
                self.ui.TancTT3.setProperty("value", pTT3)
                self.ui.TancTT4.setProperty("value", pTT4)

                self.updateTankBG(pTT1, self.ui.TancTT1)
                self.updateTankBG(pTT2, self.ui.TancTT2)
                self.updateTankBG(pTT3, self.ui.TancTT3)
                self.updateTankBG(pTT4, self.ui.TancTT4)
                
                #TDI TANKS#

                #STAN POL TANKS#
                pPT1 = round(dF['Procent'][14])
                pPT2 = round(dF['Procent'][13])
                pPT3 = round(dF['Procent'][11])
                pPT5 = round(dF['Procent'][6])
                            
                self.ui.TancPT1.setProperty("value", pPT1)
                self.ui.TancPT2.setProperty("value", pPT2)
                self.ui.TancPT3.setProperty("value", pPT3)
                self.ui.TancPT5.setProperty("value", pPT5)

                self.updateTankBG(pPT1, self.ui.TancPT1)
                self.updateTankBG(pPT2, self.ui.TancPT2)
                self.updateTankBG(pPT3, self.ui.TancPT3)
                self.updateTankBG(pPT5, self.ui.TancPT5)
                #STAN POL TANKS#  

                #SAN 45%, 25% TANKS#
                pPT6 = round(dF['Procent'][7])
                pPT7 = round(dF['Procent'][8]) 
                pPT4 = round(dF['Procent'][10])

                self.ui.TancPT6.setProperty("value", pPT6)
                self.ui.TancPT7.setProperty("value", pPT7)
                self.ui.TancPT4.setProperty("value", pPT4)

                self.updateTankBG(pPT6, self.ui.TancPT6)
                self.updateTankBG(pPT7, self.ui.TancPT7)
                self.updateTankBG(pPT4, self.ui.TancPT4)
                #SAN 45% TANKS#

                #POLYFUNCTIONAL, DILLUTION DOCKET AND PHD

                pPT8 = round(dF['Procent'][9])
                pPT9 = round(dF['Procent'][12]) 
                pPT10 = round(dF['Procent'][2]) 
                pPT11 = round(dF['Procent'][3])

                self.ui.TancPT8.setProperty("value", pPT8)
                self.ui.TancPT9.setProperty("value", pPT9)
                self.ui.TancPT10.setProperty("value", pPT10)
                self.ui.TancPT11.setProperty("value", pPT11)

                self.updateTankBG(pPT8, self.ui.TancPT8)
                self.updateTankBG(pPT9, self.ui.TancPT9)
                self.updateTankBG(pPT10, self.ui.TancPT10)
                self.updateTankBG(pPT11, self.ui.TancPT11)
                 #POLYFUNCTIONAL, DILLUTION DOCKET AND PHD
        except OSError as e:
                print(e)
                print("Timeout error occured re-trying...:{}".format(date.today()))
               
        # GETS THE % FROM THE GETDATA FUNCTION FOR EACH TANK #
    
    #FUNCTION THAT CHANGES THE COLOR OF THE CHUNK IF IT DROPS UNDER SET VALUE#
    def updateTankBG(self, fillpercent, Tanc):

        threshholdValue = 20
        
        if fillpercent < threshholdValue:
            Tanc.setStyleSheet("QProgressBar::chunk"
                          "{"
                          "background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #EC6570, stop: 1 #9A0B0B);"

                          "}")
        else:
            Tanc.setStyleSheet("QProgressBar::chunk"
                          "{"
                          "background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #6EEE87,stop: 1 #5FC52E);"
                          "}")        
                        
        #FUNCTION THAT CHANGES THE COLOR OF THE CHUNK IF IT DROPS UNDER SET VALUE#

    def loadData(self,dF): ##HELPER FUNCTION TO GET THE TANK TONS ARRAY##
        
        # CURRENT VALUE OF TANK IN % MUL WITH THE 1st CONSTANT +/- SECOND CONSTANT
        
        cTT1 = dF['Procent'][0] * cT['c1_TT1'] + cT['c2_TT2']
        cTT2 = dF['Procent'][1] * cT['c1_TT2'] + cT['c2_TT2'] 
        cTT3 = dF['Procent'][5] * cT['c1_TT3'] + cT['c2_TT3'] 
        cTT4 = dF['Procent'][4] * cT['c1_TT4'] + cT['c2_TT4'] 

        cPT1 = dF['Procent'][14] * cT['c1_PT1'] + cT['c2_PT1'] 
        cPT2 = dF['Procent'][13] * cT['c1_PT2'] + cT['c2_PT2'] 
        cPT3 = dF['Procent'][11] * cT['c1_PT3'] + cT['c2_PT3'] 
        cPT4 = dF['Procent'][10] * cT['c1_PT4'] + cT['c2_PT4'] 
        cPT5 = dF['Procent'][6] * cT['c1_PT5'] + cT['c2_PT5'] 

        cPT6 = dF['Procent'][7] * cT['c1_PT6'] + cT['c2_PT6']
        cPT7 = dF['Procent'][8] * cT['c1_PT7'] + cT['c2_PT7']
        cPT8 = dF['Procent'][9] * cT['c1_PT8'] + cT['c2_PT8']
        cPT9 = dF['Procent'][12] * cT['c1_PT9'] + cT['c2_PT9']
        cPT10 = dF['Procent'][2] * cT['c1_PT10'] + cT['c2_PT10']
        cPT11 = dF['Procent'][3] * cT['c1_PT11'] + cT['c2_PT11']


        cArr = [cTT1,cTT2,cTT3,cTT4,cPT1,cPT2
                ,cPT3,cPT4,cPT5,cPT6,cPT7,cPT8,
                cPT9,cPT10,cPT11]
        
        cArrInt = [int(i) for i in cArr]

        return cArrInt
        
    def showNewWindow(self,dF): ##CREATE NEW WINDOW FOR THE QUANTITY TABLE
        if self.window.w2.TabelDate.isVisible() == True:
            arr = self.loadData(dF)
            path = f'rapoarte/{date.today()}.txt'

            if os.path.exists(path) == False:
                with open(path,'w') as filewrite:
                        filewrite.write(str(arr))

            
            with open(path,'r') as fileread:
                diferenta = fileread.read()
                txt = eval(diferenta)
            

            for item in range(len(arr)):
                self.window.w2.TabelDate.setItem(item,0,QTableWidgetItem(str(txt[item])))          
                self.window.w2.TabelDate.setItem(item,1,QTableWidgetItem(str(arr[item])))
                self.window.w2.TabelDate.setItem(item,2,QTableWidgetItem(str(arr[item]-txt[item])))

    #HAMBURGER MENU ANIMATION#
    def slideSideMenu(self):

        if self.ui.fullMenuWidget.isVisible()==True:

            self.animation = QtCore.QPropertyAnimation(self.ui.fullMenuWidget, b"maximumWidth")
            self.animation.setDuration(300)
            self.animation.setStartValue(52)
            self.animation.setEndValue(143)
            self.animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutQuart)
            self.animation.start()

        else:
            self.animation = QtCore.QPropertyAnimation(self.ui.iconWidget, b"minimumWidth")
            self.animation.setDuration(300)
            self.animation.setStartValue(143)
            self.animation.setEndValue(52)
            self.animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutQuart)
            self.animation.start()
    #HAMBURGER MENU ANIMATION#
    def copyTabel(self):
        selected = self.window.w2.TabelDate.selectAll()
        
        # copied = '\t'+"\t".join([str(self.window.w2.TabelDate.horizontalHeaderItem(i).text()) 
        #                             for i in range(selected[0].leftColumn(), selected[0].rightColumn()+1)])
        # copied = copied + '\n'

        # for row in range(selected[0].topRow(), selected[0].bottomRow()+1):
        #     copied += self.window.w2.TabelDate.verticalHeaderItem(row).text() + '\t'
        #     for column in range(selected[0].leftColumn(), selected[0].rightColumn()+1):
        #         try:
        #             copied += str(self.window.w2.TabelDate.item(row,column).text()) + "\t"
        #         except AttributeError:
        #             copied += "\t"
        #     copied = copied[:-1] + "\n" #eliminate last '\t'
        #     print(copied)


    #DRAGABLE WINDOWLESS FRAME#
    def mousePressEvent(self, event):
        self.dragPos = event.globalPosition().toPoint()


    def mouseMoveEvent(self, event):
        self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos )
        self.dragPos = event.globalPosition().toPoint()
        event.accept()
    #DRAGABLE WINDOWLESS FRAME#
    def closeEvent(self,event):
        
        quit_msg = "Are you sure you want to close the program?"
        reply = QMessageBox.question(self,'Message',
                                     quit_msg,QMessageBox.StandardButton.Yes, QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            self.window.close()
            event.accept()
        else:
            event.ignore()




       

if __name__ == '__main__':
    app = QApplication(sys.argv)

    with open("styles/style.qss","r") as style_file:
        style_str = style_file.read()

    app.setStyleSheet(style_str)


    w = MainWindow()
    w.show()
    
    
    sys.exit(app.exec()) #START EVENT LOOP#       
