import random
import math
import ui
from constants import COLORS, WIDTH, HEIGHT, MAX_DIST, BORDER

# Maximum interaction distance between particles
MAX_DIST2 = MAX_DIST * MAX_DIST
# Values for dividing the screen into rectangular fields
deltaW = WIDTH // MAX_DIST + 1
deltaH = HEIGHT // MAX_DIST + 1

# Matrices responsible for the laws of the world
LINKS, LINKS_POSSIBLE, COUPLING = [], [], []
# A list of all links, a list of all fields (the screen is divided into fields to reduce complexity)
links, fields = [], []


class Particle:
    """
    This class is responsible for the particle, her movement and attributes
    """
    def __init__(self, particle_type, x, y):
        """
        Initializes an object of the Particle class, adds it to the field appropriate to its position
        :param particle_type: the type of particle responsible for its distinctive features
        :param x: horizontal position
        :param y: vertical position
        """
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
        """
        Moves the particle according to its velocity, reflects it off the walls
        """
        self.x += self.vx
        self.y += self.vy
        # Deceleration due to friction force
        self.vx *= 0.98
        self.vy *= 0.98

        # Prevention of abnormal speeds
        magnitude = math.sqrt(self.vx * self.vx + self.vy * self.vy)
        if magnitude > 1:
            self.vx /= magnitude
            self.vy /= magnitude

        # Reflection from the walls
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

    def check_to_change_field(self, i, j):
        """
        Checks whether the particle needs to be transferred to another field, and does so if necessary
        :param i: the horizontal index of the field
        :param j: the vertical index of the field
        """
        if (round(self.x / MAX_DIST) != i) or (round(self.y / MAX_DIST) != j):
            fields[i][j].remove(self)
            fields[round(self.x / MAX_DIST)][round(self.y / MAX_DIST)].append(self)


class Link:
    """
    This class is responsible for the connections between particles
    """
    def __init__(self, a, b):
        """
        Initializes the connection
        :param a: the first particle of the bond
        :param b: the second particle of the bond
        """
        self.a = a
        self.b = b

    def break_or_attract(self):
        """
        Checks whether it is necessary to break the connection. Calculates the attraction caused by the bond
        """
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
    LINKS = [3, 0, 1]
    LINKS_POSSIBLE = [[2, 0, 1], [3, 0, 2], [3, 2, 0]]
    COUPLING = [[0, -1, -1], [1, 1, 0], [0, -1, -1]]
    LINKS = [1, 1]
    LINKS_POSSIBLE = [[0, 0], [0, 0]]
    COUPLING = [[-1, 1], [-1, 0]]
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
    return canlink


def calc_interaction(a: Particle, b: Particle, distance2):
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


def search_to_link_and_interact(a, b, particle_to_link, min_dist2):
    distance2 = (a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y)
    calc_interaction(a, b, distance2)
    if distance2 < min_dist2:
        if check_canlink(a, b, distance2):
            return b, distance2
        else:
            return particle_to_link, min_dist2
    else:
        return particle_to_link, min_dist2


def mmmodel():
    for link in links:
        link.break_or_attract()

    for i in range(deltaW):
        for j in range(deltaH):
            for a in fields[i][j]:
                particle_to_link = 0
                min_dist2 = (WIDTH + HEIGHT) ** 2
                for b in fields[i][j]:
                    if b != a:
                        particle_to_link, min_dist2 = search_to_link_and_interact(a, b, particle_to_link, min_dist2)
                if i < deltaW - 1:
                    i_next = i + 1
                    for b in fields[i_next][j]:
                        particle_to_link, min_dist2 = search_to_link_and_interact(a, b, particle_to_link, min_dist2)
                if j < deltaH - 1:
                    j_next = j + 1
                    for b in fields[i][j_next]:
                        particle_to_link, min_dist2 = search_to_link_and_interact(a, b, particle_to_link, min_dist2)
                    if i < deltaW - 1:
                        i_next = i + 1
                        for b in fields[i_next][j_next]:
                            particle_to_link, min_dist2 = search_to_link_and_interact(a, b, particle_to_link, min_dist2)
                    if i > 0:
                        i_prev = i - 1
                        for b in fields[i_prev][j_next]:
                            particle_to_link, min_dist2 = search_to_link_and_interact(a, b, particle_to_link, min_dist2)
                if particle_to_link != 0:
                    a.bonds.append(particle_to_link)
                    particle_to_link.bonds.append(a)
                    a.links_number += 1
                    particle_to_link.links_number += 1
                    links.append(Link(a, particle_to_link))

                a.move()
                a.check_to_change_field(i, j)
