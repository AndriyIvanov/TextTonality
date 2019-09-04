from PyQt5 import QtWidgets, uic
import sys
import os
import TestEmotion
from enum import Enum

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

class Tonality(Enum):
    POSITIVE = 'Положительная тональность'
    NEUTRAL = 'Нейтральная тональность'
    NEGATIVE = 'Отрицательная тональность'

class Colors(Enum):
    POSITIVE = '#aef28b'
    NEUTRAL = '#fbf3a6'
    NEGATIVE = '#ee7676'

class Ui(QtWidgets.QWidget):    
    toneClassifier = TestEmotion.ToneClassifier()
    tonality = Tonality.NEUTRAL
    color = Colors.NEUTRAL
    result = 0

    #Tonality limits
    UPPER_LIMIT = 60
    LOWER_LIMIT = 40

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi(CURRENT_DIR + '/MainForm.ui', self)
        
        self.textInput =  self.findChild(QtWidgets.QTextEdit, 'textEdit_ForAnalys')
        #self.textInput.document().setPlainText ('Хорошее кино, надо будет еще раз сходить')
        self.analysBtn = self.findChild(QtWidgets.QPushButton, 'pushButton_Analys')
        self.resultLbl = self.findChild(QtWidgets.QLabel, 'label_Result')
        
        self.resultLCD = self.findChild(QtWidgets.QLCDNumber, 'lcdNumber_Result')

        self.analysBtn.clicked.connect(self.printButtonPressed)
        self.show()

    def printButtonPressed(self):
        self.result = self.toneClassifier.analyse(self.textInput.toPlainText())[0][0].item()*100
        print(self.result)
        self.resultEvaluation()
        self.resultLbl.setStyleSheet('QLabel { background-color : ' + self.color.value + ';}')
        self.resultLbl.setText (self.tonality.value)
        self.resultLCD.display(self.result)
    
    def resultEvaluation(self):
        if (self.result > self.UPPER_LIMIT) :
            self.tonality = Tonality.POSITIVE
            self.color = Colors.POSITIVE
        elif (self.result < self.LOWER_LIMIT) :
            self.tonality = Tonality.NEGATIVE
            self.color = Colors.NEGATIVE
            self.result = 100-self.result
            return
        else:
            self.tonality = Tonality.NEUTRAL
            self.color = Colors.NEUTRAL


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()