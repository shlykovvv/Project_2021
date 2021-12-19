import random
import math
import ui
from constants import COLORS, WIDTH, HEIGHT, MAX_DIST, BORDER


MAX_DIST2 = MAX_DIST * MAX_DIST
deltaW = WIDTH // MAX_DIST + 1
deltaH = HEIGHT // MAX_DIST + 1


class Link:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def break_or_attract(self):
        dist2 = (self.a.x - self.b.x) ** 2 + (self.a.y - self.b.y) ** 2
        if dist2 > MAX_DIST2 / 4:
            self.a.links_number -= 1
            self.b.links_number -= 1
            self.a.bonds.remove(self.b)
            self.b.bonds.remove(self.a)
            links.remove(self)
        elif dist2 > ui.NODE_RADIUS * ui.NODE_RADIUS * 4:
            angle = math.atan2(self.a.y - self.b.y, self.a.x - self.b.x)
            self.a.vx += math.cos(angle) * ui.LINK_FORCE * ui.SPEED
            self.a.vy += math.sin(angle) * ui.LINK_FORCE * ui.SPEED
            self.b.vx -= math.cos(angle) * ui.LINK_FORCE * ui.SPEED
            self.b.vy -= math.sin(angle) * ui.LINK_FORCE * ui.SPEED


class Particle:
    def __init__(self, particle_type, x, y):
        self.type = particle_type
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
            self.vx += ui.SPEED * 0.05
            if self.x < 0:
                self.x = -self.x
                self.vx *= -0.5
        elif self.x > WIDTH - BORDER:
            self.vx -= ui.SPEED * 0.05
            if self.x > WIDTH:
                self.x = WIDTH * 2 - self.x
                self.vx *= -0.5
        if self.y < BORDER:
            self.vy += ui.SPEED * 0.05
            if self.y < 0:
                self.y = -self.y
                self.vy *= -0.5
        elif self.y > HEIGHT - BORDER:
            self.vy -= ui.SPEED * 0.05
            if self.y > HEIGHT:
                self.y = HEIGHT * 2 - self.y
                self.vy *= -0.5


LINKS, LINKS_POSSIBLE, COUPLING = [], [], []
links, fields = [], []


def generate_rules():
    global LINKS, LINKS_POSSIBLE, COUPLING
    LINKS, LINKS_POSSIBLE, COUPLING = [], [], []
    for i in range(ui.NUMBER_OF_TYPES):
        LINKS.append(math.floor(random.random() * 4))
        COUPLING.append([])
        LINKS_POSSIBLE.append([])
        for j in range(ui.NUMBER_OF_TYPES):
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
    for i in range(ui.NODE_COUNT):  # put particles randomly
        Particle(random.randint(0, ui.NUMBER_OF_TYPES - 1), random.random() * (WIDTH - 2 * ui.NODE_RADIUS) +
                 ui.NUMBER_OF_TYPES, random.random() * (HEIGHT - 2 * ui.NODE_RADIUS) + ui.NUMBER_OF_TYPES)


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
        if distance2 < ui.NODE_RADIUS * ui.NODE_RADIUS * 4:
            if distance2 < 1:
                distance2 = 1
            a_force = 1 / distance2
            b_force = 1 / distance2
        angle = math.atan2(a.y - b.y, a.x - b.x)
        a.vx += math.cos(angle) * a_force * ui.SPEED
        a.vy += math.sin(angle) * a_force * ui.SPEED
        b.vx -= math.cos(angle) * b_force * ui.SPEED
        b.vy -= math.sin(angle) * b_force * ui.SPEED


def mmmodel():
    for link in links:
        link.break_or_attract()

    for i in range(deltaW):
        for j in range(deltaH):
            for a in fields[i][j]:
                particle_to_link = 0
                particle_to_link_min_dist2 = (WIDTH + HEIGHT) ** 2
                for b in fields[i][j]:
                    if b != a:
                        distance2 = (a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y)
                        calc_interactions(a, b, distance2)
                        d2 = check_canlink(a, b, distance2)
                        if d2 != -1 and d2 < particle_to_link_min_dist2:
                            particle_to_link_min_dist2 = d2
                            particle_to_link = b
                if i < deltaW - 1:
                    i_next = i + 1
                    for b in fields[i_next][j]:
                        distance2 = (a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y)
                        calc_interactions(a, b, distance2)
                        d2 = check_canlink(a, b, distance2)
                        if d2 != -1 and d2 < particle_to_link_min_dist2:
                            particle_to_link_min_dist2 = d2
                            particle_to_link = b
                if j < deltaH - 1:
                    j_next = j + 1
                    for b in fields[i][j_next]:
                        distance2 = (a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y)
                        calc_interactions(a, b, distance2)
                        d2 = check_canlink(a, b, distance2)
                        if d2 != -1 and d2 < particle_to_link_min_dist2:
                            particle_to_link_min_dist2 = d2
                            particle_to_link = b
                    if i < deltaW - 1:
                        i_next = i + 1
                        for b in fields[i_next][j_next]:
                            distance2 = (a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y)
                            calc_interactions(a, b, distance2)
                            d2 = check_canlink(a, b, distance2)
                            if d2 != -1 and d2 < particle_to_link_min_dist2:
                                particle_to_link_min_dist2 = d2
                                particle_to_link = b
                    if i > 0:
                        i_prev = i - 1
                        for b in fields[i_prev][j_next]:
                            distance2 = (a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y)
                            calc_interactions(a, b, distance2)
                            d2 = check_canlink(a, b, distance2)
                            if d2 != -1 and d2 < particle_to_link_min_dist2:
                                particle_to_link_min_dist2 = d2
                                particle_to_link = b
                if particle_to_link != 0:
                    a.bonds.append(particle_to_link)
                    particle_to_link.bonds.append(a)
                    a.links_number += 1
                    particle_to_link.links_number += 1
                    links.append(Link(a, particle_to_link))
                a.move()
                # moving particle to another field
                if (round(a.x / MAX_DIST) != i) or (round(a.y / MAX_DIST) != j):
                    fields[i][j].remove(a)
                    fields[round(a.x / MAX_DIST)][round(a.y / MAX_DIST)].append(a)
