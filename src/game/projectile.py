
import math

from src.game import config


class Projectile:
    def __init__(self, x, y, direction_x, direction_y):
        self.x = x
        self.y = y

        magnitude = math.hypot(direction_x, direction_y)

        if magnitude == 0:
            self.vx = 0
            self.vy = -config.PLAYER_PROJECTILE_SPEED
        else:
            self.vx = direction_x / magnitude * config.PLAYER_PROJECTILE_SPEED
            self.vy = direction_y / magnitude * config.PLAYER_PROJECTILE_SPEED

        self.radius = 5
        self.damage = config.PLAYER_PROJECTILE_DAMAGE

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
