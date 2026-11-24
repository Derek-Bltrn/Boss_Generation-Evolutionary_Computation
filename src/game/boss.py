
import math

from src.game import config
from src.game.projectile import Projectile


class Boss:
    def __init__(self):
        self.x = config.SCREEN_WIDTH / 2
        self.y = 120

        self.radius = config.BOSS_RADIUS
        self.max_health = 100
        self.health = self.max_health

        self.projectiles = []

        # Temporary attack configuration.
        self.projectile_speed = 180
        self.fire_interval = 60
        self.fire_cooldown = 60

    def update(self, player):
        if self.fire_cooldown > 0:
            self.fire_cooldown -= 1

        if self.fire_cooldown == 0:
            self.shoot(player)
            self.fire_cooldown = self.fire_interval

        for projectile in self.projectiles:
            projectile.update()

        self.projectiles = [
            projectile for projectile in self.projectiles
            if not projectile.is_outside()
        ]

    def shoot(self, player):
        projectile = Projectile(
            self.x,
            self.y,
            player.x - self.x,
            player.y - self.y,
            speed=self.projectile_speed,
            damage=1,
            owner="boss"
        )

        self.projectiles.append(projectile)

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
