'''
/* =======================================================================
   (c) 2015, Kre8 Technology, Inc.

   Name:          Robot Escape
   By:            Qin Chen
   Last Updated:  6/10/18

   PROPRIETARY and CONFIDENTIAL
   ========================================================================*/
'''
# This program shows how threads can be created using Thread class and your
# own functions. Another way of creating threads is subclass Thread and override
# run().
# 

import sys
sys.path.append('../')
import time  # sleep
import threading
import Tkinter as tk
import Queue
from comm_ble import RobotComm

#logging.basicConfig(level=logging.DEBUG,format='(%(threadName)-10s) %(message)s',)

class Event(object):
    def __init__(self, event_type, event_data, robotList):
      self.type = event_type #string
      self.data = event_data #list of number or character depending on type

class FSM(threding.Thread):
    def __init__(self, startState, states, q_handle):
        self.go = False
        self.quit = False

        self.startState = startState
        self.states = []

        self.q = q_handle

    def run(self):
        current_state = self.startState

        while not self.quit and self.go:
            if not q.empty():
                event = q.get()
                for theInput in current_state
                

class BehaviorThreads(object):
    Threshold_border = 20   # if floor sensor reading falls equal or below this value, border is detected
    Threshold_obstacle = 50   # if prox sensor reading is equal or higher than this, obstacle is detected
    
    def __init__(self, robot_list):
    	self.robot_list = robot_list
        self.go = False
        self.quit = False
        # events queues for communication between threads
        self.alert_q = Queue.Queue()
        self.motion_q = Queue.Queue()
        self.t_robot_watcher = None     # thread handles
        self.t_motion_handler = None
        
        # start a watcher thread
        #The t_robot_watcher is an instance variable?
        t_robot_watcher = threading.Thread(name='watcher thread', target=self.robot_event_watcher, args=(self.alert_q, self.motion_q))
        t_robot_watcher.daemon = True
        t_robot_watcher.start()
        #why do the following step?
        self.t_robot_watcher = t_robot_watcher

        return

    ###################################
    # This function is called when border is detected
    ###################################
    #def get_out (self, robot):
    #    pass

    # This function monitors the sensors
    def robot_event_watcher(self, q1, q2):
        count = 0

        #logging.debug('starting...')
        while not self.quit: #the GUI's stopProg turns the self.quit into True, so this daemon thread ends
            for robot in self.robot_list:
                if self.go and robot:
                    #print('inside event watcher loop')
                    prox_l = robot.get_proximity(0)
                    prox_r = robot.get_proximity(1)
                    line_l = robot.get_floor(0)
                    line_r = robot.get_floor(1)

                    if (prox_l > BehaviorThreads.Threshold_obstacle or prox_r > BehaviorThreads.Threshold_obstacle):
                        alert_event = Event("alert", [prox_l,prox_r])
                        q1.put(alert_event)
                        count += 1
	                    #update movement every 5 ticks, to avoid being too sensitive?
                        if (count % 5 == 0):
                            obs_event = Event("obstacle", [prox_l, prox_r])
                            q2.put(obs_event)
                        
                    else:
                        if (count > 0):
                        	# free event is created when robot goes from obstacle to no obstacle
                            #logging.debug("free of obstacle")
                            free_event = Event("free",[])
                            q2.put(free_event)  # put event in motion queue
                            q1.put(free_event)  # put event in alert queue
                            count = 0
                else:
                    #print 'waiting ...'
                    pass

            time.sleep(0.02)	# delay to give alert thread more processing time. Otherwise, it doesn't seem to have a chance to serve 'free' event
        return

    ##############################################################
    # Implement your motion handler. You need to get event using the passed-in queue handle and
    # decide what Hamster should do. Hamster needs to avoid obstacle while escaping. Hamster
    # stops moving after getting out of the border and remember to flush the motion queue after getting out.
    #############################################################

    def avoid_obstacle(left):
        for robot in self.robot_list:
            if left:
                robot.set_wheel(1, -20)
                robot.set_wheel(0, 20)
            else:
                robot.set_wheel(1, 20)
                robot.set_wheel(0, -20)



    def robot_motion_handler(self, q):
        #print(' go robot go')

        while not self.quit:
            #print(self.go, 'motion handler self go')
            if self.go:
                if not q.empty():
                    print(q.qsize(), 'motion handler q size')
                    #print "hahahahahahha"
                    
                    #return
                    event = q.get()
                    #print('otion handler ', event.type)

                    if event.type == "border":
                        for robot in self.robot_list:
                            robot.set_wheel(1, 0)
                            robot.set_wheel(0, 0)
                            robot.set_musical_note(60)
                            time.sleep(3)                   
                            robot.set_musical_note(0)
                        return

                    elif event.type == "obstacle":
                        for robot in self.robot_list:
                            #robot.set_wheel(1, -20)
                            #robot.set_wheel(0, -20)
                            #time.sleep(0.1)
                            robot.set_wheel(1, -20)
                            robot.set_wheel(0, 20)
                            #time.sleep(2)
                    elif event.type == "free":
                        for robot in self.robot_list:
                            robot.set_wheel(1, 30)
                            robot.set_wheel(0, 30)
                            robot.set_musical_note(0)
                #time.sleep(0.005)


                                       


