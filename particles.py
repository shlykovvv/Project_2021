import pygame
import pygame.draw
import sys
import random
import math

FPS = 600  # TODO: узнать максимальное адекватное
w = 600
h = 400
DARK = (50, 50, 50)

RED = (250, 20, 20)
BROWN = (200, 140, 100)
BLUE_SEA = (80, 170, 140)
BLUE = (0, 150, 230)
PURPLE = (130, 0, 200)
GREEN = (0, 128, 0)
GREY = (130, 130, 130)
PINK = (250, 150, 210)
WHITE = (200, 200, 200)
COLORS = [RED, BROWN, BLUE_SEA, BLUE, PURPLE, GREEN, GREY, PINK, WHITE]
BG = (20, 55, 75, 255)

NUMBER_OF_TYPES = 3  # TODO: добавить контроллер-scrollbar
NODE_COUNT = 250  # TODO: добавить контроллер-scrollbar
SIMULATIONS_PER_FRAME = 2  # TODO: добавить контроллер-scrollbar

DRAW_CONNECTIONS = True  # TODO: добавить галочку

NODE_RADIUS = 5
MAX_DIST = 100
MAX_DIST2 = MAX_DIST * MAX_DIST
SPEED = 4
BORDER = 30
fw = w // MAX_DIST + 1
fh = h // MAX_DIST + 1
LINK_FORCE = -0.015


class Link:
    def __init__(self, a, b):
        self.a = a
        self.b = b


class Particle:
    def __init__(self, type, x, y):
        self.type = type
        self.x = x
        self.y = y
        self.sx = 0
        self.sy = 0
        self.links = 0
        self.bonds = []
        self.color = COLORS[self.type]


def generateRules():
    global LINKS, LINKS_POSSIBLE, COUPLING
    LINKS = []
    LINKS_POSSIBLE = []
    COUPLING = []
    for i in range(NUMBER_OF_TYPES):
        LINKS.append(math.floor(random.random() * 4))
        COUPLING.append([])
        LINKS_POSSIBLE.append([])
        for j in range(NUMBER_OF_TYPES):
            LINKS_POSSIBLE[i].append(math.floor(random.random() * 4))
            COUPLING[i].append(math.floor(random.random() * 3 - 1))
    print(LINKS)
    print(LINKS_POSSIBLE)
    print(COUPLING)


def add(type, x, y):
    p = Particle(type, x, y)
    fields[round(p.x / MAX_DIST)][round(p.y / MAX_DIST)].append(p)
    return p


def new_world():
    generateRules()
    global fields, links
    fields = [0] * fw  # array for dividing scene into parts to reduce complexity
    for i in range(fw):
        fields[i] = [0] * fh
        for j in range(fh):
            fields[i][j] = []
    links = []
    for i in range(NODE_COUNT):  # put particles randomly
        add(random.randint(0, NUMBER_OF_TYPES - 1), random.random() * (w - 2 * NODE_RADIUS) + NUMBER_OF_TYPES,
            random.random() * (h - 2 * NODE_RADIUS) + NUMBER_OF_TYPES)


def applyForce(a, b):
    d2 = (a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y)
    canLink = False
    if d2 < MAX_DIST2:
        dA = COUPLING[a.type][b.type] / d2
        dB = COUPLING[b.type][a.type] / d2
        if a.links < LINKS[a.type] and b.links < LINKS[b.type]:
            if d2 < MAX_DIST2 / 4:
                if not b in a.bonds and not a in b.bonds:
                    typeCountA = 0
                    for p in a.bonds:
                        if p.type == b.type:
                            typeCountA += 1
                    typeCountB = 0
                    for p in b.bonds:
                        if p.type == a.type:
                            typeCountB += 1
                    if typeCountA < LINKS_POSSIBLE[a.type][b.type] and typeCountB < LINKS_POSSIBLE[b.type][a.type]:
                        canLink = True
        else:
            if not b in a.bonds and not a in b.bonds:
                dA = 1 / d2
                dB = 1 / d2
        angle = math.atan2(a.y - b.y, a.x - b.x)
        if d2 < 1:
            d2 = 1
        if d2 < NODE_RADIUS * NODE_RADIUS * 4:
            dA = 1 / d2
            dB = 1 / d2
        a.sx += math.cos(angle) * dA * SPEED
        a.sy += math.sin(angle) * dA * SPEED
        b.sx -= math.cos(angle) * dB * SPEED
        b.sy -= math.sin(angle) * dB * SPEED
    if canLink:
        return d2
    else:
        return -1


