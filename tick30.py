#!/usr/bin/python
# -*- coding: utf8 -*-

# set up the window size
from kivy.config import Config
Config.set('graphics', 'width', 1080)
Config.set('graphics', 'height', 670)
Config.write()
# import the kivy modules
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Color, Ellipse, Line
from kivy.graphics.instructions import Callback
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.interactive import InteractiveLauncher
from kivy.properties import NumericProperty, StringProperty, ListProperty
from kivy.event import EventDispatcher
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
# import the python modules that are needed: time for recording time, random for shuffling items and csv for saving .csv files
import time
import random
import csv

# writes the name of the file run that will be saved in the .csv
expVersion = __file__

# global variables with the experimental sentences used in the experiment
TOT_red = 'TICK cercles sont rouges'
SOM_red = 'POCK cercles sont rouges'
nTOT_red = 'TICK cercles ne sont pas rouges'
nSOM_red = 'POCK cercles ne sont pas rouges'

TOT_blu = 'TICK cercles sont bleus'
SOM_blu = 'POCK cercles sont bleus'
nTOT_blu = 'TICK cercles ne sont pas bleus'
nSOM_blu = 'POCK cercles ne sont pas bleus'

# global variables for colors
RED = (.9,.1,0)
BLUE = (0, .1, .9)
WHITE = (1,1,1)

# global variables for wait time (the lag time between the participant's answer and the plotting of a new trial) in Yes/No and Comparison phases
WAIT_YN = 2
WAIT_COMP = 1

# global variables that categorize all the phases into YN (for Yes/No) and COMP (for comparison) phases
YN = ['YN', 'YN_rb']
COMP = ['COMP', 'COMP_rb', 'COMP_neg_rb', 'COMP_mix_rb']



# global variables that categorize the test phases vs. instruction ones
TESTPHASES = YN + COMP
INSTRUCTIONS = ['instruct', 'instruct2','instruct_rb','instruct_comp_rb','instruct_neg_rb']

# global variable including the points for plotting the circles in the two possible phases
framePoint= {'YN': [150, 250, 775, 250, 775, 625, 150, 625, 150, 250],
    
    'COMP':  [[50, 250, 450, 250, 450, 580, 50, 580, 50, 250],
     [600, 250, 1000, 250, 1000, 580, 600, 580, 600, 250]]
    }

