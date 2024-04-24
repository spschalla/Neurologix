
import math
import random
import time;
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import pyqtgraph as pg
from random import randint



# Windows that are involved in the running of the device

pressurePrompt = None;
''' Reference to first screen here '''
w = None;

'''
The sensor select screens for each of the two operation modes of the device. 
'''
EVDSensorSelectScreen = None;
LumbarSensorSelect = None;

ZeroingPrompt = None;

# Flags that are needed for device operation

''' Drainage type flags go here 
 @ mode: Device Type
 mode=1 : EVD System
 mode=0 : LumbarDrainage System
 mode=-1 : Not set


 @ Control: Type of Control Over the Device
 -1: Not been set yet
  0: Device is controlled by an pressure transducer
  1: Device is controlled by a strain gauge
'''

''' Transducer Type goes here
-1: not set 
 0: Pressure Transducer
 1: Strain Gauge
'''
mode = -1
controlFlag = -1
transducerFlag = -1

''' Transducer Type goes here
-1: not set 
 0: Pressure Transducer
 1: Strain Gauge
'''

'''
Sensor markers are here
'''

baselinePressure = 0

# Pressure Stuff goes here 
opening_pressure_val = 0;
openPressure_str = ""


'''
All of the Windows that are created as part of UI are kept track of here

'''
ZeroingWindow = None;
CalibrationWindow = None;
SucessWindow = None;
DrainageScreen = None;
OpenPressure = None;
UnitPrompt = None;
VolumePrompt = None;
VolumetricMaximum = None;


# Screens involved with pressure

ZeroingPrompt = None;

openingPressure = None;         # Enter opening pressure
closeDelayPrompt = None;        # Ask if there is a closing time delay
closeDelay = None;              # Enter closing time delay
volumeLimitPrompt = None;       # Asl volume limit
volumeLimit = None;
summary = None;



# Volume limit info
volume_limit_val = 0;
volumeLimit_str = "";

operationScreen = None;

volumeString = ""
volumeamount = 0;

# Volume limit info
volumeAmount = 0;
volumeString = "";

pressureAmount = 0
pressureSummary = 0

pressureString = ""

closeDelayString = ''
closeDelay = 0

volumeLimit_str = ''
volumeLimit = 0;
max_Vol = 0
maxVol_str = ''

# Operation Screen Globals start here
alarmScreen = None;
zeroScreen = None;
clampScreen = None;
clearedScreen = None;
programScreen = None;
errorScreen = None;
logScreen = None;

class LogScreen(QWidget):
    global logScreen
    def __init__(self):
        super().__init__();
        self.setFixedWidth(800);
        self.setFixedHeight(400);
        self.grid = QGridLayout();

        
        self.text_field = QPlainTextEdit(self)
        self.text_field.setMinimumSize (1024,600)
        self.text_field.setStyleSheet("background-image: url(background.png); background-attachment: fixed")

        # Display label goes here 
        self.display_label = QLabel('Scroll through I/O Information');
        self.display_label.setAlignment(Qt.AlignCenter)
        self.display_label.setFont(QFont('Helvetica', 40));
        self.display_label.setStyleSheet('background: transparent; color: gold');

        # Adding the logs as needed
        self.log1_label = QLabel('Run1: Information Here');
        self.log1_label.setAlignment(Qt.AlignCenter);
        self.log1_label.setFont(QFont('Helvetica', 40));
        self.log1_label.setStyleSheet('background: transparent; color:gold');

        self.backButton = QPushButton('Back');
        self.backButton.setFont(QFont('Helvetica', 40));
        self.backButton.setStyleSheet('background: transparent; color:gold');
        self.backButton.clicked.connect(self.back);
        


        self.grid.addWidget(self.display_label, 2,6,2,15);
        self.grid.addWidget(self.log1_label, 7, 6,2,15)
        self.grid.addWidget(self.backButton, 10, 6,2,15);

        self.setLayout(self.grid)
    def back(self):
        logScreen.hide();

        






class ClampDevice(QWidget):
    global clampScreen
    def __init__(self):
        super().__init__();
        self.setFixedWidth(800);
        self.setFixedHeight(400);
        self.grid = QGridLayout();

        self.text_field = QPlainTextEdit(self)
        self.text_field.setMinimumSize (1024,600)
        self.text_field.setStyleSheet("background-image: url(background.png); background-attachment: fixed")

        self.ClampQuestion = QLabel('Select Clamp Duration')
        self.ClampQuestion.setFont(QFont('Arial',50));
        self.ClampQuestion.setAlignment(Qt.AlignCenter);
        self.ClampQuestion.setStyleSheet('background: transparent; color: gold')
        self.grid.addWidget(self.ClampQuestion, 0,4,2,10)

        self.Clamp5 = QPushButton('5 \n Minutes');
        self.Clamp5.setFont(QFont('Arial',28));
        self.Clamp5.clicked.connect(self.ClampScreen5)
        self.Clamp5.setStyleSheet('background: transparent; color: gold')
        self.grid.addWidget(self.Clamp5, 6,0,3,3)

        self.Clamp10 = QPushButton('10\n Minutes')
        self.Clamp10.setFont(QFont('Arial',28));
        self.Clamp10.clicked.connect(self.ClampScreen10)
        self.Clamp10.setStyleSheet('background: transparent; color: gold')
        self.grid.addWidget(self.Clamp10, 6,7,3,3)

        self.ClampInfinity = QPushButton('Indefintely \n');
        self.ClampInfinity.setFont(QFont('Arial',32));
        self.ClampInfinity.clicked.connect(self.ClampScreen)
        self.ClampInfinity.setStyleSheet('background: transparent; color: gold')
        self.grid.addWidget(self.ClampInfinity,6,13,3,3)

        self.BackButton = QPushButton('Back \n');
        self.BackButton.setFont(QFont('Arial', 30))
        self.BackButton.clicked.connect(self.Back)
        self.BackButton.setStyleSheet('background: transparent; color: gold')

        self.grid.addWidget(self.BackButton, 11,7,3,3)
        self.setLayout(self.grid)
    def ClampScreen5(self):
        self.ClampQuestion.setVisible(False)
        self.Clamp5.setVisible(False)
        self.Clamp10.setVisible(False)
        self.ClampInfinity.setVisible(False)
        self.grid.removeWidget(self.BackButton)

        self.ClampedLabel = QLabel('Device is Clamped');
        self.ClampedLabel.setStyleSheet('background: transparent; color: gold')
        self.ClampedLabel.setFont(QFont('Arial',40));
        self.ClampedLabel.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(self.ClampedLabel, 0,6,3,3);

        self.lcd = QLCDNumber()
        self.lcd.setStyleSheet('background: transparent; color: gold')
        self.grid.addWidget(self.lcd, 3,6,4,3);
        self.timer = QTimer(self);



        self.time = 300
        self.lcd.display("%d:%02d" % (self.time/60,self.time % 60))

        # Restart the timer
        self.timer.start(1000)

        # To update timer
        self.timer.timeout.connect(self.updateLCD)
        

        self.grid.addWidget(self.lcd, 5,6,3,3)

        self.grid.addWidget(self.BackButton, 9,6,4,4)
    def ClampScreen(self):
        self.ClampQuestion.setVisible(False)
        self.Clamp5.setVisible(False)
        self.Clamp10.setVisible(False)
        self.ClampInfinity.setVisible(False)
        self.grid.removeWidget(self.BackButton)

        self.ClampedLabel = QLabel('Device is Clamped');
        self.ClampedLabel.setStyleSheet('background: transparent; color:gold')
        self.ClampedLabel.setFont(QFont('Arial',40));
        self.ClampedLabel.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(self.ClampedLabel, 0,6,3,3);
    



        self.grid.addWidget(self.BackButton, 9,6,3,3)
    def ClampScreen10(self):
        self.ClampQuestion.setVisible(False)
        self.Clamp5.setVisible(False)
        self.Clamp10.setVisible(False)
        self.ClampInfinity.setVisible(False)
        self.grid.removeWidget(self.BackButton)

        self.ClampedLabel = QLabel('Device is Clamped');
        self.ClampedLabel.setStyleSheet('background: transparent; color: gold')
        self.ClampedLabel.setFont(QFont('Arial',40));
        self.ClampedLabel.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(self.ClampedLabel, 0,6,3,3);

        self.lcd = QLCDNumber()
        self.lcd.setStyleSheet('background: transparent; color: gold')
        self.grid.addWidget(self.lcd, 3,6,4,3);
        self.timer = QTimer(self);



        self.time = 600
        self.lcd.display("%d:%02d" % (self.time/60,self.time % 60))

        # Restart the timer
        self.timer.start(1000)

        # To update timer
        self.timer.timeout.connect(self.updateLCD)
        

        self.grid.addWidget(self.lcd, 5,6,3,3)

        self.grid.addWidget(self.BackButton, 9,6,4,4)
    def upDelay(self):
         
         self.time = (self.time + 60)
         self.lcd.display("%d:%02d" % (self.time/60,self.time % 60))
    def updateLCD(self):
        self.timer
        # Update the lcd
        self.time -= 1
        if self.time >= 0:
            self.lcd.display("%d:%02d" % (self.time/60,self.time % 60))
        else:
            self.timer.stop()
    def Back(self):
        global clampScreen
        clampScreen.hide()

class ZeroDevice(QWidget):
    global zeroScreen;
    def __init__(self):
        super().__init__();
        self.setFixedWidth(600);
        self.setFixedHeight(300);
        self.grid = QGridLayout();

        self.text_field = QPlainTextEdit(self)
        self.text_field.setMinimumSize (1024,600)
        self.text_field.setStyleSheet("background-image: url(background.png); background-attachment: fixed")


        self.ZeroLabel = QLabel('Zero Transducer');
        self.ZeroLabel.setFont(QFont('Arial',40));
        self.ZeroLabel.setAlignment(Qt.AlignCenter)
        self.ZeroLabel.setStyleSheet('background: transparent; color: gold');
        self.grid.addWidget(self.ZeroLabel, 0,5,3,5);
        
        reminder_text = '-Ensure Proper Positioning \n -Open Stopcocks \n -Press Zero When Ready'
        self.Reminders = QLabel(reminder_text);
        self.Reminders.setStyleSheet('background: transparent; color: gold')
        self.Reminders.setFont(QFont('Arial',15));
        self.Reminders.setAlignment(Qt.AlignCenter);
        self.grid.addWidget(self.Reminders, 3,6,4,3)

        self.ZeroButton = QPushButton('Zero');
        self.ZeroButton.setStyleSheet('background: transparent; color: gold')
        self.ZeroButton.setFont(QFont('Arial',39));
        self.ZeroButton.clicked.connect(self.AfterZero)
        self.grid.addWidget(self.ZeroButton, 9,2,4,4)


        self.BackButton = QPushButton('Back');
        self.BackButton.setStyleSheet('background: transparent; color: gold')
        self.BackButton.setFont(QFont('Arial',39));
        self.BackButton.clicked.connect(self.Back);
        self.grid.addWidget(self.BackButton, 9,10,4,4);
        self.setLayout(self.grid)
    def AfterZero(self):
        self.Reminders.setHidden(True);
        self.ZeroButton.setHidden(True);
        #self.BackButton.setHidden(True);

        self.ZeroLabel = QLabel('Zeroing Sucessful');
        self.ZeroLabel.setFont(QFont('Arial',25));
        self.grid.addWidget(self.ZeroLabel, 5,6,3,5)
        #self.grid.removeWidget(self.BackButton)
        self.grid.addWidget(self.BackButton, 10,5,3,5)
    def Back(self):
        global zeroScreen;
        zeroScreen.hide();