def model():
    for i in range(fw):
        for j in range(fh):
            for a in fields[i][j]:
                a.x += a.sx
                a.y += a.sy
                a.sx *= 0.98
                a.sy *= 0.98
                # velocity normalization
                # idk if it is still necessary
                magnitude = math.sqrt(a.sx * a.sx + a.sy * a.sy)
                if magnitude > 1:
                    a.sx /= magnitude
                    a.sy /= magnitude

                # border repulsion
                if a.x < BORDER:
                    a.sx += SPEED * 0.05
                    if a.x < 0:
                        a.x = -a.x
                        a.sx *= -0.5
                elif a.x > w - BORDER:
                    a.sx -= SPEED * 0.05
                    if a.x > w:
                        a.x = w * 2 - a.x
                        a.sx *= -0.5
                if a.y < BORDER:
                    a.sy += SPEED * 0.05
                    if a.y < 0:
                        a.y = -a.y
                        a.sy *= -0.5
                elif a.y > h - BORDER:
                    a.sy -= SPEED * 0.05
                    if a.y > h:
                        a.y = h * 2 - a.y
                        a.sy *= -0.5
    for link in links:
        a = link.a
        b = link.b
        d2 = (a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y)
        if d2 > MAX_DIST2 / 4:
            a.links -= 1
            b.links -= 1
            a.bonds.remove(b)
            b.bonds.remove(a)
            links.remove(link)
            i -= 1
        elif d2 > NODE_RADIUS * NODE_RADIUS * 4:
            angle = math.atan2(a.y - b.y, a.x - b.x)
            a.sx += math.cos(angle) * LINK_FORCE * SPEED
            a.sy += math.sin(angle) * LINK_FORCE * SPEED
            b.sx -= math.cos(angle) * LINK_FORCE * SPEED
            b.sy -= math.sin(angle) * LINK_FORCE * SPEED

    # moving particle to another field
    for i in range(fw):
        for j in range(fh):
            for a in fields[i][j]:
                if (round(a.x / MAX_DIST) != i) or (round(a.y / MAX_DIST) != j):
                    fields[i][j].remove(a)
                    fields[round(a.x / MAX_DIST)][round(a.y / MAX_DIST)].append(a)

    # dividing scene into parts to reduce complexity
    for i in range(fw):
        for j in range(fh):
            for a in fields[i][j]:
                particleToLink = 0
                particleToLinkMinDist2 = (w + h) * (w + h)
                for b in fields[i][j]:
                    if b != a:
                        d2 = applyForce(a, b)
                        if d2 != -1 and d2 < particleToLinkMinDist2:
                            particleToLinkMinDist2 = d2
                            particleToLink = b
                if i < fw - 1:
                    iNext = i + 1
                    for b in fields[iNext][j]:
                        d2 = applyForce(a, b)
                        if d2 != -1 and d2 < particleToLinkMinDist2:
                            particleToLinkMinDist2 = d2
                            particleToLink = b
                if j < fh - 1:
                    jNext = j + 1
                    for b in fields[i][jNext]:
                        d2 = applyForce(a, b)
                        if d2 != -1 and d2 < particleToLinkMinDist2:
                            particleToLinkMinDist2 = d2
                            particleToLink = b
                    if i < fw - 1:
                        iNext = i + 1
                        for b in fields[iNext][jNext]:
                            d2 = applyForce(a, b)
                            if d2 != -1 and d2 < particleToLinkMinDist2:
                                particleToLinkMinDist2 = d2
                                particleToLink = b
                if particleToLink != 0:
                    a.bonds.append(particleToLink)
                    particleToLink.bonds.append(a)
                    a.links += 1
                    particleToLink.links += 1
                    links.append(Link(a, particleToLink))


def Calc_coord_for_link(z1, z2):
    return z1 + (z2 - z1) * NODE_RADIUS / distance


new_world()
# view
pygame.init()
screen = pygame.display.set_mode((w + 150, h))  # TODO: допокно для кнопок и регуляторов, нужно его улучшить и сделать красивым
pygame.display.update()
clock = pygame.time.Clock()
finished = False

smallfont = pygame.font.SysFont('Corbel', int(w / 40))
text = smallfont.render('Create new world', True, (0, 0, 0))  # TODO: сделать кнопку красивой
color_light = (250, 250, 250)
color_dark = (170, 170, 170)

while not finished:
    clock.tick(FPS)
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mouse[0] >= w and mouse[1] <= h / 5:
                new_world()
    for i in range(SIMULATIONS_PER_FRAME):
        model()
    pygame.draw.rect(screen, DARK, (0, 0, w, h))
    for i in range(fw):
        for j in range(fh):
            for a in fields[i][j]:
                pygame.draw.circle(screen, a.color, (a.x, a.y), NODE_RADIUS)
    if DRAW_CONNECTIONS:
        for l in links:
            distance = ((l.b.x - l.a.x) ** 2 + (l.b.y - l.a.y) ** 2) ** 0.5
            link_color = ((l.a.color[0] + l.b.color[0]) / 2, (l.a.color[1] + l.b.color[1]) / 2,
                          (l.a.color[2] + l.b.color[2]) / 2)  # TODO: мб градиент цвета
            pygame.draw.line(screen, link_color, (Calc_coord_for_link(l.a.x, l.b.x), Calc_coord_for_link(l.a.y, l.b.y)),
                             (Calc_coord_for_link(l.b.x, l.a.x), Calc_coord_for_link(l.b.y, l.a.y)), math.floor(NODE_RADIUS / 2))
    if mouse[0] >= w and mouse[1] <= h / 5:
        pygame.draw.rect(screen, color_light, [w, 0, w + 150, h / 5])
    else:
        pygame.draw.rect(screen, color_dark, [w, 0, w + 150, h / 5])
    screen.blit(text, (w + 20, h / 10 - 5))
    pygame.display.update()
pygame.quit()
