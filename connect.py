import numpy as np
import pygame as py
import sys
import math
import random

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1


BLUE = (50, 50, 200)
BLACK = (0, 0, 0)
RED = (250, 50, 50)
YELLOW = (200, 200, 0)

def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board


def drop_piece(board, row, col, piece):
	board[row][col] = piece


def is_valid_location(board, col):
	return board[ROW_COUNT - 1][col] == 0



def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

def print_board(board):
	print(np.flip(board, 0))

def winning_move(board, piece):
	#check for horizontal location for the win
	for c in range(COLUMN_COUNT - 3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece :
				return True
	#check for vertical position
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT - 3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece :
				return True

	#check positively sloped diagonal
	for c in range(COLUMN_COUNT - 3):
		for r in range(ROW_COUNT - 3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece :
				return True
	#check for negatively sloped position
	for c in range(COLUMN_COUNT - 4,COLUMN_COUNT):
		for r in range(ROW_COUNT - 3):
			if board[r][c] == piece and board[r+1][c-1] == piece and board[r+2][c-2] == piece and board[r+3][c-3] == piece :
				return True

def draw_board(board):
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			py.draw.rect(screen, BLUE, (c*SQUARESIZE, (r+1)*SQUARESIZE, SQUARESIZE, SQUARESIZE))
			py.draw.circle(screen, BLACK, (int(c*SQUARESIZE + SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			if board[r][c] == 1:
				py.draw.circle(screen, RED, (int(c*SQUARESIZE + SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == 2:
				py.draw.circle(screen, YELLOW, (int(c*SQUARESIZE + SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	py.display.update()		

turn = random.randint(PLAYER, AI)
board = create_board()
print_board(board)
game_over = False

py.init()

SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)
RADIUS = int(SQUARESIZE/2 - 5)

screen = py.display.set_mode(size)
draw_board(board)
py.display.update()

myfont = py.font.SysFont("monospace", 75)

while not game_over :

	for event in py.event.get():
		if event.type == py.QUIT:
			sys.exit()
		if event.type == py.MOUSEMOTION:
			py.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			posx = event.pos[0]
			if turn == PLAYER:
				py.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
			# else:
			# 	py.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
			py.display.update()


		if event.type == py.MOUSEBUTTONDOWN:
			py.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			#Ask for player 1
			if turn == PLAYER:
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))
				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, 1)

					if winning_move(board, 1):
						lable = myfont.render("Player 1 Won", 1, RED)
						screen.blit(lable, (40,10))
						game_over = True

					turn += 1
					turn = turn%2
					print_board(board)
					draw_board(board)
	

			#Ask player 2 turn
	if turn == AI and not game_over:
		# posx = event.pos[0]
		# col = int(math.floor(posx/SQUARESIZE))
		col = random.randint(0, COLUMN_COUNT - 1)
		if is_valid_location(board, col):
			py.time.wait(100)
			row = get_next_open_row(board, col)
			drop_piece(board, row, col, 2)

			if winning_move(board, 2):
				lable = myfont.render("Player 2 Won", 1, YELLOW)
				screen.blit(lable, (40,10))
				game_over = True


	

			print_board(board)
			draw_board(board)

			turn += 1
			turn = turn%2

	if game_over:
		py.time.wait(3000)