
import math
from functools import lru_cache

import pygame

from src.game import config


@lru_cache(maxsize=16)
def _boss_projectile_sprite(radius: float) -> pygame.Surface:
    diameter = 2 * math.ceil(radius) + 1
    scale = 8
    scaled_diameter = diameter * scale
    surface = pygame.Surface((scaled_diameter, scaled_diameter), pygame.SRCALPHA)
    color = (255, 80, 80)
    surface.fill((*color, 0))
    center = scaled_diameter // 2
    pygame.draw.circle(surface, color, (center, center), round(radius * scale))
    return pygame.transform.smoothscale(surface, (diameter, diameter))


class Renderer:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        )

        pygame.display.set_caption("Evolutionary Boss Generation")
        self.clock = pygame.time.Clock()

    
    
    def draw(self, player, boss):
        self.screen.fill(config.BACKGROUND_COLOR)

        # Player projectiles.
        for projectile in player.projectiles:
            pygame.draw.circle(
                self.screen,
                (255, 220, 100),
                (int(projectile.x), int(projectile.y)),
                projectile.radius
            )

        # Boss projectiles.
        for projectile in boss.projectiles:
            sprite = _boss_projectile_sprite(projectile.radius)
            bounds = sprite.get_rect(center=(int(projectile.x), int(projectile.y)))
            self.screen.blit(sprite, bounds)

        # Player.
        player_center = (int(player.x), int(player.y))
        invulnerable = player.invulnerability_ticks > 0
        player_color = config.PLAYER_COLOR
        if invulnerable:
            elapsed_ticks = config.PLAYER_INVULNERABILITY_TICKS - player.invulnerability_ticks
            phase = math.tau * elapsed_ticks / config.PLAYER_INVULNERABLE_PULSE_TICKS
            blend = (1 - math.cos(phase)) / 2
            player_color = pygame.Color(*config.PLAYER_INVULNERABLE_COLOR).lerp(
                config.PLAYER_INVULNERABLE_PULSE_COLOR, blend
            )
        pygame.draw.circle(
            self.screen,
            player_color,
            player_center,
            player.radius
        )
        if invulnerable:
            pygame.draw.circle(
                self.screen,
                config.PLAYER_INVULNERABLE_OUTLINE_COLOR,
                player_center,
                player.radius,
                width=3,
            )

        # Boss.
        pygame.draw.circle(
            self.screen,
            config.BOSS_COLOR,
            (int(boss.x), int(boss.y)),
            boss.radius
        )

        # Boss health bar.
        bar_width = 300
        bar_height = 15
        bar_x = (config.SCREEN_WIDTH - bar_width) // 2
        bar_y = 25

        health_ratio = boss.health / boss.max_health

        pygame.draw.rect(
            self.screen,
            (65, 65, 75),
            (bar_x, bar_y, bar_width, bar_height)
        )

        pygame.draw.rect(
            self.screen,
            config.BOSS_COLOR,
            (bar_x, bar_y, bar_width * health_ratio, bar_height)
        )

        # Player health.
        font = pygame.font.SysFont(None, 32)

        health_text = font.render(
            f"HP: {player.health}/{config.PLAYER_MAX_HEALTH}",
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            health_text,
            (20, config.SCREEN_HEIGHT - 45)
        )
        
        pygame.display.flip()