class GUI(object):
    def __init__(self, root, threads_handle):  #self.t_handle = threads_handle
        self.root = root
        self.t_handle = threads_handle
        self.event_q = threads_handle.alert_q
        self.t_alert_handler = None
        self.canvas = None
        self.prox_l_id = None
        self.prox_r_id = None
        self.initUI()

    ##########################################################
    # 1. Create a canvas widget and three canvas items: a square, and two lines 
    # representing prox sensor readings.
    # 2. Create two button widgets, for start and exit.
    # 3. Create a thread for alert handler, which is responsible for displaying prox sensors.
    ##########################################################
    def initUI(self):
        self.root.geometry("400x600")
        self.root.title("Hamster_escape")

        #self.t_alert_handler = 
        self.cc = tk.Canvas(self.root, bg = "green", width = 400, height = 545)
        self.cc.pack(side = "top")

        hamsterIcon = self.cc.create_rectangle(130, 260, 270, 400, fill = "blue", width = 3.6)

        self.lineLeft = self.cc.create_line(170, 260, 170, 260, width = 3, fill = "red")
        self.lineRight = self.cc.create_line(230, 260, 230, 260, width = 3, fill = "red")

        b1 = tk.Button(self.root, text = "Start")
        b1.bind("<Button-1>", self.startRobot)
        b1.pack(side = "bottom")

        bb = tk.Button(self.root, text = "Exit")
        bb.bind("<Button-1>", self.stopProg)
        bb.pack(side = "bottom")
        #print "hahahahahaha"
        
        #create alert handler which is in charge of displaying
        #threading.Thread(name = alert_thread, target = robot_alert_handler, args = )
        self.robot_alert_handler(self.event_q)
 

    ###################################################
    # Handles prox sensor display and warning(sound).
    # Query event queue(using passed-in queue handle).
    # If there is an "alert" event, display red beams.
    # Erase the beams when "free" event is in queue.
    # This runs in the main GUI thread. Remember to schedule
    # a callback of itself after 50 milliseconds.
    ###################################################
    def robot_alert_handler(self, q):
        if not q.empty():#process an event every time
            current_event = q.get()
            #print(q.qsize(), 'robot alert handler q size')

            # for robot in self.t_handle.robot_list:
                # robot.set_buzzer(0)

            #initialize every time, in case it's free
            self.cc.coords(self.lineLeft, 170, 260, 170, 260)
            self.cc.coords(self.lineRight, 230, 260, 230, 260)

            if current_event.type == "border":
                #set musical code
                '''
                for robot in self.t_handle.robot_list:
                    print('current event border')
                    #return
                #print "hahhaah"

                '''
                for robot in self.t_handle.robot_list:
                    robot.set_musical_note(0)

                #self.stopProg()

            elif current_event.type == "alert":
                lp = current_event.data[0]
                rp = current_event.data[1]
                self.cc.coords(self.lineLeft, 170, 260, 170, 260-lp*2.5)
                self.cc.coords(self.lineRight, 230, 260, 230, 260-rp*2.5)
                for robot in self.t_handle.robot_list:
                    robot.set_musical_note(40)

            elif current_event.type == "obstacle":

                lp = current_event.data[0]
                rp = current_event.data[1]
                self.cc.coords(self.lineLeft, 170, 260, 170, 260-lp*2.5)
                self.cc.coords(self.lineRight, 230, 260, 230, 260-rp*2.5)

        self.cc.after(50, self.robot_alert_handler, (q))
     
    def startRobot(self, event=None):
        self.t_handle.go = True
        for robot in self.t_handle.robot_list:
            robot.set_wheel(1, 30)
            robot.set_wheel(0, 30)
        return

    def stopProg(self, event=None):
        self.t_handle.quit = True
        
        for robot in self.t_handle.robot_list:
            robot.reset()
        '''
        self.t_handle.t_motion_handler.join()
        self.t_handle.t_robot_watcher.join()
        self.t_alert_handler.join()
        '''
        self.root.quit()    # close GUI window
        return   

def main():
    max_robot_num = 1   # max number of robots to control
    comm = RobotComm(max_robot_num)
    comm.start()
    print 'Bluetooth starts'
    robotList = comm.robotList

    root = tk.Tk()
    #print "hahahah"
    t_handle = BehaviorThreads(robotList)
    #print "haha"
    gui = GUI(root, t_handle)

    root.mainloop()

    comm.stop()
    comm.join()

if __name__== "__main__":
  sys.exit(main())
  