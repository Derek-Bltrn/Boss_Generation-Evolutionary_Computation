
import pygame

from src.game import config


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
            pygame.draw.circle(
                self.screen,
                (255, 80, 80),
                (int(projectile.x), int(projectile.y)),
                projectile.radius
            )

        # Player.
        pygame.draw.circle(
            self.screen,
            config.PLAYER_COLOR,
            (int(player.x), int(player.y)),
            player.radius
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


