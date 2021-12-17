import pygame
import math
from constants import WIDTH, HEIGHT, NODE_RADIUS, BACKGROUND_COLOR
import ui
from model import deltaW, deltaH


def draw_background():
    pygame.draw.rect(ui.screen, BACKGROUND_COLOR, (0, 0, WIDTH, HEIGHT))
    pygame.draw.rect(ui.screen, 'black', (WIDTH, 0, WIDTH + 150, HEIGHT))


def draw_particles(fields):
    for i in range(deltaW):
        for j in range(deltaH):
            for a in fields[i][j]:
                pygame.draw.circle(ui.screen, a.color, (a.x, a.y), NODE_RADIUS)


def calc_coord_for_link(z1, z2, dist):
    return z1 + (z2 - z1) * NODE_RADIUS / dist


def draw_links(links):
    for link in links:
        dist = ((link.b.x - link.a.x) ** 2 + (link.b.y - link.a.y) ** 2) ** 0.5
        link_color = ((link.a.color[0] + link.b.color[0]) / 2, (link.a.color[1] + link.b.color[1]) / 2,
                      (link.a.color[2] + link.b.color[2]) / 2)
        pygame.draw.line(ui.screen, link_color,
                         (calc_coord_for_link(link.a.x, link.b.x, dist), calc_coord_for_link(link.a.y, link.b.y, dist)),
                         (calc_coord_for_link(link.b.x, link.a.x, dist), calc_coord_for_link(link.b.y, link.a.y, dist)),
                         math.floor(NODE_RADIUS / 2))
