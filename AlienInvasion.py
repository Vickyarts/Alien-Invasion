#!/bin/python3
import pygame
import game_functions as gf
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from game_status import Game_status
from scoreboard import Scoreboard
from button import Button

def run_game():
	"""Runs the game"""
	pygame.init()
	game_setting = Settings()
	screen = pygame.display.set_mode((game_setting.screen_width,game_setting.screen_height))
	pygame.display.set_caption('Alien Invasion')
	stats = Game_status(game_setting)
	sboard = Scoreboard(game_setting,screen,stats)
	ship = Ship(game_setting,screen)
	bullets = Group()
	aliens = Group()
	play_button = Button(game_setting,screen,"play")
	
	while True:
		gf.check_events(game_setting,screen,stats,ship,aliens,bullets,play_button,sboard)
		if stats.game_active:
			ship.update(game_setting.ship_speed)
			gf.update_bullet(game_setting,screen,stats,aliens,bullets,ship,sboard)
			gf.update_aliens(game_setting,stats,screen,ship,aliens,bullets,sboard)
		gf.update_screen(game_setting,screen,stats,ship,aliens,bullets,play_button,sboard)
		
gf.clear_screen()
run_game()
