from __future__ import annotations

import pygame

from .core_loop import OroboroCoreEngine


class PygameExplorationWorld:
    def __init__(self, width: int = 600, height: int = 600) -> None:
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Oroboro Exploration World")
        self.clock = pygame.time.Clock()
        self.engine = OroboroCoreEngine()
        self.running = True
        self.player_x = width // 2
        self.player_y = height // 2
        self.artifact_position = (width // 2, height // 4)

    def run(self) -> None:
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player_x -= 4
            if keys[pygame.K_RIGHT]:
                self.player_x += 4
            if keys[pygame.K_UP]:
                self.player_y -= 4
            if keys[pygame.K_DOWN]:
                self.player_y += 4

            if abs(self.player_x - self.artifact_position[0]) < 25 and abs(self.player_y - self.artifact_position[1]) < 25:
                self.engine.loop("artifact discovered", source="pygame")
            else:
                self.engine.loop("explore the world", source="pygame")

            self.screen.fill((10, 10, 30))
            pygame.draw.circle(self.screen, (255, 255, 0), self.artifact_position, 15)
            pygame.draw.rect(self.screen, (200, 200, 255), (self.player_x, self.player_y, 20, 20))
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


def main() -> None:
    world = PygameExplorationWorld()
    world.run()
