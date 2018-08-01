##### The basic idea is Breath First Search
#### BTW, it's pretty fun, not very easy

import Queue as que


class Board():
	def __init__(self):
		self.black = False
		self.group = None
		self.searched = False

num = [-100000]
MAX_NUM = 101
n = MAX_NUM


def BFS(qqq, dx, dy, theBoard):
	if qqq.empty():
		return

	global num
	tmp = qqq.get() # tmp thus should be a list with [count, i, j]
	
	num[tmp[0]] += 1 #record that the area of the current group(count) is added by one
	
	print str(tmp[1])+str(tmp[2])
	print tmp[0]
	print " "

	theBoard[tmp[1]][tmp[2]].searched = True
	for i in range(8):
		if dx[i] + tmp[1] > 0 and dx[i] + tmp[1] < n and dy[i] + tmp[2] > 0 and dy[i] + tmp[2] < n:
		#if the 8 areas around the starting point is black, without 0 g exceeding it
			if theBoard[dx[i] + tmp[1]][dy[i] + tmp[2]].black and not theBoard[dx[i] + tmp[1]][dy[i] + tmp[2]].searched:
				qqq.put([tmp[0], dx[i] + tmp[1], dy[i] + tmp[2]])
				theBoard[dx[i] + tmp[1]][dy[i] + tmp[2]].searched = True

	BFS(qqq, dx, dy, theBoard)




def main():
	#assume the board is a 100 x 100 SQUARe
	count = 0
	# a type of GAO DUAN CAO ZUO, go to google for more info
	dx = (1, 0, -1, -1, -1, 0, 1, 1)
	dy = (1, 1, 1, 0, -1, -1, -1, 0)

	#set the initial values of the board all to -1
	aaa = [[-1 for x in range(MAX_NUM)] for y in range(MAX_NUM)]

	n = input("Input the dimensions of the square board: ")
	
	#init the board data
	for i in range(MAX_NUM):
		for j in range(MAX_NUM):
			tmp = Board()
			aaa[i][j] = tmp

	#inputting the board data
	for i in range(1, n+1):
		for j in range(1, n+1):
			nnn = input()
			nnn = int(nnn)
			tmp = Board()
			if nnn == 1:
				tmp.black = True
			else:
				tmp.black = False
			aaa[i][j] = tmp
	'''
	for i in range(n+2):
		for j in range(n+2):
			print aaa[i][j].black
	'''

	#building and maintaining a queue for BFS
	#Notice that this queue is First In First Out
	qqq = que.Queue() #que.Queue is a class in the module 'que', and qqq is an instance of the class

	#an array(list) used to record how many area every group(each with different 'count') has
	

	for i in range(1, n+1):
		for j in range(1, n+1):
			tmp = aaa[i][j] #tmp stores the value of aaa[i][j]
			if not tmp.black:
				continue
			elif tmp.group == None:
				count += 1
				global num
				num.append(0) #Now the group one has zero area, the area will be counted afterwards in BFS()
				qqq.put([count, i, j])#record its coordinates for the BFS
				BFS(qqq, dx, dy, aaa) # aaa ==> theBoard
			else:
				continue

	max_area = -1000000
	for i in range(1, len(num)):
		if num[i] > max_area:
			max_area = num[i]

	print "The maximum area is " + str(max_area)


if __name__ == "__main__":
	main()