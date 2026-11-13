import random


def getOptions(player):
    options = ["speed", "attackSpeed", "damage", "regen", "pan", "cleaver"]
    if player.maxHp < 200:
        options.append("heart")
    if player.extraShots < 4:
        options.append("multi")
    if player.pierce < 3:
        options.append("pierce")
    if player.cleavers.level >= 3:
        options.remove("cleaver")
    if player.pan.level >= 5:
        options.remove("pan")
    if player.cleavers.level > 0 and player.cleavers.spins < 5:
        options.append("spins")
    return random.sample(options, 3)


def getText(name, player):
    if name == "speed":
        return "Botas: +40 velocidade"
    if name == "attackSpeed":
        return "Ataque rápido: -20% intervalo"
    if name == "damage":
        return "Mais força: +1 dano"
    if name == "regen":
        return "Regeneração: +1 vida por segundo"
    if name == "heart":
        return "Coração: +1 coração"
    if name == "multi":
        return "Tiro múltiplo: +1 projétil"
    if name == "pierce":
        return "Perfurante: atravessa +1 inimigo"
    if name == "spins":
        return "Cutelo: " + str(player.cleavers.spins + 1) + " giros seguidos"
    if name == "cleaver":
        if player.cleavers.level == 0:
            return "NOVO - Cutelo"
        return "Cutelo nv " + str(player.cleavers.level + 1)
    if name == "pan":
        if player.pan.level == 0:
            return "NOVO - Frigideira"
        return "Frigideira nv " + str(player.pan.level + 1)


def apply(name, player):
    if name == "speed":
        player.speed += 40
    if name == "attackSpeed":
        player.attackDelay *= 0.8
    if name == "damage":
        player.damage += 1
    if name == "regen":
        player.regen += 1
    if name == "heart":
        player.maxHp += 20
        player.hp += 20
    if name == "multi":
        player.extraShots += 1
    if name == "pierce":
        player.pierce += 1
    if name == "spins":
        player.cleavers.spins += 1
    if name == "cleaver":
        player.cleavers.level += 1
    if name == "pan":
        player.pan.level += 1
