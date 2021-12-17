import pygame
import math


FPS = 600  # TODO: узнать максимальное адекватное
w = 600
h = 400


screen = pygame.display.set_mode((w + 150, h))  # TODO: допокно для кнопок и регуляторов, нужно его улучшить и сделать красивым


def calc_coord_for_link(z1, z2, radius, dist):
    return z1 + (z2 - z1) * radius / dist


def draw_link(l, radius):
    dist = ((l.b.x - l.a.x) ** 2 + (l.b.y - l.a.y) ** 2) ** 0.5
    link_color = ((l.a.color[0] + l.b.color[0]) / 2, (l.a.color[1] + l.b.color[1]) / 2,
                  (l.a.color[2] + l.b.color[2]) / 2)  # TODO: мб градиент цвета
    pygame.draw.line(screen, link_color,
                     (calc_coord_for_link(l.a.x, l.b.x, radius, dist), calc_coord_for_link(l.a.y, l.b.y, radius, dist)),
                     (calc_coord_for_link(l.b.x, l.a.x, radius, dist), calc_coord_for_link(l.b.y, l.a.y, radius, dist)),
                     math.floor(radius / 2))