# a global dictionary that contains all the pairs or triplets of configurations and sentences for each phase
itemGroups = {





'YN': [ [['T',TOT_red],['T',SOM_red],['M',TOT_red],['M',SOM_red],['Z',TOT_red],['Z',SOM_red],['T',TOT_red],['T',SOM_red],['M',TOT_red],['M',SOM_red],['Z',TOT_red],['Z',SOM_red]], [['T',TOT_red],['T',SOM_red],['M',TOT_red],['M',SOM_red],['Z',TOT_red],['Z',SOM_red],['T',TOT_red],['T',SOM_red],['M',TOT_red],['M',SOM_red],['Z',TOT_red],['Z',SOM_red]] ],


'YN_rb': [ [['T',TOT_red],['T',SOM_blu],['M',TOT_red],['M',SOM_blu],['Z',TOT_red],['Z',SOM_blu],['T',TOT_red],['T',SOM_blu],['M',TOT_red],['M',SOM_blu],['Z',TOT_red],['Z',SOM_blu]], [['T',TOT_red],['T',SOM_blu],['M',TOT_red],['M',SOM_blu],['Z',TOT_red],['Z',SOM_blu],['T',TOT_red],['T',SOM_blu],['M',TOT_red],['M',SOM_blu],['Z',TOT_red],['Z',SOM_blu]] ],





'COMP': [ [['M','Z',SOM_red],['Z','M',SOM_red],['T','Z',SOM_red],['Z','T',SOM_red],['T','M',SOM_red],['M','T',SOM_red],['T','Z',TOT_red],['Z','T',TOT_red],['T','M',TOT_red],['M','T',TOT_red],['T','Z',TOT_red],['M','T',TOT_red]], [['M','Z',SOM_red],['Z','M',SOM_red],['T','Z',SOM_red],['Z','T',SOM_red],['T','M',SOM_red],['M','T',SOM_red],['T','Z',TOT_red],['Z','T',TOT_red],['T','M',TOT_red],['M','T',TOT_red],['Z','T',TOT_red],['T','M',TOT_red]] ],




'COMP_rb': [ [['M','Z',SOM_red],['T','M',SOM_blu],['T','Z',SOM_blu],['Z','T',SOM_red],['T','M',SOM_red],['M','Z',SOM_blu],['T','Z',TOT_blu],['Z','T',TOT_red],['T','M',TOT_red],['M','Z',TOT_blu],['Z','T',TOT_blu],['M','T',TOT_red]],

 [['M','T',SOM_blu],['Z','M',SOM_red],['T','Z',SOM_red],['Z','T',SOM_blu],['Z','M',SOM_blu],['M','T',SOM_red],['T','Z',TOT_red],['T','Z',TOT_blu],['Z','M',TOT_blu],['T','M',TOT_red],['Z','T',TOT_red],['M','Z',TOT_blu]] ],
 
 
 
'COMP_neg_rb': [  [['M','T',nSOM_blu],['Z','T',nSOM_blu],['T','M',nSOM_blu],['M','T',nTOT_blu],['Z','T',nTOT_blu],['M','Z',nTOT_blu],
 ['T','Z',nSOM_red],['Z','M',nSOM_red],['Z','T',nSOM_red],['T','M',nTOT_red],['Z','M',nTOT_red],['T','Z',nTOT_red] ] ,
 
 [['Z','M',nSOM_red],['M','Z',nSOM_red],['T','Z',nSOM_red], ['M','T',nTOT_red],['M','Z',nTOT_red],['Z','T',nTOT_red],
 ['T','Z',nSOM_blu], ['Z','T',nSOM_blu],['T','M',nSOM_blu],['T','M',nTOT_blu],['Z','M',nTOT_blu],['T','Z',nTOT_blu] ] ],
 
 
 
 
'COMP_mix_rb': [ [['M','Z',SOM_red],['T','M',SOM_blu],['T','Z',SOM_blu],['Z','T',SOM_red],['T','M',SOM_red],['M','Z',SOM_blu],['T','Z',TOT_blu],['Z','T',TOT_red],['T','M',TOT_red],['M','Z',TOT_blu],['Z','T',TOT_blu],['M','T',TOT_red], 
['Z','M',nSOM_red],['M','Z',nSOM_red],['T','Z',nSOM_red], ['M','T',nTOT_red],['M','Z',nTOT_red],['Z','T',nTOT_red],
 ['T','Z',nSOM_blu], ['Z','T',nSOM_blu],['T','M',nSOM_blu],['T','M',nTOT_blu],['Z','M',nTOT_blu],['T','Z',nTOT_blu] ],

 [['M','T',SOM_blu],['Z','M',SOM_red],['T','Z',SOM_red],['Z','T',SOM_blu],['Z','M',SOM_blu],['M','T',SOM_red],['T','Z',TOT_red],['T','Z',TOT_blu],['Z','M',TOT_blu],['T','M',TOT_red],['Z','T',TOT_red],['M','Z',TOT_blu], 
 ['M','T',nSOM_blu],['Z','T',nSOM_blu],['T','M',nSOM_blu],['M','T',nTOT_blu],['Z','T',nTOT_blu],['M','Z',nTOT_blu],
 ['T','Z',nSOM_red],['Z','M',nSOM_red],['Z','T',nSOM_red],['T','M',nTOT_red],['Z','M',nTOT_red],['T','Z',nTOT_red] ] ]
 
}


class Circles(object):

    def __init__(self, posx, posy, color, size):
        self.x = posx
        self.y = posy
        self.col = color
        self.size = size


