import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_RADIUS
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    clock = pygame.time.Clock()
    dt = 0
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    battle_beast = Player(x, y)
    asteroids_group = pygame.sprite.Group()
    Asteroid.containers = (asteroids_group, updatable, drawable)
    AsteroidField.containers = (updatable)
    asteroid_field_object = AsteroidField()
    shots_group = pygame.sprite.Group()
    Shot.containers = (shots_group, drawable, updatable)

    
    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 
        screen.fill("black")
        for thing in drawable:
            thing.draw(screen)
        pygame.display.flip()
        time_passed = clock.tick(60)
        dt = time_passed / 1000
        updatable.update(dt)
        for roid in asteroids_group:
            if roid.collides_with(battle_beast):
                log_event("player_hit")
                print("Game over!")
                sys.exit()


if __name__ == "__main__":
    main()
