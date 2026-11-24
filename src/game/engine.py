
from src.game import config
from src.game.player import Player
from src.game.boss import Boss


class GameEngine:
    def __init__(self):
        self.player = Player()
        self.boss = Boss()

        self.tick = 0
        self.max_ticks = config.MAX_COMBAT_TICKS

        self.finished = False
        self.winner = None

    def update(self, move_x, move_y, shooting=False, target=None):
        if self.finished:
            return

        # Update player movement and projectiles.
        self.player.update(move_x, move_y)

        # Player shooting.
        if shooting and target is not None:
            self.player.shoot(target[0], target[1])

        # Check projectile collisions.
        remaining_projectiles = []

        for projectile in self.player.projectiles:
            if self.boss.collides_with(projectile):
                self.boss.take_damage(projectile.damage)
            else:
                remaining_projectiles.append(projectile)

        self.player.projectiles = remaining_projectiles

        # Advance simulation time.
        self.tick += 1

        # Check combat results.
        if self.boss.is_defeated():
            self.finished = True
            self.winner = "player"

        elif self.player.health <= 0:
            self.finished = True
            self.winner = "boss"

        elif self.tick >= self.max_ticks:
            self.finished = True
            self.winner = "boss"

    @property
    def elapsed_seconds(self):
        return self.tick / config.TICKS_PER_SECOND

    @property
    def remaining_seconds(self):
        return max(
            0,
            config.MAX_COMBAT_SECONDS - self.elapsed_seconds
        )
