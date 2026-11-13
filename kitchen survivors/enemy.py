import pygame

types = {
    "banano": {"hp": 2, "calm": 50, "angry": 150, "dist": 250},
    "tomate": {"hp": 3, "calm": 40, "angry": 130, "dist": 220},
    "ovo": {"hp": 1, "calm": 70, "angry": 180, "dist": 280},
}


class Enemy:
    def __init__(self, pos, kind):
        self.kind = kind
        self.pos = pygame.Vector2(pos)
        self.stats = types[kind]
        self.hp = self.stats["hp"]
        self.angry = False
        self.flash = 0

    def takeDamage(self, amount):
        self.hp -= amount
        self.flash = 0.1

    def update(self, playerPos, dt):
        if self.flash > 0:
            self.flash -= dt

        toPlayer = playerPos - self.pos
        distance = toPlayer.length()

        if distance < self.stats["dist"]:
            self.angry = True

        speed = self.stats["calm"]
        if self.angry:
            speed = self.stats["angry"]

        if distance > 0:
            self.pos += toPlayer.normalize() * speed * dt
