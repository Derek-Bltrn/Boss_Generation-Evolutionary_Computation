
import pygame

from src.game import config
from src.game.projectile import Projectile


class Player:
    def __init__(self):
        self.x = config.SCREEN_WIDTH / 2
        self.y = config.SCREEN_HEIGHT - 80

        self.radius = config.PLAYER_RADIUS
        self.speed = config.PLAYER_SPEED
        self.health = config.PLAYER_MAX_HEALTH
        self.invulnerability_ticks = 0

        self.projectiles = []
        self.shoot_cooldown = 0

    
    def update(self, move_x, move_y):
        # Normalize movement to prevent faster diagonal movement.
        direction = pygame.Vector2(move_x, move_y)

        if direction.length_squared() > 0:
            direction = direction.normalize()

        self.x += direction.x * config.DELTA_TIME * self.speed
        self.y += direction.y * config.DELTA_TIME * self.speed

        # Keep the player inside the arena.
        self.x = max(
            self.radius,
            min(config.SCREEN_WIDTH - self.radius, self.x)
        )

        self.y = max(
            self.radius,
            min(config.SCREEN_HEIGHT - self.radius, self.y)
        )

        # Update shooting cooldown.
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        if self.invulnerability_ticks > 0:
            self.invulnerability_ticks -= 1

        # Update projectiles.
        for projectile in self.projectiles:
            projectile.update()

        # Remove projectiles outside the arena.
        self.projectiles = [
            projectile for projectile in self.projectiles
            if not projectile.is_outside()
        ]


    def shoot(self, target_x, target_y):
        if self.shoot_cooldown > 0:
            return

        projectile = Projectile(
            self.x,
            self.y,
            target_x - self.x,
            target_y - self.y
        )

        self.projectiles.append(projectile)

        self.shoot_cooldown = (
            config.TICKS_PER_SECOND // config.PLAYER_FIRE_RATE
        )

    def take_damage(self, damage):
        if self.invulnerability_ticks > 0 or damage <= 0:
            return

        self.health = max(0, self.health - damage)
        if self.health > 0:
            self.invulnerability_ticks = config.PLAYER_INVULNERABILITY_TICKS

    def collides_with(self, projectile):
        distance = pygame.Vector2(
            self.x - projectile.x,
            self.y - projectile.y
        ).length()

        return distance <= self.radius + projectile.radius

