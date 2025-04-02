from dataclasses import dataclass, field
from typing import Dict, List
from item_system import EquipmentSet, EquipmentType, WeaponCategory
from weapon import Weapon, Gun
from enemy import Enemy
import random

MAX_LEVEL = 150
MAX_REBIRTH = 10
STAT_NAMES = ["STR", "END", "DEX", "LUK", "SPD"]


def get_required_exp(level: int) -> int:
	if level >= MAX_LEVEL:
		return 0
	if level <= 10:
		return level * 1500
	elif level <= 20:
		return level * 6000
	elif level <= 30:
		return level * 16000
	elif level <= 40:
		return level * 30000
	elif level <= 50:
		return level * 50000
	elif level <= 60:
		return level * 70000
	elif level <= 70:
		return level * 100000
	elif level <= 80:
		return level * 150000
	elif level <= 90:
		return level * 200000
	elif level == 100:
		return 1_000_000_000
	else:
		return int(get_required_exp(level - 1) * 1.15)


@dataclass
class Player:
	x: int = 100
	y: int = 100
	weapon: Weapon = field(default_factory=Gun)
	level: int = 1
	rebirth: int = 0
	exp: int = 0
	stat_points: int = 0
	stats: Dict[str, int] = field(default_factory=lambda: {name: 5 for name in STAT_NAMES})
	equipment: EquipmentSet = field(default_factory=EquipmentSet)

	def move_to(self, target_pos):
		self.x, self.y = target_pos

	def attack(self, enemies: List[Enemy]):
		print("공격 실행")
		for enemy in enemies:
			if not enemy.is_alive():
				continue
			if enemy.try_dodge():
				print(f"{enemy.name}이(가) 공격을 회피했습니다!")
				continue

			crit_chance = self.get_crit_rate() - enemy.crit_resist
			is_crit = random.random() < (crit_chance / 100)

			base_damage = self.get_base_attack_power()
			if is_crit:
				base_damage *= (1 + self.get_crit_damage() / 100)
				print("치명타 발생!")

			enemy.take_damage(base_damage, is_crit=is_crit)

	def gain_exp(self, amount: int):
		self.exp += amount
		print(f"EXP +{amount:,} → 현재 EXP: {self.exp:,}/{get_required_exp(self.level):,}")
		while self.exp >= get_required_exp(self.level) and self.level < MAX_LEVEL:
			self.exp -= get_required_exp(self.level)
			self.level += 1
			self.stat_points += 5
			print(f"레벨 업! → {self.level}레벨 달성, 스탯 포인트 +5 (총 보유: {self.stat_points})")

	def can_rebirth(self):
		return self.level >= 110 and self.rebirth < MAX_REBIRTH

	def rebirth_player(self):
		if not self.can_rebirth():
			print("환생 조건이 충족되지 않았습니다.")
			return
		self.rebirth += 1
		self.level = 1
		self.exp = 0
		self.stat_points += self.get_rebirth_bonus_stats()
		print(f"환생 완료! 현재 환생 횟수: {self.rebirth}")

	def get_rebirth_bonus_stats(self):
		if 110 <= self.level < 120:
			return 10
		elif 120 <= self.level < 130:
			return 25
		elif 130 <= self.level < 140:
			return 50
		elif 140 <= self.level <= 149:
			return 75
		elif self.level == 150:
			return 100
		return 0

	def get_max_stat_value(self):
		if self.rebirth >= 10:
			return 550
		elif self.rebirth >= 5:
			return 500
		elif self.rebirth >= 1:
			return 450
		return 400

	def assign_stat(self, stat_name: str, amount: int):
		if stat_name not in self.stats:
			print("존재하지 않는 스탯입니다.")
			return
		current = self.stats[stat_name]
		max_value = self.get_max_stat_value()
		if amount <= self.stat_points and current + amount <= max_value:
			self.stats[stat_name] += amount
			self.stat_points -= amount
		else:
			print("스탯 할당 실패: 포인트 부족 또는 최대치 초과")

	def get_total_hp(self):
		str_val = self.stats["STR"]
		hp = 0
		for i in range(1, str_val + 1):
			if i <= 400:
				hp += 15
			elif i <= 500:
				hp += int(15 * 1.5)
			elif i <= 550:
				hp += int(15 * 2)
		return 300 + hp + self.equipment.get_total_bonus("hp_bonus")

	def get_base_attack_power(self):
		weapon = self.equipment.get_item(EquipmentType.WEAPON)
		stat_type = "STR"
		if weapon and isinstance(weapon.weapon_category, WeaponCategory):
			stat_type = "DEX" if weapon.weapon_category == WeaponCategory.RANGED else "STR"

		stat_val = self.stats.get(stat_type, 0)
		multiplier = 0
		for i in range(1, stat_val + 1):
			if i <= 400:
				multiplier += 0.01
			elif i <= 500:
				multiplier += 0.015
			elif i <= 550:
				multiplier += 0.02

		base_attack = weapon.base_attack if weapon else 5
		return base_attack * (1 + multiplier)

	def get_stamina(self):
		end_val = self.stats["END"]
		stamina = 0
		for i in range(1, end_val + 1):
			if i <= 400:
				stamina += 8
			elif i <= 500:
				stamina += int(8 * 1.5)
			elif i <= 550:
				stamina += int(8 * 2)
		return 200 + stamina + self.equipment.get_total_bonus("stamina_bonus")

	def get_defense(self):
		end_val = self.stats["END"]
		multiplier = 0
		for i in range(1, end_val + 1):
			if i <= 400:
				multiplier += 0.008
			elif i <= 500:
				multiplier += 0.012
			elif i <= 550:
				multiplier += 0.016
		base_def = 20 * (1 + multiplier)
		return base_def + self.equipment.get_total_bonus("base_defense")

	def get_accuracy(self):
		return 60 + (self.stats["DEX"] // 30)

	def get_crit_rate(self):
		base = 5 + (self.stats["DEX"] // 20) + (self.stats["LUK"] // 10)
		return base + self.equipment.get_total_bonus("crit_rate_bonus")

	def get_crit_damage(self):
		dex_bonus = (self.stats["DEX"] // 20) * 9
		luk_bonus = (self.stats["LUK"] // 10) * 9
		return 50 + dex_bonus + luk_bonus + self.equipment.get_total_bonus("crit_dmg_bonus")

	def get_drop_rate_bonus(self):
		return 1 + (self.stats["LUK"] // 100) + self.equipment.get_total_bonus("drop_rate_bonus")

	def get_evasion_rate(self):
		return 10 + (self.stats["LUK"] // 100) + self.equipment.get_total_bonus("evasion_bonus")

	def get_move_speed(self):
		speed = 70 + (self.stats["SPD"] // 3)
		return min(speed + self.equipment.get_total_bonus("move_speed_bonus"), 150)

	def get_attack_speed_bonus(self):
		return self.stats["SPD"] * 0.3 + self.equipment.get_total_bonus("attack_speed_bonus")

	def show_stats(self):
		print(f"레벨: {self.level}, 환생: {self.rebirth}, 경험치: {self.exp:,}/{get_required_exp(self.level):,}")
		print(f"스탯 포인트: {self.stat_points}")
		for stat, value in self.stats.items():
			print(f"{stat}: {value}")

	def __str__(self):
		return f"플레이어 (레벨 {self.level}, 환생 {self.rebirth})"

	def get_summary(self) -> Dict[str, any]:
		return {
			"level": self.level,
			"rebirth": self.rebirth,
			"exp": f"{self.exp:,} / {get_required_exp(self.level):,}",
			"stats": self.stats.copy(),
			"stat_points": self.stat_points,
			"hp": self.get_total_hp(),
			"attack": round(self.get_base_attack_power(), 2),
			"defense": round(self.get_defense(), 2),
			"stamina": self.get_stamina(),
			"accuracy": self.get_accuracy(),
			"crit_rate": self.get_crit_rate(),
			"crit_damage": self.get_crit_damage(),
			"drop_rate": self.get_drop_rate_bonus(),
			"move_speed": self.get_move_speed(),
			"attack_speed": round(self.get_attack_speed_bonus(), 2),
		}
