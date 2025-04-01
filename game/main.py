# main.py
import pygame
from player import Player
from enemy import Enemy, EnemyType
from weapon import Sword, Gun

# 게임 초기화
pygame.init()
screen = pygame.display.set_mode((800, 600))
player = Player(x=100, y=100)
enemies = [Enemy(x=400, y=100, type=EnemyType.ELITE)]

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		# 마우스 클릭: 좌클릭 이동 / 우클릭 공격
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				player.move_to(pygame.mouse.get_pos())
			elif event.button == 3:
				player.attack(enemies)

	player.update()
	for enemy in enemies:
		enemy.update(player)

	screen.fill((0, 0, 0))
	player.draw(screen)
	for enemy in enemies:
		enemy.draw(screen)
	pygame.display.flip()

pygame.quit()