class Configuration(object):

    def __init__(self, tyype='YN1', nred = 6, nblue = 6, nred2 = 0, nblue2 = 0):
        self.nred = nred
        self.nblue = nblue
        self.nred2 = nred2
        self.nblue2 = nblue2
        self.circles = []
        self.tyype = tyype
        self.setupConf()
        
    circlePositions= {'YN':  ([200,300],[350,300],[500,300],[650,300],[200,400],[350,400],[500,400],[650,400],[200,500],[350,500],[500,500],[650,500]),'COMP':  ([[70,270],[170,270],[270,270],[370,270],[70,375],[170,375],[270,375],[370,375],[70,480],[170,480],[270,480],[370,480]],[[620,270],[720,270],[820,270],[920,270],[620,375],[720,375],[820,375],[920,375],[620,480],[720,480],[820,480],[920,480]])}
       
    circleSize= {'YN': 80,'COMP': 60}
      
    def setupConf(self):
        
        if self.tyype in YN:
        
            circlePosz = list(self.circlePositions['YN'])

            for i in range(0,self.nred):
                coord = circlePosz.pop(0)
                self.circles.append(Circles(coord[0],coord[1],RED,self.circleSize['YN']))

            for i in range(0,self.nblue):
                coord = circlePosz.pop(0)
                self.circles.append(Circles(coord[0],coord[1],BLUE,self.circleSize['YN']))
                
        if self.tyype in COMP:

            circlePosz1 = list(self.circlePositions['COMP'][0])

            for i in range(0,self.nred):
                coord = circlePosz1.pop(0)
                self.circles.append(Circles(coord[0],coord[1],RED,self.circleSize['COMP']))

            for i in range(0,self.nblue):
                coord = circlePosz1.pop(0)
                self.circles.append(Circles(coord[0],coord[1],BLUE,self.circleSize['COMP']))
            
            circlePosz2 = list(self.circlePositions['COMP'][1])

            for i in range(0,self.nred2):
                coord = circlePosz2.pop(0)
                self.circles.append(Circles(coord[0],coord[1],RED,self.circleSize['COMP']))

            for i in range(0,self.nblue2):
                coord = circlePosz2.pop(0)
                self.circles.append(Circles(coord[0],coord[1],BLUE,self.circleSize['COMP']))
            
            
                     
class EventHandler(Widget):
    trialDisplayed = NumericProperty(0)
    keyPressed = ListProperty([])
  
    def __init__(self, **kwargs):
        super(EventHandler, self).__init__(**kwargs)
        Window.bind(on_key_down=self.on_key)
           
    def on_key(self, keycode, *args):
    	self.keyPressed.append([args[2], time.time()])
    	

            

events = EventHandler()


class Trials(object):

    def __init__(self):
        self.setup = None
        self.question = None
        self.ans = None
        self.time = None
        self.timeStart = None
        self.val = None

    def evalTrial(self):
        
        if self.question == TOT_red:
            if self.ans == 'm' and self.setup.nred == 12: return 'correct'
            elif self.ans == 'c' and self.setup.nred < 12: return 'correct'
            else: return 'incorrect'
            
        if self.question == SOM_red:
            if self.ans == 'm' and self.setup.nred > 0: return 'correct'
            elif self.ans == 'c' and self.setup.nred == 0: return 'correct'
            else: return 'incorrect'
            
                
        if self.question == TOT_blu:
            if self.ans == 'm' and self.setup.nred == 0: return 'correct'
            elif self.ans == 'c' and self.setup.nred > 0: return 'correct'
            else: return 'incorrect'
            
        if self.question == SOM_blu:
            if self.ans == 'm' and self.setup.nred < 12: return 'correct'
            elif self.ans == 'c' and self.setup.nred == 12: return 'correct'
            else: return 'incorrect'
            
            
            
            
    def writeEval (self, val):
        self.val = val   
              
    def writeTrial (self, ans, time):
        self.time = time
        self.ans = ans

  
class Session(object):

    def __init__(self, tyype, number):
        self.tyype = tyype
        self.number = number
        self.trials = []
        self.makeSession()

    def makeSession(self):

        for group in itemGroups[self.tyype]:

            random.shuffle(group)
            for tr in group:

                if self.tyype in YN:                

                    if tr[0] == 'T': nred = 12
                    if tr[0] == 'Z': nred = 0
                    if tr[0] == 'M': nred = random.randint(4,8)
                    thisTrial = Trials()                
                    thisTrial.setup = Configuration(self.tyype, nred,12-nred)
                    thisTrial.question = tr[1]
                
                if self.tyype in COMP:
                
                    if tr[0] == 'T': nred = 12
                    if tr[0] == 'Z': nred = 0
                    if tr[0] == 'M': nred = random.randint(4,8)
                    if tr[1] == 'T': nred2 = 12
                    if tr[1] == 'Z': nred2 = 0
                    if tr[1] == 'M': nred2 = random.randint(4,8)
                    
                    thisTrial = Trials()                
                    thisTrial.setup = Configuration(self.tyype, nred,12-nred, nred2, 12-nred2)
                    thisTrial.question = tr[2]
     
                self.trials.append(thisTrial)	



