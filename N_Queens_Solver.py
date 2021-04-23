import sys, os
import subprocess
import tkinter as tk

from math import ceil
from N_Queens_GUI import displayGUI, displayNonGUI, resetGUI
from tkinter import *

# GUI Input
root= tk.Tk()

root.minsize(250,200)

canvas1 = tk.Canvas(root,  relief = 'raised')
canvas1.pack()


label1 = tk.Label(root, text='N Queens Problem Solver')
label1.config(font=('helvetica', 14))
canvas1.create_window(200, 25, window=label1)

label2 = tk.Label(root, text='Enter your chessboard size (>= 4):')
label2.config(font=('helvetica', 10))
canvas1.create_window(200, 100, window=label2)

entry1 = tk.Entry (root) 
canvas1.create_window(200, 140, window=entry1)


presented = False
inputFile = open("input.cnf", mode='w')
clausesCounter = 0

def initState():
	global clausesCounter
	open('input.cnf', 'w').close()
	clausesCounter=0

def main():
	global inputFile
	global presented
	
	initState()
	inputFile = open("input.cnf", mode='w')

	N = int(entry1.get())

	label3 = tk.Label(root, fg='red', text="UNSATISFIABLE, Can't create chess board with "+ str(N)+"x"+str(N)+" size")
	label3.config(font=('helvetica', 10))

	if (N < 4):
		label3.pack()

	label3.after(5000 , lambda: label3.destroy())

	numOfTile = N*N
	prepareSATFiles(N, numOfTile)
                
	if N <= 12:
		if(presented == True):
			presented = False
			resetGUI(N)

		else:
			presented = True
			displayGUI(N)
			
	else:
		displayNonGUI(N)

		label4 = tk.Label(root, fg='red', text="Chess board too large, answer is printed on the terminal interface")
		label4.config(font=('helvetica', 10))
		label4.pack()
		label4.after(10000 , lambda: label4.destroy())


def replaceCNFHeader(string):
	with open("input.cnf",'r') as readInputFile:
		get_all_lines=readInputFile.readlines()
	with open("input.cnf",'w') as writeInputFile:
		for i,line in enumerate(get_all_lines,1): 
			if i == 1:                             
				writeInputFile.writelines(string)
			else:
				writeInputFile.writelines(line)

#generate clauses
def prepareSATFiles(N, numOfTile):

	global inputFile
	global clausesCounter

	inputFile.write("p cnf {0:d} {1:d}\n".format((N * N), int(clausesCounter)))
	
	
	genBaseConstraints(N, numOfTile)  #generate NxN chess board base constraints
	genRowConstraints(N, numOfTile)   #generate NxN chess board row constraints
	genColumnConstraints(N, numOfTile)   #generate NxN chess board column constraints
	genUpperBoundDiagonalConstraints(N, numOfTile) #generate NxN chess board upper bound diagonal constraints
	genLowerBoundDiagonalConstraints(N, numOfTile) #generate NxN chess board lower bound diagonal constraints
	inputFile.close()


	CNFHeaderUpdated = "p cnf {0:d} {1:d}\n".format((N * N), int(clausesCounter))
	replaceCNFHeader(CNFHeaderUpdated)
	inputFile.close()

	subprocess.run(['C:/cygwin/bin/minisat', "input.cnf", "solution.sol"], stdout=subprocess.PIPE)

def genBaseConstraints(N, numOfTile):

	global inputFile
	global clausesCounter


	for i in range(1, numOfTile+1):
		inputFile.write("{0:d} ".format(i))
		if i % N == 0:
			inputFile.write("0\n")
			clausesCounter+=1

def genRowConstraints(N, numOfTile):

	global inputFile
	global clausesCounter

	for i in range(1, numOfTile+1):
		row = ceil(i / N)

		# print constraints to CNF file
		for j in range(i, row*N + 1):
			if j == i:
				continue
			inputFile.write("-{0:d} -{1:d} 0\n".format(i, j))
			clausesCounter+=1


def genColumnConstraints(N, numOfTile):

	global inputFile
	global clausesCounter

	for i in range(1, numOfTile+1):
		# print constraints to CNF file
		for j in range(i, numOfTile+1, N):
			if j == i:
				continue
			inputFile.write("-{0:d} -{1:d} 0\n".format(i, j))
			clausesCounter+=1


def genUpperBoundDiagonalConstraints(N, numOfTile):

	global inputFile
	global clausesCounter


	for i in range(1, numOfTile+1):
		
		row = ceil(i / N)
		col = i % N

		if col == 0: col = N

		# print constraints to CNF filees
		for j in range(i, min(((N - col + row) * N + 1), numOfTile+1), N + 1):
			if j == i:
				continue
			inputFile.write("-{0:d} -{1:d} 0\n".format(i, j))
			clausesCounter+=1


def genLowerBoundDiagonalConstraints(N, numOfTile):
	
	global inputFile
	global clausesCounter

	for i in range(1, numOfTile+1):
		# print constraints to CNF filees
		for j in range(i, numOfTile+1, N - 1):
			if j == i: 
				continue
			elif ceil((j - (N - 1)) / N) == ceil(j / N):
				break
			inputFile.write("-{0:d} -{1:d} 0\n".format(i, j))
			clausesCounter+=1

button1 = tk.Button(canvas1, text='Get Solution', command=main, bg='teal', fg='white', font=('helvetica', 9, 'bold'))
canvas1.create_window(200, 180, window=button1)

root.mainloop()