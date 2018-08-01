'''
/* =======================================================================
   (c) 2015, Kre8 Technology, Inc.
   Stater program of 3-state obstacle avoidance using FSM.

   Name:          starter_tk_3state_avoid.py
   By:            Qin Chen
   Last Updated:  6/10/18

   PROPRIETARY and CONFIDENTIAL
   ========================================================================*/
'''
import sys
import time
import threading
import Tkinter as tk
import Queue
from comm_ble import RobotComm  # no dongle
#from HamsterAPI.comm_usb import RobotComm  # yes dongle

class Event(object):
    def __init__(self, event_type, event_data):
        self.type = event_type #string
        self.data = event_data #list of number or character depending on type

##############################
# Finite state machine engine
##############################
class StateMachine(object):
    def __init__(self, name, eventQ_handle, robot_control):
        self.name = name        # machine name
        self.states = []    # list of lists, [[state name, event, transition, next_state],...]
        self.start_state = None
        self.end_states = []    # list of name strings
        self.q = eventQ_handle
        self.done = robot_control.done
        return

    def set_start_state(self, state_name):
        self.start_state = state_name
        return

    def get_start_state(self):
        return self.start_state
        
    def add_end_state(self, state_name):
        self.end_states.append(state_name)
        return
            
    def add_state(self, state, event, callback, next_state):
        self.states.append([state, event, callback, next_state]) # append to list
        return
    
    # you must set start state before calling run()
    def run(self):
        current_state = self.start_state
        #while not self.q.empty(): # for a machine that has end states
        while not self.done:
            #print "hhhahahahahhahahahah"
            #print current_state
            time.sleep(0.01)
            '''
            if current_state in self.end_states:
                break
            '''
            if not self.q.empty():
                e = self.q.get()
                print e.type
                for c in self.states:
                    #check if the current event matches and the input matches
                    if c[0] == current_state and c[1] == e.type:
                        #print "It works"
                        c[2]()  # invoke callback function
                        #print "It works again"
                        current_state = c[3]    # next state
                        break   # get out of inner for-loop
        return

################################
# Hamster control
################################
class RobotBehavior(object):
    def __init__(self, robot_list):
        self.done = False   # set by GUI button
        self.go = False     # set by GUI button
        self.robot_list = robot_list
        self.robot = None
        self.q2 = Queue.Queue() # event queue for FSM
        self.spawn_threads()
        return

    def event_watcher(self, q):
        '''
        while True:
            print self.go
            time.sleep(0.02)
        '''

        count = 0
        while True:
            if self.done:
                return

            #print "hhhhhhhhhhhhhhh "
            if self.robot_list and self.go:
                self.robot = self.robot_list[0]
                
                ###########################################################
                # Implement event producer here. The events are obstacle on left, right or no obstacle. Design your
                # logic for what event gets created based on sensor readings.
                ###########################################################
                #print('inside event watcher loop')

                prox_l = self.robot.get_proximity(0)
                prox_r = self.robot.get_proximity(1)
                line_l = self.robot.get_floor(0)
                line_r = self.robot.get_floor(1)

                if (prox_l > 36 or prox_r > 36):
                    if prox_l > prox_r:
                        obs_event = Event("obsLeft", [prox_l, prox_r])
                        self.q2.put(obs_event)
                    else:
                        obs_event = Event("obsRight", [prox_l, prox_r])
                        self.q2.put(obs_event)
                else:
                    # free event is created when robot goes from obstacle to no obstacle
                    #logging.debug("free of obstacle")
                    free_event = Event("free",[])
                    self.q2.put(free_event)  # put event in motion queue
                    count = 0        
            else:
                #print 'waiting ...'
                pass

            time.sleep(0.01)
            
            #return


    def spawn_threads(self):
        ###########################################################
        # Two threads are created here.
        # 1. create a watcher thread that reads sensors and registers events: obstacle on left, right or no obstacle. This
        #   thread runs the method event_watcher() you are going to implement below.
        # 2. Instantiate StateMachine and populate it with avoidance states, triggers, etc. Set start state.
        # 3. Create a thread to run FSM engine.
        ########################################################### 
        watcher_thread = threading.Thread(name = "watcher", target = self.event_watcher, args = (self.q2,))
        watcher_thread.setDaemon(True)
        watcher_thread.start()

        sm = StateMachine("avoidance", self.q2, self)

        sm.add_state("TurningLeft", "obsLeft", self.turning_left, "TurningLeft")
        sm.add_state("TurningLeft", "free", self.moving_forward, "GoingForward")
        sm.add_state("TurningRight", "obsRight", self.turning_right, "TurningRight")
        sm.add_state("TurningRight", "free", self.moving_forward, "GoingForward")
        sm.add_state("GoingForward", "obsLeft", self.turning_right, "TurningRight")
        sm.add_state("GoingForward", "obsRight", self.turning_left, "TurningLeft")
        sm.add_state("GoingForward", "free", self.moving_forward, "GoingForward")

        sm.set_start_state("GoingForward")

        sm_thread = threading.Thread(name = "sm_thread", target = sm.run)
        sm_thread.setDaemon(True)
        sm_thread.start()

    #######################################
    # Implement Hamster movements to avoid obstacle
    #######################################
    def turning_left(self):
        if self.go and self.robot_list:
        self.robot = self.robot_list[0]
        self.robot.set_wheel(0, -10)
        self.robot.set_wheel(1, 35)

    def turning_right(self):
        if self.go and self.robot_list:
        self.robot = self.robot_list[0]
        self.robot.set_wheel(0, 35)
        self.robot.set_wheel(1, -10)

    def moving_forward(self):
        if self.go and self.robot_list:
        self.robot = self.robot_list[0]
        self.robot.set_wheel(0, 35)
        self.robot.set_wheel(1, 35)
          
class GUI(object):
    def __init__(self, root, robot_control):
        self.root = root
        self.robot_control = robot_control
        
        canvas = tk.Canvas(root, bg="white", width=300, height=250)
        canvas.pack(expand=1, fill='both')
        canvas.create_rectangle(175, 175, 125, 125, fill="green")

        b1 = tk.Button(root, text='Go')
        b1.pack()
        b1.bind('<Button-1>', self.startProg)

        b2 = tk.Button(root, text='Exit')
        b2.pack()
        b2.bind('<Button-1>', self.stopProg)
        return
    
    def startProg(self, event=None):
        self.robot_control.go = True
        return

    def stopProg(self, event=None):
        self.robot_control.done = True      
        self.root.quit()    # close window
        return

def main():
    gMaxRobotNum = 1 # max number of robots to control
    comm = RobotComm(gMaxRobotNum)
    comm.start()
    print 'Bluetooth starts'

    robot_list = comm.robotList
    behaviors = RobotBehavior(robot_list)

    frame = tk.Tk()
    GUI(frame, behaviors)
    frame.mainloop()

    comm.stop()
    comm.join()
    return

if __name__ == "__main__":
    sys.exit(main())