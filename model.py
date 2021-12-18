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
        self.vx = 0
        self.vy = 0
        self.links_number = 0
        self.bonds = []
        self.color = COLORS[self.type]
        fields[round(self.x / MAX_DIST)][round(self.y / MAX_DIST)].append(self)

    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.98
        self.vy *= 0.98
        # velocity normalization
        # idk if it is still necessary
        magnitude = math.sqrt(self.vx * self.vx + self.vy * self.vy)
        if magnitude > 1:
            self.vx /= magnitude
            self.vy /= magnitude

        # border repulsion
        if self.x < BORDER:
            self.vx += SPEED * 0.05
            if self.x < 0:
                self.x = -self.x
                self.vx *= -0.5
        elif self.x > WIDTH - BORDER:
            self.vx -= SPEED * 0.05
            if self.x > WIDTH:
                self.x = WIDTH * 2 - self.x
                self.vx *= -0.5
        if self.y < BORDER:
            self.vy += SPEED * 0.05
            if self.y < 0:
                self.y = -self.y
                self.vy *= -0.5
        elif self.y > HEIGHT - BORDER:
            self.vy -= SPEED * 0.05
            if self.y > HEIGHT:
                self.y = HEIGHT * 2 - self.y
                self.vy *= -0.5


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
        Particle(random.randint(0, NUMBER_OF_TYPES - 1), random.random() * (WIDTH - 2 * NODE_RADIUS) + NUMBER_OF_TYPES,
                 random.random() * (HEIGHT - 2 * NODE_RADIUS) + NUMBER_OF_TYPES)


def check_canlink(a: Particle, b: Particle, distance2):
    canlink = False
    if distance2 < MAX_DIST2 / 4:
        if a.links_number < LINKS[a.type] and b.links_number < LINKS[b.type]:
            if b not in a.bonds and a not in b.bonds:
                type_count_a = 0
                for p in a.bonds:
                    if p.type == b.type:
                        type_count_a += 1
                type_count_b = 0
                for p in b.bonds:
                    if p.type == a.type:
                        type_count_b += 1
                if type_count_a < LINKS_POSSIBLE[a.type][b.type] and type_count_b < LINKS_POSSIBLE[b.type][a.type]:
                    canlink = True
    if canlink:
        return distance2
    else:
        return -1


def calc_interactions(a: Particle, b: Particle, distance2):
    if distance2 < MAX_DIST2:
        a_force = COUPLING[a.type][b.type] / distance2
        b_force = COUPLING[b.type][a.type] / distance2
        if a.links_number >= LINKS[a.type] or b.links_number >= LINKS[b.type]:
            if b not in a.bonds and a not in b.bonds:
                a_force = 1 / distance2
                b_force = 1 / distance2
        if distance2 < NODE_RADIUS * NODE_RADIUS * 4:
            if distance2 < 1:
                distance2 = 1
            a_force = 1 / distance2
            b_force = 1 / distance2
        angle = math.atan2(a.y - b.y, a.x - b.x)
        a.vx += math.cos(angle) * a_force * SPEED
        a.vy += math.sin(angle) * a_force * SPEED
        b.vx -= math.cos(angle) * b_force * SPEED
        b.vy -= math.sin(angle) * b_force * SPEED


def mmmodel():
    for i in range(deltaW):
        for j in range(deltaH):
            for a in fields[i][j]:
                a.move()
    for link in links:
        a = link.a
        b = link.b
        d2 = (a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y)
        if d2 > MAX_DIST2 / 4:
            a.links_number -= 1
            b.links_number -= 1
            a.bonds.remove(b)
            b.bonds.remove(a)
            links.remove(link)
            i -= 1
        elif d2 > NODE_RADIUS * NODE_RADIUS * 4:
            angle = math.atan2(a.y - b.y, a.x - b.x)
            a.vx += math.cos(angle) * LINK_FORCE * SPEED
            a.vy += math.sin(angle) * LINK_FORCE * SPEED
            b.vx -= math.cos(angle) * LINK_FORCE * SPEED
            b.vy -= math.sin(angle) * LINK_FORCE * SPEED

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
                        distance2 = (a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y)
                        calc_interactions(a, b, distance2)
                        d2 = check_canlink(a, b, distance2)
                        if d2 != -1 and d2 < particleToLinkMinDist2:
                            particleToLinkMinDist2 = d2
                            particleToLink = b
                if i < deltaW - 1:
                    iNext = i + 1
                    for b in fields[iNext][j]:
                        distance2 = (a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y)
                        calc_interactions(a, b, distance2)
                        d2 = check_canlink(a, b, distance2)
                        if d2 != -1 and d2 < particleToLinkMinDist2:
                            particleToLinkMinDist2 = d2
                            particleToLink = b
                if j < deltaH - 1:
                    jNext = j + 1
                    for b in fields[i][jNext]:
                        distance2 = (a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y)
                        calc_interactions(a, b, distance2)
                        d2 = check_canlink(a, b, distance2)
                        if d2 != -1 and d2 < particleToLinkMinDist2:
                            particleToLinkMinDist2 = d2
                            particleToLink = b
                    if i < deltaW - 1:
                        iNext = i + 1
                        for b in fields[iNext][jNext]:
                            distance2 = (a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y)
                            calc_interactions(a, b, distance2)
                            d2 = check_canlink(a, b, distance2)
                            if d2 != -1 and d2 < particleToLinkMinDist2:
                                particleToLinkMinDist2 = d2
                                particleToLink = b
                if particleToLink != 0:
                    a.bonds.append(particleToLink)
                    particleToLink.bonds.append(a)
                    a.links_number += 1
                    particleToLink.links_number += 1
                    links.append(Link(a, particleToLink))
