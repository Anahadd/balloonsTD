import pygame
import random
import math

pygame.init()

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BTD Inspired Tower Defense")

gold = 100
tower_cost = 50

path = [(WIDTH, HEIGHT // 2), (650, HEIGHT // 2), (500, 150), (350, 400), (200, 200), (0, 100)]

class Enemy(pygame.sprite.Sprite):
    def __init__(self, path):
        super().__init__()
        self.image = pygame.Surface([40, 40])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.speed = 2
        self.path = path
        self.waypoint_index = 0
        self.set_waypoint()

    def set_waypoint(self):
        if self.waypoint_index < len(self.path):
            self.target_x, self.target_y = self.path[self.waypoint_index]
            self.waypoint_index += 1

    def move_towards_waypoint(self):
        dx = self.target_x - self.rect.x
        dy = self.target_y - self.rect.y
        dist = math.sqrt(dx * dx + dy * dy)
        if dist == 0:
            return

        dx /= dist
        dy /= dist
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        if abs(self.target_x - self.rect.x) < 5 and abs(self.target_y - self.rect.y) < 5:
            self.set_waypoint()

    def update(self):
        self.move_towards_waypoint()
        if self.waypoint_index == len(self.path) + 1:
            self.kill()

class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([50, 50])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.range = 100

    def get_target(self, enemies):
        min_distance = 99999
        nearest_enemy = None
        for enemy in enemies:
            dist = math.sqrt((self.rect.x - enemy.rect.x) ** 2 + (self.rect.y - enemy.rect.y) ** 2)
            if dist < self.range and dist < min_distance:
                nearest_enemy = enemy
                min_distance = dist
        return nearest_enemy

    def shoot(self, enemies):
        target = self.get_target(enemies)
        if target:
            target.kill()

# Main loop
running = True
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
towers = pygame.sprite.Group()

while running:
    screen.fill(GREEN)

    pygame.draw.lines(screen, GREY, False, path, 50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if gold >= tower_cost:
                x, y = pygame.mouse.get_pos()
                tower = Tower(x, y)
                towers.add(tower)
                all_sprites.add(tower)
                gold -= tower_cost

    if random.randint(0, 100) == 0:
        enemy = Enemy(path)
        all_sprites.add(enemy)
        enemies.add(enemy)

    for tower in towers:
        tower.shoot(enemies)

    all_sprites.update()

    all_sprites.draw(screen)

    font = pygame.font.SysFont(None, 36)
    gold_text = font.render(f'Gold: {gold}', True, BLACK)
    screen.blit(gold_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

    gold += 1

pygame.quit()
