import pygame

from circleshape import CircleShape
from constants import PLAYER_RADIUS, PLAYER_SHOOT_COOLDOWN, PLAYER_SHOOT_SPEED
from constants import PLAYER_SPEED as PL
from constants import PLAYER_TURN_SPEED
from shot import Shot


class Player(CircleShape):
    timer = 0

    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(dt * -1)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(dt * -1)
        if keys[pygame.K_SPACE]:
            self.shoot()

        self.timer -= dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PL * dt

    def shoot(self):
        if self.timer < 0:
            shot = Shot(self.position.x, self.position.y, self.rotation)
            shot.velocity = (
                pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
            )

            self.timer = PLAYER_SHOOT_COOLDOWN