class AlarmScreen(QWidget):
     global alarmTimer 
     def __init__(self):
        super().__init__();
        self.setFixedWidth(600);
        self.setFixedHeight(300);
        self.grid = QGridLayout();

        self.text_field = QPlainTextEdit(self)
        self.text_field.setMinimumSize (1024,600)
        self.text_field.setStyleSheet("background-image: url(background.png); background-attachment: fixed")

        # Now we add the appropriate labels
        self.silencedLabel = QLabel('Alarm Silenced');
        self.silencedLabel.setStyleSheet('background: transparent; color: gold')
        self.silencedLabel.setFont(QFont('Arial',30));
        self.silencedLabel.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(self.silencedLabel, 0,6,2,3)

        self.lcd = QLCDNumber()
        self.lcd.setStyleSheet('background: transparent; color: gold')
        self.grid.addWidget(self.lcd, 3,6,4,3);
        self.timer = QTimer(self);



        self.time = 300
        self.lcd.display("%d:%02d" % (self.time/60,self.time % 60))



        self.timer.stop()
        self.time = 300
        self.lcd.display("%d:%02d" % (self.time/60,self.time % 60))

        # Restart the timer
        self.timer.start(1000)

        # To update timer
        self.timer.timeout.connect(self.updateLCD)

        self.AddDelayButton = QPushButton('+ ')
        self.AddDelayButton.setStyleSheet('background: transparent; color: gold')
        self.AddDelayButton.setFont(QFont('Arial', 15))
        self.AddDelayButton.clicked.connect(self.upDelay);
        self.grid.addWidget(self.AddDelayButton, 10,4,3,3)

        self.backButton = QPushButton('Back');
        self.backButton.setFont(QFont('Arial',15));
        self.backButton.setStyleSheet('background: transparent; color: gold')
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
# Class is responsible for the Window that contains all of the options of setting up the drain
class Operation(QWidget):

    # Set up the screens
    def __init__(self):
        super().__init__();
        self.setFixedWidth(1024);
        self.setFixedHeight(600);
        self.grid = QGridLayout();

        self.text_field = QPlainTextEdit(self)
        self.text_field.setMinimumSize (1024,600)
        self.text_field.setStyleSheet("background-image: url(background.png); background-attachment: fixed")

        

        print('Labels go here')
        # This sets up the label for the MODE OF OPERATION 
        # NB: NEEDS TO BE INTEGRATED W/ THE Previous set of code

        # Operation Mode of 0 corresponds to pressure_controlled an 
        mode_label_text = ''
        if controlFlag==1:
            # Pressure Controlled Mode
            mode_label_text = 'Pressure Controlled \n Volume Limited'
        else:
            mode_label_text= 'Volume Controlled \n Pressure Limited'
        self.modeLabel = QLabel(mode_label_text)
        self.modeLabel.setFont(QFont('Arial',18))
        self.modeLabel.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(self.modeLabel, 0,0,3,4)
        self.modeLabel.setStyleSheet('background: transparent; color: gold')


        # Adding the appropriate units here 
        pressure_label_text = openPressure_str + " " + unitFlag;
        self.pressureLabel = QLabel(pressure_label_text)
        self.pressureLabel.setFont(QFont('Arial',18))
        self.pressureLabel.setAlignment(Qt.AlignCenter)
        self.pressureLabel.setStyleSheet('background: transparent; color: gold')
        self.grid.addWidget(self.pressureLabel, 0,4,3,2)


        if (controlFlag==1):
            self.closingDelay = QLabel('Closing Delay: \n' + str(closeDelay) + ' seconds');
            self.closingDelay.setFont(QFont('Arial',18))
            self.closingDelay.setAlignment(Qt.AlignCenter)
            self.closingDelay.setStyleSheet('background: transparent; color: gold')
            self.grid.addWidget(self.closingDelay, 0,6,3,4);
        else:
            self.volumeCollected = QLabel('Volume Collected: \n' + str(200) + ' mL');
            self.volumeCollected.setFont(QFont('Arial',18))
            self.volumeCollected.setAlignment(Qt.AlignCenter)
            self.volumeCollected.setStyleSheet('background: transparent; color: gold')
            self.grid.addWidget(self.volumeCollected, 0,6,3,4);

        tempVol = -1

        if controlFlag==1:
            tempVol =  maxVol_str
        else:
            tempVol = volumeamount
        self.volumeLimit = QLabel('Volume Limit: \n' + str(tempVol) + ' mL');
        self.volumeLimit.setFont(QFont('Arial',18));
        self.volumeLimit.setAlignment(Qt.AlignCenter)
        self.volumeLimit.setStyleSheet('background: transparent; color: gold')
        self.grid.addWidget(self.volumeLimit, 0,10,3,3);

        rate_text =''
        if controlFlag==1:
            rate_text = 'Rate Limiting: \n Volume'
        else:
            rate_text = 'Rate Limiting: \n Pressure'
        
        self.RateLimit = QLabel(rate_text)
        self.RateLimit.setFont(QFont('Arial',18));
        self.RateLimit.setAlignment(Qt.AlignCenter)
        self.RateLimit.setStyleSheet('background: transparent; color: gold')
        self.grid.addWidget(self.RateLimit, 0,13,3,2);
        


        print('RHS Stuff start here')


        icp_target_text =''
        if controlFlag==1:
            icp_target_text = 'Minimum Pressure: \n' + str(opening_pressure_val) + ' ' + unitFlag
        else:
            icp_target_text = 'Maximal Pressure: \n' + str(pressureAmount) + ' ' + unitFlag

        self.ICPTarget = QLabel(icp_target_text)
        self.ICPTarget.setFont(QFont('Arial',20));
        self.ICPTarget.setAlignment(Qt.AlignCenter);
        self.ICPTarget.setStyleSheet('background: transparent; color: gold')
        self.grid.addWidget(self.ICPTarget, 3,13,2,2)

        # volume target
        volume_target_text = ''
        if controlFlag==1:
            volume_target_text = 'Maximum Drainge Amount: \n ' + maxVol_str + ' mL'
        else:
            volume_target_text = 'Minimum Drainage Amount: \n ' + str(volumeAmount) + ' mL'
        self.VolumeTarget = QLabel(volume_target_text)
        self.VolumeTarget.setFont(QFont('Arial', 20))
        self.VolumeTarget.setAlignment(Qt.AlignCenter);
        self.VolumeTarget.setStyleSheet('background: transparent; color: gold')
        self.grid.addWidget(self.VolumeTarget, 5,13,2,2)

        # Go/Stop Button
        self.RunPauseLabel = QLabel('')
        self.RunPauseLabel.setFont(QFont('Arial', 20))
        self.RunPauseLabel.setAlignment(Qt.AlignCenter);
        self.RunPauseLabel.setStyleSheet('background: transparent; color: gold')
        self.grid.addWidget(self.RunPauseLabel, 7,13,6,2);
        

        print('Bottom Row')
        self.silenceAlarm = QPushButton('Silence \n Alarm')
        self.silenceAlarm.setStyleSheet('background: transparent; color: gold')
        self.silenceAlarm.clicked.connect(self.Alarm)
        self.silenceAlarm.setFont(QFont('Arial',20))
        self.grid.addWidget(self.silenceAlarm,13,13,2,2);

       
        self.ZeroButton = QPushButton('Zero \n')
        self.ZeroButton.setFont(QFont('Arial',20))
        self.ZeroButton.setStyleSheet('background: transparent; color: gold')
        self.ZeroButton.clicked.connect(self.ZeroDevice);
        self.grid.addWidget(self.ZeroButton,13,10,2,3);

        self.ClampButton = QPushButton('Clamp \n Device')
        self.ClampButton.setFont(QFont('Arial', 20));
        self.ClampButton.setStyleSheet('background: transparent; color: gold')
        self.ClampButton.clicked.connect(self.Clamp);
        self.grid.addWidget(self.ClampButton, 13,6,2,4)

        self.ProgramButton = QPushButton('Change \nProgram');
        self.ProgramButton.setFont(QFont('Arial',20));
        self.ProgramButton.setStyleSheet('background: transparent; color: gold')
        self.ProgramButton.clicked.connect(self.changeProgram);
        self.grid.addWidget(self.ProgramButton, 13,0,2,4);

        self.log = QPushButton('I/O \n Information')
        self.log.setFont(QFont('Arial', 20));
        self.log.setStyleSheet('background: transparent; color: gold')
        self.log.clicked.connect(self.toIO)
        self.grid.addWidget(self.log, 13,4,2,2)

        self.movie = QMovie('check.gif');
        self.RunPauseLabel.setMovie(self.movie);
        self.RunPauseLabel.setStyleSheet('background: transparent; color: gold')
        self.startMovie();

        # Temperature vs time dynamic plot
        self.plot_graph = pg.PlotWidget()
        self.plot_graph.setStyleSheet('background: transparent; color: gold')
       
        pen = pg.mkPen(color=(255, 0, 0))
        self.plot_graph.setTitle("Waveform Graph", color="b", size="20pt")
        styles = {"color": "red", "font-size": "10px"}
        self.plot_graph.setLabel("left", "Pressure (mmHg)", **styles)
        self.plot_graph.setLabel('right', 'Volume (mL)', **styles);
        self.plot_graph.setLabel("bottom", "Time (minutes)", **styles)
        self.plot_graph.addLegend()
        self.plot_graph.setYRange(0,80)
        self.time = list(range(10))
        self.pressure = [randint(20, 40) for _ in range(10)]

        self.volume = [0 for _ in range(10)]

        self.volume_line =  self.plot_graph.plot(
            self.time,
            self.volume,
            name="Volume Drained",
            pen=pen,
            symbol="+",
            symbolSize=19,
            symbolBrush="g",
        )

        # Get a line reference
        self.pressure_line = self.plot_graph.plot(
            self.time,
            self.pressure,
            name="ICPGraph",
            pen=pen,
            symbol="+",
            symbolSize=19,
            symbolBrush="b",
        )
        # Add a timer to simulate new temperature measurements
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()
    def toIO(self):
        global logScreen;
        if logScreen == None:
            logScreen = LogScreen();
        else:
            logScreen.show();

    def startMovie(self):
        self.movie.start();

    def update_plot(self):
        self.time = self.time[1:]
        self.time.append(self.time[-1] + 1)
        self.pressure = self.pressure[1:]
        self.pressure.append(randint(20, 40))
        self.pressure_line.setData(self.time, self.pressure)

        self.volume = self.volume[1:]

        max_vol=40
        self.volume.append(min(self.volume[-1] + randint(3,6), max_vol))
        self.volume_line.setData(self.time, self.volume)

        if (self.volume[-1] >=max_Vol): 
            pass 
        

        self.grid.addWidget(self.plot_graph,3,1,10,12)

    
        self.setLayout(self.grid);

    def Alarm(self):
        global alarmScreen
        alarmScreen = AlarmScreen();
        alarmScreen.show()
    def ZeroDevice(self):
        global zeroScreen;
        zeroScreen = ZeroDevice();
        zeroScreen.show();
    def Clamp(self):
        global clampScreen;
        clampScreen = ClampDevice();
        clampScreen.show()
    def changeProgram(self):
        pass

