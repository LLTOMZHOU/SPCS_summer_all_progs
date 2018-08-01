'''
/* =======================================================================
   (c) 2015, Kre8 Technology, Inc.
   This is a program that is provided to students in Robot AI class.
   Students use this it to build different Hamster behaviors.

   Name:          tk_behaviors_starter.py
   By:            Qin Chen
   Last Updated:  5/10/18

   PROPRIETARY and CONFIDENTIAL
   ========================================================================*/
'''
import sys
import time
import threading
import Tkinter as tk
from comm_ble import RobotComm	# no dongle
#from HamsterAPI.comm_usb import RobotComm	# yes dongle

################################
# Hamster control
################################
class RobotBehaviorThread(threading.Thread):
	def __init__(self, robotList):
		super(RobotBehaviorThread, self).__init__()
		self.go = False
		self.done = False
		self.square_var = False
		self.follow_var = False
		self.shy_var = False
		self.line_follow_var = False
		self.robotList = robotList
		return

	def run(self):  #Something calls the method called exactly 'run', so this name can't be changed
		robot=None
		while not self.done:
			for robot in self.robotList:
				#print('go', self.go, 'square', self.square_var)
				if robot:
					if self.square_var:
						#print "asdfasdfad"
						#self.done = False
						self.square()
					elif self.follow_var:
						self.follow()
					elif self.line_follow_var:
						self.line_follow()
					elif self.shy_var:
						self.shy()

					#############################################
					# START OF YOUR WORKING AREA!!!
					#############################################

					#############################################
					# END OF YOUR WORKING AREA!!!
					#############################################					
		# stop robot activities, such as motion, LEDs and sound
		# clean up after exit button pressed
		if robot:
			robot.reset()
			time.sleep(0.1)
		return

	def square(self):
		print "This is something"
		robot = None
		while not self.done:
			for robot in self.robotList:
				if robot:
					robot.set_wheel(0, 30)
					robot.set_wheel(1, 30)
					time.sleep(2)
					robot.set_wheel(0, 0)
					time.sleep(1.6)
					robot.set_wheel(0, 30)
					robot.set_wheel(1, 30)
					time.sleep(2)
					robot.set_wheel(0, 0)
					time.sleep(1.6)
					robot.set_wheel(0, 30)
					robot.set_wheel(1, 30)
					time.sleep(2)
					robot.set_wheel(0, 0)
					time.sleep(1.6)
					robot.set_wheel(0, 30)
					robot.set_wheel(1, 30)
					time.sleep(2)
					robot.set_wheel(0, 0)
					time.sleep(1.6)

	def doNothing(self):
		return 

	def shy(self):
		robot = None
		while not self.done:
			for robot in self.robotList:
				if robot:
					robot.set_wheel(0, 40)
					robot.set_wheel(1, 40)
					while not self.done:  #is it useful
						robot.set_wheel(0, 40)
						robot.set_wheel(1, 40)
						if robot.get_proximity(1) > 30 or robot.get_proximity(0) > 30:
							robot.set_wheel(0, -30)
							robot.set_wheel(1, -30)
							time.sleep(0.2)

	def follow(self):
		robot = None
		while not self.done:
			for robot in self.robotList:
				if robot:
					while not self.done:
						robot.set_wheel(0, 30)
						robot.set_wheel(1, 30)
						if robot.get_proximity(0) > 50 or robot.get_proximity(1) > 50:
							robot.set_wheel(0, 0)
							robot.set_wheel(1, 0)
							time.sleep(0.17)
						if robot.get_proximity(0) > 10 or robot.get_proximity(1) > 10:
							if robot.get_proximity(0) - robot.get_proximity(1) > 3:
								robot.set_wheel(0, 12)
								robot.set_wheel(1, 40)
								time.sleep(0.1) 
							if robot.get_proximity(1) - robot.get_proximity(0) > 3:
								robot.set_wheel(1, 12)
								robot.set_wheel(0, 40)
								time.sleep(0.1)


	def line_follow(self):
		robot = None
		while not self.done:
			for robot in self.robotList:
				if robot:
					robot.set_wheel(0, 30)
					robot.set_wheel(1, 30)
					if robot.get_floor(0) - robot.get_floor(1) > 20:
						robot.set_wheel(0,60)
						robot.set_wheel(1,5)
						time.sleep(0.06)
						robot.set_wheel(0, 30)
						robot.set_wheel(1, 30)
					elif robot.get_floor(1) - robot.get_floor(0) > 20:
						robot.set_wheel(1,60)
						robot.set_wheel(0,5)
						time.sleep(0.06)
						robot.set_wheel(0, 30)
						robot.set_wheel(1, 30)



					



class GUI(object):
	#GUI(frame, behaviors)
	def __init__(self, root, robot_control):#robot_control is behaviors
		self.root = root
		self.robot_control = robot_control
		root.geometry('400x30')
		root.title('Hamster Control')

		b1 = tk.Button(root, text='Go')
		b1.pack(side='left')
		b1.bind('<Button-1>', self.startProg)

		b2 = tk.Button(root, text='Exit')
		b2.pack(side='left')
		b2.bind('<Button-1>', self.stopProg)

		b3 = tk.Button(root, text = "Square")
		b3.pack(side = "left")
		b3.bind('<Button-1>', self.square)

		b4 = tk.Button(root, text = "Follow")
		b4.pack(side = "left")
		b4.bind('<Button-1>', self.follow)

		b5 = tk.Button(root, text = "Shy")
		b5.pack(side = "left")
		b5.bind('<Button-1>', self.shy)

		b6 = tk.Button(root, text = "Line_follow")
		b6.pack(side = "left")
		b6.bind('<Button-1>', self.line_follow)
		return

	def startProg(self, event=None):
		self.robot_control.go = True
		return

	def stopProg(self, event=None):
		self.robot_control.done = True		
		self.root.quit() 	# close window
		return

	def square(self, event = None):
		self.robot_control.square_var = True
		return

	def follow(self, event = None):
		self.robot_control.follow_var = True
		return

	def shy(self, event = None):
		self.robot_control.shy_var = True
		return

	def line_follow(self, event = None):
		self.robot_control.line_follow_var = True
		return
#################################
# Don't change any code below!! #
#################################

def main():
    # instantiate COMM object
    gMaxRobotNum = 1; # max number of robots to control
    comm = RobotComm(gMaxRobotNum)
    comm.start()
    print 'Bluetooth starts'  
    robotList = comm.robotList

    #print robotList
    behaviors = RobotBehaviorThread(robotList)
    behaviors.start()#The robotbehaviorthread extends thread class, so it has 'start' method

    frame = tk.Tk()
    GUI(frame, behaviors)
    frame.mainloop()

    comm.stop()
    comm.join()
    print("terminated!")

if __name__ == "__main__":
    sys.exit(main())