class DisplayWidget(Widget):
    
  
    def __init__(self, session, **kwargs):
        super(DisplayWidget, self).__init__(**kwargs)
        self.session = session   
# Window.clearcolor = (0.1, 0.1, 0.1, 1.)
        self.update_drawing()
        self.display_label()
                   
    def drawCircles(self, *args):
        with self.canvas:

	    # draws all the circles (contained in the setup) of the current trial                                                    
            for circle in self.session.trials[self.ntrial].setup.circles:
                Color(*circle.col)
                d = circle.size
                Ellipse(pos=(circle.x , circle.y), size=(d, d))

	
	    
    def update_drawing(self):
        self.canvas.clear()
        # gets the trial that is gonna be displayed
        self.ntrial = events.trialDisplayed
 #       events.bind(trialDisplayed=self.callcall)

        # writes the presentation time
        self.session.trials[self.ntrial].timeStart = time.time() + 0.5
        print 'now plotting the trial', self.ntrial
        with self.canvas:
            
            if self.session.tyype in YN:
                Color(*WHITE)
                Line(points=framePoint['YN'], width=2.5)
            
            if self.session.tyype in COMP:
                Color(*WHITE)
                Line(points=framePoint['COMP'][0], width=2.5)
                Color(*WHITE)
                Line(points=framePoint['COMP'][1], width=2.5)
             
            Clock.schedule_once(self.drawCircles,0.5)          
#            self.drawCircles()                                    
#                self.cb = Callback(self.my_callback)
                                        
    def display_label (self):
        self.label = Label(text = self.session.trials[events.trialDisplayed].question, font_size=30, x=400) 
        self.add_widget(self.label)
            
#    def my_callback (self, instr):
#        pass
    
    def callcall (self, *args):
        # updates the drawing
        self.update_drawing()
#        self.remove_widget(self.label)
        self.display_label()


class Phases(object):
        
    def __init__ (self, layout, phase = 'nameinput', number = 0):
        self.name = None
        self.number = number
        self.phase = phase
        self.layout = layout
        self.display = None
        self.session = None
        self.store = []
        self.length = 1
        events.bind(keyPressed=self.moveOn)
        self.runPhase()
        
    allPhases = ['instruct', 'YN','instruct_rb','YN_rb','instruct_comp_rb','COMP_rb','instruct_rb','YN_rb', 'instruct_neg_rb', 'COMP_neg_rb', 'instruct_neg_rb', 'COMP_mix_rb', 'fin'] 
#    phaseLength = {'nameinput':1, 'instruct': 1, 'YN0': 12, 'instruct2':1, 'YN1':96, 'COMP1': 96, 'YN2':24, 'COMP2': 24,  'YN3':24, 'COMP3': 24}
    
     
    def lenPhase(self):
        lenblock = 0
        for gr in itemGroups[self.phase]:
            lenblock += len(gr)
        return lenblock    
            
    def moveOn(self, *args):
        
#        print events.keyPressed[-1][0]
                
