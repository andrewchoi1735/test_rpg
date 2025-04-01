from enum import Enum
import pygame


class EnemyType(Enum):
	NORMAL = 1
	ELITE = 2
	BOSS = 3
	FIELD_BOSS = 4
	WORLD_BOSS = 5


class Enemy:
	def __init__(self, x, y, type=EnemyType.NORMAL):
		self.x = x
		self.y = y
		self.hp = self.get_hp_by_type(type)
		self.type = type

	def get_hp_by_type(self, type):
		base = 50
		if type == EnemyType.ELITE:
			return base * 2
		elif type == EnemyType.BOSS:
			return base * 5
		elif type == EnemyType.FIELD_BOSS:
			return base * 10
		elif type == EnemyType.WORLD_BOSS:
			return base * 20
		return base

	def update(self, player):
		# 간단한 추적 로직
		if player.x > self.x: self.x += 1
		if player.x < self.x: self.x -= 1
		if player.y > self.y: self.y += 1
		if player.y < self.y: self.y -= 1

	def draw(self, surface):
		pygame.draw.rect(surface, (255, 0, 0), (self.x, self.y, 32, 32))
