import Tkinter as tk

counter = 0

def counterLabel(thelabel):
	global counter
	counter += 1
	thelabel.config(text = str(counter))
	thelabel.after(1000, counterLabel, (thelabel))

def main():
	rootWin = tk.Tk()
	rootWin.geometry("200x100")
	rootWin.title("Counting seconds")

	label = tk.Label(rootWin, fg = "light green", bg = "dark green")
	label.pack()

	print "hhhh"
	counterLabel(label)
	rootWin.mainloop()

main()