#        if events.keyPressed[-1][0] in ['m','z'] and self.phase in TESTPHASES and events.trialDisplayed < self.length and len ([key for key in events.keyPressed if key[0] in ['m','z']]) >= 1 and (events.keyPressed[-1][1] - events.keyPressed[-2][1]) < 2:
#            print events.keyPressed[-1], 'is going to be deleted because', events.keyPressed[-1][1] - events.keyPressed[-2][1], 'is smaller than 2'
 #           del (events.keyPressed[-1])
 #           print events.keyPressed[-1], 'heres the last one recorded'

        if self.phase in YN: waitTime = WAIT_YN
        if self.phase in COMP: waitTime = WAIT_COMP    
        
        if events.keyPressed[-1][0] in ['m','c'] and self.phase in TESTPHASES and events.trialDisplayed < self.length and (len ([key for key in events.keyPressed if key[0] in ['m','c']]) < 2 or (len ([key for key in events.keyPressed if key[0] in ['m','c']]) >= 2 and (events.keyPressed[-1][1] - [key for key in events.keyPressed if key[0] in ['m','c']][-2][1]) >= waitTime)) :
                        
            print 'ora si sta salvando il TRIAL numero:', events.trialDisplayed, 'che ha avuto risposta:', events.keyPressed[-1][0]
            if self.session.trials[events.trialDisplayed].time == None:        
                self.session.trials[events.trialDisplayed].writeTrial(ans = events.keyPressed[-1][0], time =  time.time()- self.session.trials[events.trialDisplayed].timeStart)
            print 'il time start e: ', self.session.trials[events.trialDisplayed].timeStart
            print 'il tempo di risposta e', self.session.trials[events.trialDisplayed].time
                        
            if self.phase in YN:

                feedb = self.session.trials[events.trialDisplayed].evalTrial()
                print feedb
                self.session.trials[events.trialDisplayed].writeEval(feedb)
                
                self.displayFeedback(fb=feedb)
                if events.trialDisplayed < self.length-1:
                    Clock.schedule_once(self.trialNext, WAIT_YN)
                else: 
                    events.unbind(trialDisplayed=self.display.callcall)
                    Clock.schedule_once(self.displaySpacetoC,3)
            
            if self.phase in COMP:
                if events.trialDisplayed < self.length-1:
                    Clock.schedule_once(self.trialNext, WAIT_COMP)
                else:
                    events.unbind(trialDisplayed=self.display.callcall)
                    Clock.schedule_once(self.displaySpacetoY,3)

        if events.keyPressed[-1][0] == ' ' and events.trialDisplayed == self.length-1 and self.phase in TESTPHASES + INSTRUCTIONS:


            if self.phase in TESTPHASES: 
                self.storePhase() 
                print 'just stored the session', self.session.tyype, 'number', self.session.number           
                self.csvWrite()
                print 'now saving'
           
            print 'changing phase'
        
            self.number += 1
            if len(self.allPhases) > 0:
                self.phase = self.allPhases.pop(0)
            else: self.phase = 'fin'
            self.layout.remove_widget(self.display)
            events.trialDisplayed = 0
                       
            self.runPhase()
#            print 'trial should be 0', events.trialDisplayed
            

    def displayFeedback(self, fb, *args):
        self.feedback = Label(text= fb , font_size=40, x=400, y=100, italic=True, color=[1,1,0,1])
        self.display.add_widget(self.feedback)
        

    def displaySpacetoC(self, *args):
        self.layout.remove_widget(self.display)
        self.display = Label(text= u"""Cette phase est terminée, appuyez sur la touche ESPACE """ , font_size=20)
        self.layout.add_widget(self.display)
            
    def displaySpacetoY(self, *args):
        self.layout.remove_widget(self.display)
        self.display = Label(text= u"""Cette phase est terminée, appuyez sur la touche ESPACE  """ , font_size=20)
        self.layout.add_widget(self.display)

               
    def trialNext(self, *args):
        events.trialDisplayed += 1
    
    def on_text(self, *args):
        self.name = args[1]
    
    def on_enter(self,*args):
        self.name = self.name.split(':')[1]       
