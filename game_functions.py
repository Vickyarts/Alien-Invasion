import pygame
import sys
import json
import os
from time import sleep
from bullet import Bullet
from alien import Alien

#Sound Effects
pygame.mixer.init(44100,-16,2,1024)
bullet_sound = pygame.mixer.Sound('audios/shoot.wav')
hit_sound = pygame.mixer.Sound('audios/explosion.wav')
shiphit_sound = pygame.mixer.Sound('audios/shiphit.wav')
Play_Button = pygame.mixer.Sound('audios/play_button.wav') 
restart_sound = pygame.mixer.Sound('audios/restart.wav')

def check_events(gsets,screen,stats,ships,aliens,bullets,button,sboard):
	"""Checks the user action"""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			print('Visit: https://github.com/Vickyarts')
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_event(gsets,screen,ships,bullets,event)
		elif event.type == pygame.KEYUP:
			check_keyup_event(gsets,screen,ships,bullets,event)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(gsets,screen,stats,ships,aliens,bullets,button,sboard, mouse_x, mouse_y)

def check_keydown_event(gsets,screen,ships,bullet,event):
	"""Actions for button pressed events"""			
	if event.type == pygame.KEYDOWN:
		if event.key == pygame.K_RIGHT:
			ships.mright = True
		elif event.key == pygame.K_LEFT:
			ships.mleft = True
		elif event.key == pygame.K_SPACE:
			fire_bullet(gsets,screen,ships,bullet)
		elif event.key == pygame.K_q:
			print('Visit: https://github.com/Vickyarts')
			sys.exit()
		elif event.key == pygame.K_ESCAPE:
			sleep(10)
			
		
def check_keyup_event(gsets,screen,ships,bullet,event):	
	"""Actions for button released events"""
	if event.type == pygame.KEYUP:
		if event.key == pygame.K_RIGHT:
			ships.mright = False
		elif event.key == pygame.K_LEFT:
			ships.mleft = False
				

def update_screen(gsets,screen,stats,ships,aliens,bullets,button,sboard):
	"""Update the screen"""
	screen.fill(gsets.bg_color)	
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ships.draw_ship()
	aliens.update()
	aliens.draw(screen)
	sboard.show_score()
	if not stats.game_active:
		button.draw_button()
	pygame.display.flip()

def update_bullet(gsets,screen,stats,aliens,bullets,ships,sboard):
	"""Update the bullet using the update method and deleting bullets when it reaches the top of the screen"""
	bullets.update()
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	check_bullet_alien_collision(gsets,screen,stats,ships,aliens,bullets,sboard)
	
def fire_bullet(gsets,screen,ships,bullets):
	"""Fire a limited amount of bullets"""
	if len(bullets) < gsets.bullet_limit:
		bullet_sound.play()
		new_bullet = Bullet(gsets,screen,ships)
		bullets.add(new_bullet)
			
def check_bullet_alien_collision(gsets,screen,stats,ships,aliens,bullets,sboard):
	"""Checks for bullet alien collisions and remove that alien"""
	collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
	if collisions:
		for alien in collisions.values():
			hit_sound.play()
			stats.score += gsets.alien_points * len(alien)
			sboard.prep_score()
		check_high_score(stats,sboard)
	if len(aliens) == 0:
		gsets.speed_up()
		bullets.empty()
		stats.level += 1
		sboard.prep_level()
		alien_fleet(gsets,screen,aliens,ships)
		
def get_number_aliens_x(gsets,alien_width):
	"""Give the number of aliens can be placed in a row"""
	available_space_x = gsets.screen_width - (2 * alien_width)
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x
	
def get_number_aliens_y(gsets,alien_height,ship_height):
	"""Give the number of aliens can be placed in a column"""
	available_space_y = gsets.screen_height - 3 * alien_height - ship_height
	number_aliens_y = int(available_space_y  / (2 * alien_height))
	return number_aliens_y
	
	
