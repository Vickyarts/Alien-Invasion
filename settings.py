import json

files = 'save.json'

def load_res():
	"""Loads the resolution from the save file"""
	with open(files) as f:
		resolution = json.load(f)
		return resolution 

class Settings:
	"""This class stores all the settings"""
	def __init__(self):
		self.resolution = load_res()
		self.screen_width = self.resolution[0]
		self.screen_height = self.resolution[1]
		self.bg_color = (0,0,0)
		self.ship_limit = 3
		#Bullet properties
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (255,215,0)
		self.bullet_limit = 3
		#Alien fleet fall speed
		self.fleet_drop_speed = 10
		#Increase 10% speed for leach level
		self.speed_scale = 1.1
		#Increase the points for each alien
		self.score_scale = 1.5
		self.saved_high_score = self.resolution[2]
		self.initialize_level_sets()

	def initialize_level_sets(self):
		"""Set the initial speed and points"""
		self.ship_speed = 1.5
		self.bullet_speed = 3
		#alien's speed
		self.alien_speed = 0.5
		#fleet direction 1 represent right, -1 left
		self.fleet_direction = 1
		self.alien_points = 50
	
	def speed_up(self):
		"""Increase the speed"""
		self.ship_speed *= self.speed_scale
		self.bullet_speed *= self.speed_scale
		self.alien_speed *= self.speed_scale
		self.alien_points = int(self.alien_points * self.score_scale)

