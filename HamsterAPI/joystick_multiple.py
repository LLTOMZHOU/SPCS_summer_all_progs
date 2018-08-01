'''
/* =======================================================================
   (c) 2015, Kre8 Technology, Inc.

   Name:          Joystick for Hamster
   By:            Qin Chen
   Last Updated:  5/10/18

   PROPRIETARY and CONFIDENTIAL
   ========================================================================*/
'''
import sys
import Tkinter as tk
from comm_ble import RobotComm
#for PC, need to import from commm_usb

class Robots(object):
    def __init__(self, robotList):
        self.robotList = robotList
        #print self.robotList
        return

    def move_forward(self, event=None):
        if self.robotList:
            for robot in self.robotList:
                robot.set_wheel(0,50)
                robot.set_wheel(1,50)
        else:
            print "waiting for robot"

    def move_backward(self, event=None):
        if self.robotList:
            for robot in self.robotList:
                robot.set_wheel(0,-30)
                robot.set_wheel(1,-30)
        else:
            print "waiting for robot"

    def move_left(self, event=None, count):
        theCount = 0
        if self.robotList:
            for robot in self.robotList:
                if theCount == count:
                    robot.set_wheel(0, 0)
                    robot.set_wheel(1, 50)
                theCount += 1
        else:
                print "waiting for robot"

    def move_right(self, event=None, count):
        theCount = 0
        if self.robotList:
            for robot in self.robotList:
                if theCount == count:
                    robot.set_wheel(0, 0)
                    robot.set_wheel(1, 50)
                theCount += 1
        else:
                print "waiting for robot"

    def get_prox(self, left, count):
        #print "the get_prox is running"
        theCount = 0
        if self.robotList:
            for robot in self.robotList: # Single return values
                if theCount == count
                    if left:
                        return int(robot.get_proximity(0)) # The function just ends here 
                    else:
                        return int(robot.get_proximity(1)) # Or here
                theCount += 1

    def get_floor(self, left, count):
        theCount = 0
        if self.robotList:
            for robot in self.robotList: # Single return values
                if theCount == count
                    if left:
                        return int(robot.get_floor(0)) # The function just ends here 
                    else:
                        return int(robot.get_floor(1)) # Or here
                theCount += 1

    def stop_move(self, event=None, count):
        theCount = 0
        if self.robotList:
            for robot in self.robotList:
                if theCount == count:
                    robot.set_wheel(0, 0)
                    robot.set_wheel(1, 0)
                theCount += 1

    def reset_robot(self, event=None): # use Hamster API reset()
        if self.robotList:
            for robot in self.robotList:
                robot.reset()

class UI(object):
    #The UI accesses the robot_control API through calling the methods that are in robot_handle(instance of Robots CLS)
    def __init__(self, root, robot_handle):#gui = UI(m, robot_handle)  robot_handle = Robots(robotList)
        self.root = root #root is the main window created in the 'main' function
        self.robot_handle = robot_handle  # handle to robot commands
        self.canvas = None
        self.prox_l_id = None
        self.prox_r_id = None
        self.floor_l_id = None
        self.floor_r_id = None
        self.initUI()
        return

    def initUI(self):
        ###################################################################
        # Create a Hamster joystick window which contains
        # 1. a canvas widget where "sensor readings" are displayed
        # 2. a square representing Hamster
        # 3. 4 canvas items to display floor sensors and prox sensors
        # 4. a button for exit, i.e., a call to stopProg(), given in this class
        # 5. listen to key press and key release when focus is on this window
        ###################################################################
        self.root.geometry("400x550")
        self.root.title("Joystick")

        cc = tk.Canvas(self.root, bg = "green", width = 400, height = 520)
        cc.pack(side = "top")

        hamsterIcon = cc.create_rectangle(130, 260, 270, 400, fill = "blue", width = 3.6)

        self.lineLeft = cc.create_line(170, 260, 170, 260, width = 3)
        self.lineRight = cc.create_line(230, 260, 230, 260, width = 3)
        self.leftDect = cc.create_rectangle(150, 375, 190, 400, fill = "black", width = 3.6)
        self.rightDect = cc.create_rectangle(210, 375, 250, 400, fill = "black", width = 3.6)

        bb = tk.Button(self.root, text = "Exit")
        bb.bind("<Button-1>", self.stopProg)
        bb.pack(side = "bottom")
        
        ##For each widget, you can bind Python functions and methods to events.
        self.root.bind("<Key>", self.keydown)
        self.root.bind("<KeyRelease>", self.keyup)

        self.display_sensor(cc, 0)
        ##For each widget, you can bind Python functions and methods to events.

        #while True:
        #for i in range(1000):
            #print "hahahahahaha"



    
    ######################################################
    # This function refreshes floor and prox sensor display every 100 milliseconds.
    # Register callback using Tkinter's after method().
    ######################################################
    def display_sensor(self, cc, count): ##cc ==> canvas

        lbl = ""
        if not self.robot_handle.robotList:
            lbl = tk.Label(self.root, text = "No robots found...", fg = "red", bg = "black")
            lbl.pack(side = "top")
            cc.after(90, self.display_sensor, (cc))
            return

        self.prox_l_id = self.robot_handle.get_prox(True, count)
        self.prox_r_id = self.robot_handle.get_prox(False, count)
        self.floor_l_id = self.robot_handle.get_floor(True, count)
        self.floor_r_id = self.robot_handle.get_floor(False, count)

        lp = self.prox_l_id
        rp = self.prox_r_id

        #print type(lp)
        ###line = cc.create_line(10,10,50,30, width = 3)

        cc.coords(self.lineLeft, 170, 260, 170, 260-lp*2.5)
        cc.coords(self.lineRight, 230, 260, 230, 260-rp*2.5)

        cc.itemconfig(self.rightDect, fill = "black")
        cc.itemconfig(self.leftDect, fill = "black")

        if self.floor_r_id >40:
            cc.itemconfig(self.rightDect, fill = "white")
        if self.floor_l_id >40:
            cc.itemconfig(self.leftDect, fill = "white")

        cc.after(90, self.display_sensor, (cc))



    ####################################################
    # Implement callback function when key press is detected
    ####################################################
    def keydown(self, event):
        if event.char == "w":
            self.robot_handle.move_forward(0)
        elif event.char == "a":
            self.robot_handle.move_left(0)
        elif event.char == "s":
            self.robot_handle.move_backward(0)
        elif event.char == "d":
            self.robot_handle.move_right(0)
        elif event.char == 



    #####################################################
    # Implement callback function when key release is detected
    #####################################################
    def keyup(self, event):
        self.robot_handle.stop_move()
        

    def stopProg(self, event=None):
        self.root.quit()    # close window
        self.robot_handle.reset_robot()
        return
    

def main(argv=None):
    gMaxRobotNum = 2 # max number of robots to control
    comm = RobotComm(gMaxRobotNum)
    comm.start()

    #The comm thread is actively searching for connections
    print 'Bluetooth starts'
    robotList = comm.robotList

    #print robotList
    robot_handle = Robots(robotList)
    #print type(robotList)

    m = tk.Tk() #root
    gui = UI(m, robot_handle)

    m.mainloop()

    comm.stop()
    comm.join()

if __name__ == "__main__":
    sys.exit(main())