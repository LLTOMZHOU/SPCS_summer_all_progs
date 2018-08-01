import Tkinter as tk
import time


lbl = None

def sayHello(event):
	global lbl
	print type(lbl)
	lbl.config(text = "Oh! Hi")
	
count = 0
def changeLine(theCanvas, theLine):
	global count
	count += 1

	if count % 2 == 1:
		theCanvas.coords(theLine, 0, 0, 50, 50)
	else:
		print count
		theCanvas.coords(theLine, 10, 10, 100, 80)

	theCanvas.after(600, changeLine, theCanvas, theLine)


def main():
	rootWin = tk.Tk()
	rootWin.geometry("550x300")
	rootWin.title("tk_test")

	labelOne = tk.Label(rootWin, text = "Oh!")
	labelOne.pack(side = "top")
	global lbl
	#lbl = labelOne
	lbl = labelOne

	b1 = tk.Button(rootWin, text = "This is a Button")
	b1.bind("<Button-1>", sayHello)
	b1.pack(side = "bottom")
	
	c = tk.Canvas(rootWin, bg = "gold")
	c.pack()

	line = c.create_line(0, 0, 50, 50, fill = "black")
	#print type(line) #line is of type "int", it's a handle
	changeLine(c, line)
	
	rootWin.mainloop()

if __name__ == "__main__":
	main()

	'''
b.bind("<Key>", command)
self.wwwwwwwwroot.bind("<KeyReleased>", command)

def command(event):
	event.char == "w" or "asdasdwwww"
	'''