import tkinter
import numpy as np
import random
import time
import enum
from _Getch import *


class GridWorldUI():
	# Simulation CONSTANTS
	WINDOW_HEIGHT = 900
	WINDOW_WIDTH = 1200
	WINDOW_MARGIN = 30
	UI_MARGIN_1 = 200
	UI_MARGIN_2 = 80
	BACKGROUND_COLOR = 'black'
	MAP_COLOR = 'white'
	GRID_COLOR = 'black'
	AGENT_COLOR = 'black'
	UI_TEXT_COLOR = 'white'


	def __init__(self, x1_max, x2_max):
		
		## Create a canvas
		self.canvas = tkinter.Canvas(
			bg = self.BACKGROUND_COLOR, 
			height = self.WINDOW_HEIGHT + self.UI_MARGIN_2, 
			width = self.WINDOW_WIDTH+ self.UI_MARGIN_1
		)
		self.canvas.pack()
		self.canvas.create_rectangle(
			self.WINDOW_MARGIN, self.WINDOW_MARGIN, 
			self.WINDOW_WIDTH - self.WINDOW_MARGIN, 
			self.WINDOW_HEIGHT-self.WINDOW_MARGIN, 
			fill = self.MAP_COLOR
		)
		
		# Draw the grids
		self.x1_interval = (self.WINDOW_WIDTH - 2 * self.WINDOW_MARGIN) / x1_max
		self.x2_interval = (self.WINDOW_HEIGHT - 2 * self.WINDOW_MARGIN) / x2_max
		
		for i in range(x1_max + 1): # Columns
			self.canvas.create_line(
				self.WINDOW_MARGIN + i * self.x1_interval, self.WINDOW_MARGIN,
				self.WINDOW_MARGIN + i * self.x1_interval, self.WINDOW_HEIGHT - self.WINDOW_MARGIN,
				fill = self.GRID_COLOR, width = 2
			)
		for i in range(x2_max + 1):	# Rows
			self.canvas.create_line(
				self.WINDOW_MARGIN, self.WINDOW_MARGIN + i * self.x2_interval,
				self.WINDOW_WIDTH - self.WINDOW_MARGIN, self.WINDOW_MARGIN + i * self.x2_interval,
				fill = self.GRID_COLOR, width = 2
			)


		# Create UI elements
		self.water = self.canvas.create_text(
			self.WINDOW_WIDTH / 4,
			self.WINDOW_HEIGHT,
			text = 'Water: ', font = "Roboto 30",
			fill = self.UI_TEXT_COLOR)
		self.food = self.canvas.create_text(
			self.WINDOW_WIDTH / 4 * 3,
			self.WINDOW_HEIGHT,
			text = 'Food: ',  font = "Roboto 30",
			fill = self.UI_TEXT_COLOR)

		self.canvas.update()

	def spawn_agent(self, x_1, x_2):
		return self.canvas.create_rectangle(
			self.WINDOW_MARGIN + (float(x_1) + 0.25) * self.x1_interval, 
			self.WINDOW_MARGIN + (float(x_2) + 0.25) * self.x2_interval,
			self.WINDOW_MARGIN + (float(x_1) + 0.75) * self.x1_interval, 
			self.WINDOW_MARGIN + (float(x_2) + 0.75) * self.x2_interval,
			fill = self.AGENT_COLOR
		)

	def move_agent(self, direction):
		if direction == 'w':
			self.canvas.move(self.agent, 0, -self.x2_interval)
		elif direction == 'a':
			self.canvas.move(self.agent, -self.x1_interval, 0)
		elif direction == 's':
			self.canvas.move(self.agent, 0, self.x2_interval)
		elif direction == 'd':
			self.canvas.move(self.agent, self.x1_interval, 0)
		elif direction == ' ':
			pass
		elif direction == 't':
			return 1
		else:
			print('wrong input')
		self.canvas.update()

	def update_resource(self, water, food):
		self.canvas.itemconfig(self.water, text = 'Water: ' + str(water) + '.')
		self.canvas.itemconfig(self.food, text = 'Food: ' + str(food) + '.')
		self.canvas.update()

	

	




	
	def test(self):
		x1_new = input("starting x1:")
		x2_new = input("starting x2:")
		self.agent = self.spawn_agent(x1_new,x2_new)
		self.canvas.update()
		
		while True:
			water = input("update water")
			food  = input ("update food")

			self.update_resource(water, food)
			
			direction = getch()
			status = self.move_agent(direction)
			if(status):
				break
			
	




gw = GridWorldUI(100,80)
gw.test()
