from dataclasses import dataclass, field
from enum import Enum
from typing import Dict


class EquipmentType(Enum):
	WEAPON = "무기"
	ARMOR = "방어구"
	ACCESSORY = "악세사리"


class WeaponCategory(Enum):
	MELEE = "근거리"
	RANGED = "원거리"


@dataclass
class Item:
	name: str
	type: EquipmentType
	stat_bonus: Dict[str, int] = field(default_factory=dict)  # STR, DEX, 등
	crit_rate_bonus: float = 0.0
	crit_dmg_bonus: float = 0.0
	drop_rate_bonus: float = 0.0
	move_speed_bonus: float = 0.0
	attack_speed_bonus: float = 0.0
	base_attack: float = 0.0
	base_defense: float = 0.0
	hp_bonus: int = 0
	stamina_bonus: int = 0
	evasion_bonus: int = 0
	weapon_category: WeaponCategory = None  # 무기 타입 구분용 (근거리/원거리)

	def get_stat(self, stat_name: str) -> int:
		return self.stat_bonus.get(stat_name, 0)

	def __str__(self):
		return f"{self.name} ({self.type.value})"


@dataclass
class EquipmentSet:
	equipped: Dict[EquipmentType, Item] = field(default_factory=dict)

	def equip(self, item: Item):
		self.equipped[item.type] = item

	def get_total_bonus(self, attr: str) -> float:
		return sum(getattr(item, attr, 0.0) for item in self.equipped.values())

	def get_stat_bonus(self, stat_name: str) -> int:
		return sum(item.get_stat(stat_name) for item in self.equipped.values())

	def get_item(self, etype: EquipmentType) -> Item:
		return self.equipped.get(etype, None)

	def get_attack_stat_type(self) -> str:
		weapon = self.get_item(EquipmentType.WEAPON)
		if weapon and weapon.weapon_category == WeaponCategory.RANGED:
			return "DEX"
		return "STR"  # 기본은 근거리

	def __str__(self):
		return "\n".join(f"[{etype.name}] {item.name}" for etype, item in self.equipped.items())
