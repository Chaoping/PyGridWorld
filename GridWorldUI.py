import tkinter
import numpy as np
import random
import time
import enum



class GridWorldUI():
	# Simulation CONSTANTS
	WINDOW_HEIGHT = 800
	WINDOW_WIDTH = 1000
	WINDOW_MARGIN = 30
	UI_MARGIN_1 = 200
	UI_MARGIN_2 = 80
	BACKGROUND_COLOR = 'black'
	MAP_COLOR = 'white'
	GRID_COLOR = 'black'
	AGENT_COLOR = 'black'
	UI_TEXT_COLOR = 'white'
	WATER_COLOR = 'blue'
	FOOD_COLOR = 'brown'


	def __init__(self, x1_max, x2_max, agent_x1, agent_x2, agent_sight):
		
		## Create a canvas
		self.canvas = tkinter.Canvas(
			bg = self.BACKGROUND_COLOR, 
			height = self.WINDOW_HEIGHT + self.UI_MARGIN_2, 
			width = self.WINDOW_WIDTH+ self.UI_MARGIN_1
		)
		self.canvas.pack()
		
		# main map
		self.canvas.create_rectangle(
			# top left
			self.WINDOW_MARGIN, 
			self.WINDOW_MARGIN, 
			
			# bottom right
			self.WINDOW_WIDTH - self.WINDOW_MARGIN, 
			self.WINDOW_HEIGHT-self.WINDOW_MARGIN, 
			
			fill = self.MAP_COLOR
		)

		# agent view	
		self.agent_grid_unit = agent_sight * 2 + 1
		self.agent_sight = agent_sight
		self.canvas.create_rectangle(
			self.WINDOW_WIDTH ,
			self.WINDOW_MARGIN,
			self.WINDOW_WIDTH + (self.UI_MARGIN_1 - self.WINDOW_MARGIN),
			self.UI_MARGIN_1,
			fill = self.MAP_COLOR
		)

		'''
			so for the agent view, the width is 
			(self.UI_MARGIN_1 - self.WINDOW_MARGIN)
			and the height is
			(self.UI_MARGIN_1 - self.WINDOW_MARGIN)
		'''

		self.agent_grid_coords = (self.WINDOW_WIDTH,self.WINDOW_MARGIN)
	
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

		# Draw the small grids
		self.agent_x1_interval = (self.UI_MARGIN_1 - self.WINDOW_MARGIN) / (self.agent_grid_unit)
		self.agent_x2_interval = (self.UI_MARGIN_1 - self.WINDOW_MARGIN) / (self.agent_grid_unit)

		for i in range(self.agent_grid_unit + 1): # Columns
			self.canvas.create_line(
				self.WINDOW_WIDTH + i * self.agent_x1_interval, self.WINDOW_MARGIN,
				self.WINDOW_WIDTH + i * self.agent_x1_interval, self.UI_MARGIN_1,
				fill = self.GRID_COLOR, width = 2
			)
		for i in range(self.agent_grid_unit + 1):	# Rows
			self.canvas.create_line(
				self.WINDOW_WIDTH, self.WINDOW_MARGIN + i * self.agent_x2_interval,
				self.WINDOW_WIDTH + (self.UI_MARGIN_1 - self.WINDOW_MARGIN), self.WINDOW_MARGIN + i * self.agent_x2_interval,
				fill = self.GRID_COLOR, width = 2
			)
		
		# container for resource shapes
		self.water_objects = []
		self.food_objects = []

		# container for agent shapes
		self.agent_objects = []


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

		self.spawn_agent(agent_x1,agent_x2)
		self.canvas.update()

	
	def spawn_agent(self, x_2, x_1):
		self.agent = self.canvas.create_rectangle(
			self.WINDOW_MARGIN + (float(x_1) + 0.25) * self.x1_interval, 
			self.WINDOW_MARGIN + (float(x_2) + 0.25) * self.x2_interval,
			self.WINDOW_MARGIN + (float(x_1) + 0.75) * self.x1_interval, 
			self.WINDOW_MARGIN + (float(x_2) + 0.75) * self.x2_interval,
			fill = self.AGENT_COLOR
		)

	def move_agent(self, x_2, x_1):
		self.canvas.coords(
			self.agent, 
			self.WINDOW_MARGIN + (float(x_1) + 0.25) * self.x1_interval, 
			self.WINDOW_MARGIN + (float(x_2) + 0.25) * self.x2_interval,
			self.WINDOW_MARGIN + (float(x_1) + 0.75) * self.x1_interval, 
			self.WINDOW_MARGIN + (float(x_2) + 0.75) * self.x2_interval)

		self.canvas.update()

	# Display the physiology variables under the map
	def update_physiology(self, water, water_max, food, food_max):
		self.canvas.itemconfig(self.water, text = 'Water: ' + str(water) + '/' + str(water_max))
		self.canvas.itemconfig(self.food, text = 'Food: ' + str(food) + '/' + str(food_max))
		self.canvas.update()

	# Draw water on map
	def update_water(self, x2, x1):
		# remove existing ones
		for i in self.water_objects:
			self.canvas.delete(i)
		
		# draw new ones
		self.water_objects = []
		for i in range(x1.__len__()):
			self.water_objects.append(self.canvas.create_polygon(
				self.WINDOW_MARGIN + x1[i] * self.x1_interval, 
				self.WINDOW_MARGIN + x2[i] * self.x2_interval,

				self.WINDOW_MARGIN + (x1[i] + 1) * self.x1_interval, 
				self.WINDOW_MARGIN + (x2[i] + 1) * self.x2_interval,

				self.WINDOW_MARGIN + x1[i] * self.x1_interval, 
				self.WINDOW_MARGIN + (x2[i] + 1) * self.x2_interval,

				fill = self.WATER_COLOR
				))
		self.canvas.update()


	def update_food(self, x2, x1):
		# remove existing ones
		for i in self.food_objects:
			self.canvas.delete(i)
		
		# draw new ones
		self.food_objects = []
		for i in range(x1.__len__()):
			self.food_objects.append(self.canvas.create_polygon(
				self.WINDOW_MARGIN + x1[i] * self.x1_interval, 
				self.WINDOW_MARGIN + x2[i] * self.x2_interval,

				self.WINDOW_MARGIN + (x1[i] + 1) * self.x1_interval, 
				self.WINDOW_MARGIN + (x2[i] + 1) * self.x2_interval,

				self.WINDOW_MARGIN + (x1[i] + 1) * self.x1_interval, 
				self.WINDOW_MARGIN + x2[i] * self.x2_interval,

				fill = self.FOOD_COLOR
				))
		
		self.canvas.update()
	
	# agent's view
	def update_agent_view(self, land_view, water_view, food_view):
		

		
		# delete everything
		for i in self.agent_objects:
			self.canvas.delete(i)
		
		self.agent_objects = []
		for i in range(self.agent_grid_unit):
			for j in range(self.agent_grid_unit):
				# land
				if land_view[i,j] == 1:
					# draw a cross
					print("incomplete view")
					print(self.agent_grid_coords)
					self.agent_objects.append(
						self.canvas.create_line(
							# bottom-left
							self.agent_grid_coords[0] + self.agent_x1_interval * j,
							self.agent_grid_coords[1] + self.agent_x2_interval * (i + 1),

							# top-right
							self.agent_grid_coords[0] + self.agent_x1_interval * (j + 1),
							self.agent_grid_coords[1] + self.agent_x2_interval * i,

							fill = self.GRID_COLOR, width = 2

						)
					)
					self.agent_objects.append(
						self.canvas.create_line(
							# top-left
							self.agent_grid_coords[0] + self.agent_x1_interval * j,
							self.agent_grid_coords[1] + self.agent_x2_interval * i,

							# bottom-right
							self.agent_grid_coords[0] + self.agent_x1_interval * (j + 1),
							self.agent_grid_coords[1] + self.agent_x2_interval * (i + 1),

							fill = self.GRID_COLOR, width = 2
						)
					)
					

				# water 
				if water_view[i,j] == 1:
					# draw a blue
					self.agent_objects.append(
						self.canvas.create_polygon(
							# top-left
							self.agent_grid_coords[0] + self.agent_x1_interval * j,
							self.agent_grid_coords[1] + self.agent_x2_interval * i,

							# bottom-right
							self.agent_grid_coords[0] + self.agent_x1_interval * (j + 1),
							self.agent_grid_coords[1] + self.agent_x2_interval * (i + 1),

							# bottom-left
							self.agent_grid_coords[0] + self.agent_x1_interval * j,
							self.agent_grid_coords[1] + self.agent_x2_interval * (i + 1),

							fill = self.WATER_COLOR				
						)
					)

				# food
				if food_view[i,j]  == 1:
					# draw a brown
					self.agent_objects.append(
						self.canvas.create_polygon(
							# top-left
							self.agent_grid_coords[0] + self.agent_x1_interval * j,
							self.agent_grid_coords[1] + self.agent_x2_interval * i,

							# bottom-right
							self.agent_grid_coords[0] + self.agent_x1_interval * (j + 1),
							self.agent_grid_coords[1] + self.agent_x2_interval * (i + 1),

							# top-right
							self.agent_grid_coords[0] + self.agent_x1_interval * (j + 1),
							self.agent_grid_coords[1] + self.agent_x2_interval * i,

							fill = self.FOOD_COLOR
						)
					)

		# draw a new agent
		self.agent_objects.append(
			self.canvas.create_rectangle(
				self.agent_grid_coords[0] + self.agent_x1_interval * (self.agent_sight + 0.25),
				self.agent_grid_coords[1] + self.agent_x2_interval * (self.agent_sight + 0.25),
				self.agent_grid_coords[0] + self.agent_x1_interval * (self.agent_sight + 0.75),
				self.agent_grid_coords[1] + self.agent_x2_interval * (self.agent_sight + 0.75),
				fill = self.AGENT_COLOR
				)
			)
		
		self.canvas.update()
		


		







	
	def test(self):
		x1_new = input("starting x1:")
		x2_new = input("starting x2:")
		#self.agent = self.spawn_agent(x1_new,x2_new)
		self.canvas.update()
		
		
		while True:
			water = input("update water")
			food  = input ("update food")
			#self.update_physiology(water, food)
			
			
			x1 = [int(x) for x in input("x1").split()]
			x2 = [int(x) for x in input("x2").split()]
			self.update_water(x1, x2)
			
			x1 = [int(x) for x in input("x1").split()]
			x2 = [int(x) for x in input("x2").split()]
			self.update_food(x1, x2)

			
			
	




#gw = GridWorldUI(100,80)
#gw.test()
