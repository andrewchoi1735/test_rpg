class Weapon:
	def __init__(self, damage):
		self.damage = damage

	def attack(self, player, enemies):
		raise NotImplementedError


class Sword(Weapon):
	def __init__(self):
		super().__init__(damage=10)

	def attack(self, player, enemies):
		print("검 공격!")  # 예: 근거리 공격 처리


class Gun(Weapon):
	def __init__(self):
		super().__init__(damage=5)

	def attack(self, player, enemies):
		print("총 발사!")  # 예: 원거리 공격 처리
