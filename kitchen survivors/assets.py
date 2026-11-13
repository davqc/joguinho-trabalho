import pygame

# pasta onde este arquivo esta, sem usar o os
folder = __file__.replace("\\", "/").rsplit("/", 1)[0] + "/assets/"


def loadSize(name, size=40):
    image = pygame.image.load(folder + name).convert_alpha()
    return pygame.transform.scale(image, (size, size))


def loadScale(name, scale):
    image = pygame.image.load(folder + name).convert_alpha()
    w = int(image.get_width() * scale)
    h = int(image.get_height() * scale)
    return pygame.transform.scale(image, (w, h))


def silhouette(image, color):
    mask = pygame.mask.from_surface(image)
    return mask.to_surface(setcolor=color, unsetcolor=(0, 0, 0, 0))


def loadAssets():
    img = {}
    img["grass"] = loadSize("grass.png")

    img["front"] = []
    img["back"] = []
    img["frontGray"] = []
    img["backGray"] = []
    for i in range(1, 4):
        front = loadSize("player_front_" + str(i) + ".png")
        back = loadSize("player_back_" + str(i) + ".png")
        img["front"].append(front)
        img["back"].append(back)
        img["frontGray"].append(silhouette(front, (150, 150, 150)))
        img["backGray"].append(silhouette(back, (150, 150, 150)))

    files = {
        "banano": ("banano.png", "banano2.png"),
        "tomate": ("tomato.png", "tomato2.png"),
        "ovo": ("ovito.png", "ovito2.png"),
    }
    img["enemy"] = {}
    img["enemyWhite"] = {}
    for kind in files:
        calm = loadSize(files[kind][0])
        angry = loadSize(files[kind][1])
        img["enemy"][kind] = (calm, angry)
        img["enemyWhite"][kind] = (silhouette(calm, "white"), silhouette(angry, "white"))

    img["colher"] = loadSize("colher.png")
    img["faca"] = loadSize("faca.png")
    img["garfo"] = loadSize("garfo.png")

    img["dust"] = []
    for i in range(1, 7):
        img["dust"].append(loadScale("dash" + str(i) + ".png", 1.5))

    img["cleaver"] = []
    for i in range(1, 6):
        img["cleaver"].append(loadScale("cutelo" + str(i) + ".png", 1))

    img["pan"] = []
    img["panFlip"] = []
    for i in range(1, 13):
        pan = loadScale("fryingpan" + str(i) + ".png", 2)
        img["pan"].append(pan)
        img["panFlip"].append(pygame.transform.flip(pan, True, False))

    img["crosshair"] = loadScale("mira.png", 1)
    img["heart"] = loadScale("heart.png", 1)
    img["heartEmpty"] = loadScale("heartempty.png", 1)

    img["font"] = pygame.font.Font(folder + "fonts/DeterminationSansWebRegular-369X.ttf", 32)
    return img