#        print 'questo e il name:     ', self.name
        self.layout.remove_widget(self.textinput)
        # setting phase to instructions
        print 'si cambia fase'
        self.phase = self.allPhases.pop(0)
        print 'la fase nuova e : ', self.phase
        self.number += 1
        events.trialDisplayed = 0

        self.runPhase()
    
    def storePhase(self):
        self.store.append(self.session)
    
    def csvWrite(self):
        with open(self.name+'.csv','w') as f:
            csvf = csv.writer(f)
            csvf.writerow(['version', 'subject', 'sessionNumber', 'phase', 'ntrial', 'tstart', 'rt', 'nred', 'nred2', 'question', 'answer', 'value'])

            if len(self.store) > 0:
                for sessionStored in self.store:
                        sessionNumber = sessionStored.number
                        tyype = sessionStored.tyype
                        trialnum = [1]
                        for trial in sessionStored.trials:
                            question = trial.question
                            answer = trial.ans
                            rt = trial.time
                            tstart = trial.timeStart - timeStartExp
                            val = trial.val 
                            nred = trial.setup.nred
                            nred2 = trial.setup.nred2            
 
                            csvf.writerow([expVersion, self.name, sessionNumber, tyype, trialnum[0], tstart, rt, nred, nred2, question, answer, val])
                            trialnum[0] += 1
            f.close()
            

                
    def runPhase(self):
    
        if self.phase in TESTPHASES: self.length = self.lenPhase()      
        else: self.length = 1
        print 'il numero dei trial della fase', self.phase, ' e: ', self.length

         
        print 'siamo nella fase', self.phase, 'e nell item', events.trialDisplayed
        
        if self.phase == 'instruct':

            self.display = Label(text= u"""                  Bonjour et Bienvenue à la deuxième session de cette Expérience!
        Comme dans la première session, votre tâche consistera à lire et évaluer des phrases écrites en français qui contiennent deux quantificateurs fictionnels:
                TICK et POCK.

        La signification de ces deux quantificateurs est la même que dans la session précédente. De plus, cette session est composée des mêmes deux phases:

               PHASE VRAI/FAUX
            Lisez la phrase proposée et  jugez si elle est vraie ou fausse sur la base de la figure.
            Appuyez sur "v" si vous pensez  qu\'elle est vraie ou sur "f" si vous pensez qu\'elle est fausse. 
            Après chacune de vos réponses, un feedback (correct ou incorrect) apparaîtra sur l\'écran. 

               PHASE DE COMPARAISON

            Choisissez la figure qui représente le mieux le sens de la phrase.
            Appuyez sur "f" pour la figure de gauche, "v" pour la figure de droite.

            Cependant soyez attentifs! Parce qu'il y aura quelques changements dans les phrases. 

            Votre temps n\'est pas limité. Essayez cependant de répondre de façon intuitive, sans réfléchir trop longtemps. 

               Pour commencer la phase d\'essai, appuyez sur la touche "espace". 
                  Bonne chance!
""", font_siz=20)
            self.layout.add_widget(self.display)
        
        if self.phase == 'nameinput':
            self.textinput = TextInput(text = u'Veuillez écrire votre nom ici:', multiline=False)
            self.textinput.width = 250
            self.textinput.bind(text=self.on_text)
            self.textinput.bind(on_text_validate=self.on_enter)
            self.layout.add_widget(self.textinput)
               
            
        if self.phase == 'instruct2':
            self.display = Label(text= 'nella prossima fase dovrete fare comparison \n press SPACE BAR to continue', font_size=20  )
            self.layout.add_widget(self.display)
            
            
        if self.phase == 'instruct_rb':
            self.display = Label(text= u"""          Lisez la phrase proposée et appuyez sur "v" si vous pensez qu\'elle est vraie 
            ou sur "f" si vous pensez qu\'elle est fausse. 
         Après chacune de vos réponses, un feedback (correct ou incorrect) apparaîtra sur l\'écran. 
            Lisez attentivement les phrases, parce que la tâche est un peu plus complexe. 
            Pour passer à la phase suivante, appuyez sur la touche "espace". """, font_size=20  )
            self.layout.add_widget(self.display)
            
            
        if self.phase == 'instruct_comp_rb':
            self.display = Label(text= u"""          Choisissez la figure qui représente le mieux le sens de la phrase. 
            Appuyez sur "f" pour la figure de gauche, "v" pour la figure de droite.
            Veuillez répondre d\'une manière naturelle en suivant votre propre intuition. 
            Pour passer à la phase suivante, appuyez sur la touche "espace". """, font_size=20  )
            self.layout.add_widget(self.display)
            
            
        if self.phase == 'instruct_neg_rb':
            self.display = Label(text= u"""          Choisissez la figure qui représente le mieux le sens de la phrase. 
            Appuyez sur "f" pour la figure de gauche, "v" pour la figure de droite.
            Prêtez attention aux phrases, parce que certaines d\'entre elles contiennent 
            de petits changements qui sont pourtant importants. 
            Veuillez répondre d\'une manière naturelle en suivant votre propre intuition.
             Pour passer à la phase suivante, appuyez sur la touche "espace". """, font_size=20  )
            self.layout.add_widget(self.display)
            
            
            
            
                        
        if self.phase == 'fin':
            self.display = Label(text= u"""              Cette expérience est terminée.
               Merci beaucoup de votre collaboration et bonne journée!""", font_size=20  )
            self.layout.add_widget(self.display)

           
                
        if self.phase in TESTPHASES:
                
                print 'plotting trial', events.trialDisplayed, 'phase', self.phase
                self.session = Session(self.phase,self.number)
                self.display = DisplayWidget(self.session)
                events.bind(trialDisplayed=self.display.callcall)

                self.layout.add_widget(self.display)
  
            

#########   APP   CLASS  ################        
timeStartExp = time.time()
              
class TiktokApp(App):
                
    def build(self):	
        layout = BoxLayout(orientation='vertical')
        phase = Phases(layout)
        return layout

if __name__ == '__main__':
    TiktokApp().run()