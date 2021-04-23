import tkinter as tk
from tkinter import *

master = tk.Tk()
master.title("N Queens Problem Solver with Minisat")

lightTile = 'white'
darkTile = 'black'

dummyImg = tk.PhotoImage()
queenIcon = tk.PhotoImage(file='images/pion_queen.png')
unicorn = tk.PhotoImage(file='images/unicorn_jose_32.png')

master.tk.call('wm', 'iconphoto', master._w, queenIcon)

def resetGUI():
	master.withdraw()
	master.deiconify()

def displayGUI(N):

	with open('solution.sol', mode='r') as f:
		content = f.read().splitlines()
		
	f.close()

	solved = content[0]

	if solved=='UNSAT':
		print("This problem is unsolvable for N = %d" %N)
		return
		
	result = content[1].split()

	rowNum = -1
	columnNum = 0

	tileColor = lightTile

	for i in range(N*N):

		if (i%N) == 0:
			rowNum += 1
			columnNum = 0
			
			if (N%2) == 0:
                                if (tileColor == darkTile):
                                        tileColor = lightTile
                                else:
                                        tileColor = darkTile

		tileNum = int(result[i])

		if tileNum < 0:
			tk.Label(master, bg=tileColor, image=dummyImg, width=64, height=64, compound='center').grid(row=rowNum,column=columnNum)
		else:
			tk.Label(master, bg=tileColor, image=unicorn, width=64, height=64, compound='center').grid(row=rowNum,column=columnNum)

		columnNum += 1

		if (tileColor == darkTile):
			tileColor = lightTile
		else:
			tileColor = darkTile
	  
	master.mainloop()

def displayNonGUI(N):

	with open('solution.sol', mode='r') as f:
		content = f.read().splitlines()
	f.close()

	solved = content[0]

	if solved=='UNSAT':
		print("This problem is unsolvable for N = %d" %N)
		return

	result = content[1].split()

	rowNum = -1
	columNum = 0

	for i in range(N*N):

		if (i%N) == 0:
			rowNum += 1
			columnNum = 0
			print('')

		tileNum = int(result[i])

		if tileNum < 0:
			print(" _ ", end="")
		else:
			print(" X ", end="")

		columnNum += 1

	print('\n')
