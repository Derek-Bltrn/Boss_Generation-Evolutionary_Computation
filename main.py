
import pygame

from src.game.engine import GameEngine
from src.game.renderer import Renderer
from src.game import config


def main():
    renderer = Renderer()
    engine = GameEngine()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not running:
            break

        
        keys = pygame.key.get_pressed()

        move_x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        move_y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])

        shooting = pygame.mouse.get_pressed()[0]
        target = pygame.mouse.get_pos()

        engine.update(move_x, move_y, shooting, target)


        # Render the current game state.
        renderer.draw(engine.player, engine.boss)

        if engine.finished:
            print(f"Combat finished!")
            print(f"Winner: {engine.winner}")
            print(f"Elapsed time: {engine.elapsed_seconds:.2f}s")
            running = False

        renderer.clock.tick(config.TICKS_PER_SECOND)

    pygame.quit()


if __name__ == "__main__":
    main()
