import pygame

from player import Player
from world import World
from oroboro_mind import OroboroMind



pygame.init()


screen = pygame.display.set_mode(
    (600,600)
)


pygame.display.set_caption(
    "Oroboro Explorer"
)



clock = pygame.time.Clock()



player = Player()

world = World()

mind = OroboroMind()



running=True



while running:


    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running=False



    keys = pygame.key.get_pressed()


    player.move(keys)



    # Oroboro observes the world

    if abs(player.x-250)<20 and abs(player.y-150)<20:

        mind.observe(
            "Artifact discovered"
        )


    screen.fill(
        (10,10,30)
    )



    # draw artifact

    pygame.draw.circle(
        screen,
        (255,255,0),
        (250,150),
        15
    )



    player.draw(screen)



    pygame.display.flip()


    clock.tick(60)



pygame.quit()