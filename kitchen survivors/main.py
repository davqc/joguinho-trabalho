import math
import random
import pygame
from assets import loadAssets
from player import Player
from enemy import Enemy
import upgrades

pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Kitchen Survivors")
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

img = loadAssets()
font = img["font"]
center = pygame.Vector2(400, 400)
dim = pygame.Surface((800, 800))
dim.set_alpha(150)


def newGame():
    global player, enemies, shots, spawnTimer, state, options
    player = Player()
    enemies = []
    shots = []
    spawnTimer = 0
    options = []
    state = "playing"


def choose(i):
    global state
    upgrades.apply(options[i], player)
    state = "playing"


def text(msg, x, y, middle=False):
    image = font.render(msg, True, "white")
    if middle:
        screen.blit(image, image.get_rect(center=(x, y)))
    else:
        screen.blit(image, (x, y))


def drawAt(image, pos):
    screen.blit(image, image.get_rect(center=pos - camTopLeft))


newGame()
mouseWorld = pygame.Vector2(0, 0)
camTopLeft = pygame.Vector2(0, 0)
dt = 0
running = True

while running:
    #----------------------------
    # camera
    #----------------------------
    # focuspoint é tipo o centro da camera, ja camtopleft é pra desenhar ela corretamente como as surfaces usam superior esquerdo como base, ele é basicamente 1/3 do caminho do jogador ate o mouse
    mouse = pygame.Vector2(pygame.mouse.get_pos())
    focuspoint = player.pos + (mouse - center) * 0.5
    camTopLeft = focuspoint - center
    mouseWorld = mouse + camTopLeft

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if state == "playing" and event.key == pygame.K_SPACE:
                player.tryDash(mouseWorld)
            if state == "upgrade":
                if event.key == pygame.K_1:
                    choose(0)
                elif event.key == pygame.K_2:
                    choose(1)
                elif event.key == pygame.K_3:
                    choose(2)
            if state == "dead" and event.key == pygame.K_r:
                newGame()

        if event.type == pygame.MOUSEBUTTONDOWN and state == "upgrade" and event.button == 1:
            for i in range(3):
                if abs(event.pos[1] - (350 + i * 70)) < 30:
                    choose(i)
                    break

    if state == "playing":
        player.update(dt, mouseWorld)

        spawnTimer -= dt
        if spawnTimer <= 0:
            spawnTimer = 1.5
            spawnPos = player.pos + pygame.Vector2(800, 0).rotate(random.randint(0, 359))
            enemies.append(Enemy(spawnPos, random.choice(["banano", "tomate", "ovo"])))

        for enemy in enemies:
            enemy.update(player.pos, dt)
            if enemy.pos.distance_to(player.pos) < 50:
                player.takeDamage(8 * dt)

        if player.attackTimer <= 0:
            shots.extend(player.shoot(mouseWorld))

        player.cleavers.update(dt, player, enemies)
        player.pan.update(dt, player, enemies, mouseWorld)

        for shot in shots:
            shot.update(dt)
            for enemy in enemies:
                if enemy in shot.hitList:
                    continue
                if shot.pos.distance_to(enemy.pos) < 40:
                    enemy.takeDamage(player.damage)
                    shot.registerHit(enemy)
                    break

        alive = []
        for shot in shots:
            if shot.timeLeft > 0:
                alive.append(shot)
        shots = alive

        levelUp = False
        alive = []
        for enemy in enemies:
            if enemy.hp <= 0:
                if player.gainXp():
                    levelUp = True
            else:
                alive.append(enemy)
        enemies = alive

        if player.hp <= 0:
            state = "dead"
        elif levelUp:
            options = upgrades.getOptions(player)
            state = "upgrade"

    # desenho
    screen.fill("darkgray")

    # ------------------- 
    # GRAMA INFINITA
    # -------------------
    # BASICAMENTE ele sempre desenha grama onde a camera ta ne ai tipo esse valorzinho offx e offy e pra camera n se limitar a se mover so nos tiles e conseguir mostrar meio tile
    # entao tipo esse valor coluna * 40 e linha * 40 e pra mutiplica pelo valor do tile

    offX = -(camTopLeft.x % 40)
    offY = -(camTopLeft.y % 40)
    for coluna in range(21):
        for linha in range(21):
            screen.blit(img["grass"], (offX + coluna * 40, offY + linha * 40))

    for dust in player.dust:
        progress = 1 - dust[1] / 0.35
        frame = min(5, int(progress * 6))
        image = img["dust"][frame].copy()
        image.set_alpha(int(255 * (1 - progress)))
        screen.blit(image, image.get_rect(midbottom=dust[0] - camTopLeft))

    for enemy in enemies:
        if enemy.flash > 0:
            pair = img["enemyWhite"][enemy.kind]
        else:
            pair = img["enemy"][enemy.kind]
        if enemy.angry:
            drawAt(pair[1], enemy.pos)
        else:
            drawAt(pair[0], enemy.pos)

    for shot in shots:
        if shot.image is None:
            angle = math.degrees(math.atan2(shot.direction.y, shot.direction.x))
            shot.image = pygame.transform.rotate(img[shot.kind], -90 - angle)
        drawAt(shot.image, shot.pos)

    player.cleavers.draw(screen, img, camTopLeft)

    if player.facingBack:
        sprites = img["back"]
        gray = img["backGray"]
    else:
        sprites = img["front"]
        gray = img["frontGray"]
    if player.readyFlash > 0:
        sprites = gray
    drawAt(sprites[player.walkFrame()], player.pos)

    player.pan.draw(screen, img, camTopLeft)

    # interface
    for i in range(int(player.maxHp / 20)):
        x = 10 + i * 36
        screen.blit(img["heartEmpty"], (x, 10))
        fill = min(1, max(0, (player.hp - i * 20) / 20))
        if fill > 0:
            w = int(img["heart"].get_width() * fill)
            screen.blit(img["heart"], (x, 10), (0, 0, w, img["heart"].get_height()))

    pygame.draw.rect(screen, "black", (10, 48, 200, 10))
    pygame.draw.rect(screen, "gold", (10, 48, 200 * player.xp / player.xpToLevel, 10))
    text("Nível " + str(player.level), 10, 64)

    y = 95
    if player.cleavers.level > 0:
        text("Cutelo nv " + str(player.cleavers.level) + " (" + str(player.cleavers.spins) + " giros)", 10, y)
        y += 25
    if player.pan.level > 0:
        text("Frigideira nv " + str(player.pan.level), 10, y)

    if state == "upgrade":
        screen.blit(dim, (0, 0))
        text("Subiu de nível! colunaha:", 400, 250, True)
        for i in range(3):
            text(str(i + 1) + " - " + upgrades.getText(options[i], player), 400, 350 + i * 70, True)

    if state == "dead":
        screen.blit(dim, (0, 0))
        text("Fim de jogo", 400, 350, True)
        text("Aperte R para recomeçar", 400, 420, True)

    screen.blit(img["crosshair"], img["crosshair"].get_rect(center=mouse))

    pygame.display.flip()
    dt = clock.tick(75) / 1000

pygame.quit()
