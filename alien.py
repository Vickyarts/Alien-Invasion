import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
	"""A class which has alien's all the properties"""
	def __init__(self,gsets,screen):
		super().__init__()
		self.screen = screen
		self.settings = gsets
		self.image = pygame.image.load('images/alien.bmp')
		self.rect = self.image.get_rect()
		#spawn alien at the top left corner
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height
		#store the current alien position
		self.x = float(self.rect.x)
	
	def draw_alien(self):
		"""Draw alien to the screen"""
		self.screen.blit(self.image,self.rect)
		
	def update(self):
		"""Update the position of the alien"""
		self.x += (self.settings.alien_speed * self.settings.fleet_direction)
		self.rect.x = self.x

		
	def check_edge(self):
		"""Check whether the alien touches the edge"""
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right:
			return True
		elif self.rect.left <= 0:
			return True
		else:
			return False

