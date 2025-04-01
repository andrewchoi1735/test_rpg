from dataclasses import dataclass
from enum import Enum
import random


class EnemyType(Enum):
	NORMAL = "일반"
	ELITE = "엘리트"
	BOSS = "보스"
	FIELD_BOSS = "필드 보스"
	WORLD_BOSS = "월드 보스"


@dataclass
class Enemy:
	name: str
	type: EnemyType
	level: int
	max_hp: int
	current_hp: int
	defense: float
	crit_resist: float  # 치명타 저항
	dodge_rate: float  # 회피율

	def is_alive(self):
		return self.current_hp > 0

	def take_damage(self, damage: float, is_crit: bool = False):
		effective_damage = damage * (1 - self.defense / 100)
		self.current_hp -= int(effective_damage)
		print(f"{self.name}이(가) {int(effective_damage)} 데미지를 받았습니다. 남은 HP: {self.current_hp}")
		if self.current_hp <= 0:
			print(f"{self.name} 처치됨!")

	def try_dodge(self):
		return random.random() < (self.dodge_rate / 100)

	def get_status(self):
		return f"[{self.type.value}] {self.name} - HP: {self.current_hp}/{self.max_hp}"


# 테스트용 적 인스턴스 생성 예시
def create_dummy_enemy():
	return Enemy(
		name="오염된 좀비",
		type=EnemyType.ELITE,
		level=120,
		max_hp=8000,
		current_hp=8000,
		defense=25.0,
		crit_resist=10.0,
		dodge_rate=5.0
	)