def create_aliens(gsets,screen,aliens,alien_width,alien_number,alien_height,row_number):
	"""Create the a single alien"""
	alien = Alien(gsets,screen)
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.y = alien_height + 2 * alien_height * row_number
	alien.rect.x = alien.x
	alien.rect.y = alien.y
	aliens.add(alien)

def alien_fleet(gsets,screen,aliens,ship):
	"""Create a fleet of aliens"""
	alien = Alien(gsets,screen)
	alien_width = alien.rect.width
	alien_height = alien.rect.height
	number_aliens_x = get_number_aliens_x(gsets,alien_width)
	row_number = get_number_aliens_y(gsets,alien_height,ship.rect.height)
	
	for number_rows in range(row_number):
		for alien_number in range(number_aliens_x):
			create_aliens(gsets,screen,aliens,alien_width,alien_number,alien_height,number_rows)

def update_aliens(gsets,stats,screen,ship,aliens,bullets,sboard):
	"""Update the aliens"""
	check_fleet_edge(gsets,aliens)
	aliens.update()
	check_aliens_bottom(gsets,stats,screen,aliens,ship,bullets,sboard)
	if pygame.sprite.spritecollideany(ship,aliens):
		ship_hit(gsets,stats,screen,aliens,ship,bullets,sboard)

def ship_hit(gsets,stats,screen,aliens,ships,bullets,sboard):
	"""Used to minus the life and restart when the player loses all the life"""
	if stats.ships_left >= 2:
		shiphit_sound.play()
		stats.ships_left -= 1
		sboard.prep_ship()
	elif stats.ships_left == 1:
		stats.ships_left -= 1
		restart_sound.play()
		pygame.mouse.set_visible(True)
		stats.game_active = False
		sleep(1.3)
	else:
		restart_sound.play()
		pygame.mouse.set_visible(True)
		stats.game_active = False
		sleep(1.3)
	aliens.empty()
	bullets.empty()
	alien_fleet(gsets,screen,aliens,ships)
	ships.ship_center()
	clear_screen()
	sleep(1.5)

def change_fleet_direction(gsets,aliens):
	"""Change the direction of the alien fleet when it reaches the edge"""
	for alien in aliens.sprites():
		alien.rect.y += gsets.fleet_drop_speed
	gsets.fleet_direction *= -1

def check_fleet_edge(gsets,aliens):
	"""Checks whether the fleet reaches the edge or not"""
	for alien in aliens.sprites():
		if alien.check_edge():
			change_fleet_direction(gsets,aliens)
			break

def check_aliens_bottom(gsets,stats,screen,aliens,ships,bullets,sboard):
	"""Checks whether the aliens reaches the bottom"""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			ship_hit(gsets,stats,screen,aliens,ships,bullets,sboard)
			break

def check_play_button(gsets,screen,stats,ships,aliens,bullet,button,sboard,mouse_x,mouse_y):
	"""Checks whether the play button is clicked"""
	clicked_button = button.rect.collidepoint(mouse_x, mouse_y)
	
	if clicked_button and not stats.game_active:
		Play_Button.play()
		pygame.mouse.set_visible(False)
		gsets.initialize_level_sets()
		stats.reset_status()
		stats.game_active = True
		sboard.prep_level()
		sboard.prep_high_score()
		stats.score = 0
		sboard.prep_score()
		sboard.prep_ship()
		bullet.empty()
		aliens.empty()
		alien_fleet(gsets,screen,aliens,ships)
		ships.ship_center()
		
def check_high_score(stats,sboard):
	"""Change the high score and store the score"""
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sboard.prep_high_score()
		sboard.show_score()
		high_score_store(stats)

def high_score_store(stats):
	"""Store the high score"""
	files = 'save.json'
	with open(files) as f:
		sets = json.load(f)
	with open(files,'w') as f:
		sets.pop()
		sets.append(stats.high_score)
		json.dump(sets,f)

def clear_screen():
	"""Clears the screen"""
	if os.name == "nt":
		os.system("cls")
	else:
		os.system("clear")
