
import math

from src.game import config


class Boss:
    def __init__(self):
        self.x = config.SCREEN_WIDTH / 2
        self.y = 120

        self.radius = config.BOSS_RADIUS
        self.max_health = 100
        self.health = self.max_health

    def take_damage(self, damage):
        self.health = max(0, self.health - damage)

    def collides_with(self, projectile):
        distance = math.hypot(
            self.x - projectile.x,
            self.y - projectile.y
        )

        return distance <= self.radius + projectile.radius

    def is_defeated(self):
        return self.health <= 0
