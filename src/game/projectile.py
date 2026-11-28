
import math

from src.game import config


class Projectile:
    def __init__(
        self,
        x,
        y,
        direction_x,
        direction_y,
        speed=None,
        damage=None,
        owner="player",
        *,
        radius: float = 5,
    ):
        self.x = x
        self.y = y

        self.speed = (
            speed if speed is not None
            else config.PLAYER_PROJECTILE_SPEED
        )

        self.damage = (
            damage if damage is not None
            else config.PLAYER_PROJECTILE_DAMAGE
        )

        self.owner = owner
        self.radius = radius

        magnitude = math.hypot(direction_x, direction_y)

        if magnitude == 0:
            direction_x, direction_y = 0, -1
            magnitude = 1

        self.vx = direction_x / magnitude * self.speed
        self.vy = direction_y / magnitude * self.speed

    def update(self):
        self.x += self.vx * config.DELTA_TIME
        self.y += self.vy * config.DELTA_TIME

    def is_outside(self):
        return (
            self.x < -self.radius
            or self.x > config.SCREEN_WIDTH + self.radius
            or self.y < -self.radius
            or self.y > config.SCREEN_HEIGHT + self.radius
        )