class Summary(QWidget):
    def __init__(self):
        print(closeDelay)
        super().__init__()
        self.setFixedWidth(1024);
        self.setFixedHeight(600);

        self.text_field = QPlainTextEdit(self)
        self.text_field.setMinimumSize (1024,600)
        self.text_field.setStyleSheet("background-image: url(background.png); background-attachment: fixed")
        
        self.grid = QGridLayout()

        
        self.setLayout(self.grid)


        for x in range(0,15):
            for y in range(0,15):
                tmp = QLabel('')
                tmp.setStyleSheet('background: transparent; color: gold')

                self.grid.addWidget(tmp, x, y)


        self.setUp = QLabel("Summary Screen");
        self.setUp.setFont(QFont("Arial",56));
        self.setUp.setAlignment(Qt.AlignCenter);
        self.setUp.setStyleSheet('background: transparent; color: gold')
        self.grid.addWidget(self.setUp, 0,6,4,3)

        # Device Type
        label = ''

        if mode==1:
            label='Lumbar Drain Mode'
        else:
            label = 'EVD Mode'

        # Device Type
        self.DeviceType = QLabel(label)
        self.DeviceType.setFont(QFont('Arial', 30))
        self.DeviceType.setAlignment(Qt.AlignCenter)
        self.DeviceType.setStyleSheet('background: transparent; color: gold')
        self.grid.addWidget(self.DeviceType, 4, 6, 2, 3)


        drive_by = None;
        p = None;
        v = None;
        delay = None
        if controlFlag == 1:
            drive_by = "Pressure Controlled-Volume Limited";
            p = openPressure_str + " " + unitFlag;
            v = maxVol_str + 'mL'
            delay = str(closeDelay) + ' seconds'
        else:
            drive_by = "Volume Controlled-Pressure Limited";
            p = pressureString + ' ' + unitFlag
            v = str(volumeAmount) + ' mL'
        
        
        bolded_font = QFont('Arial', 30);
        bolded_font.setBold(True);
        
        if (controlFlag==1):
            # Sets the label
            self.closeDelay = QLabel(' Closing Delay is: ');
            self.closeDelay.setFont(QFont('Arial', 30));
            self.closeDelay.setStyleSheet('background: transparent; color: gold')
            self.grid.addWidget(self.closeDelay,11,6,1,1)

            # Sets the bolded value 
            self.Delay = QLabel(delay);
            self.Delay.setFont(bolded_font)
            self.Delay.setStyleSheet('background: transparent; color: gold')
            self.grid.addWidget(self.Delay, 11,7,1,1)
        # How it is driven
        self.driveLabel = QLabel(drive_by);
        self.driveLabel.setFont(QFont("Arial",30))
        self.driveLabel.setAlignment(Qt.AlignCenter)
        self.driveLabel.setStyleSheet('background: transparent; color: gold')
        self.grid.addWidget(self.driveLabel, 5, 6, 2, 3);

        # Opening Pressure

        # Sets the label
        self.openingPressure = QLabel("Opening pressure:");
        self.openingPressure.setAlignment(Qt.AlignCenter)
        self.openingPressure.setFont(QFont("Arial", 30))
        self.openingPressure.setStyleSheet('background: transparent; color: gold')
        self.grid.addWidget(self.openingPressure, 7, 6,1,1);

        # Sets how it is driven
        self.PressureValue = QLabel(p)
        self.PressureValue.setFont(bolded_font);
        self.PressureValue.setStyleSheet('background: transparent; color: gold')
        self.PressureValue.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(self.PressureValue, 7,8,1,1 )

        # volume limit

        self.volumeLimit = QLabel("Volume Limit per hour:");
        self.volumeLimit.setStyleSheet('background: transparent; color: gold')
        self.volumeLimit.setAlignment(Qt.AlignCenter)
        self.volumeLimit.setFont(QFont("Arial", 30))
        self.VolumeAmount = QLabel(v);
        self.VolumeAmount.setStyleSheet('background: transparent; color: gold')
        self.VolumeAmount.setAlignment(Qt.AlignCenter)
        self.VolumeAmount.setFont(bolded_font)

        if controlFlag==0:
            self.grid.addWidget(self.volumeLimit, 10, 6,1,1)
            self.grid.addWidget(self.VolumeAmount,10,8,1,1 )

        else:
            self.grid.addWidget(self.volumeLimit, 9, 5,1,1)

            self.grid.addWidget(self.VolumeAmount,9,8,1,1 )



        self.Next = QPushButton('Next \n');
        self.Next.setStyleSheet('background: transparent; color: gold')
        self.Next.setFont(QFont('Arial',30))
        self.Next.clicked.connect(self.toOperation)
        self.grid.addWidget(self.Next, 16,6,2,3)


        #self.setLayout(self.grid)
    def toOperation(self):
        global operationScreen;
        operationScreen = Operation();
        operationScreen.show();
        self.hide();


class ClosingDelay(QWidget):

    def __init__(self):

        super().__init__()
        self.setFixedWidth(1024);
        self.setFixedHeight(600);

        self.grid = QGridLayout()

        self.text_field = QPlainTextEdit(self)
        self.text_field.setMinimumSize (1024,600)
        self.text_field.setStyleSheet("background-image: url(background.png); background-attachment: fixed")

        # Welcome Label
        self.welcomeLabel = QLabel("What is the closing delay? \n");
        self.welcomeLabel.setFont(QFont("Arial",50 ));
        self.welcomeLabel.setAlignment(Qt.AlignCenter)
        self.welcomeLabel.setStyleSheet('background: transparent; color: gold')

        self.backButton = QPushButton('Back \n')
        self.backButton.setFont(QFont("Arial", 30));
        self.backButton.clicked.connect(self.back);
        self.backButton.setStyleSheet('background: transparent; color: gold')

        # Display Label
        self.display_label = QLabel("" + "\n");
        self.display_label.setFont(QFont("Arial", 50));
        self.display_label.setAlignment(Qt.AlignCenter)
        self.display_label.setStyleSheet('background: transparent; color: gold')

  # Button setup happens here
        self.button0 = QPushButton("\n");
        self.button0.setStyleSheet('background: transparent; color: gold')
        self.button0.setFont(QFont("Arial", 30));
        self.button0.clicked.connect(self.press0);
        self.grid.addWidget(self.button0, 11, 4, 2, 2);

        # Button setup happens here
        self.button1 = QPushButton("\n");
        self.button1.setStyleSheet('background: transparent; color: gold')
        self.button1.setFont(QFont("Arial", 30));
        self.button1.clicked.connect(self.press1);

        self.button2 = QPushButton("\n");
        self.button2.setStyleSheet('background: transparent; color: gold')
        self.button2.setFont(QFont("Arial", 30));
        self.button2.clicked.connect(self.press2)

        self.button3 = QPushButton("\n");
        self.button3.setStyleSheet('background: transparent; color: gold')
        self.button3.setFont(QFont("Arial", 30))
        self.button3.clicked.connect(self.press3);

        self.button4 = QPushButton("\n");
        self.button4.setStyleSheet('background: transparent; color: gold')
        self.button4.setFont(QFont("Arial", 30));
        self.button4.clicked.connect(self.press4);

        self.button5 = QPushButton("\n");
        self.button5.setStyleSheet('background: transparent; color: gold')
        self.button5.setFont(QFont("Arial", 30))
        self.button5.clicked.connect(self.press5);

        self.button6 = QPushButton("\n");
        self.button6.setStyleSheet('background: transparent; color: gold')
        self.button6.setFont(QFont("Arial", 30))
        self.button6.clicked.connect(self.press6);

        self.button7 = QPushButton("\n");
        self.button7.setStyleSheet('background: transparent; color: gold')
        self.button7.setFont(QFont("Arial", 30))
        self.button7.clicked.connect(self.press7);

        self.button8 = QPushButton("\n");
        self.button8.setStyleSheet('background: transparent; color: gold')
        self.button8.setFont(QFont("Arial", 30))
        self.button8.clicked.connect(self.press8);

        self.button9 = QPushButton("\n");
        self.button9.setStyleSheet('background: transparent; color: gold')
        self.button9.setFont(QFont("Arial", 30))
        self.button9.clicked.connect(self.press9);

        self.button_dot = QPushButton(". \n");
        self.button_dot.setStyleSheet('background: transparent; color: gold')
        self.button_dot.setFont(QFont("Arial", 30))
        self.button_dot.clicked.connect(self.pressDot)

        self.enterButton = QPushButton("Enter \n");
        self.enterButton.setFont(QFont("Arial", 30));
        self.enterButton.setStyleSheet('background: transparent; color: gold; border: 3px solid-white')
        self.enterButton.clicked.connect(self.enter);

        self.clearButton = QPushButton("Clear \n");
        self.clearButton.setStyleSheet('background: transparent; color: black')
        self.clearButton.setFont(QFont("Arial", 30));
        self.clearButton.clicked.connect(self.clear);
        self.button1.setIcon(QIcon('1.png'))
        self.button1.setIconSize(QSize(80,80))

        self.button2.setIcon(QIcon('2.png'))
        self.button2.setIconSize(QSize(80,80))

        self.button3.setIcon(QIcon('3.png'))
        self.button3.setIconSize(QSize(80,80))


        self.button4.setIcon(QIcon('4.png'))
        self.button4.setIconSize(QSize(80,80))


        self.button5.setIcon(QIcon('5.png'))
        self.button5.setIconSize(QSize(80,80))


        self.button6.setIcon(QIcon('6.png'))
        self.button6.setIconSize(QSize(80,80))

        self.button7.setIcon(QIcon('7.png'))
        self.button7.setIconSize(QSize(80,80))


        self.button8.setIcon(QIcon('8.png'))
        self.button8.setIconSize(QSize(80,80))
                
        self.button9.setIcon(QIcon('9.png'))
        self.button9.setIconSize(QSize(80,80))

        self.button0.setIcon(QIcon('0.png'))
        self.button0.setIconSize(QSize(80,80))        


        self.LabelButton = QLabel('seconds');
        self.LabelButton.setStyleSheet('background: transparent; color: gold')
        self.LabelButton.setAlignment(Qt.AlignCenter)
        self.LabelButton.setFont(QFont("Arial", 30))
        
        # Adding buttons to grid
        self.grid.addWidget(self.button1, 5,0,2,2);
        self.grid.addWidget(self.button2, 5, 2, 2, 2);
        self.grid.addWidget(self.button3, 5, 4,2,2);
        self.grid.addWidget(self.button4, 7, 0,2,2);
        self.grid.addWidget(self.button5, 7,2,2,2);
        self.grid.addWidget(self.button6, 7,4,2,2);
        self.grid.addWidget(self.button7, 9,0,2,2);
        self.grid.addWidget(self.button8, 9,2,2,2);
        self.grid.addWidget(self.button9, 9, 4,2,2);
        self.grid.addWidget(self.button_dot, 11,0,2,2)
        self.grid.addWidget(self.welcomeLabel, 0, 0, 2, 15);

        self.grid.addWidget(self.backButton, 13, 10, 2, 4)
        self.grid.addWidget(self.display_label, 5,10,2,4);
        self.grid.addWidget(self.LabelButton, 8,10,2,4)
        self.grid.addWidget(self.enterButton,10,10,2,4);
        self.setLayout(self.grid)


    def press1(self):
        global closeDelayString;
        closeDelayString += "1";

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(closeDelayString);

    def press2(self):
        global closeDelayString;
        closeDelayString += "2";
        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(closeDelayString);

    def press3(self):
        global closeDelayString;
        closeDelayString += "3";

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(closeDelayString);

    def press4(self):
        global closeDelayString;
        closeDelayString += "4";

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(closeDelayString);

    def press5(self):
        global closeDelayString;
        closeDelayString += "5";

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(closeDelayString);

    def press6(self):
        global closeDelayString;
        closeDelayString += "6";

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(closeDelayString);

    def press7(self):
        global closeDelayString;
        closeDelayString += "7";

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(closeDelayString);

    def press8(self):
        global closeDelayString;
        closeDelayString += "8";

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(closeDelayString);

    def press9(self):
        global closeDelayString;
        closeDelayString += "9";

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(closeDelayString);

    def pressDot(self):
        global closeDelayString;
        closeDelayString += "."

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(closeDelayString);

    def press0(self):
        global closeDelayString;
        closeDelayString += "0";

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(closeDelayString);

    def enter(self):
        global closeDelay, SummaryScreen;
        closeDelay = float(closeDelayString);
        SummaryScreen = Summary();
        SummaryScreen.show();
        self.hide()

    def clear(self):
        global closeDelayString
        global closeDelay;
        closeDelayString = "";
        closeDelay = 0;
        self.display_label.setText(closeDelayString);
    def back(self):
        pass

