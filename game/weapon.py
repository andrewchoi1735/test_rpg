from game.item_system import EquipmentType, Item, WeaponCategory


class Weapon:
	def __init__(self, damage: int, fire_rate: float):
		self.damage = damage  # 한 발 데미지
		self.fire_rate = fire_rate  # 분당 발사 횟수

	def attack(self, player, enemies):
		raise NotImplementedError

class Sword(Weapon):
	def __init__(self):
		super().__init__(damage=10, fire_rate=60)

	def attack(self, player, enemies):
		print("검 공격!")  # 예: 근거리 공격 처리


class Gun(Weapon):
	def __init__(self):
		super().__init__(damage=5, fire_rate=30)  # 1분당 30발

	def attack(self, player, enemies):
		print(f"{player}이 권총으로 {self.damage} 데미지를 입힙니다!")
	# 실제 게임에서는 타겟팅, 명중 계산, 쿨타임 등 추가 가능


burst_balcan = Item(
	name="Burst Balcan",
	type=EquipmentType.WEAPON,
	attack_speed_bonus=600,
	base_attack=20000,
	weapon_category=WeaponCategory.RANGED
)
