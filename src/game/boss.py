
import math
import random

from src.game import config
from src.game.projectile import Projectile


class Boss:
    def __init__(self, seed=None):
        self.x = config.SCREEN_WIDTH / 2
        self.y = 120

        self.radius = config.BOSS_RADIUS
        self.max_health = 100
        self.health = self.max_health

        self.projectiles = []

        # Temporary attack configuration.
        # Later, these values will come from the chromosome.
        self.attack_patterns = [1, 2, 0]
        self.projectile_speed = 180
        self.projectile_count = 5
        self.fire_interval = 60
        self.fire_cooldown = 60

        # Attack switching every 10 seconds.
        self.attack_duration = 10 * config.TICKS_PER_SECOND
        self.attack_timer = 0

        # Independent random generator for reproducibility.
        self.rng = random.Random(seed)

        self.current_attack = self.rng.choice(
            self.attack_patterns
        )

        # Used by rotating attack patterns.
        self.attack_step = 0

    def update(self, player):
        if self.is_defeated():
            return

        # Change attack pattern every 600 ticks.
        self.attack_timer += 1

        if self.attack_timer >= self.attack_duration:
            self.change_attack()
            self.attack_timer = 0

        # Update firing cooldown.
        if self.fire_cooldown > 0:
            self.fire_cooldown -= 1

        if self.fire_cooldown == 0:
            self.shoot(player)
            self.fire_cooldown = self.fire_interval

        # Update boss projectiles.
        for projectile in self.projectiles:
            projectile.update()

        self.projectiles = [
            projectile for projectile in self.projectiles
            if not projectile.is_outside()
        ]

    def change_attack(self):
        # Avoid repeating the same pattern consecutively.
        available = [
            pattern for pattern in self.attack_patterns
            if pattern != self.current_attack
        ]

        if available:
            self.current_attack = self.rng.choice(available)

        # Reset rotating patterns.
        self.attack_step = 0

    def shoot(self, player):
        angle = math.atan2(
            player.y - self.y,
            player.x - self.x
        )

        pattern = self.current_attack
        angles = []

        if pattern == 0:
            # Aimed attack.
            angles = [angle]

        elif pattern == 1:
            # Fan attack.
            spread = math.radians(15)
            count = self.projectile_count

            angles = [
                angle + (i - (count - 1) / 2) * spread
                for i in range(count)
            ]

        elif pattern == 2:
            # Radial attack.
            count = self.projectile_count

            angles = [
                i * (2 * math.pi / count)
                for i in range(count)
            ]

        elif pattern == 3:
            # Spiral attack.
            rotation = self.attack_step * math.radians(20)

            angles = [
                rotation + i * (2 * math.pi / self.projectile_count)
                for i in range(self.projectile_count)
            ]

        elif pattern == 4:
            # Burst attack.
            # Multiple projectiles with a narrow spread.
            count = self.projectile_count
            spread = math.radians(5)

            angles = [
                angle + (i - (count - 1) / 2) * spread
                for i in range(count)
            ]

        elif pattern == 5:
            # Cross attack.
            rotation = self.attack_step * math.radians(10)

            angles = [
                rotation + i * (math.pi / 2)
                for i in range(4)
            ]

        elif pattern == 6:
            # Wave attack.
            offset = math.sin(
                self.attack_step * 0.5
            ) * math.radians(35)

            angles = [
                angle + offset
            ]

        elif pattern == 7:
            # Double fan attack.
            count = self.projectile_count
            spread = math.radians(12)

            for base_angle in [angle, angle + math.pi]:
                angles.extend([
                    base_angle + (i - (count - 1) / 2) * spread
                    for i in range(count)
                ])

        else:
            raise ValueError(f"Invalid attack pattern: {pattern}")

        for projectile_angle in angles:
            projectile = Projectile(
                self.x,
                self.y,
                math.cos(projectile_angle),
                math.sin(projectile_angle),
                speed=self.projectile_speed,
                damage=1,
                owner="boss"
            )

            self.projectiles.append(projectile)

        self.attack_step += 1

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
