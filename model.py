import random
import math
from ui import NUMBER_OF_TYPES, NODE_COUNT
from constants import COLORS, WIDTH, HEIGHT, NODE_RADIUS, LINK_FORCE, SPEED, MAX_DIST, BORDER


MAX_DIST2 = MAX_DIST * MAX_DIST
deltaW = WIDTH // MAX_DIST + 1
deltaH = HEIGHT // MAX_DIST + 1


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


LINKS, LINKS_POSSIBLE, COUPLING = [], [], []
links, fields = [], []


def generate_rules():
    global LINKS, LINKS_POSSIBLE, COUPLING
    LINKS, LINKS_POSSIBLE, COUPLING = [], [], []
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


def add_particle(type, x, y):
    p = Particle(type, x, y)
    fields[round(p.x / MAX_DIST)][round(p.y / MAX_DIST)].append(p)
    return p


def create_new_world():
    generate_rules()
    global fields, links
    fields = [0] * deltaW  # array for dividing scene into parts to reduce complexity
    for i in range(deltaW):
        fields[i] = [0] * deltaH
        for j in range(deltaH):
            fields[i][j] = []
    links = []
    for i in range(NODE_COUNT):  # put particles randomly
        add_particle(random.randint(0, NUMBER_OF_TYPES - 1), random.random() * (WIDTH - 2 * NODE_RADIUS) +
                     NUMBER_OF_TYPES, random.random() * (HEIGHT - 2 * NODE_RADIUS) + NUMBER_OF_TYPES)


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


def mmmodel():
    for i in range(deltaW):
        for j in range(deltaH):
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
                elif a.x > WIDTH - BORDER:
                    a.sx -= SPEED * 0.05
                    if a.x > WIDTH:
                        a.x = WIDTH * 2 - a.x
                        a.sx *= -0.5
                if a.y < BORDER:
                    a.sy += SPEED * 0.05
                    if a.y < 0:
                        a.y = -a.y
                        a.sy *= -0.5
                elif a.y > HEIGHT - BORDER:
                    a.sy -= SPEED * 0.05
                    if a.y > HEIGHT:
                        a.y = HEIGHT * 2 - a.y
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
    for i in range(deltaW):
        for j in range(deltaH):
            for a in fields[i][j]:
                if (round(a.x / MAX_DIST) != i) or (round(a.y / MAX_DIST) != j):
                    fields[i][j].remove(a)
                    fields[round(a.x / MAX_DIST)][round(a.y / MAX_DIST)].append(a)

    # dividing scene into parts to reduce complexity
    for i in range(deltaW):
        for j in range(deltaH):
            for a in fields[i][j]:
                particleToLink = 0
                particleToLinkMinDist2 = (WIDTH + HEIGHT) * (WIDTH + HEIGHT)
                for b in fields[i][j]:
                    if b != a:
                        d2 = applyForce(a, b)
                        if d2 != -1 and d2 < particleToLinkMinDist2:
                            particleToLinkMinDist2 = d2
                            particleToLink = b
                if i < deltaW - 1:
                    iNext = i + 1
                    for b in fields[iNext][j]:
                        d2 = applyForce(a, b)
                        if d2 != -1 and d2 < particleToLinkMinDist2:
                            particleToLinkMinDist2 = d2
                            particleToLink = b
                if j < deltaH - 1:
                    jNext = j + 1
                    for b in fields[i][jNext]:
                        d2 = applyForce(a, b)
                        if d2 != -1 and d2 < particleToLinkMinDist2:
                            particleToLinkMinDist2 = d2
                            particleToLink = b
                    if i < deltaW - 1:
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