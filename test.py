'''
This is a test file for discovering more uses of Tkinter
'''

import Tkinter as tk
import Queue as que
import time
######Part ONE########

Event_Queue = que.Queue()

def display(root, lbl):

	global Event_Queue
	if not Event_Queue.empty():
		event = Event_Queue.get()
		lbl.config(text = event.char, fg = "green")

	lbl.after(70, display, root, lbl)


def key_down(event):
	global Event_Queue
	Event_Queue.put(event)
	print event.char

def key_up(event):
	#print event.char #in python or MAC OS input, when a key is being pressed for a long time, it's seen as being constantly hit
	pass
def main():
	rootWin = tk.Tk()

	rootWin.geometry("200x50")
	rootWin.title("test")

	rootWin.bind("<Key>", key_down)
	rootWin.bind("<KeyRelease>", key_up)

	label = tk.Label(rootWin, text = "Currently no key is pressed", fg = "red", bg = "blue")
	label.pack(side = "top")

	#print "hahahahh"
	display(rootWin, label)
	rootWin.mainloop()


if __name__ == "__main__":
	main()