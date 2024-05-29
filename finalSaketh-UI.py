
import math
import random
import time;
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import pyqtgraph as pg
from random import randint

# Values here

baselinePressure = 0.0                          # Transducer Pressure Value
units=''                                        # Units for measuring pressure
operation_mode = ""                             # How device is run

openPressure_str = ""                           # Value of opening pressure string that is displayed
opening_pressure_val = 0                        # opening pressure value

maxVolume_str = ''                              # Value of maximal volume string that is displayed
maxVolume_val = 0.0                               # maximal volume drained (mL/hr)

clampDuration_str = ''
clampDuration_val = 0

# All flags go here
zeroComplete=False
zeroNowFlag = False
zeroLaterFlag = False
adjustFlag = False
clampFlag = False
# Main Window that controls the action here 

w = None                            # Main window
toTransducer = None                 # Transducer Type   
zeroNow = None;                     # Zero Now
zeroWarningScreen = None            # Warning Screen for Zero Later
drainSelection = None               # Select how drainage occurs
unitScreen = None                   # Units for pressure drainage
drainagePressure = None             # Screen for drainage pressure
volumeDrainage = None               # Screen for volume drainage
adjustScreen = None                 # Screen for adjusting drainage
summaryScreen = None                # Screen that has summary information
operationScreen = None              # Screen that starts operation
alarmScreen = None                  # Screen that indicates alarm is going off
opZeroScreen = None                 # Screen that zero from operation screen
clampScreen = None                  # Screen that controls if device is clamped
clampedEntry = None                 # Screen that lets you enter numbers in
clampTimer = None                   # Device is clamped
ioScreen = None                     # I/O Screen


class IOScreen(QWidget):
 def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedWidth(1050)
        self.setFixedHeight(400)
        self.grid = QGridLayout()


        
        self.text_field = QPlainTextEdit(self)
        self.text_field.setMinimumSize (1050,400)
        self.text_field.setStyleSheet("background-image: url(gray-background.png); background-attachment: fixed")

        self.ClearLabel = QPushButton('Clear Volume')
        self.ClearLabel.setStyleSheet('background-image: url(./gray-background.png); color: gold; border: 2px solid-black; padding:20px')
        self.ClearLabel.setFont(QFont('Futura',30))
        self.grid.addWidget(self.ClearLabel, 0,6,2,2)

        self.LastClear=QLabel('Last Cleared: ')
        self.LastClear.setStyleSheet('background-image: url(./gray-background.png); color: gold; border: 2px solid-black; padding:20px')
        self.LastClear.setFont(QFont('Futura',30))
        self.grid.addWidget(self.LastClear, 2,6,2,2)

        self.CurrentVolume=QLabel('Current Volume: ')
        self.CurrentVolume.setStyleSheet('background-image: url(./gray-background.png); color: gold; border: 2px solid-black; padding:20px')
        self.CurrentVolume.setFont(QFont('Futura',30))
        self.grid.addWidget(self.CurrentVolume, 4,6,2,2)

        self.VolumeDrained = QLabel('Volume Drained: ')
        self.VolumeDrained.setStyleSheet('background-image: url(./gray-background.png); color: gold; border: 2px solid-black; padding:20px')
        self.VolumeDrained.setFont(QFont('Futura',30))
        self.grid.addWidget(self.VolumeDrained, 6,6,2,2)


        self.setLayout(self.grid)

class ClampedTimer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedWidth(1050)
        self.setFixedHeight(400)
        self.grid = QGridLayout()


        
        self.text_field = QPlainTextEdit(self)
        self.text_field.setMinimumSize (1050,400)
        self.text_field.setStyleSheet("background-image: url(gray-background.png); background-attachment: fixed")

        self.ClampedLabel = QLabel('Device is Clamped');
        self.ClampedLabel.setStyleSheet('background-image: url(./gray-background.png); color: gold; border: 2px solid-black; padding:20px')
        self.ClampedLabel.setFont(QFont('Futura',40));
        self.ClampedLabel.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(self.ClampedLabel, 0,6,5,3);

        self.lcd = QLCDNumber()
        self.lcd.setStyleSheet('background: transparent; color: gold')
        self.timer = QTimer(self);



        self.time = int(clampDuration_val*60)
        self.lcd.display("%d:%02d" % (self.time/60,self.time % 60))

        # Restart the timer
        self.timer.start(1000)

        # To update timer
        self.timer.timeout.connect(self.updateLCD)
        

        self.grid.addWidget(self.lcd, 6,6,3,3)

        self.BackButton = QPushButton('Unclamp \n \n')
        self.BackButton.setFont(QFont('Futura', 30))
        self.BackButton.setStyleSheet('background-image: url(./gray-background.png); color: gold; border: 2px solid-black; padding:20px')
        self.BackButton.clicked.connect(self.Back)

        self.grid.addWidget(self.BackButton, 10,6,3,5)

        self.setLayout(self.grid)
    def updateLCD(self):
        self.timer
        # Update the lcd
        self.time -= 1
        if self.time >= 0:
            self.lcd.display("%d:%02d" % (self.time/60,self.time % 60))
        else:
            self.timer.stop()
    def Back(self):
        self.close()



class ClampCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedWidth(1050)
        self.setFixedHeight(400)
        self.grid = QGridLayout()

        
        self.text_field = QPlainTextEdit(self)
        self.text_field.setMinimumSize (1050,400)
        self.text_field.setStyleSheet("background-image: url(gray-background.png); background-attachment: fixed")

        # Welcome Label
        self.welcomeLabel = QLabel("Clamp Duration?")
        self.welcomeLabel.setWordWrap(True)
        self.welcomeLabel.setFont(QFont("Futura",40 ))
        self.welcomeLabel.setAlignment(Qt.AlignCenter)
        self.welcomeLabel.setStyleSheet('background: transparent; color: gold')

        self.size=QSize(50,50)

        self.backButton = QPushButton('Back \n')
        self.backButton.setFont(QFont("Futura", 38))
        self.backButton.clicked.connect(self.unClamp)
        self.backButton.setStyleSheet('background: transparent; color: gold')

        # Display Label
        self.display_label = QPushButton("" + "\n")
        self.display_label.setFont(QFont("Futura", 60))
        #self.display_label.setAlignment(Qt.AlignCenter)
        self.display_label.setStyleSheet('background: transparent; color: gold')

        # Button setup happens here
        self.button0 = QPushButton("")
        self.button0.clicked.connect(self.press0)
        self.button0.setIcon(QIcon('0.png'))
        self.button0.setIconSize(self.size)
        self.button0.setStyleSheet('background: #1C1A1B;;border: 0px')

        # Button setup happens here
        self.button1 = QPushButton("")
        self.button1.clicked.connect(self.press1)
        self.button1.setIcon(QIcon('1.png'))
        self.button1.setIconSize(self.size)
        self.button1.setStyleSheet('background: #1C1A1B; border: 0px')


        self.button2 = QPushButton("")
        self.button2.clicked.connect(self.press2)
        self.button2.setIcon(QIcon('2.png'))
        self.button2.setIconSize(self.size)
        self.button2.setStyleSheet('background: #1C1A1B; border: 0px')
       
        self.button3 = QPushButton("")
        self.button3.clicked.connect(self.press3)
        self.button3.setIcon(QIcon('3.png'))
        self.button3.setIconSize(self.size)
        self.button3.setStyleSheet('background: #1C1A1B; border: 0px')
       
      

        self.button4 = QPushButton("")
        self.button4.clicked.connect(self.press4)
        self.button4.setIcon(QIcon('4.png'))
        self.button4.setIconSize(self.size)
        self.button4.setStyleSheet('background: #1C1A1B; border: 0px')


        self.button5 = QPushButton("")
        self.button5.setIcon(QIcon('5.png'))
        self.button5.clicked.connect(self.press5)
        self.button5.setIconSize(self.size)
        self.button5.setStyleSheet('background: #1C1A1B; border: 0px')


        self.button6 = QPushButton("");
        self.button6.setIcon(QIcon('6.png'))
        self.button6.clicked.connect(self.press6)
        self.button6.setIconSize(self.size)
        self.button6.setStyleSheet('background: #1C1A1B; border: 0px')

        self.button7 = QPushButton("");
        self.button7.clicked.connect(self.press7);
        self.button7.setIcon(QIcon('7.png'))
        self.button7.setIconSize(self.size)
        self.button7.setStyleSheet('background: #1C1A1B; border: 0px')

        self.button8 = QPushButton("")
        self.button8.clicked.connect(self.press8)
        self.button8.setIcon(QIcon('8.png'))
        self.button8.setIconSize(self.size)
        self.button8.setStyleSheet('background: #1C1A1B; border: 0px')
        
        self.button9 = QPushButton("");
        self.button9.clicked.connect(self.press9)
        self.button9.setIcon(QIcon('9.png'))
        self.button9.setIconSize(self.size)
        self.button9.setStyleSheet('background: #1C1A1B; border: 0px')      

        self.button_dot = QPushButton(". \n");
        self.button_dot.setFont(QFont("Futura", 38))
        self.button_dot.clicked.connect(self.pressDot)
        self.button_dot.setStyleSheet('background: #1C1A1B; border: 0px; color: white')

        self.enterButton = QPushButton("");
        self.enterButton.setIcon(QIcon('enter.png'))
        self.enterButton.setIconSize(self.size)
        self.enterButton.setStyleSheet('background: #1C1A1B; border: 0px')
        self.enterButton.clicked.connect(self.enter);


        self.clearButton = QPushButton("");
        self.clearButton.setIcon(QIcon('reset.png'))
        self.clearButton.clicked.connect(self.clear)
        self.clearButton.setIconSize(self.size)

        self.clearButton.setStyleSheet('background: #1C1A1B; border: 0px')
        

        self.LabelButton = QLabel('minutes');
        self.LabelButton.setAlignment(Qt.AlignCenter)
        self.LabelButton.setFont(QFont("Futura", 38))
        self.LabelButton.setStyleSheet('background: transparent; color: gold')
        
        # Adding buttons to grid
        self.grid.addWidget(self.button1, 7,0,2,3);
        self.grid.addWidget(self.button2, 7, 3, 2, 3);
        self.grid.addWidget(self.button3, 7, 6,2,3);
        self.grid.addWidget(self.button4, 9, 0,2,3);
        self.grid.addWidget(self.button5, 9,3,2,3);
        self.grid.addWidget(self.button6, 9,6,2,3);
        self.grid.addWidget(self.button7, 11,0,2,3);
        self.grid.addWidget(self.button8, 11,3,2,3);
        self.grid.addWidget(self.button9, 11,6,2,3);
        self.grid.addWidget(self.button0, 13, 3, 2, 3);

        self.grid.addWidget(self.clearButton, 13, 6, 2, 3);


        self.grid.addWidget(self.button_dot, 13,0,2,3)
        self.grid.addWidget(self.welcomeLabel, 2, 0, 2, 15);

       # self.grid.addWidget(self.backButton, 13, 10, 2, 4)
        self.grid.addWidget(self.display_label, 5,10,2,4);
        self.grid.addWidget(self.LabelButton, 7,10,2,4)
        self.grid.addWidget(self.enterButton,13,11,2,3);
        self.setLayout(self.grid)

    def press0(self):
        global clampDuration_str;
        clampDuration_str += "0";
 

        self.display_label.setText(clampDuration_str);
        
    def press1(self):
        global clampDuration_str;
        clampDuration_str += "1";

        self.display_label.setFont(QFont("Futura", 60));
        self.display_label.setText(clampDuration_str);
    def press2(self):
        global clampDuration_str;
        clampDuration_str += "2";

        self.display_label.setFont(QFont("Futura", 60));
        self.display_label.setText(clampDuration_str);
    def press3(self):
        global clampDuration_str;
        clampDuration_str += "3";

        self.display_label.setFont(QFont("Futura", 60));
        self.display_label.setText(clampDuration_str);
    def press4(self):
        global clampDuration_str;
        clampDuration_str += "4";

        self.display_label.setFont(QFont("Futura", 60));
        self.display_label.setText(clampDuration_str);
    def press5(self):
        global clampDuration_str;
        clampDuration_str += "5";

        self.display_label.setFont(QFont("Futura", 60));
        self.display_label.setText(clampDuration_str);
    def press6(self):
        global clampDuration_str;
        clampDuration_str += "6";

        self.display_label.setFont(QFont("Futura", 60));
        self.display_label.setText(clampDuration_str);
    def press7(self):
        global clampDuration_str;
        clampDuration_str += "7";

        self.display_label.setFont(QFont("Futura", 60));
        self.display_label.setText(clampDuration_str);
    def press8(self):
        global clampDuration_str;
        clampDuration_str += "8";

        self.display_label.setFont(QFont("Futura", 60));
        self.display_label.setText(clampDuration_str);
    def press9(self):
        global clampDuration_str;
        clampDuration_str += "9";

        self.display_label.setFont(QFont("Futura", 60));
        self.display_label.setText(clampDuration_str);
    def pressDot(self):
        global clampDuration_str;
        clampDuration_str += "."

        self.display_label.setFont(QFont("Futura", 60));
        self.display_label.setText(clampDuration_str);
    def enter(self):

        global clampDuration_val, clampTimer
        clampDuration_val = float(clampDuration_str)

        # To Clamp Now
        clampTimer = ClampedTimer()
        clampTimer.show()
        self.hide()



    def clear(self):
        global clampDuration_val;
        global clampDuration_str;
        clampDuration_str = "";
        clampDuration_val = None;
        self.display_label.setText(clampDuration_str);  
    def unClamp(self):
        self.close()

