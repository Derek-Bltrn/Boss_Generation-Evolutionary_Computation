
import math
import random
from dataclasses import dataclass
from typing import Literal

from src.game import config
from src.game.projectile import Projectile


MovementPattern = Literal["zigzag", "horizontal", "vertical", "oval"]


@dataclass(frozen=True)
class BossConfig:
    attack_patterns: tuple[int, int, int] = (0, 1, 2)
    max_health: int = 100
    projectile_speed: float = 180
    projectile_count: int = 5
    fire_interval: int = 60
    movement_pattern: MovementPattern = "horizontal"
    movement_speed: float = 120
    projectile_radius: float = 5

    def __post_init__(self):
        patterns = tuple(self.attack_patterns)
        if (
            len(patterns) != 3
            or any(type(pattern) is not int or not 0 <= pattern <= 7 for pattern in patterns)
            or len(set(patterns)) != 3
        ):
            raise ValueError("Boss requires three distinct attack IDs between 0 and 7.")
        object.__setattr__(self, "attack_patterns", patterns)

        for name in ("max_health", "projectile_count", "fire_interval"):
            value = getattr(self, name)
            if type(value) is not int or value <= 0:
                raise ValueError(f"{name} must be a positive integer.")

        if not math.isfinite(self.projectile_speed) or self.projectile_speed <= 0:
            raise ValueError("projectile_speed must be finite and positive.")
        if not math.isfinite(self.projectile_radius) or self.projectile_radius <= 0:
            raise ValueError("projectile_radius must be finite and positive.")

        if self.movement_pattern not in ("zigzag", "horizontal", "vertical", "oval"):
            raise ValueError("Unsupported boss movement pattern.")

        if not math.isfinite(self.movement_speed) or self.movement_speed <= 0:
            raise ValueError("movement_speed must be finite and positive.")


class Boss:
    def __init__(self, seed=None, *, configuration: BossConfig = BossConfig()):
        self.x = config.SCREEN_WIDTH / 2
        self.y = 120

        self.radius = config.BOSS_RADIUS
        self.movement_pattern = configuration.movement_pattern
        self.movement_speed = configuration.movement_speed
        self._horizontal_phase = self.x - self.radius
        self._vertical_phase = self.y - self.radius
        self._orbit_angle = 0.0
        self.max_health = configuration.max_health
        self.health = self.max_health

        self.projectiles = []

        self.attack_patterns = configuration.attack_patterns
        self.projectile_speed = configuration.projectile_speed
        self.projectile_radius = configuration.projectile_radius
        self.projectile_count = configuration.projectile_count
        self.fire_interval = configuration.fire_interval
        self.fire_cooldown = self.fire_interval

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

        self._update_movement()

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

    def _update_movement(self):
        pattern = self.movement_pattern
        if pattern == "oval":
            self._update_oval_patrol()
            return

        step = self.movement_speed * config.DELTA_TIME
        if pattern in ("horizontal", "zigzag"):
            # The zigzag uses a 4:3 ratio to preserve the configured diagonal speed.
            horizontal_step = step * 0.8 if pattern == "zigzag" else step
            self._horizontal_phase, self.x = self._advance_patrol(
                self._horizontal_phase, horizontal_step, config.SCREEN_WIDTH - self.radius
            )
        if pattern in ("vertical", "zigzag"):
            vertical_step = step * 0.6 if pattern == "zigzag" else step
            self._vertical_phase, self.y = self._advance_patrol(
                self._vertical_phase, vertical_step, config.SCREEN_HEIGHT / 2 - self.radius
            )

    def _advance_patrol(self, phase: float, step: float, upper_bound: float) -> tuple[float, float]:
        round_trip = 2 * (upper_bound - self.radius)
        phase = (phase + step) % round_trip
        # Fold the return leg back into the same patrol bounds.
        return phase, self.radius + min(phase, round_trip - phase)

    def _update_oval_patrol(self):
        horizontal_radius = 150
        vertical_radius = 70
        # Use the larger radius so the configured speed is the peak speed.
        angle_step = self.movement_speed * config.DELTA_TIME / horizontal_radius
        self._orbit_angle = (self._orbit_angle + angle_step) % math.tau
        self.x = config.SCREEN_WIDTH / 2 + horizontal_radius * math.sin(self._orbit_angle)
        self.y = 120 + vertical_radius * (1 - math.cos(self._orbit_angle))

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
                owner="boss",
                radius=self.projectile_radius,
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
