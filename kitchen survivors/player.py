import random
import pygame
from weapons import Cleavers, FryingPan


class Shot:
    def __init__(self, pos, direction, pierce, kind):
        self.pos = pygame.Vector2(pos)
        self.direction = direction
        self.timeLeft = 1.5
        self.pierce = pierce
        self.hitList = []
        self.kind = kind
        self.image = None

    def update(self, dt):
        self.pos += self.direction * 600 * dt
        self.timeLeft -= dt

    def registerHit(self, enemy):
        self.hitList.append(enemy)
        if self.pierce > 0:
            self.pierce -= 1
        else:
            self.timeLeft = 0


class Player:
    def __init__(self):
        self.pos = pygame.Vector2(0, 0)
        self.speed = 250
        self.moveDir = pygame.Vector2(0, 0)
        self.maxHp = 100
        self.hp = 100
        self.regen = 0

        self.damage = 1
        self.attackDelay = 0.6
        self.attackTimer = 0
        self.extraShots = 0
        self.pierce = 0

        self.xp = 0
        self.xpToLevel = 1
        self.level = 1

        self.walkStep = 0
        self.walkTimer = 0
        self.facingBack = False

        self.dashTime = 0
        self.dashCooldown = 0
        self.dashDir = pygame.Vector2(0, 0)
        self.readyFlash = 0
        self.dust = []

        self.cleavers = Cleavers()
        self.pan = FryingPan()

    def atkFactor(self):
        return 0.6 / self.attackDelay

    def update(self, dt, mouseWorld):
        self.attackTimer -= dt

        keys = pygame.key.get_pressed()
        d = pygame.Vector2(0, 0)
        if keys[pygame.K_w]:
            d.y -= 1
        if keys[pygame.K_s]:
            d.y += 1
        if keys[pygame.K_a]:
            d.x -= 1
        if keys[pygame.K_d]:
            d.x += 1
        if d.length() > 0:
            d = d.normalize()
        self.moveDir = d

        if self.dashTime > 0:
            self.pos += self.dashDir * 1000 * dt
            self.dashTime -= dt
        else:
            self.pos += d * self.speed * dt

        # animacao de andar (1, 2, 1, 3)
        self.facingBack = mouseWorld.y < self.pos.y
        if d.length() > 0 and self.dashTime <= 0:
            self.walkTimer += dt
            if self.walkTimer >= 0.12:
                self.walkTimer -= 0.12
                self.walkStep = (self.walkStep + 1) % 4
        else:
            self.walkStep = 0
            self.walkTimer = 0

        # recarga do dash
        if self.dashCooldown > 0:
            self.dashCooldown -= dt
            if self.dashCooldown <= 0:
                self.dashCooldown = 0
                self.readyFlash = 0.12
        if self.readyFlash > 0:
            self.readyFlash -= dt

        alive = []
        for dust in self.dust:
            dust[1] -= dt
            if dust[1] > 0:
                alive.append(dust)
        self.dust = alive

        self.hp = min(self.maxHp, self.hp + self.regen * dt)

    def walkFrame(self):
        return (0, 1, 0, 2)[self.walkStep]

    def takeDamage(self, amount):
        if self.dashTime > 0:
            return
        self.hp -= amount

    def shoot(self, mouseWorld):
        aim = mouseWorld - self.pos
        if aim.length() == 0:
            return []
        aim = aim.normalize()

        total = 1 + self.extraShots
        middle = (total - 1) / 2
        shots = []
        for i in range(total):
            direction = aim.rotate((i - middle) * 12)
            kind = random.choice(["colher", "faca", "garfo"])
            shots.append(Shot(self.pos, direction, self.pierce, kind))

        self.attackTimer = self.attackDelay
        return shots

    def tryDash(self, mouseWorld):
        if self.dashTime > 0 or self.dashCooldown > 0:
            return

        if self.moveDir.length() > 0:
            direction = pygame.Vector2(self.moveDir)
        else:
            toMouse = mouseWorld - self.pos
            if toMouse.length() == 0:
                return
            direction = toMouse.normalize()

        self.dashDir = direction
        self.dashTime = 0.15
        self.dashCooldown = 3.0
        self.dust.append([pygame.Vector2(self.pos.x, self.pos.y + 20), 0.35])

    def gainXp(self):
        self.xp += 1
        if self.xp >= self.xpToLevel:
            self.xp -= self.xpToLevel
            self.xpToLevel += 1
            self.level += 1
            return True
        return False