class ClampDeviceFunction(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedWidth(1050)
        self.setFixedHeight(400)
        self.grid = QGridLayout()

        self.text_field = QPlainTextEdit(self)
        self.text_field.setMinimumSize (1050,400)
        self.text_field.setStyleSheet("background-image: url(gray-background.png); background-attachment: fixed")
                
        # Now we ask all of the questions that we need to here 
        self.DisplayLabel = QLabel("Select Clamp Duration")
        self.DisplayLabel.setStyleSheet('background-image: url(./gray-background.png); color: gold; border: 2px solid-black')
        self.DisplayLabel.setFont(QFont("Futura", 60))
        self.grid.addWidget(self.DisplayLabel, 2,6,2,3)

        self.timedClamp = QPushButton("Timed \n Clamp")
        self.timedClamp.setStyleSheet('background-image: url(./gray-background.png); color: gold; border: 2px solid-black')
        self.timedClamp.setFont(QFont("Futura", 45))
        self.timedClamp.clicked.connect(self.timedClampFunction)
        self.grid.addWidget(self.timedClamp, 5,3,6,4)
        
        self.untimedClamp = QPushButton("Indefinite \n Clamp")
        self.untimedClamp.setStyleSheet('background-image: url(./gray-background.png); color: gold; border: 2px solid-black')
        self.untimedClamp.clicked.connect(self.untimedClampFunction)
        self.untimedClamp.setFont(QFont("Futura", 45))
        self.grid.addWidget(self.untimedClamp, 5,8,6,4)
        self.setLayout(self.grid)

    def backFunction(self):
        self.close()
    def timedClampFunction(self):
        global clampedEntry
        self.DisplayLabel.hide()
        self.timedClamp.hide()
        self.untimedClamp.hide()

        clampedEntry = ClampCalculator()
        clampedEntry.show()
        self.hide()



    def untimedClampFunction(self):
        self.DisplayLabel.hide()
        self.timedClamp.hide()
        self.untimedClamp.hide()

        # We nee to make new label here


        self.DeviceClamp = QLabel('Device is Clamped')
        self.DeviceClamp.setStyleSheet('background-image: url(./gray-background.png); color: gold; border: 2px solid-black')
        self.DeviceClamp.setFont(QFont("Futura", 60))
        self.grid.addWidget(self.DeviceClamp, 2,6,2,3)


        self.unClamp = QPushButton('Unclamp')
        self.unClamp.setStyleSheet('background-image: url(./gray-background.png); color: gold; border: 2px solid-black')
        self.unClamp.clicked.connect(self.backFunction)
        self.unClamp.setFont(QFont("Futura", 45))
        self.grid.addWidget(self.unClamp, 10,5,4,4)

class AlarmScreen(QWidget):
     def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedWidth(1050)
        self.setFixedHeight(400)
        self.grid = QGridLayout()

        self.text_field = QPlainTextEdit(self)
        self.text_field.setMinimumSize (1050,400)
        self.text_field.setStyleSheet("background-image: url(gray-background.png); background-attachment: fixed")

        # Now we add the appropriate labels
        self.silencedLabel = QLabel('Alarm Silenced')
        self.silencedLabel.setStyleSheet('background: transparent; color: gold;')
        self.silencedLabel.setFont(QFont('Futura',50))
        self.silencedLabel.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(self.silencedLabel, 0,5,2,3)

        self.image_label = QLabel('')
        self.image_label.setStyleSheet('background-image: url(bell.png)')
        self.grid.addWidget(self.image_label, 2,0,6,3)

        self.lcd = QLCDNumber()
        self.lcd.setStyleSheet('background: transparent; color: gold')
        self.grid.addWidget(self.lcd, 3,5,4,3)
        self.timer = QTimer(self)



        self.timer.stop()
        self.time = 120
        self.lcd.display("%d:%02d" % (self.time/60,self.time % 60))

        # Restart the timer
        self.timer.start(1000)

        # To update timer
        self.timer.timeout.connect(self.updateLCD)

        self.AddDelayButton = QPushButton('+ ')
        self.AddDelayButton.setStyleSheet('background-image: url(./gray-background.png); color: gold; border: 2px solid-black')
        self.AddDelayButton.setFont(QFont('Futura', 30))
        self.AddDelayButton.clicked.connect(self.upDelay);
        self.grid.addWidget(self.AddDelayButton, 10,4,3,3)

        self.backButton = QPushButton('Back');
        self.backButton.setFont(QFont('Futura',30));
        self.backButton.setStyleSheet('background-image: url(./gray-background.png); color: gold; border: 2px solid-black')
        self.backButton.clicked.connect(self.Back);
        self.grid.addWidget(self.backButton, 10,8,3,3);


        self.setLayout(self.grid);
     def upDelay(self):
         self.time = (self.time + 60)
         self.lcd.display("%d:%02d" % (self.time/60,self.time % 60))
     def Back(self):
        global alarmScreen;
        alarmScreen.hide();


     def updateLCD(self):
        self.timer
        # Update the lcd
        self.time -= 1
        if self.time >= 0:
            self.lcd.display("%d:%02d" % (self.time/60,self.time % 60))
        else:
            self.timer.stop()

class OPZeroDevice(QWidget):

    def __init__(self):
        super().__init__();
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedWidth(1050)
        self.setFixedHeight(400)
        self.grid = QGridLayout();

        for x in range(15):
            for y in range(15):
                tmp = QLabel('');
                self.grid.addWidget(tmp, x,y)

        self.text_field = QPlainTextEdit(self)
        self.text_field.setMinimumSize (1920,1080)
        self.text_field.setStyleSheet("background-image: url(gray-background.png); background-attachment: fixed")


        self.ZeroLabel = QLabel('Zero Transducer');
        self.ZeroLabel.setFont(QFont('Futura',60));
        self.ZeroLabel.setAlignment(Qt.AlignCenter)
        self.ZeroLabel.setStyleSheet('background: transparent; color: gold');
        self.grid.addWidget(self.ZeroLabel, 0,5,3,5);
        
        reminder_text = '-Ensure Proper Positioning \n -Open Stopcocks \n -Press Zero When Ready'
        self.Reminders = QLabel(reminder_text);
        self.Reminders.setStyleSheet('background: transparent; color: gold')
        self.Reminders.setFont(QFont('Futura',20));
        self.Reminders.setAlignment(Qt.AlignCenter);
        self.grid.addWidget(self.Reminders, 3,6,4,3)

        self.ZeroButton = QPushButton('Zero');
        self.ZeroButton.setStyleSheet('background-image: url(./gray-background.png); color: gold; border: 2px solid-black')
        self.ZeroButton.setFont(QFont('Futura',40));
        self.ZeroButton.clicked.connect(self.AfterZero)
        self.grid.addWidget(self.ZeroButton, 9,2,4,4)


        self.BackButton = QPushButton('Back');
        self.BackButton.setStyleSheet('background-image: url(./gray-background.png); color: gold; border: 2px solid-black')
        self.BackButton.setFont(QFont('Futura',40));
        self.BackButton.clicked.connect(self.Back);
        self.grid.addWidget(self.BackButton, 9,10,4,4);
        self.setLayout(self.grid)
    def AfterZero(self):
        self.Reminders.setHidden(True);
        self.ZeroButton.setHidden(True);
        #self.BackButton.setHidden(True);

        self.ZeroLabel = QLabel('Zeroing Sucessful');
        self.ZeroLabel.setStyleSheet('color:gold')
        self.ZeroLabel.setFont(QFont('Futura',40));
        self.grid.addWidget(self.ZeroLabel, 5,5,3,6)
        self.ZeroLabel.setAlignment(Qt.AlignCenter)
        #self.grid.removeWidget(self.BackButton)
        self.grid.addWidget(self.BackButton, 10,5,3,5)
    def Back(self):
        global opZeroScreen;
        opZeroScreen.hide();

class Operation(QWidget):
    # Set up the screens
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedWidth(1050)
        self.setFixedHeight(400)
        self.grid = QGridLayout()

        self.text_field = QPlainTextEdit(self)
        self.text_field.setMinimumSize (1920,1080)
        self.text_field.setStyleSheet("background-image: url(gray-background.png); background-attachment: fixed")


        program = ''
        drainage_pressure = ''
        volume_limit = ''
        total_volume_limit = ''
        adjustable = ''
        program = operation_mode

        # Drain Pressure
        if operation_mode=='Volume Drain':
            drainage_pressure = 'No Drainage \n Pressure'
        else:
            drainage_pressure = "Drainage Pressure: \n" + str(opening_pressure_val) + ' ' + units
        
        # Volume Limit
        if operation_mode=='Pressure Drain':
            volume_limit = 'No Volume Limit'
        else:
            volume_limit = 'Volume Limit: \n' + str(maxVolume_str) + ' \nmL/hr'

        if adjustFlag:
            adjustable = 'Dynamic Drainage \n Enabled'
        else:
            adjustable = 'Dynamic Drainage \n Disabled'

        # Total Volume
        total_volume_limit = 'Total Volume Limit: \n 100 mL'

        # Top row of labels
        self.OperationLabel = QLabel(operation_mode)
        self.OperationLabel.setFont(QFont('Futura', 30))
        self.OperationLabel.setAlignment(Qt.AlignCenter)
        self.OperationLabel.setStyleSheet('background: transparent; color: gold; border: 2px solid white')

        self.drainPressureLabel = QLabel(drainage_pressure)
        self.drainPressureLabel.setFont(QFont('Futura',30))
        self.drainPressureLabel.setAlignment(Qt.AlignCenter)
        self.drainPressureLabel.setStyleSheet('background: transparent; color: gold; border: 2px solid white')
        
        self.volumeLimitLabel = QLabel(volume_limit)
        self.volumeLimitLabel.setFont(QFont('Futura',30))
        self.volumeLimitLabel.setAlignment(Qt.AlignCenter)
        self.volumeLimitLabel.setStyleSheet('background: transparent; color: gold; border: 2px solid white')

        self.totalVolumeLimitLabel = QLabel(total_volume_limit)
        self.totalVolumeLimitLabel.setFont(QFont('Futura', 30))
        self.totalVolumeLimitLabel.setAlignment(Qt.AlignCenter)
        self.totalVolumeLimitLabel.setStyleSheet('background: transparent; color: gold; border: 2px solid white')

        self.dynamicDrainageLabel = QLabel(adjustable)
        self.dynamicDrainageLabel.setFont(QFont('Futura', 30))
        self.dynamicDrainageLabel.setAlignment(Qt.AlignCenter)
        self.dynamicDrainageLabel.setStyleSheet('background: transparent; color: gold; border: 2px solid white')

        # Adding to the top row
        self.grid.addWidget(self.OperationLabel, 0,0,2,2)
        self.grid.addWidget(self.drainPressureLabel, 0,3,2,2)
        self.grid.addWidget(self.volumeLimitLabel, 0,6,2,2)
        self.grid.addWidget(self.totalVolumeLimitLabel, 0,9,2,2)
        self.grid.addWidget(self.dynamicDrainageLabel, 0,12,2,2) 


        self.restartButton = QPushButton('Restart \n')
        self.restartButton.setFont(QFont("Futura", 40))
        self.restartButton.clicked.connect(self.restartFunction)

        self.IOButton = QPushButton('I/O \n Logs')
        self.IOButton.setFont(QFont("Futura", 40))
        self.IOButton.clicked.connect(self.IOFunction)

        self.ClampButton = QPushButton('Clamp \n Device')
        self.ClampButton.setFont(QFont("Futura", 40))
        self.ClampButton.clicked.connect(self.clampDeviceFunction)
        
        self.ZeroButton = QPushButton('Zero \n Device')
        self.ZeroButton.setFont(QFont("Futura", 40))
        self.ZeroButton.clicked.connect(self.zeroDeviceFunction)

        
        self.SilenceAlarm =  QPushButton("Silence \n Alarm")
        self.SilenceAlarm.setFont(QFont("Futura", 40))
  
        self.SilenceAlarm.clicked.connect(self.silenceAlarmFunction)

        self.IOButton.setStyleSheet('background-image: url(gray-background.png);  color: gold; border:0px')
        self.ClampButton.setStyleSheet('background-image: url(gray-background.png);  color: gold; border:0px')
        self.ZeroButton.setStyleSheet('background-image: url(gray-background.png);  color: gold; border:0px')
        self.SilenceAlarm.setStyleSheet('background-image: url(gray-background.png);  color: gold; border:0px')
        self.restartButton.setStyleSheet('background-image: url(gray-background.png);  color: gold; border:0px')
        
        self.grid.addWidget(self.restartButton, 13,0,2,2)
        self.grid.addWidget(self.IOButton, 13,3,2,2)
        self.grid.addWidget(self.ClampButton, 13, 6, 2,2)
        self.grid.addWidget(self.ZeroButton, 13, 9, 2, 2)
        self.grid.addWidget(self.SilenceAlarm, 13, 12,2,2)


        # Adding the pressure graph now

        self.plot_graph = pg.PlotWidget()
        self.plot_graph.setStyleSheet('background-image: url(gray-background.png);')
       
        pen = pg.mkPen(color=(0, 255, 255))
        self.plot_graph.setTitle("ICP Graph", color="cyan", size="20pt")

        
        styles = {"color": "blue", "font-size": "10px"}
        self.plot_graph.setLabel("left", "Pressure (mmHg)", **styles)
        self.plot_graph.setLabel("bottom", "Time (minutes)", **styles)
        self.plot_graph.addLegend()
        self.plot_graph.setYRange(0,80)
        self.time = list(range(10))
        self.pressure = [randint(20, 40) for _ in range(10)]

        # Get a line reference
        self.pressure_line = self.plot_graph.plot(
            self.time,
            self.pressure,
            name="ICPGraph",
            pen=pen,
            symbol="x",
            symbolSize=5,
            symbolBrush="cyan",
        )
        # Add a timer to simulate new temperature measurements
        self.icptimer = QTimer()
        self.icptimer.setInterval(100)
        self.icptimer.timeout.connect(self.updateICP)
        self.icptimer.start()
        self.grid.addWidget(self.plot_graph,6,1,5,5)

        pen = pg.mkPen(color=(0, 255, 255))
        self.plot_graph.setTitle("ICP Graph", color="cyan", size="20pt")

        # Adding GIF here
        self.RunLabel = QLabel('')
        self.RunLabel.setFont(QFont('Futura', 20))
        self.RunLabel.setAlignment(Qt.AlignCenter);
        self.RunLabel.setStyleSheet('background: transparent; color: gold')
        self.grid.addWidget(self.RunLabel, 4,12,7,2);
        self.go_movie = QMovie('final_running.gif')
        self.RunLabel.setMovie(self.go_movie)
        self.RunLabel.setStyleSheet('background: transparent; color: gold')
        self.startMovie()


        self.stop_movie = QMovie('error.gif')
        self.stop_movie.start()
        if clampFlag==True:
            self.RunLabel.setMovie(self.stop_movie)


        self.setLayout(self.grid)
    def startMovie(self):
        self.go_movie.start()
    def startPauseMovie(self):
        self.stop_movie.start();
    def updateICP(self):
        self.time = self.time[1:]
        self.time.append(self.time[-1] + 1)
        self.pressure = self.pressure[1:]
        self.pressure.append(randint(20, 40))
        self.pressure_line.setData(self.time, self.pressure)        

    def silenceAlarmFunction(self):
        global alarmScreen
        self.RunLabel.setMovie(self.stop_movie)
        alarmScreen = AlarmScreen()
        alarmScreen.show()
        

    
    def IOFunction(self):
        global ioScreen
        ioScreen = IOScreen()
        ioScreen.show()

    def zeroDeviceFunction(self):
        global opZeroScreen
        opZeroScreen = OPZeroDevice()
        opZeroScreen.show()

    def clampDeviceFunction(selF):
        global clampScreen
        clampScreen = ClampDeviceFunction()
        clampScreen.show()

    
    
    
    def restartFunction(self):
        global zeroComplete, zeroNowFlag, zeroLaterFlag, adjustFlag, units, operation_mode, openPressure_str, opening_pressure_val, maxVolume_str, maxVolume_val
        global toTransducer,zeroNow,zeroWarningScreen,drainSelection,unitScreen,drainagePressure,volumeDrainage,adjustScreen,summaryScreen
        zeroComplete=False
        zeroNowFlag = False
        zeroLaterFlag = False
        adjustFlag = False
        baselinePressure = 0.0                         
        units=''                                       
        operation_mode = ""                       
        openPressure_str = ""                       
        opening_pressure_val = 0                     
        maxVolume_str = ''                            
        maxVolume_val = 0.0 

        toTransducer = None                 # Transducer Type   
        zeroNow = None;                     # Zero Now
        zeroWarningScreen = None            # Warning Screen for Zero Later
        drainSelection = None               # Select how drainage occurs
        unitScreen = None                   # Units for pressure drainage
        drainagePressure = None             # Screen for drainage pressure
        volumeDrainage = None               # Screen for volume drainage
        adjustScreen = None                 # Screen for adjusting drainage
        summaryScreen = None                # Screen that has summary information
        operationScreen = None              # Screen that starts operation          

        w.show()

class Summary(QWidget):
    def __init__(self): 
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedWidth(1920)
        self.setFixedHeight(1080)
        self.grid = QGridLayout()      
        self.text_field = QPlainTextEdit(self)
        self.text_field.setMinimumSize (1920,1080)
        self.text_field.setStyleSheet("background-image: url(gray-background.png); background-attachment: fixed")


        self.summaryLabel = QLabel("Summary Information");
        self.summaryLabel.setStyleSheet('background: transparent; color: gold')
        self.summaryLabel.setFont(QFont("Futura", 75));
        self.summaryLabel.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(self.summaryLabel,  0,6,2,3)


        '''
        'Volume Drain \n Pressure Limit'
        'Pressure Drain \n Volume Limit'
        'Volume Drain'
        'Pressure Drain'
        
        '''
        drain_mode = '' 
        drain_pressure = ''
        volume_limit = ''
        adjustment = ''

        if operation_mode == 'Volume Drain \n Pressure Limit':
            drain_mode = 'Volume Drain  Pressure Limit'
        elif operation_mode=='Pressure Drain \n Volume Limit':
            drain_mode = 'Pressure Drain Volume Limit'
        elif operation_mode=='Pressure Drain':
            drain_mode = 'Pressure Drain'
        elif operation_mode=='Volume Drain':
            drain_mode = 'Volume Drain'
        
        if operation_mode == 'Pressure Drain' or operation_mode=='Pressure Drain \n Volume Limit' or operation_mode=='Volume Drain \n Pressure Limit':
            drain_pressure = 'Drainage Pressure is: ' + str(opening_pressure_val)  + ' ' + units
        else:
            drain_pressure = "No Drainage Pressure"

        if operation_mode=='Volume Drain' or operation_mode=='Pressure Drain Volume Limit' or operation_mode == 'Volume Drain \n Pressure Limit':
            volume_limit = "Volume Limit: " + str(maxVolume_val) + " mL/hr"
        else:
            volume_limit = "No Volume Limit"

        if adjustFlag==True:
            adjustment = 'Dynamic drainage enabled'
        else:
            adjustment = 'Dynamic drainage disabled'

        self.PressureLabel = QLabel(drain_pressure)
        self.PressureLabel.setFont(QFont('Futura', 65))
        self.PressureLabel.setStyleSheet('background:transparent; color:gold')    
        self.PressureLabel.setAlignment(Qt.AlignCenter)


        self.VolumeLabel = QLabel(volume_limit)
        self.VolumeLabel.setAlignment(Qt.AlignCenter)
        self.VolumeLabel.setFont(QFont('Futura', 65))
        self.VolumeLabel.setStyleSheet('background:transparent; color:gold')  
        
        self.adjustLabel = QLabel(adjustment)
        self.adjustLabel.setFont(QFont('Futura', 65))
        self.adjustLabel.setStyleSheet('background:transparent; color:gold')  
        self.adjustLabel.setAlignment(Qt.AlignCenter)

        self.operationButton = QPushButton('Next')
        self.operationButton.setFont(QFont("Futura", 65))
        self.operationButton.setStyleSheet('background-image: url(gray-background.png); background-attachment: fixed; color: gold; border:0px')
        self.operationButton.clicked.connect(self.startOperation)
        

        self.grid.addWidget(self.PressureLabel, 2,6,2,3)
        self.grid.addWidget(self.VolumeLabel, 3, 6, 2, 3)
        self.grid.addWidget(self.adjustLabel, 4, 6, 2, 3)

        self.grid.addWidget(self.operationButton, 6,6,2,3)
        self.setLayout(self.grid)

    def startOperation(self):
        global operationScreen
        operationScreen = Operation()
        operationScreen.show()
        summaryScreen.hide()    
       
class Adjustment(QWidget):
    def __init__(self): 
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedWidth(1920)
        self.setFixedHeight(1080)
        self.grid = QGridLayout()      
        self.text_field = QPlainTextEdit(self)
        self.text_field.setMinimumSize (1920,1080)
        self.text_field.setStyleSheet("background-image: url(gray-background.png); background-attachment: fixed")




        self.dynamicDrain = QLabel("Enable Dynamic Drainage?");
        self.dynamicDrain.setStyleSheet('background: transparent; color: gold')
        self.dynamicDrain.setFont(QFont("Futura", 75));
        self.dynamicDrain.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(self.dynamicDrain, 2,0,2,15)
        

        self.adjustDrain = QPushButton("Yes \n \n")
        self.adjustDrain.setStyleSheet('background-image: url(./gray-background.png); color: gold; border: 2px solid-black')
        self.adjustDrain.clicked.connect(self.adjustFunction)
        self.adjustDrain.setFont(QFont("Futura", 45))
        self.grid.addWidget(self.adjustDrain, 5,3,6,4)


        self.noAdjustDrain = QPushButton("No \n \n")
        self.noAdjustDrain.clicked.connect(self.noadjustFunction)
        self.noAdjustDrain.setFont(QFont("Futura", 45))
        self.noAdjustDrain.setStyleSheet('background-image: url(./gray-background.png); color: gold; border: 2px solid-black')
        self.grid.addWidget(self.noAdjustDrain, 5,8,6,4)


        self.Back = QPushButton("Back \n")
        self.Back.setStyleSheet('background-image: url(./gray-background.png); color: gold; border: 2px solid-black')
        self.Back.setFont(QFont("Futura", 45))
        self.Back.clicked.connect(self.BackScreen)
        self.grid.addWidget(self.Back, 13,6,2,3)
        self.setLayout(self.grid)

    def BackScreen(self): 
        global drainagePressure, adjustScreen
        print(operation_mode) 
        if operation_mode=='Pressure Drain':
            drainagePressure.show()
            adjustScreen.hide()
        if operation_mode=='Volume Drain':
            volumeDrainage.show()
            adjustScreen.hide()
        if operation_mode=='Pressure Drain \n Volume Limit':
            volumeDrainage.show()
            adjustScreen.hide()
        if operation_mode=='Volume Drain \n Pressure Limit':
            drainagePressure.show()
            volumeDrainage.hide()

    def adjustFunction(self):
        global adjustFlag, summaryScreen
        adjustFlag = True

        summaryScreen = Summary()
        summaryScreen.show()
        adjustScreen.hide()


    
    def noadjustFunction(self):
        global adjustFlag, summaryScreen
        adjustFlag = False

        summaryScreen = Summary()
        summaryScreen.show()
        adjustScreen.hide()

class VolumeLimit(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.text_field = QPlainTextEdit(self)
        self.text_field.setMinimumSize (1980,1080)
        self.text_field.setStyleSheet("background-image: url(gray-background.png); background-attachment: fixed")
        self.setFixedWidth(1980);
        self.setFixedHeight(1080);

        self.grid = QGridLayout()




        # Welcome Label
        self.welcomeLabel = QLabel("Select Drainage Volume")
        self.welcomeLabel.setWordWrap(True)
        self.welcomeLabel.setFont(QFont("Futura",60 ))
        self.welcomeLabel.setAlignment(Qt.AlignCenter)
        self.welcomeLabel.setStyleSheet('background: transparent; color: gold')

        self.size=QSize(200,200)

        self.backButton = QPushButton('Back \n')
        self.backButton.setFont(QFont("Futura", 38))
        self.backButton.clicked.connect(self.back)
        self.backButton.setStyleSheet('background: transparent; color: gold')

        # Display Label
        self.display_label = QLabel("" + "\n")
        self.display_label.setFont(QFont("Futura", 60))
        #self.display_label.setAlignment(Qt.AlignCenter)
        self.display_label.setStyleSheet('background: transparent; color: gold')

        # Button setup happens here
        self.button0 = QPushButton("")
        self.button0.clicked.connect(self.press0)
        self.button0.setIcon(QIcon('0.png'))
        self.button0.setIconSize(self.size)
        self.button0.setStyleSheet('background: #1C1A1B;;border: 0px')

        # Button setup happens here
        self.button1 = QPushButton("")
        self.button1.clicked.connect(self.press1)
        self.button1.setIcon(QIcon('1.png'))
        self.button1.setIconSize(self.size)
        self.button1.setStyleSheet('background: #1C1A1B; border: 0px')


        self.button2 = QPushButton("")
        self.button2.clicked.connect(self.press2)
        self.button2.setIcon(QIcon('2.png'))
        self.button2.setIconSize(self.size)
        self.button2.setStyleSheet('background: #1C1A1B; border: 0px')
        
        self.button3 = QPushButton("")
        self.button3.clicked.connect(self.press3)
        self.button3.setIcon(QIcon('3.png'))
        self.button3.setIconSize(self.size)
        self.button3.setStyleSheet('background: #1C1A1B; border: 0px')
        
        

        self.button4 = QPushButton("")
        self.button4.clicked.connect(self.press4)
        self.button4.setIcon(QIcon('4.png'))
        self.button4.setIconSize(self.size)
        self.button4.setStyleSheet('background: #1C1A1B; border: 0px')


        self.button5 = QPushButton("")
        self.button5.setIcon(QIcon('5.png'))
        self.button5.clicked.connect(self.press5)
        self.button5.setIconSize(self.size)
        self.button5.setStyleSheet('background: #1C1A1B; border: 0px')


        self.button6 = QPushButton("");
        self.button6.setIcon(QIcon('6.png'))
        self.button6.clicked.connect(self.press6)
        self.button6.setIconSize(self.size)
        self.button6.setStyleSheet('background: #1C1A1B; border: 0px')

        self.button7 = QPushButton("");
        self.button7.clicked.connect(self.press7);
        self.button7.setIcon(QIcon('7.png'))
        self.button7.setIconSize(self.size)
        self.button7.setStyleSheet('background: #1C1A1B; border: 0px')

        self.button8 = QPushButton("")
        self.button8.clicked.connect(self.press8)
        self.button8.setIcon(QIcon('8.png'))
        self.button8.setIconSize(self.size)
        self.button8.setStyleSheet('background: #1C1A1B; border: 0px')
        
        self.button9 = QPushButton("");
        self.button9.clicked.connect(self.press9)
        self.button9.setIcon(QIcon('9.png'))
        self.button9.setIconSize(self.size)
        self.button9.setStyleSheet('background: #1C1A1B; border: 0px')      

        self.button_dot = QPushButton(". \n");
        self.button_dot.setFont(QFont("Futura", 38))
        self.button_dot.clicked.connect(self.pressDot)
        self.button_dot.setStyleSheet('background: #1C1A1B; border: 0px; color: white')

        self.enterButton = QPushButton("");
        self.enterButton.setIcon(QIcon('enter.png'))
        self.enterButton.setIconSize(self.size)
        self.enterButton.setStyleSheet('background: #1C1A1B; border: 0px')
        self.enterButton.clicked.connect(self.enter);


        self.clearButton = QPushButton("");
        self.clearButton.setIcon(QIcon('reset.png'))
        self.clearButton.clicked.connect(self.clear)
        self.clearButton.setIconSize(self.size)

        self.clearButton.setStyleSheet('background: #1C1A1B; border: 0px')
        

        self.LabelButton = QLabel('mL/hr');
        self.LabelButton.setAlignment(Qt.AlignCenter)
        self.LabelButton.setFont(QFont("Futura", 38))
        self.LabelButton.setStyleSheet('background: transparent; color: gold')
        
        # Adding buttons to grid
        self.grid.addWidget(self.button1, 7,0,2,3);
        self.grid.addWidget(self.button2, 7, 3, 2, 3);
        self.grid.addWidget(self.button3, 7, 6,2,3);
        self.grid.addWidget(self.button4, 9, 0,2,3);
        self.grid.addWidget(self.button5, 9,3,2,3);
        self.grid.addWidget(self.button6, 9,6,2,3);
        self.grid.addWidget(self.button7, 11,0,2,3);
        self.grid.addWidget(self.button8, 11,3,2,3);
        self.grid.addWidget(self.button9, 11,6,2,3);
        self.grid.addWidget(self.button0, 13, 3, 2, 3);

        self.grid.addWidget(self.clearButton, 13, 6, 2, 3);


        self.grid.addWidget(self.button_dot, 13,0,2,3)
        self.grid.addWidget(self.welcomeLabel, 0, 0, 2, 15);

        self.grid.addWidget(self.backButton, 13, 10, 2, 4)
        self.grid.addWidget(self.display_label, 5,10,2,4);
        self.grid.addWidget(self.LabelButton, 7,10,2,4)
        self.grid.addWidget(self.enterButton,9,11,2,3);
        self.setLayout(self.grid)

    def press0(self):
        global maxVolume_str
        maxVolume_str += "0"
        self.display_label.setText(maxVolume_str)
        self.display_label.setAlignment(Qt.AlignCenter)
    
    def press1(self):
        global maxVolume_str;
        maxVolume_str += "1";

        self.display_label.setFont(QFont("Futura", 60))
        self.display_label.setText(maxVolume_str)
        self.display_label.setAlignment(Qt.AlignCenter)
    def press2(self):
        global maxVolume_str;
        maxVolume_str += "2";

        self.display_label.setFont(QFont("Futura", 60))
        self.display_label.setText(maxVolume_str)
        self.display_label.setAlignment(Qt.AlignCenter)
    def press3(self):
        global maxVolume_str
        maxVolume_str += "3"

        self.display_label.setFont(QFont("Futura", 60))
        self.display_label.setText(maxVolume_str)
        self.display_label.setAlignment(Qt.AlignCenter)
    def press4(self):
        global maxVolume_str
        self.display_label.setAlignment(Qt.AlignCenter)
        maxVolume_str += "4"

        self.display_label.setFont(QFont("Futura", 60))
        self.display_label.setText(maxVolume_str)
        self.display_label.setAlignment(Qt.AlignCenter)
    def press5(self):
        global maxVolume_str
        maxVolume_str += "5"
        self.display_label.setFont(QFont("Futura", 60))
        self.display_label.setText(maxVolume_str)
        self.display_label.setAlignment(Qt.AlignCenter)

    def press6(self):
        global maxVolume_str
        maxVolume_str += "6"
        self.display_label.setFont(QFont("Futura", 60))
        self.display_label.setText(maxVolume_str)
        self.display_label.setAlignment(Qt.AlignCenter)
    def press7(self):
        global maxVolume_str;
        maxVolume_str += "7"

        self.display_label.setFont(QFont("Futura", 60))
        self.display_label.setText(maxVolume_str)
        self.display_label.setAlignment(Qt.AlignCenter)
    def press8(self):
        global maxVolume_str;
        maxVolume_str += "8";

        self.display_label.setFont(QFont("Futura", 60));
        self.display_label.setText(maxVolume_str);
    def press9(self):
        global maxVolume_str;
        maxVolume_str += "9"

        self.display_label.setFont(QFont("Futura", 60))
        self.display_label.setText(maxVolume_str)
        self.display_label.setAlignment(Qt.AlignCenter)
    def pressDot(self):
        global maxVolume_str
        maxVolume_str += "."

        self.display_label.setFont(QFont("Futura", 60))
        self.display_label.setText(maxVolume_str)
        self.display_label.setAlignment(Qt.AlignCenter)
    def enter(self):
        global maxVolume_str, maxVolume_val, adjustScreen, drainagePressure, unitScreen
        maxVolume_val = float(maxVolume_str)

        if operation_mode=='Volume Drain':
            adjustScreen = Adjustment()
            adjustScreen.show()
            volumeDrainage.hide()
        elif operation_mode=='Pressure Drain \n Volume Limit':
            adjustScreen = Adjustment()
            adjustScreen.show()
            volumeDrainage.hide()
        elif operation_mode=='Volume Drain \n Pressure Limit':
            unitScreen = UnitSelection()
            unitScreen.show()
            volumeDrainage.hide()


    def clear(self):
        global maxVolume_val
        global maxVolume_str
        maxVolume_str = ""
        self.display_label.setText(openPressure_str);  
        self.display_label.setAlignment(Qt.AlignCenter)
    def back(self):
        global drainSelection, maxVolume_str,maxVolume_val
        maxVolume_val=0
        maxVolume_str=''


        if operation_mode=='Volume Drain':
            drainSelection.show()
            volumeDrainage.hide()
        elif operation_mode=='Pressure Drain \n Volume Limit':
            drainagePressure.show()
            volumeDrainage.hide()
        elif operation_mode=='Volume Drain \n Pressure Limit':
            drainSelection.show()
            volumeDrainage.hide()

class OpeningPressure(QWidget):
    def __init__(self): 
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedWidth(1920)
        self.setFixedHeight(1080)
        self.grid = QGridLayout()      
        self.text_field = QPlainTextEdit(self)
        self.text_field.setMinimumSize (1920,1080)
        self.text_field.setStyleSheet("background-image: url(gray-background.png); background-attachment: fixed")
        
        
        # Set Up Label
        self.drainageLabel = QLabel("Select Drainage Pressure");
        self.drainageLabel.setStyleSheet('background: transparent; color: gold')
        self.drainageLabel.setFont(QFont("Futura", 75));
        self.drainageLabel.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(self.drainageLabel, 0, 0, 2, 15);


        self.size=QSize(200,200)

        self.backButton = QPushButton('Back \n')
        self.backButton.setFont(QFont("Futura", 38))
        self.backButton.clicked.connect(self.backFunction)
        self.backButton.setStyleSheet('background: transparent; color: gold')

        # Display Label
        self.display_label = QPushButton("" + "\n")
        self.display_label.setFont(QFont("Futura", 60))
        #self.display_label.setAlignment(Qt.AlignCenter)
        self.display_label.setStyleSheet('background: transparent; color: gold')

        # Button setup happens here
        self.button0 = QPushButton("")
        self.button0.clicked.connect(self.press0)
        self.button0.setIcon(QIcon('0.png'))
        self.button0.setIconSize(self.size)
        self.button0.setStyleSheet('background: #1C1A1B;;border: 0px')

        # Button setup happens here
        self.button1 = QPushButton("")
        self.button1.clicked.connect(self.press1)
        self.button1.setIcon(QIcon('1.png'))
        self.button1.setIconSize(self.size)
        self.button1.setStyleSheet('background: #1C1A1B; border: 0px')


        self.button2 = QPushButton("")
        self.button2.clicked.connect(self.press2)
        self.button2.setIcon(QIcon('2.png'))
        self.button2.setIconSize(self.size)
        self.button2.setStyleSheet('background: #1C1A1B; border: 0px')
       
        self.button3 = QPushButton("")
        self.button3.clicked.connect(self.press3)
        self.button3.setIcon(QIcon('3.png'))
        self.button3.setIconSize(self.size)
        self.button3.setStyleSheet('background: #1C1A1B; border: 0px')
       
      

        self.button4 = QPushButton("")
        self.button4.clicked.connect(self.press4)
        self.button4.setIcon(QIcon('4.png'))
        self.button4.setIconSize(self.size)
        self.button4.setStyleSheet('background: #1C1A1B; border: 0px')


        self.button5 = QPushButton("")
        self.button5.setIcon(QIcon('5.png'))
        self.button5.clicked.connect(self.press5)
        self.button5.setIconSize(self.size)
        self.button5.setStyleSheet('background: #1C1A1B; border: 0px')


        self.button6 = QPushButton("");
        self.button6.setIcon(QIcon('6.png'))
        self.button6.clicked.connect(self.press6)
        self.button6.setIconSize(self.size)
        self.button6.setStyleSheet('background: #1C1A1B; border: 0px')

        self.button7 = QPushButton("");
        self.button7.clicked.connect(self.press7);
        self.button7.setIcon(QIcon('7.png'))
        self.button7.setIconSize(self.size)
        self.button7.setStyleSheet('background: #1C1A1B; border: 0px')

        self.button8 = QPushButton("")
        self.button8.clicked.connect(self.press8)
        self.button8.setIcon(QIcon('8.png'))
        self.button8.setIconSize(self.size)
        self.button8.setStyleSheet('background: #1C1A1B; border: 0px')
        
        self.button9 = QPushButton("");
        self.button9.clicked.connect(self.press9)
        self.button9.setIcon(QIcon('9.png'))
        self.button9.setIconSize(self.size)
        self.button9.setStyleSheet('background: #1C1A1B; border: 0px')      

        self.button_dot = QPushButton(". \n");
        self.button_dot.setFont(QFont("Futura", 38))
        self.button_dot.clicked.connect(self.pressDot)
        self.button_dot.setStyleSheet('background: #1C1A1B; border: 0px; color: white')

        self.enterButton = QPushButton("");
        self.enterButton.setIcon(QIcon('enter.png'))
        self.enterButton.setIconSize(self.size)
        self.enterButton.setStyleSheet('background: #1C1A1B; border: 0px')
        self.enterButton.clicked.connect(self.enter);


        self.clearButton = QPushButton("");
        self.clearButton.setIcon(QIcon('reset.png'))
        self.clearButton.clicked.connect(self.clear)
        self.clearButton.setIconSize(self.size)

        self.clearButton.setStyleSheet('background: #1C1A1B; border: 0px')
        

        self.LabelButton = QLabel(units);
        self.LabelButton.setAlignment(Qt.AlignCenter)
        self.LabelButton.setFont(QFont("Futura", 38))
        self.LabelButton.setStyleSheet('background: transparent; color: gold')
        
        # Adding buttons to grid
        self.grid.addWidget(self.button1, 7,0,2,3);
        self.grid.addWidget(self.button2, 7, 3, 2, 3);
        self.grid.addWidget(self.button3, 7, 6,2,3);
        self.grid.addWidget(self.button4, 9, 0,2,3);
        self.grid.addWidget(self.button5, 9,3,2,3);
        self.grid.addWidget(self.button6, 9,6,2,3);
        self.grid.addWidget(self.button7, 11,0,2,3);
        self.grid.addWidget(self.button8, 11,3,2,3);
        self.grid.addWidget(self.button9, 11,6,2,3);
        self.grid.addWidget(self.button0, 13, 3, 2, 3);

        self.grid.addWidget(self.clearButton, 13, 6, 2, 3);


        self.grid.addWidget(self.button_dot, 13,0,2,3)
        self.grid.addWidget(self.drainageLabel, 0, 0, 2, 15);

        self.grid.addWidget(self.backButton, 13, 10, 2, 4)
        self.grid.addWidget(self.display_label, 5,10,2,4);
        self.grid.addWidget(self.LabelButton, 7,10,2,4)
        self.grid.addWidget(self.enterButton,9,11,2,3);
        self.setLayout(self.grid)

    def press0(self):
        global openPressure_str;
        openPressure_str += "0";

        self.display_label.setText(openPressure_str);
        self.display_label.setFont(QFont("Futura", 60));
        
    def press1(self):
        global openPressure_str;
        openPressure_str += "1";

        self.display_label.setFont(QFont("Futura", 60));
        self.display_label.setText(openPressure_str);
    def press2(self):
        global openPressure_str;
        openPressure_str += "2";

        self.display_label.setFont(QFont("Futura", 60));
        self.display_label.setText(openPressure_str);
    def press3(self):
        global openPressure_str;
        openPressure_str += "3";

        self.display_label.setFont(QFont("Futura", 60));
        self.display_label.setText(openPressure_str);
    def press4(self):
        global openPressure_str;
        openPressure_str += "4";

        self.display_label.setFont(QFont("Futura", 60));
        self.display_label.setText(openPressure_str);
    def press5(self):
        global openPressure_str;
        openPressure_str += "5";

        self.display_label.setFont(QFont("Futura", 60));
        self.display_label.setText(openPressure_str);
    def press6(self):
        global openPressure_str;
        openPressure_str += "6";

        self.display_label.setFont(QFont("Futura", 60));
        self.display_label.setText(openPressure_str);
    def press7(self):
        global openPressure_str;
        openPressure_str += "7";

        self.display_label.setFont(QFont("Futura", 60));
        self.display_label.setText(openPressure_str);
    def press8(self):
        global openPressure_str;
        openPressure_str += "8";

        self.display_label.setFont(QFont("Futura", 60));
        self.display_label.setText(openPressure_str);
    def press9(self):
        global openPressure_str;
        openPressure_str += "9";

        self.display_label.setFont(QFont("Futura", 60));
        self.display_label.setText(openPressure_str);
    def pressDot(self):
        global openPressure_str;
        openPressure_str += "."

        self.display_label.setFont(QFont("Futura", 60));
        self.display_label.setText(openPressure_str);
    def enter(self):

        global opening_pressure_val, volumeDrainage, adjustScreen
        opening_pressure_val = float(openPressure_str);
    
        # Need to check where we are coming from and move accordingly
        if operation_mode=='Pressure Drain':
            adjustScreen = Adjustment();
            adjustScreen.show()
            drainagePressure.hide()
        elif operation_mode=='Pressure Drain \n Volume Limit':
            volumeDrainage = VolumeLimit()
            volumeDrainage.show()
            drainagePressure.hide()
        elif operation_mode=='Volume Drain \n Pressure Limit':
            adjustScreen = Adjustment();
            adjustScreen.show()
            drainagePressure.hide()
        


    def clear(self):
        global opening_pressure_val;
        global openPressure_str;
        openPressure_str = "";
        opening_pressure_val = None;
        self.display_label.setText(openPressure_str);  
    def backFunction(self):
        global drainSelection, openPressure_str,opening_pressure_val
        openPressure_str=''
        opening_pressure_val=0

        # Where did we come from?

        if operation_mode=='Pressure Drain':
            unitScreen.show()
            drainagePressure.hide()
        elif operation_mode=='Pressure Drain \n Volume Limit':
            unitScreen.show()
            drainagePressure.hide()
        elif operation_mode=='Volume Drain \n Pressure Limit':
            # Go back to the volume selection screen
            unitScreen.show()
            drainagePressure.hide()




        self.setLayout(self.grid)

class UnitSelection(QWidget):
    def __init__(self): 
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedWidth(1920)
        self.setFixedHeight(1080)
        self.grid = QGridLayout()      
        self.text_field = QPlainTextEdit(self)
        self.text_field.setMinimumSize (1920,1080)
        self.text_field.setStyleSheet("background-image: url(gray-background.png); background-attachment: fixed")
        
        # Set Up Label
        self.setUp = QLabel("Select Desired Units Mode");
        self.setUp.setStyleSheet('background: transparent; color: gold')
        self.setUp.setFont(QFont("Futura", 75));
        self.setUp.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(self.setUp, 0, 0, 2, 15);

        # Back Button Implementation

        self.backButton = QPushButton("Back \n");
        self.backButton.setFont(QFont("Futura", 60));
        self.backButton.setStyleSheet('background-image: url(./gray-background.png); color: gold; border: 2px solid-black')
        self.backButton.clicked.connect(self.backFunction)

        self.grid.addWidget(self.backButton, 13, 6, 2, 3);

        # Check what the volume/pressure_flags are
        self.mmHg = QPushButton("mmHg \n");
        self.mmHg.setStyleSheet('background-image: url(./gray-background.png); color: gold; border: 2px solid-black; padding:30px')
        self.mmHg.setFont(QFont("Futura",60));
        self.mmHg.clicked.connect(self.mmHgUnits)
        self.grid.addWidget(self.mmHg, 5,3, 6, 4);

        self.cmH20 = QPushButton("cmH20\n");
        self.cmH20.setStyleSheet('background-image: url(./gray-background.png); color: gold; border: 2px solid-black;padding:30px')
        self.cmH20.setFont(QFont("Futura", 60));
        self.cmH20.clicked.connect(self.cmH20Units)
        self.grid.addWidget(self.cmH20, 5, 8, 6, 4);

        self.setLayout(self.grid)

    def mmHgUnits(self):
        # load the opening pressure here regardless of where we came from

        global drainagePressure, units
        units = 'mmHg'
        drainagePressure = OpeningPressure()
        drainagePressure.show()

        unitScreen.hide()


    def cmH20Units(self):
        # load the opening pressure here regardless of where we came from 
        global drainagePressure, units
        units = 'cmH20'
        drainagePressure = OpeningPressure()
        drainagePressure.show()

        unitScreen.hide()


    def backFunction(self):
        if operation_mode=='Pressure Drain':
            drainSelection.show()
            unitScreen.hide()
        elif operation_mode=='Pressure Drain \n Volume Limit':
            drainSelection.show()
            unitScreen.hide()
        elif operation_mode=='Volume Drain \n Pressure Limit':
            # Go back to the volume selection screen
            volumeDrainage.show()
            unitScreen.hide()

class DrainageSelection(QWidget):
    def __init__(self):
       
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedWidth(1920)
        self.setFixedHeight(1080)
        self.grid = QGridLayout()      
        self.text_field = QPlainTextEdit(self)
        self.text_field.setMinimumSize (1920,1080)
        self.text_field.setStyleSheet("background-image: url(gray-background.png); background-attachment: fixed")


        self.DrainageQuestion = QLabel("Select Drainage Mode")
        self.DrainageQuestion.setAlignment(Qt.AlignCenter)
        self.DrainageQuestion.setFont(QFont("Futura", 75))
        self.DrainageQuestion.setStyleSheet('background: transparent; color: gold')
        self.grid.addWidget(self.DrainageQuestion, 2,0,2,15)



        self.PressureButton = QPushButton("Pressure \n")
        self.PressureButton.setStyleSheet('background-image: url(./gray-background.png); color: gold; border: 2px solid-black')
        self.PressureButton.setFont(QFont("Futura",50))
        self.PressureButton.clicked.connect(self.pressureFunction)
        self.grid.addWidget(self.PressureButton, 4,0,4,3)

        self.VolumeButton = QPushButton("Volume \n")
        self.VolumeButton.setStyleSheet('background-image: url(./gray-background.png); color: gold; border: 2px solid-black')
        self.VolumeButton.setFont(QFont("Futura",50))
        self.VolumeButton.clicked.connect(self.volumeFunction)
        self.grid.addWidget(self.VolumeButton, 4,4,4,3)

        self.PressureLimitVol = QPushButton("Pressure Limited \n Volume")
        self.PressureLimitVol.setStyleSheet('background-image: url(./gray-background.png); color: gold; border: 2px solid-black')
        self.PressureLimitVol.setFont(QFont("Futura",50))
        self.PressureLimitVol.clicked.connect(self.pressureLimit)
        self.grid.addWidget(self.PressureLimitVol, 4,8,4,3)

        self.VolumeLimitPres = QPushButton("Volume Limited \n Pressure")
        self.VolumeLimitPres.setStyleSheet('background-image: url(./gray-background.png); color: gold; border: 2px solid-black')
        self.VolumeLimitPres.setFont(QFont("Futura",50))
        self.VolumeLimitPres.clicked.connect(self.volumeLimit)
        self.grid.addWidget(self.VolumeLimitPres, 4,12,4,3)



        self.setLayout(self.grid)

    def pressureFunction(self):
        global operation_mode, unitScreen
        operation_mode = 'Pressure Drain'

        unitScreen = UnitSelection()
        unitScreen.show()  
        drainSelection.hide()

        # Units -> pressure -> adjust -> summary 


    def volumeFunction(self):
        global operation_mode, volumeDrainage
        operation_mode = 'Volume Drain'

        volumeDrainage = VolumeLimit()
        volumeDrainage.show()
        drainSelection.hide()

        # volume -> adjust -> summary 

    def pressureLimit(self):
        global operation_mode, unitScreen
        operation_mode = 'Pressure Drain \n Volume Limit'
        unitScreen = UnitSelection()
        unitScreen.show()  
        drainSelection.hide()

        # Units -> pressure -> volume limit -> adjust -> summary 

    def volumeLimit(self):
        global operation_mode, volumeDrainage
        operation_mode = 'Volume Drain \n Pressure Limit'
        
        volumeDrainage = VolumeLimit()
        volumeDrainage.show()
        drainSelection.hide()
        # volume limit -> units -> pressure -> adjust -> summary 



    def back(self):

        global zeroNow, zeroLater, drainSelection
        if zeroNowFlag==True:
            zeroNow.show()
        if zeroLaterFlag==True:
            zeroWarningScreen.show()
        drainSelection.hide()

class ZeroTransducer(QWidget):
    def __init__(self):
       
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedWidth(1920)
        self.setFixedHeight(1080)
        self.grid = QGridLayout()      
        self.text_field = QPlainTextEdit(self)
        self.text_field.setMinimumSize (1920,1080)
        self.text_field.setStyleSheet("background-image: url(gray-background.png); background-attachment: fixed")

        self.calibration_count = 0

        self.zeroPrompt = QLabel('Zero both the Patient Monitor and the AutoEVD \n at the Same time')
        self.zeroPrompt.setAlignment(Qt.AlignCenter)
        self.zeroPrompt.setFont(QFont("Futura", 75))
        self.zeroPrompt.setStyleSheet('background: transparent; color: gold')
        self.grid.addWidget(self.zeroPrompt,  2,0,2,15)
    


        self.ZeroingButton = QPushButton("Zero");
        self.ZeroingButton.setFont(QFont("Futura", 75));
        self.ZeroingButton.setStyleSheet('background-image: url(./gray-background.png); color: gold; border: 2px solid-black')
        self.ZeroingButton.clicked.connect(self.Calibration)
        self.grid.addWidget(self.ZeroingButton, 4,8,4,3);


        self.backButton = QPushButton("Back");
        self.backButton.setFont(QFont("Futura", 75))
        self.backButton.setStyleSheet('background-image: url(./gray-background.png); color: gold; border: 2px solid-black')
        self.backButton.clicked.connect(self.backFunction)
        self.grid.addWidget(self.backButton, 4,4,4,3);
        self.setLayout(self.grid);



    def backFunction(self):

        global zeroNowFlag
        #zeroNowFlag=False;
        toTransducer.show()
        zeroNow.hide()

    def restart(self):
        global baselinePressure
        temp = 0;
        for i in range(5):
            temp += random.randint(1,10);
            time.sleep(1);

        baselinePressure = temp/5.0;

    def continueFunction(self):

        # Need to revert everything here

        self.restartButton.hide()
        self.continueButton.hide()
        self.CalibrationLabel.hide()


        self.backButton.show()
        self.zeroPrompt.show()
        self.ZeroingButton.show()

        global zeroNowFlag,drainSelection
        zeroNowFlag = True 
        drainSelection = DrainageSelection()
        drainSelection.show()
        zeroNow.hide()

    def Calibration(self):
        global zeroComplete
        if self.calibration_count==0:
            global baselinePressure
            temp = 0;
            for i in range(5):
                temp += random.randint(1,10);
                time.sleep(1);

            baselinePressure = temp/5.0;
            self.calibration_count+=1

            self.backButton.hide()
            self.zeroPrompt.hide()
            self.ZeroingButton.hide()

        status_text=''

        if 0.0 <= baselinePressure <= 10.0:
            zeroComplete = True
            status_text = 'Calibration Sucessful!'
        else:
            zeroComplete = False
            status_text = 'Calibration Failed. Please try again'


        self.CalibrationLabel = QLabel(status_text)
        self.CalibrationLabel.setAlignment(Qt.AlignCenter)
        self.CalibrationLabel.setFont(QFont("Futura", 75))
        self.CalibrationLabel.setStyleSheet('background: transparent; color: gold')
        self.grid.addWidget(self.CalibrationLabel, 2,0,2,15)
        

        self.restartButton = (QPushButton("Restart \n"))
        self.restartButton.setStyleSheet('background-image: url(./gray-background.png); color: gold; border: 2px solid-black')
        self.restartButton.setFont(QFont("Futura", 75))
        self.restartButton.clicked.connect(self.restart)
        self.grid.addWidget(self.restartButton, 5,3,10,3)
        


        self.continueButton = QPushButton("Continue \n")
        self.continueButton.setFont(QFont("Futura", 75))
        self.continueButton.clicked.connect(self.continueFunction)
        self.continueButton.setStyleSheet('background-image: url(./gray-background.png); color: gold; border: 2px solid-black')
        self.grid.addWidget(self.continueButton, 5,8,10,3)

        self.setLayout(self.grid)
    
class ZeroWarningScreen(QWidget):
    def __init__(self):

        # Set up for the remainder of the process
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedWidth(1920)
        self.setFixedHeight(1080)
        self.grid = QGridLayout()      
        self.text_field = QPlainTextEdit(self)
        self.text_field.setMinimumSize (1920,1080)
        self.text_field.setStyleSheet("background-image: url(gray-background.png); background-attachment: fixed")



        self.warningLabel = QLabel("Warning! Device must be zeroed \n before device runs!")
        self.warningLabel.setFont(QFont("Futura", 75))
        self.warningLabel.setAlignment(Qt.AlignCenter)
        self.warningLabel.setStyleSheet('background: transparent; color: gold')
        self.grid.addWidget(self.warningLabel,2,6,2,3)



        self.backButton = (QPushButton("Back \n"))
        self.backButton.setStyleSheet('background-image: url(./gray-background.png); color: gold; border: 2px solid-black')
        self.backButton.setFont(QFont("Futura", 60))
        self.backButton.clicked.connect(self.backFunction)
        self.grid.addWidget(self.backButton, 5,3,6,4)


        self.continueButton = QPushButton("Continue \n")
        self.continueButton.setFont(QFont("Futura", 60))
        self.continueButton.clicked.connect(self.continueFunction)
        self.continueButton.setStyleSheet('background-image: url(./gray-background.png); color: gold; border: 2px solid-black')
        self.grid.addWidget(self.continueButton, 5,8,6,4)
        self.setLayout(self.grid)

    def backFunction(self):
        toTransducer.show()
        zeroWarningScreen.hide()
    def continueFunction(self):
        global zeroLaterFlag, drainSelection
        zeroLaterFlag = True 
        drainSelection = DrainageSelection()
        drainSelection.show()
        zeroWarningScreen.hide()

class ZeroSetUp(QWidget):
    def __init__(self):

        # Set up for the remainder of the process
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedWidth(1920)
        self.setFixedHeight(1080)
        self.grid = QGridLayout()      
        self.text_field = QPlainTextEdit(self)
        self.text_field.setMinimumSize (1920,1080)
        self.text_field.setStyleSheet("background-image: url(gray-background.png); background-attachment: fixed")

        # Zero Now or Later Label
        self.chooseLabel = QLabel(" Zero Now or Later?  ")
        self.chooseLabel.setFont(QFont("Futura", 75))
        self.chooseLabel.setAlignment(Qt.AlignCenter)
        self.chooseLabel.setStyleSheet('background: transparent; color: gold')
        self.grid.addWidget(self.chooseLabel,2,6,2,3)

        # Zero Now Button
        self.ZeroNow = QPushButton("Zero \n Now")
        self.ZeroNow.setStyleSheet('background-image: url(./gray-background.png); color: gold; border: 2px solid-black')
        self.ZeroNow.setFont(QFont("Futura", 45))
        self.ZeroNow.clicked.connect(self.ZeroNowFunction)
        self.grid.addWidget(self.ZeroNow, 5,3,6,4)


        # Zero Later Button
        self.ZeroLater = QPushButton("Zero \n Later")
        self.ZeroLater.setFont(QFont("Futura", 45))
        self.ZeroLater.clicked.connect(self.ZeroLaterFunction)
        self.ZeroLater.setStyleSheet('background-image: url(./gray-background.png); color: gold; border: 2px solid-black')
        self.grid.addWidget(self.ZeroLater, 5,8,6,4)


        self.Back = QPushButton("Back \n")
        self.Back.setStyleSheet('background-image: url(./gray-background.png); color: gold; border: 2px solid-black')
        self.Back.setFont(QFont("Futura", 45))
        self.Back.clicked.connect(self.BackScreen)
        self.grid.addWidget(self.Back, 13,6,2,3)
        self.setLayout(self.grid)

    def ZeroNowFunction(self):
        global zeroNow, zeroComplete, zeroNowFlag
        
        zeroNowFlag = True
        zeroNow = ZeroTransducer()
        zeroNow.show()
        toTransducer.hide()


    def ZeroLaterFunction(self):
        global zeroWarningScreen,zeroComplete, zeroLaterFlag
        zeroComplete = False                
        zeroLaterFlag= False
        zeroWarningScreen = ZeroWarningScreen()
        zeroWarningScreen.show()
        toTransducer.hide()

    def BackScreen(self): 
        if w !=None:
            w.show()
        toTransducer.hide()

class SelectTransducer(QWidget):
    def __init__(self):

        # Set up for the remainder of the process
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedWidth(1920)
        self.setFixedHeight(1080)
        self.grid = QGridLayout()      
        self.text_field = QPlainTextEdit(self)
        self.text_field.setMinimumSize (1920,1080)
        self.text_field.setStyleSheet("background-image: url(gray-background.png); background-attachment: fixed")


        # Now we ask all of the questions that we need to here 
        self.DisplayLabel = QLabel("Select Device Type")
        self.DisplayLabel.setStyleSheet('background-image: url(./gray-background.png); color: gold; border: 2px solid-black')
        self.DisplayLabel.setFont(QFont("Futura", 60))
        self.grid.addWidget(self.DisplayLabel, 2,6,2,3)

        # Pressure transducer
        self.PressureTransducer = QPushButton("EVD \n")
        self.PressureTransducer.setStyleSheet('background-image: url(./gray-background.png); color: gold; border: 2px solid-black')
        self.PressureTransducer.setFont(QFont("Futura", 45))
        self.PressureTransducer.clicked.connect(self.pressureTransducer)
        self.grid.addWidget(self.PressureTransducer, 5,3,6,4)
        
        # Strain Gauge
        self.NoPressureTransducer = QPushButton("Non-EVD \n")
        self.NoPressureTransducer.setStyleSheet('background-image: url(./gray-background.png); color: gold; border: 2px solid-black')
        self.NoPressureTransducer.clicked.connect(self.noPressureTransducer)
        self.NoPressureTransducer.setFont(QFont("Futura", 45))
        self.grid.addWidget(self.NoPressureTransducer, 5,8,6,4)

               
        self.setLayout(self.grid)

    def pressureTransducer(self):
        global toTransducer
        toTransducer = ZeroSetUp()
        toTransducer.show()

        w.hide()

    def noPressureTransducer(self):
        global toTransducer
        toTransducer = ZeroSetUp()
        toTransducer.show()

        w.hide()
    
class MainWindow(QMainWindow):
    def __init__(self):
        global w;
        
        super(MainWindow, self).__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowTitle("")
        self.setFixedWidth(1920)
        self.setFixedHeight(1080)
        w = SelectTransducer()
        self.setStyleSheet("background-image: url(./gray-background.png);")
        self.setCentralWidget(w);

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
