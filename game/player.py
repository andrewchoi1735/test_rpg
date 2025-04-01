class Player:
	def __init__(self, x, y, weapon):
		self.x = x
		self.y = y
		self.weapon = weapon

	def move_to(self, target_pos):
		self.x, self.y = target_pos

	def attack(self, enemies):
		self.weapon.attack(self, enemies)

	def update(self):
		pass

	def draw(self, surface):
		pygame.draw.rect(surface, (0, 255, 0), (self.x, self.y, 32, 32))
