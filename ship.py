import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
	"""A class with ship properties"""
	def __init__(self,gsets,screen):
		super().__init__()
		self.screen = screen
		self.image = pygame.image.load('images/ship.bmp')
		#Positions
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom
		self.center = float(self.rect.centerx)
		self.display_width = gsets.screen_width
		self.display_height = gsets.screen_height
		self.right_limit = self.display_width - 30
		self.left_limit = 30
		#Position flags
		self.mright = False
		self.mleft = False
		
	def draw_ship(self):
		"""Draw the ship image to the screen"""
		self.screen.blit(self.image,self.rect)
		
	def update(self,speed):
		"""Update the position of the ship"""
		if self.mright:
			backright = self.center
			self.center += speed
			if self.center >= self.right_limit:
				self.center = backright
		if self.mleft:
			backleft = self.center
			self.center -= speed
			if self.center <= self.left_limit:
				self.center = backleft
		
		self.rect.centerx = self.center

	def ship_center(self):
		"""Place the ship at the center"""
		self.center = self.screen_rect.centerx
