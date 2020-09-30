import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
	"""Class manage the bullets"""
	def __init__(self,gsets,screen,ships):
		super().__init__()
		self.screen = screen
		self.rect = pygame.Rect(0,0,gsets.bullet_width,gsets.bullet_height)
		self.rect.centerx = ships.rect.centerx
		self.rect.top = ships.rect.top
		self.y = float(self.rect.y)
		self.settings = gsets
		self.color = self.settings.bullet_color
		self.speed = self.settings.bullet_speed
		
	def update(self):
		"""Method to make the bullet mvve up continously"""
		self.y -= self.speed
		self.rect.y = self.y
		
	def draw_bullet(self):
		"""Draw the bullet to the screen"""
		pygame.draw.rect(self.screen,self.color,self.rect)
	
	
