import math
import pygame


def drawRotated(screen, image, pos, screenAngle, spriteAngle):
    rotated = pygame.transform.rotate(image, spriteAngle - screenAngle)
    screen.blit(rotated, rotated.get_rect(center=pos))


class Cleavers:
    def __init__(self):
        self.level = 0
        self.spins = 1
        self.spinsLeft = 0
        self.swinging = False
        self.restTimer = 1.0
        self.swingTime = 0
        self.baseAngle = 0
        self.hitList = []
        self.center = pygame.Vector2(0, 0)

    def count(self):
        return self.level * 2

    def progress(self):
        return min(1, self.swingTime / 0.35)

    def angle(self, i):
        offset = 0
        if self.swinging:
            p = self.progress()
            offset = -180 * (p * p * (3 - 2 * p))
        return self.baseAngle + i * (360 / self.count()) + offset

    def getPos(self, i):
        return self.center + pygame.Vector2(40, 0).rotate(self.angle(i))

    def startSwing(self):
        self.swinging = True
        self.swingTime = 0
        self.hitList = []
        for i in range(self.count()):
            self.hitList.append([])

    def update(self, dt, player, enemies):
        if self.level == 0:
            return

        self.center = pygame.Vector2(player.pos)
        dt = dt * player.atkFactor()

        if not self.swinging:
            self.restTimer -= dt
            if self.restTimer <= 0:
                self.spinsLeft = self.spins
                self.startSwing()
            return

        self.swingTime += dt

        # se pegou upgrade no meio do giro
        while len(self.hitList) < self.count():
            self.hitList.append([])

        for i in range(self.count()):
            pos = self.getPos(i)
            for enemy in enemies:
                if enemy in self.hitList[i]:
                    continue
                if enemy.pos.distance_to(pos) < 30:
                    enemy.takeDamage(player.damage + 1)
                    self.hitList[i].append(enemy)

        if self.swingTime >= 0.35:
            self.baseAngle -= 180
            self.spinsLeft -= 1
            if self.spinsLeft > 0:
                self.startSwing()
            else:
                self.swinging = False
                self.restTimer = 1.0

    def draw(self, screen, img, topLeft):
        if self.level == 0:
            return

        frame = 0
        if self.swinging:
            p = self.progress()
            frame = int(4 * p * (1 - p) * 4.999)

        for i in range(self.count()):
            pos = self.getPos(i) - topLeft
            drawRotated(screen, img["cleaver"][frame], pos, self.angle(i), 0)


class FryingPan:
    def __init__(self):
        self.level = 0
        self.phase = "rest"
        self.frame = 1
        self.frameTimer = 0
        self.restTimer = 1.2
        self.flipped = False
        self.aim = pygame.Vector2(0, -1)
        self.hitList = []
        self.playerPos = pygame.Vector2(0, 0)

    def center(self):
        return self.playerPos + self.aim * 50

    def update(self, dt, player, enemies, mouseWorld):
        if self.level == 0:
            return

        self.playerPos = pygame.Vector2(player.pos)
        toMouse = mouseWorld - self.playerPos
        if toMouse.length() > 0:
            self.aim = toMouse.normalize()

        dt = dt * player.atkFactor() / 2

        if self.phase == "rest":
            self.restTimer -= dt
            if self.restTimer <= 0:
                self.phase = "windup"
                self.frame = 2
                self.frameTimer = 0

        elif self.phase == "windup":
            self.frameTimer += dt
            while self.frameTimer >= 0.045 and self.phase == "windup":
                self.frameTimer -= 0.045
                self.frame += 1
                if self.frame == 10:
                    self.phase = "hit"
                    self.hitList = []

        elif self.phase == "hit":
            damage = player.damage + 2 + (self.level - 1)
            for enemy in enemies:
                if enemy in self.hitList:
                    continue
                if enemy.pos.distance_to(self.center()) < 57:
                    enemy.takeDamage(damage)
                    self.hitList.append(enemy)

            self.frameTimer += dt
            while self.frameTimer >= 0.05 and self.phase == "hit":
                self.frameTimer -= 0.05
                self.frame += 1
                if self.frame > 12:
                    self.frame = 1
                    self.flipped = not self.flipped
                    self.phase = "rest"
                    self.restTimer = max(0.4, 1.2 - 0.15 * (self.level - 1))

    def draw(self, screen, img, topLeft):
        if self.level == 0:
            return

        if self.flipped:
            image = img["panFlip"][self.frame - 1]
        else:
            image = img["pan"][self.frame - 1]

        angle = math.degrees(math.atan2(self.aim.y, self.aim.x))
        drawRotated(screen, image, self.center() - topLeft, angle, -90)