class PressureMaximum(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(1024);
        self.setFixedHeight(600);

        self.grid = QGridLayout()
        
        self.text_field = QPlainTextEdit(self)
        self.text_field.setMinimumSize (1024,600)
        self.text_field.setStyleSheet("background-image: url(background.png); background-attachment: fixed")


        # Welcome Label
        self.welcomeLabel = QLabel("What is the maximal allowable Pressure? \n");
        self.welcomeLabel.setFont(QFont("Arial", 50));
        self.welcomeLabel.setStyleSheet('background: transparent; color: gold')
        self.welcomeLabel.setAlignment(Qt.AlignCenter);

        # Display Label
        self.display_label =QLabel("");
        self.display_label.setFont(QFont("Arial", 50));
        self.display_label.setAlignment(Qt.AlignCenter)
        self.display_label.setStyleSheet('background: transparent; color: gold')
        # need to implement the units portion of this still

        units = ' ' + unitFlag;

        self.unitLabel = QLabel(units);
        self.unitLabel.setFont(QFont("Arial", 30));
        self.unitLabel.setStyleSheet('background: transparent; color: gold')
        self.grid.addWidget(self.unitLabel, 7, 11, 1, 3);

        # Button setup happens here
        self.button0 = QPushButton("\n");
        self.button0.setStyleSheet('background: transparent; color: gold')
        self.button0.setFont(QFont("Arial", 30));
        self.button0.clicked.connect(self.press0);
        self.grid.addWidget(self.button0, 11, 4, 2, 2);

        # Button setup happens here
        self.button1 = QPushButton("\n");
        self.button1.setStyleSheet('background: transparent; color: gold')
        self.button1.setFont(QFont("Arial", 30));
        self.button1.clicked.connect(self.press1);

        self.button2 = QPushButton("\n");
        self.button2.setStyleSheet('background: transparent; color: gold')
        self.button2.setFont(QFont("Arial", 30));
        self.button2.clicked.connect(self.press2)

        self.button3 = QPushButton("\n");
        self.button3.setStyleSheet('background: transparent; color: gold')
        self.button3.setFont(QFont("Arial", 30))
        self.button3.clicked.connect(self.press3);

        self.button4 = QPushButton("\n");
        self.button4.setStyleSheet('background: transparent; color: gold')
        self.button4.setFont(QFont("Arial", 30));
        self.button4.clicked.connect(self.press4);

        self.button5 = QPushButton("\n");
        self.button5.setStyleSheet('background: transparent; color: gold')
        self.button5.setFont(QFont("Arial", 30))
        self.button5.clicked.connect(self.press5);

        self.button6 = QPushButton("\n");
        self.button6.setStyleSheet('background: transparent; color: gold')
        self.button6.setFont(QFont("Arial", 30))
        self.button6.clicked.connect(self.press6);

        self.button7 = QPushButton("\n");
        self.button7.setStyleSheet('background: transparent; color: gold')
        self.button7.setFont(QFont("Arial", 30))
        self.button7.clicked.connect(self.press7);

        self.button8 = QPushButton("\n");
        self.button8.setStyleSheet('background: transparent; color: gold')
        self.button8.setFont(QFont("Arial", 30))
        self.button8.clicked.connect(self.press8);

        self.button9 = QPushButton("\n");
        self.button9.setStyleSheet('background: transparent; color: gold')
        self.button9.setFont(QFont("Arial", 30))
        self.button9.clicked.connect(self.press9);

        self.button_dot = QPushButton(". \n");
        self.button_dot.setStyleSheet('background: transparent; color: gold')
        self.button_dot.setFont(QFont("Arial", 30))
        self.button_dot.clicked.connect(self.pressDot)

        self.enterButton = QPushButton("Enter \n");
        self.enterButton.setFont(QFont("Arial", 30));
        self.enterButton.setStyleSheet('background: transparent; color: gold;border: 3px solid white')
        self.enterButton.clicked.connect(self.enter);

        self.clearButton = QPushButton("Clear \n");
        self.clearButton.setStyleSheet('background: transparent; color: black')
        self.clearButton.setFont(QFont("Arial", 30));
        self.clearButton.clicked.connect(self.clear);

        self.button1.setIcon(QIcon('1.png'))
        self.button1.setIconSize(QSize(80,80))

        self.button2.setIcon(QIcon('2.png'))
        self.button2.setIconSize(QSize(80,80))

        self.button3.setIcon(QIcon('3.png'))
        self.button3.setIconSize(QSize(80,80))


        self.button4.setIcon(QIcon('4.png'))
        self.button4.setIconSize(QSize(80,80))


        self.button5.setIcon(QIcon('5.png'))
        self.button5.setIconSize(QSize(80,80))


        self.button6.setIcon(QIcon('6.png'))
        self.button6.setIconSize(QSize(80,80))

        self.button7.setIcon(QIcon('7.png'))
        self.button7.setIconSize(QSize(80,80))


        self.button8.setIcon(QIcon('8.png'))
        self.button8.setIconSize(QSize(80,80))
                
        self.button9.setIcon(QIcon('9.png'))
        self.button9.setIconSize(QSize(80,80))

        self.button0.setIcon(QIcon('0.png'))
        self.button0.setIconSize(QSize(80,80))        

        # Adding buttons to grid
        self.grid.addWidget(self.button1, 5, 0, 2, 2);
        self.grid.addWidget(self.button2, 5, 2, 2, 2);
        self.grid.addWidget(self.button3, 5, 4, 2, 2);
        self.grid.addWidget(self.button4, 7, 0, 2, 2);
        self.grid.addWidget(self.button5, 7, 2, 2, 2);
        self.grid.addWidget(self.button6, 7, 4, 2, 2);
        self.grid.addWidget(self.button7, 9, 0, 2, 2);
        self.grid.addWidget(self.button8, 9, 2, 2, 2);
        self.grid.addWidget(self.button9, 9, 4, 2, 2);
        self.grid.addWidget(self.button_dot, 11, 0, 2, 2)
        self.grid.addWidget(self.welcomeLabel, 0, 0, 3, 15);
        self.grid.addWidget(self.display_label, 5, 9, 1, 6);
        self.grid.addWidget(self.enterButton, 8, 10, 2, 4);
        self.grid.addWidget(self.clearButton, 13, 1, 2, 4);
        self.setLayout(self.grid)

    def press1(self):
        global pressureString;
        pressureString += "1";

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(pressureString);
        self.display_label.setAlignment(Qt.AlignCenter)

    def press2(self):
        global pressureString;
        pressureString += "2";
        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(pressureString);
        self.display_label.setAlignment(Qt.AlignCenter)

    def press3(self):
        global pressureString;
        pressureString += "3";

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(pressureString);
        self.display_label.setAlignment(Qt.AlignCenter)

    def press4(self):
        global pressureString;
        pressureString += "4";

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(pressureString);
        self.display_label.setAlignment(Qt.AlignCenter)

    def press5(self):
        global pressureString;
        pressureString += "5";

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(pressureString);
        self.display_label.setAlignment(Qt.AlignCenter)

    def press6(self):
        global pressureString;
        pressureString += "6";

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(pressureString);
        self.display_label.setAlignment(Qt.AlignCenter)

    def press7(self):
        global pressureString;
        pressureString += "7";

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(pressureString);
        self.display_label.setAlignment(Qt.AlignCenter)

    def press8(self):
        global pressureString;
        pressureString += "8";

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(pressureString);
        self.display_label.setAlignment(Qt.AlignCenter)
        self.display_label.setAlignment(Qt.AlignCenter)

    def press9(self):
        global pressureString;
        pressureString += "9";

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(pressureString);
        self.display_label.setAlignment(Qt.AlignCenter)

    def pressDot(self):
        global pressureString;
        pressureString += "."

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(pressureString);
        self.display_label.setAlignment(Qt.AlignCenter)

    def press0(self):
        global pressureString;
        pressureString += "0";

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(pressureString);
        self.display_label.setAlignment(Qt.AlignCenter)
    def enter(self):
        global pressureAmount, pressureSummary;
        pressureAmount = float(pressureString);
        pressureSummary = Summary();
        pressureSummary.show();
        self.hide()

    def clear(self):
        global pressureString
        global volumeAmount;
        pressureString = "";
        volumeAmount = 0;
        self.display_label.setText(pressureString);
        self.display_label.setAlignment(Qt.AlignCenter)

class VolumeLimit(QWidget):
    def __init__(self):

        super().__init__()
        self.setFixedWidth(1024);
        self.setFixedHeight(600);

        self.grid = QGridLayout()

        self.text_field = QPlainTextEdit(self)
        self.text_field.setMinimumSize (1024,600)
        self.text_field.setStyleSheet("background-image: url(background.png); background-attachment: fixed")


        # Welcome Label
        self.welcomeLabel = QLabel("What is max amount to be drained ? \n");
        self.welcomeLabel.setStyleSheet('background: transparent; color: gold')
        self.welcomeLabel.setFont(QFont("Arial",50));
        self.welcomeLabel.setWordWrap(True)
        self.welcomeLabel.setAlignment(Qt.AlignCenter)


        # Display Label
        self.display_label =QLabel("");
        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setAlignment(Qt.AlignCenter)
        self.display_label.setStyleSheet('background: transparent; color: gold')

        # need to implement the units portion of this still

        self.unitLabel = QLabel('mL/hr');
        self.unitLabel.setFont(QFont("Arial", 30));
        self.unitLabel.setStyleSheet('background: transparent; color: gold')
        self.unitLabel.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(self.unitLabel, 7,10,1,3);

        # Button setup happens here
        self.button0 = QPushButton("\n");
        self.button0.setFont(QFont("Arial", 30));
        self.button0.clicked.connect(self.press0);
        self.button0.setStyleSheet('background: transparent; color: gold')
        self.grid.addWidget(self.button0, 11, 4, 2, 2);


        # Button setup happens here
        self.button1 = QPushButton("\n");
        self.button1.setStyleSheet('background: transparent; color: gold')
        self.button1.setFont(QFont("Arial", 30));
        self.button1.clicked.connect(self.press1);

        self.button2 = QPushButton("\n");
        self.button2.setStyleSheet('background: transparent; color: gold')
        self.button2.setFont(QFont("Arial", 30));
        self.button2.clicked.connect(self.press2)

        self.button3 = QPushButton("\n");
        self.button3.setFont(QFont("Arial", 30))
        self.button3.setStyleSheet('background: transparent; color: gold')
        self.button3.clicked.connect(self.press3);

        self.button4 = QPushButton("\n");
        self.button4.setStyleSheet('background: transparent; color: gold')
        self.button4.setFont(QFont("Arial", 30));
        self.button4.clicked.connect(self.press4);

        self.button5 = QPushButton("\n");
        self.button5.setStyleSheet('background: transparent; color: gold')
        self.button5.setFont(QFont("Arial", 30))
        self.button5.clicked.connect(self.press5);

        self.button6 = QPushButton("\n");
        self.button6.setStyleSheet('background: transparent; color: gold')
        self.button6.setFont(QFont("Arial", 30))
        self.button6.clicked.connect(self.press6);

        self.button7 = QPushButton("\n");
        self.button7.setStyleSheet('background: transparent; color: gold')
        self.button7.setFont(QFont("Arial", 30))
        self.button7.clicked.connect(self.press7);

        self.button8 = QPushButton("\n");
        self.button8.setStyleSheet('background: transparent; color: gold')
        self.button8.setFont(QFont("Arial", 30))
        self.button8.clicked.connect(self.press8);

        self.button9 = QPushButton("\n");
        self.button9.setStyleSheet('background: transparent; color: gold')
        self.button9.setFont(QFont("Arial", 30))
        self.button9.clicked.connect(self.press9);

        self.button_dot = QPushButton(". \n");
        self.button_dot.setStyleSheet('background: transparent; color: gold')
        self.button_dot.setFont(QFont("Arial", 30))
        self.button_dot.clicked.connect(self.pressDot)

        self.enterButton = QPushButton("Enter \n");
        self.enterButton.setStyleSheet('background: transparent; color: gold; border: 3px solid white')
        self.enterButton.setFont(QFont("Arial", 30));
        self.enterButton.clicked.connect(self.enter);

        self.clearButton = QPushButton("Clear \n");
        self.clearButton.setStyleSheet('background: transparent; color: black')
        self.clearButton.setFont(QFont("Arial", 30));
        self.clearButton.clicked.connect(self.clear);

        self.button1.setIcon(QIcon('1.png'))
        self.button1.setIconSize(QSize(80,80));

        self.button2.setIcon(QIcon('2.png'))
        self.button2.setIconSize(QSize(80,80))

        self.button3.setIcon(QIcon('3.png'))
        self.button3.setIconSize(QSize(80,80))


        self.button4.setIcon(QIcon('4.png'))
        self.button4.setIconSize(QSize(80,80))


        self.button5.setIcon(QIcon('5.png'))
        self.button5.setIconSize(QSize(80,80))


        self.button6.setIcon(QIcon('6.png'))
        self.button6.setIconSize(QSize(80,80))

        self.button7.setIcon(QIcon('7.png'))
        self.button7.setIconSize(QSize(80,80))


        self.button8.setIcon(QIcon('8.png'))
        self.button8.setIconSize(QSize(80,80))
                
        self.button9.setIcon(QIcon('9.png'))
        self.button9.setIconSize(QSize(80,80))

        self.button0.setIcon(QIcon('0.png'))
        self.button0.setIconSize(QSize(80,80))        


        # Adding buttons to grid
        self.grid.addWidget(self.button1, 5,0,2,2);
        self.grid.addWidget(self.button2, 5, 2, 2, 2);
        self.grid.addWidget(self.button3, 5, 4,2,2);
        self.grid.addWidget(self.button4, 7, 0,2,2);
        self.grid.addWidget(self.button5, 7,2,2,2);
        self.grid.addWidget(self.button6, 7,4,2,2);
        self.grid.addWidget(self.button7, 9,0,2,2);
        self.grid.addWidget(self.button8, 9,2,2,2);
        self.grid.addWidget(self.button9, 9, 4,2,2);
        self.grid.addWidget(self.button_dot, 11,0,2,2)
        self.grid.addWidget(self.welcomeLabel, 2, 0, 3, 15);
        self.grid.addWidget(self.display_label, 5, 10, 2, 4);
        self.grid.addWidget(self.enterButton, 8, 10, 2, 4);
        self.grid.addWidget(self.clearButton, 13, 1, 2, 4);
        self.setLayout(self.grid)



    def press1(self):
        global volumeLimit_str;
        volumeLimit_str += "1";

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(volumeLimit_str);
        self.display_label.setAlignment(Qt.AlignCenter)
    def press2(self):
        global volumeLimit_str;
        volumeLimit_str += "2";

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(volumeLimit_str);
        self.display_label.setAlignment(Qt.AlignCenter)
    def press3(self):
        global volumeLimit_str;
        volumeLimit_str += "3";

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(volumeLimit_str);
        self.display_label.setAlignment(Qt.AlignCenter)
    def press4(self):
        global volumeLimit_str;
        volumeLimit_str += "4";

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(volumeLimit_str);
        self.display_label.setAlignment(Qt.AlignCenter)
    def press5(self):
        global volumeLimit_str;
        volumeLimit_str += "5";

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(volumeLimit_str);
        self.display_label.setAlignment(Qt.AlignCenter)
    def press6(self):
        global volumeLimit_str;
        volumeLimit_str += "6";

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(volumeLimit_str);
        self.display_label.setAlignment(Qt.AlignCenter)
    def press7(self):
        global volumeLimit_str;
        volumeLimit_str += "7";

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(volumeLimit_str);
        self.display_label.setAlignment(Qt.AlignCenter)
    def press8(self):
        global volumeLimit_str;
        volumeLimit_str += "8";

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(volumeLimit_str);
        self.display_label.setAlignment(Qt.AlignCenter)
    def press9(self):
        global volumeLimit_str;
        volumeLimit_str += "9";

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(volumeLimit_str);
        self.display_label.setAlignment(Qt.AlignCenter)
    def pressDot(self):
        global volumeLimit_str;
        volumeLimit_str += "."

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(volumeLimit_str);
        self.display_label.setAlignment(Qt.AlignCenter)
    def press0(self):
        global volumeLimit_str;
        volumeLimit_str += "0";

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(volumeLimit_str);
        self.display_label.setAlignment(Qt.AlignCenter)
    def enter(self):
        global volumeAmount, PressureLimit;
        volumeAmount = float(volumeLimit_str);
        PressureLimit = PressureMaximum();
        PressureLimit.show();
        self.hide()

    def clear(self):
        global volumeLimit_str
        global volume_limit_val;
        volumeLimit_str = "";
        volume_limit_val = 0;
        self.display_label.setText(volumeLimit_str);
        self.display_label.setAlignment(Qt.AlignCenter)
class VolumetricMaximum(QWidget):
    def __init__(self):

        super().__init__()
        self.setFixedWidth(1024);
        self.setFixedHeight(600);

        self.text_field = QPlainTextEdit(self)
        self.text_field.setMinimumSize (1024,600)
        self.text_field.setStyleSheet("background-image: url(background.png); background-attachment: fixed")
        self.grid = QGridLayout()

     # Welcome Label
        self.welcomeLabel = QLabel("What is the maximal fluid to be drained?");
        self.welcomeLabel.setFont(QFont("Arial",25 ));
        self.welcomeLabel.setAlignment(Qt.AlignCenter)
        self.welcomeLabel.setStyleSheet('background: transparent; color: gold')
        self.welcomeLabel.setWordWrap(True)

        self.backButton = QPushButton('Back \n')
        self.backButton.setFont(QFont("Arial", 30));
        self.backButton.setStyleSheet('background: transparent; color: gold')
        self.backButton.clicked.connect(self.back);

        # Display Label
        self.display_label = QLabel("" + "\n");
        self.display_label.setFont(QFont("Arial", 75));
        self.display_label.setStyleSheet('background: transparent; color: gold')
        self.display_label.setAlignment(Qt.AlignCenter)

        # Button setup happens here
        self.button0 = QPushButton("\n");
        self.button0.setFont(QFont("Arial", 30));
        self.button0.setStyleSheet('background: transparent; color: gold')
        self.button0.clicked.connect(self.press0);
        self.grid.addWidget(self.button0, 11, 4, 2, 2);


        # Button setup happens here
        self.button1 = QPushButton("\n");
        self.button1.setIcon(QIcon('1.png'))
        self.button1.setIconSize(QSize(80,80))
        self.button1.setFont(QFont("Arial", 30));
        self.button1.setStyleSheet('background: transparent; color: gold')
        self.button1.clicked.connect(self.press1);

        self.button2 = QPushButton("\n");
        self.button2.setIcon(QIcon('2.png'))
        self.button2.setIconSize(QSize(80,80));
        self.button2.clicked.connect(self.press2)
        self.button2.setStyleSheet('background: transparent; color: gold')

        self.button3 = QPushButton("\n");

        self.button3.setIcon(QIcon('3.png'))
        self.button3.setIconSize(QSize(80,80));
        self.button3.setStyleSheet('background: transparent; color: gold')
        self.button3.clicked.connect(self.press3);

        self.button4 = QPushButton("\n");
        self.button4.setFont(QFont("Arial", 30));
        self.button4.setStyleSheet('background: transparent; color: gold')
        self.button4.clicked.connect(self.press4);

        self.button5 = QPushButton("\n");
        self.button5.setStyleSheet('background: transparent; color: gold')
        self.button5.setFont(QFont("Arial", 30))
        self.button5.clicked.connect(self.press5);

        self.button6 = QPushButton("\n");
        self.button6.setStyleSheet('background: transparent; color: gold')
        self.button6.setFont(QFont("Arial", 30))
        self.button6.clicked.connect(self.press6);

        self.button7 = QPushButton("\n");
        self.button7.setStyleSheet('background: transparent; color: gold')
        self.button7.setFont(QFont("Arial", 30))
        self.button7.clicked.connect(self.press7);

        self.button8 = QPushButton("\n");
        self.button8.setStyleSheet('background: transparent; color: gold')
        self.button8.setFont(QFont("Arial", 30))
        self.button8.clicked.connect(self.press8);

        self.button9 = QPushButton("\n");
        self.button9.setStyleSheet('background: transparent; color: gold')
        self.button9.setFont(QFont("Arial", 30))
        self.button9.clicked.connect(self.press9);

        self.button_dot = QPushButton("\n");
        self.button_dot.setStyleSheet('background: transparent; color: gold')
        self.button_dot.setFont(QFont("Arial", 30))
        self.button_dot.clicked.connect(self.pressDot)

        self.enterButton = QPushButton("Enter \n");
        self.enterButton.setStyleSheet('background: transparent; color: gold; border: 3px solid white')
        self.enterButton.setFont(QFont("Arial", 30));
        self.enterButton.clicked.connect(self.enter);

        self.clearButton = QPushButton("Clear \n");
        self.clearButton.setFont(QFont("Arial", 30));
        self.clearButton.setStyleSheet('background: transparent; color: black')
        self.clearButton.clicked.connect(self.clear);
        self.grid.addWidget(self.clearButton, 13, 1, 2, 4);

        self.LabelButton = QLabel('mL \n');
        self.LabelButton.setStyleSheet('background: transparent; color: gold')
        self.LabelButton.setAlignment(Qt.AlignCenter)
        self.LabelButton.setFont(QFont("Arial", 30))
        self.button1.setIcon(QIcon('1.png'))
        self.button1.setIconSize(QSize(80,80))

        self.button2.setIcon(QIcon('2.png'))
        self.button2.setIconSize(QSize(80,80))

        self.button3.setIcon(QIcon('3.png'))
        self.button3.setIconSize(QSize(80,80))


        self.button4.setIcon(QIcon('4.png'))
        self.button4.setIconSize(QSize(80,80))


        self.button5.setIcon(QIcon('5.png'))
        self.button5.setIconSize(QSize(80,80))


        self.button6.setIcon(QIcon('6.png'))
        self.button6.setIconSize(QSize(80,80))

        self.button7.setIcon(QIcon('7.png'))
        self.button7.setIconSize(QSize(80,80))


        self.button8.setIcon(QIcon('8.png'))
        self.button8.setIconSize(QSize(80,80))
                
        self.button9.setIcon(QIcon('9.png'))
        self.button9.setIconSize(QSize(80,80))

        self.button0.setIcon(QIcon('0.png'))
        self.button0.setIconSize(QSize(80,80))        

        # Adding buttons to grid
        self.grid.addWidget(self.button1, 5,0,2,2);
        self.grid.addWidget(self.button2, 5, 2, 2, 2);
        self.grid.addWidget(self.button3, 5, 4,2,2);
        self.grid.addWidget(self.button4, 7, 0,2,2);
        self.grid.addWidget(self.button5, 7,2,2,2);
        self.grid.addWidget(self.button6, 7,4,2,2);
        self.grid.addWidget(self.button7, 9,0,2,2);
        self.grid.addWidget(self.button8, 9,2,2,2);
        self.grid.addWidget(self.button9, 9, 4,2,2);
        self.grid.addWidget(self.button_dot, 11,0,2,2)
        self.grid.addWidget(self.welcomeLabel, 1, 0, 2, 15);

        self.grid.addWidget(self.backButton, 13, 10, 2, 4)
        self.grid.addWidget(self.display_label, 5,10,2,4);
        self.grid.addWidget(self.LabelButton, 8,10,2,4)
        self.grid.addWidget(self.enterButton,10,10,2,4);
        self.setLayout(self.grid)
    def press0(self):
        global maxVol_str;
        maxVol_str += "0";
        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(maxVol_str);

    def press1(self):
        global maxVol_str;
        self.display_label.setP
        maxVol_str += "1";
        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(maxVol_str);

    def press2(self):
        global maxVol_str;
        maxVol_str += "2";
        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(maxVol_str);

    def press3(self):
        global maxVol_str;
        maxVol_str += "3";
        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(maxVol_str);

    def press4(self):
        global maxVol_str;
        maxVol_str += "4";
        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(maxVol_str);

    def press5(self):
        global maxVol_str;
        maxVol_str += "5";

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(maxVol_str);

    def press6(self):
        global maxVol_str;
        maxVol_str += "6";

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(maxVol_str);

    def press7(self):
        global maxVol_str;
        maxVol_str += "7";

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(maxVol_str);

    def press8(self):
        global maxVol_str;
        maxVol_str += "8";

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(maxVol_str);

    def press9(self):
        global maxVol_str;
        maxVol_str += "9";

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(maxVol_str);

    def pressDot(self):
        global maxVol_str;
        maxVol_str += "."

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(maxVol_str);

    def enter(self):
        global max_Vol, closeDelay;
        max_Vol = float(maxVol_str);
        closeDelay = ClosingDelay()
        closeDelay.show()
        self.hide();

    def clear(self):
        global max_Vol;
        global maxVol_str;
        maxVol_str = "";
        max_Vol = None;
        self.display_label.setText(maxVol_str);
    def back(self):
        pass

class OpeningPressure(QWidget):
    def __init__(self):

        super().__init__()

        self.text_field = QPlainTextEdit(self)
        self.text_field.setMinimumSize (1024,600)
        self.text_field.setStyleSheet("background-image: url(background.png); background-attachment: fixed")
        self.setFixedWidth(1024);
        self.setFixedHeight(600);

        self.grid = QGridLayout()


        # Welcome Label
        self.welcomeLabel = QLabel("What is the opening pressure?");
        self.welcomeLabel.setFont(QFont("Arial",50 ));
        self.welcomeLabel.setAlignment(Qt.AlignCenter)
        self.welcomeLabel.setStyleSheet('background: transparent; color: gold')

        self.backButton = QPushButton('Back \n')
        self.backButton.setFont(QFont("Arial", 30));
        self.backButton.clicked.connect(self.back);
        self.backButton.setStyleSheet('background: transparent; color: gold')

        # Display Label
        self.display_label = QLabel("" + "\n");
        self.display_label.setFont(QFont("Arial", 50));
        self.display_label.setAlignment(Qt.AlignCenter)
        self.display_label.setStyleSheet('background: transparent; color: gold')

        # Button setup happens here
        self.button0 = QPushButton("\n");
        self.button0.setFont(QFont("Arial", 30));
        self.button0.clicked.connect(self.press0);
        self.button0.setStyleSheet('background: transparent; color: gold')
        self.grid.addWidget(self.button0, 11, 4, 2, 2);


        # Button setup happens here
        self.button1 = QPushButton("\n");
        self.button1.setFont(QFont("Arial", 30));
        self.button1.clicked.connect(self.press1);
        self.button1.setStyleSheet('background: transparent; color: gold')


        self.button2 = QPushButton("\n");
        self.button2.setFont(QFont("Arial", 30));
        self.button2.clicked.connect(self.press2)
        self.button2.setStyleSheet('background: transparent; color: gold')

        self.button3 = QPushButton("\n");
        self.button3.setFont(QFont("Arial", 30))
        self.button3.clicked.connect(self.press3);
        self.button3.setStyleSheet('background: transparent; color: gold')

        self.button4 = QPushButton("\n");
        self.button4.setFont(QFont("Arial", 30));
        self.button4.clicked.connect(self.press4);
        self.button4.setStyleSheet('background: transparent; color: gold')

        self.button5 = QPushButton("\n");
        self.button5.setFont(QFont("Arial", 30))
        self.button5.clicked.connect(self.press5);
        self.button5.setStyleSheet('background: transparent; color: gold')

        self.button6 = QPushButton("\n");
        self.button6.setFont(QFont("Arial", 30))
        self.button6.clicked.connect(self.press6);
        self.button6.setStyleSheet('background: transparent; color: gold')

        self.button7 = QPushButton("\n");
        self.button7.setFont(QFont("Arial", 30))
        self.button7.clicked.connect(self.press7);
        self.button7.setStyleSheet('background: transparent; color: gold')

        self.button8 = QPushButton("\n");
        self.button8.setFont(QFont("Arial", 30))
        self.button8.clicked.connect(self.press8);
        self.button8.setStyleSheet('background: transparent; color: gold')
        
        self.button9 = QPushButton("\n");
        self.button9.setFont(QFont("Arial", 30))
        self.button9.clicked.connect(self.press9);
        self.button9.setStyleSheet('background: transparent; color: gold')

        self.button_dot = QPushButton(". \n");
        self.button_dot.setFont(QFont("Arial", 30))
        self.button_dot.clicked.connect(self.pressDot)
        self.button_dot.setStyleSheet('background: transparent; color: gold')

        self.enterButton = QPushButton("Enter \n");
        self.enterButton.setFont(QFont("Arial", 30));
        self.enterButton.clicked.connect(self.enter);

        self.enterButton.setStyleSheet('background: transparent; color: gold; border: 3px solid white')

        self.clearButton = QPushButton("Clear \n");
        self.clearButton.setFont(QFont("Arial", 30));
        self.clearButton.clicked.connect(self.clear);
        self.clearButton.setStyleSheet('background: transparent; color: black')
        self.grid.addWidget(self.clearButton, 13, 1, 2, 4);

        self.LabelButton = QLabel(unitFlag);
        self.LabelButton.setAlignment(Qt.AlignCenter)
        self.LabelButton.setFont(QFont("Arial", 30))
        self.LabelButton.setStyleSheet('background: transparent; color: gold')
        
        # Adding buttons to grid
        self.grid.addWidget(self.button1, 5,0,2,2);
        self.grid.addWidget(self.button2, 5, 2, 2, 2);
        self.grid.addWidget(self.button3, 5, 4,2,2);
        self.grid.addWidget(self.button4, 7, 0,2,2);
        self.grid.addWidget(self.button5, 7,2,2,2);
        self.grid.addWidget(self.button6, 7,4,2,2);
        self.grid.addWidget(self.button7, 9,0,2,2);
        self.grid.addWidget(self.button8, 9,2,2,2);
        self.grid.addWidget(self.button9, 9, 4,2,2);
        self.grid.addWidget(self.button_dot, 11,0,2,2)
        self.grid.addWidget(self.welcomeLabel, 0, 0, 2, 15);

        self.grid.addWidget(self.backButton, 13, 10, 2, 4)
        self.grid.addWidget(self.display_label, 5,10,2,4);
        self.grid.addWidget(self.LabelButton, 8,10,2,4)
        self.grid.addWidget(self.enterButton,10,10,2,4);
        self.setLayout(self.grid)

        self.button1.setIcon(QIcon('1.png'))
        self.button1.setIconSize(QSize(80,80))

        self.button2.setIcon(QIcon('2.png'))
        self.button2.setIconSize(QSize(80,80))

        self.button3.setIcon(QIcon('3.png'))
        self.button3.setIconSize(QSize(80,80))


        self.button4.setIcon(QIcon('4.png'))
        self.button4.setIconSize(QSize(80,80))


        self.button5.setIcon(QIcon('5.png'))
        self.button5.setIconSize(QSize(80,80))


        self.button6.setIcon(QIcon('6.png'))
        self.button6.setIconSize(QSize(80,80))

        self.button7.setIcon(QIcon('7.png'))
        self.button7.setIconSize(QSize(80,80))


        self.button8.setIcon(QIcon('8.png'))
        self.button8.setIconSize(QSize(80,80))
                
        self.button9.setIcon(QIcon('9.png'))
        self.button9.setIconSize(QSize(80,80))

        self.button0.setIcon(QIcon('0.png'))
        self.button0.setIconSize(QSize(80,80))        

    def press0(self):
        global openPressure_str;
        openPressure_str += "0";

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(openPressure_str);
    def press1(self):
        global openPressure_str;
        openPressure_str += "1";

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(openPressure_str);
    def press2(self):
        global openPressure_str;
        openPressure_str += "2";

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(openPressure_str);
    def press3(self):
        global openPressure_str;
        openPressure_str += "3";

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(openPressure_str);
    def press4(self):
        global openPressure_str;
        openPressure_str += "4";

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(openPressure_str);
    def press5(self):
        global openPressure_str;
        openPressure_str += "5";

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(openPressure_str);
    def press6(self):
        global openPressure_str;
        openPressure_str += "6";

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(openPressure_str);
    def press7(self):
        global openPressure_str;
        openPressure_str += "7";

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(openPressure_str);
    def press8(self):
        global openPressure_str;
        openPressure_str += "8";

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(openPressure_str);
    def press9(self):
        global openPressure_str;
        openPressure_str += "9";

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(openPressure_str);
    def pressDot(self):
        global openPressure_str;
        openPressure_str += "."

        self.display_label.setFont(QFont("Arial", 30));
        self.display_label.setText(openPressure_str);
    def enter(self):

        global opening_pressure_val, VolumetricMaximum;
        opening_pressure_val = float(openPressure_str);
        VolumetricMaximum = VolumetricMaximum();
        VolumetricMaximum.show();
        self.hide()

    def clear(self):
        global opening_pressure_val;
        global openPressure_str;
        openPressure_str = "";
        opening_pressure_val = None;
        self.display_label.setText(openPressure_str);  
    def back(self):
        global DrainageScreen
        DrainageScreen.show()
        self.hide()



class UnitPrompt(QWidget):
    def __init__(self):
        super().__init__();
        self.setFixedWidth(1024);
        self.setFixedHeight(600);
        self.grid = QGridLayout();
        
        self.text_field = QPlainTextEdit(self)
        self.text_field.setMinimumSize (1024,600)
        self.text_field.setStyleSheet("background-image: url(background.png); background-attachment: fixed")


        # Set Up Label
        self.setUp = QLabel("Select Desired Units Mode");
        self.setUp.setStyleSheet('background: transparent; color: gold')
        self.setUp.setFont(QFont("Arial", 50));
        self.setUp.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(self.setUp, 0, 0, 2, 15);

        # Back Button Implementation

        self.backButton = QPushButton("Back \n");
        self.backButton.setFont(QFont("Arial", 45));
        self.backButton.setStyleSheet('background: transparent; color: gold')
        self.grid.addWidget(self.backButton, 13, 6, 2, 3);

        # Check what the volume/pressure_flags are
        self.mmHg = QPushButton("mmHg \n");
        self.mmHg.setStyleSheet('background: transparent; color: gold')
        self.mmHg.setFont(QFont("Arial",40));
        self.grid.addWidget(self.mmHg, 5,3, 6, 4);

        self.cmH20 = QPushButton("cmH20\n");
        self.cmH20.setStyleSheet('background: transparent; color: gold')
        self.cmH20.setFont(QFont("Arial", 40));
        self.grid.addWidget(self.cmH20, 5, 8, 6, 4);
        print('Control Flag is ' + str(controlFlag))
        # Actually set the unit flag here
        if controlFlag ==1:
            self.mmHg.clicked.connect(self.mmPressure)
            self.cmH20.clicked.connect(self.cmPressure)
        else:
            print(controlFlag)
            self.mmHg.clicked.connect(self.mmVolume)
            self.cmH20.clicked.connect(self.cmVolume)
        self.setLayout(self.grid)
    def mmPressure(self):
        global unitFlag, OpenPressure
        unitFlag = 'mmHg'
        OpenPressure = OpeningPressure();
        OpenPressure.show()
        self.hide();
    def cmPressure(self):
        global unitFlag, OpenPressure
        unitFlag = 'cmH20'
        OpenPressure = OpeningPressure();
        OpenPressure.show()
        self.hide();
    def mmVolume(self):
        global unitFlag, VolumeLimit
        unitFlag = 'mmHg'
        VolumeLimit = VolumeLimit();
        VolumeLimit.show()
        self.hide();
    def cmVolume(self):
        global unitFlag, VolumeLimit
        unitFlag = 'cmH20'
        VolumeLimit = VolumeLimit();
        VolumeLimit.show()
        self.hide()

class DrainScreen(QWidget):
    def __init__(self):
        
        super().__init__();

        self.text_field = QPlainTextEdit(self)
        self.text_field.setMinimumSize (1024,600)
        self.text_field.setStyleSheet("background-image: url(background.png); background-attachment: fixed")
        self.setFixedWidth(1024);
        self.setFixedHeight(600);
        self.grid = QGridLayout();


        # Set Up Label
        self.setUp = QLabel("Select Drainage Mode");
        self.setUp.setStyleSheet('background: transparent; color: gold')
        self.setUp.setFont(QFont("Arial", 75));
        self.setUp.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(self.setUp, 0, 0, 2, 15);

        # Back Button Implementation

        self.backButton = QPushButton("Back \n");
        self.backButton.setFont(QFont("Arial", 45));
        self.backButton.setStyleSheet('background: transparent; color: gold')
        self.grid.addWidget(self.backButton, 13, 6, 2, 3);


        # Pressure button

        self.pressureButton = QPushButton("Pressure with \n Volume Limit");
        self.pressureButton.setStyleSheet('background: transparent; color: gold')
        self.pressureButton.setFont(QFont("Arial",30));
        self.pressureButton.clicked.connect(self.toPressure);
        self.grid.addWidget(self.pressureButton, 5,3, 6, 4);

        # Volume Button
        self.volumeButton = QPushButton("Volume with \n Pressure Limit");
        self.volumeButton.setFont(QFont("Arial", 30));
        self.volumeButton.setStyleSheet('background: transparent; color: gold')
        self.volumeButton.clicked.connect(self.toVolume);
        self.grid.addWidget(self.volumeButton, 5, 8, 6, 4);


        self.setLayout(self.grid);
    def toPressure(self):
        # Set the control of the device
        global controlFlag, UnitScreen
        controlFlag=1
        UnitScreen = UnitPrompt()
        UnitScreen.show()
        self.hide()
    
    def toVolume(self):
        global controlFlag, UnitScreen
        controlFlag = 0
        UnitScreen = UnitPrompt()
        UnitScreen.show();
        self.hide()



class ZeroScreen(QWidget):
    def __init__(self):
        super().__init__();
        self.setFixedWidth(1024);
        self.setFixedHeight(600);
        self.grid = QGridLayout();

        self.text_field = QPlainTextEdit(self)
        self.text_field.setMinimumSize (1024,600)
        self.text_field.setStyleSheet("background-image: url(background.png); background-attachment: fixed")

        """
        for i in range(0,15):
            for j in range(0,15):
                tmp_label = QLabel("")
                tmp_label.setStyleSheet("border: 4px solid black;")
                self.grid.addWidget(tmp_label, i,j);
        """

        # Set Up Label
        self.setUp = QLabel("Transducer Set Up");
        self.setUp.setStyleSheet('background: transparent; color: gold')
        self.setUp.setFont(QFont("Arial", 75));
        self.setUp.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(self.setUp, 0, 0, 2, 15);


        self.zeroPrompt = QLabel('Zero both the Patient Monitor and the IFlux \n at the Same time')
        self.zeroPrompt.setAlignment(Qt.AlignCenter)
        self.zeroPrompt.setFont(QFont("Arial", 50))
        self.zeroPrompt.setStyleSheet('background: transparent; color: gold')
        self.grid.addWidget(self.zeroPrompt,  2,0,2,15)
    


        # Zeroing Button

        self.ZeroingButton = QPushButton("Zero");
        self.ZeroingButton.setFont(QFont("Arial", 60));
        self.ZeroingButton.setStyleSheet('background: transparent; color: gold')
        self.ZeroingButton.clicked.connect(self.Calibration)
        self.grid.addWidget(self.ZeroingButton, 8,6,4,3);
        self.setLayout(self.grid);


    # Actually performs the calibration operation

    def Calibration(self):
        global baselinePressure
        temp = 0;
        for i in range(5):
            temp += random.randint(1,10);
            time.sleep(1);

        baselinePressure = temp/5.0;

        self.ZeroingButton.hide()
        self.zeroPrompt.hide()
        self.goodLabel = QLabel("Calibration Sucessful!");
        self.goodLabel.setStyleSheet("border: 2px solid black;")
        self.goodLabel.setFont(QFont("Arial", 50));
        self.goodLabel.setAlignment(Qt.AlignCenter)        
        self.grid.addWidget(self.goodLabel,4,0,2,15);

        
        self.nextButton = QPushButton('Next')
        self.nextButton.setFont(QFont("Arial", 75));
        self.nextButton.clicked.connect(self.toDrainage)
        self.grid.addWidget(self.nextButton, 8,6,4,3);

    def toDrainage(self):
        global DrainageScreen;
        self.goodLabel.hide();
        self.nextButton.hide();
        self.ZeroingButton.show();
        self.zeroPrompt.show();
        DrainageScreen = DrainScreen();
        DrainageScreen.show()
        self.hide();
        





# Really meant for Zeroing Purposes
class ZeroSetUp(QWidget):


    def __init__(self):
        super().__init__();
        self.setFixedWidth(1024);
        self.setFixedHeight(600);
        self.grid = QGridLayout();



        self.text_field = QPlainTextEdit(self)
        self.text_field.setMinimumSize (1024,600)
        self.text_field.setStyleSheet("background-image: url(background.png); background-attachment: fixed")


        # Set Up Label
        self.setUp = QLabel("Zeroing Screen");
        self.setUp.setStyleSheet('background: transparent; color: gold')
        self.setUp.setFont(QFont("Arial", 75));
        self.setUp.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(self.setUp, 0, 0, 2, 15);
        

        # Zero Now or Later Label

        self.chooseLabel = QLabel(" Zero Now or Later?  ");
        self.chooseLabel.setFont(QFont("Arial", 30));
        self.chooseLabel.setAlignment(Qt.AlignCenter)
        self.chooseLabel.setStyleSheet('background: transparent; color: gold')
        self.grid.addWidget(self.chooseLabel,2,6,2,3);

        # Zero Now Button
        self.ZeroNow = QPushButton("Zero \n Now");
        self.ZeroNow.setStyleSheet('background: transparent; color: gold')
        self.ZeroNow.setFont(QFont("Arial", 45));
        self.ZeroNow.clicked.connect(self.toCalibrate)
        self.grid.addWidget(self.ZeroNow, 5,3,6,4)


        # Zero Later Button
        self.ZeroLater = QPushButton(" Zero \n Later");
        self.ZeroLater.setFont(QFont("Arial", 45));
        self.ZeroLater.setStyleSheet('background: transparent; color: gold')
        self.ZeroLater.clicked.connect(self.toDrainage)
        self.grid.addWidget(self.ZeroLater, 5,8,6,4)


        self.Back = QPushButton("Back \n")
        self.Back.setStyleSheet('background: transparent; color: gold')
        self.Back.setFont(QFont("Arial", 45));
        self.Back.clicked.connect(self.back)
        self.grid.addWidget(self.Back, 13,6,2,3)
        self.setLayout(self.grid)
    
    def toCalibrate(self):
        global CalibrationWindow
        if (CalibrationWindow == None):
            CalibrationWindow = ZeroScreen();
            CalibrationWindow.show();
            self.hide();
        else:
            CalibrationWindow.show();
            self.hide()
    def toDrainage(self):
        global DrainageScreen;
        DrainageScreen = DrainScreen();
        DrainageScreen.show()
        self.hide();


    def back(self):
        if (mode==2):
            EVDSensorSelectScreen.show()
            self.hide();
        else:   
            LumbarSensorSelect.show()
            self.hide()



class EVD(QWidget):
     # Setup happens here
    def __init__(self):
        super().__init__();
        self.setFixedWidth(1024);
        self.setFixedHeight(600);
        self.grid = QGridLayout();        
        self.text_field = QPlainTextEdit(self)
        self.text_field.setMinimumSize (1024,600)
        self.text_field.setStyleSheet("background-image: url(background.png); background-attachment: fixed")
        

        
        # Ask what type of sensor they want
        self.DisplayLabel = QLabel("Select Sensor Type");
        self.DisplayLabel.setStyleSheet('background: transparent; color: gold')
        self.DisplayLabel.setFont(QFont("Arial", 50))

        self.grid.addWidget(self.DisplayLabel, 2,6,2,3)
        

        # Pressure transducer
        self.PressureTransducer = QPushButton("Pressure \n Transducer");
        self.PressureTransducer.setStyleSheet('background: transparent; color: gold') 
        self.PressureTransducer.setFont(QFont("Arial", 45));
        self.PressureTransducer.clicked.connect(self.toPressureTransducerZeroing)
        self.grid.addWidget(self.PressureTransducer, 5,3,6,4)
        
        # Strain Gauge
        self.CodmanDevice = QPushButton("Codman \n Device");
        self.CodmanDevice.setStyleSheet('background: transparent; color: gold')
        self.CodmanDevice.setFont(QFont("Arial", 45));
        self.CodmanDevice.clicked.connect(self.toStrainGaugeCalibration)
        self.grid.addWidget(self.CodmanDevice, 5,8,6,4)

        self.Back = QPushButton("Back \n")
        self.Back.setStyleSheet('background: transparent; color: gold')
        self.Back.setFont(QFont("Arial", 45));
        self.Back.clicked.connect(self.back)
        self.grid.addWidget(self.Back, 13,6,2,3)
        self.setLayout(self.grid)

    def toPressureTransducerZeroing(self):
        global ZeroingWindow, transducerFlag
        transducerFlag=0
        if  ZeroingWindow==None:
            ZeroingWindow = ZeroSetUp();
            ZeroingWindow.show();
            self.hide()
        else:
            ZeroingWindow.show()
            self.hide()
        
    def toStrainGaugeCalibration(self):
        global ZeroingWindow, transducerFlag
        transducerFlag=1
        if  ZeroingWindow==None:
            ZeroingWindow = ZeroSetUp();
            ZeroingWindow.show();
            self.hide()
        else:
            ZeroingWindow.show()
            self.hide()

    def back(self):
        w.show()
        self.hide()


class LumbarDrain(QWidget):

    # Setup happens here
    def __init__(self):
        super().__init__();
        self.setFixedWidth(1024);
        self.setFixedHeight(600);
        self.grid = QGridLayout();
        
        self.text_field = QPlainTextEdit(self)
        self.text_field.setMinimumSize (1024,600)
        self.text_field.setStyleSheet("background-image: url(background.png); background-attachment: fixed")

         
        # Ask what type of sensor they want
        self.DisplayLabel = QLabel("Select Sensor Type");
        self.DisplayLabel.setStyleSheet('background: transparent; color: gold')
        self.DisplayLabel.setFont(QFont("Arial", 60))
        self.grid.addWidget(self.DisplayLabel, 2,6,2,3)

        # Pressure transducer
        self.PressureTransducer = QPushButton("Pressure \n Transducer");
        self.PressureTransducer.setStyleSheet('background: transparent; color: gold')
        self.PressureTransducer.setFont(QFont("Arial", 45));
        self.PressureTransducer.clicked.connect(self.toPressureTransducerZeroing)
        self.grid.addWidget(self.PressureTransducer, 5,3,6,4)
        
        # Strain Gauge
        self.CodmanDevice = QPushButton("Codman \n Device");
        self.CodmanDevice.setStyleSheet('background: transparent; color: gold')
        self.CodmanDevice.setFont(QFont("Arial", 45));
        self.CodmanDevice.clicked.connect(self.toStrainGaugeCalibration)
        self.grid.addWidget(self.CodmanDevice, 5,8,6,4)

        self.Back = QPushButton("Back \n" )
        self.Back.setStyleSheet('background: transparent; color: gold')
        self.Back.setFont(QFont("Arial", 45));
        self.Back.clicked.connect(self.back)
        self.grid.addWidget(self.Back, 13,6,2,3)
        self.setLayout(self.grid)

    def toPressureTransducerZeroing(self):
        global ZeroingWindow, transducerFlag
        transducerFlag=0
        if  ZeroingWindow==None:
            ZeroingWindow = ZeroSetUp();
            ZeroingWindow.show();
            self.hide()
        else:
            ZeroingWindow.show()
            self.hide()
        
    def toStrainGaugeCalibration(self):
        global ZeroingWindow, transducerFlag
        transducerFlag=1
        if  ZeroingWindow==None:
            ZeroingWindow = ZeroSetUp();
            ZeroingWindow.show();
            self.hide()
        else:
            ZeroingWindow.show()
            self.hide()

    def back(self):
        w.show()
        self.hide()

# Class is responsible for the Window that contains all options of setting up the drain
class SetUp(QWidget):

    # Set up the screens
    def __init__(self):
        super().__init__();
        self.setFixedWidth(1024);
        self.setFixedHeight(600);
        self.grid = QGridLayout();


        self.setStyleSheet("background-image: url(./background.png);")

        
        # Configuration Labe;
        self.DisplayLabel = QLabel("Select Drain Type")
        self.DisplayLabel.setStyleSheet('background: transparent; color: gold')
        self.DisplayLabel.setFont(QFont("Arial", 60));



        self.grid.addWidget(self.DisplayLabel, 2,6,2,3)

        # Configuration Label

        # To EVD Mode   
        self.EVDButton = QPushButton("EVD \n")
        self.EVDButton.setFont(QFont("Arial", 50))
        self.EVDButton.clicked.connect(self.toEVD)
        self.EVDButton.setStyleSheet('background: transparent; color: gold;')



        self.grid.addWidget(self.EVDButton, 5,3,6,4)
      
        # To Lumbar Drain Mode
        self.LumbarButton = QPushButton("Lumbar \n Drain")
        self.LumbarButton.setStyleSheet('background: transparent; color: gold')
        
        self.LumbarButton.setFont(QFont("Arial", 55))
        self.LumbarButton.clicked.connect(self.toLumbar)
        self.grid.addWidget(self.LumbarButton, 5,8,6,4)

   
        self.setLayout(self.grid);

    def toEVD(self):
        global mode, EVDSensorSelectScreen;
        mode = 2;
        if (EVDSensorSelectScreen == None):
            EVDSensorSelectScreen = EVD();
            EVDSensorSelectScreen.show();
            w.hide();
        else:
            EVDSensorSelectScreen.show();
        w.hide();


    def toLumbar(self):
        global mode, LumbarSensorSelect
        mode = 1;
        if (LumbarSensorSelect == None):
            LumbarSensorSelect = LumbarDrain();
            LumbarSensorSelect.show();
            w.hide()
        else:
            LumbarSensorSelect.show();
            w.hide()
   # Responsible for setting up the help screen options
    def help(self):
        pass
# The initial set-up of the system

class MainWindow(QMainWindow):
    def __init__(self):
        global w;
        super(MainWindow, self).__init__();
        self.setWindowTitle("My App");
        self.setFixedWidth(1024);
        self.setFixedHeight(600);
        w = SetUp();

        self.setStyleSheet("background-image: url(./background.png);")
        self.setCentralWidget(w);





app = QApplication(sys.argv)

w = MainWindow()
w.show()
app.exec()
