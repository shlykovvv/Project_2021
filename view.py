import pygame
import math
from constants import WIDTH, HEIGHT
import ui
from model import deltaW, deltaH


def draw_particles(fields):
    for i in range(deltaW):
        for j in range(deltaH):
            for a in fields[i][j]:
                pygame.draw.circle(ui.screen, a.color, (a.x, a.y), ui.NODE_RADIUS)


def calc_coord_for_link(z1, z2, dist):
    return z1 + (z2 - z1) * ui.NODE_RADIUS / dist


def draw_links(links):
    for link in links:
        dist = ((link.b.x - link.a.x) ** 2 + (link.b.y - link.a.y) ** 2) ** 0.5
        link_color = ((link.a.color[0] + link.b.color[0]) / 2, (link.a.color[1] + link.b.color[1]) / 2,
                      (link.a.color[2] + link.b.color[2]) / 2)
        pygame.draw.line(ui.screen, link_color,
                         (calc_coord_for_link(link.a.x, link.b.x, dist), calc_coord_for_link(link.a.y, link.b.y, dist)),
                         (calc_coord_for_link(link.b.x, link.a.x, dist), calc_coord_for_link(link.b.y, link.a.y, dist)),
                         math.floor(ui.NODE_RADIUS / 2))


def draw_settings():
    surf = pygame.Surface((WIDTH, HEIGHT))
    surf.set_alpha(140)
    pygame.draw.rect(surf, 'white', (20, 20, 240, HEIGHT - 40))
    ui.screen.blit(surf, (0, 0))


def draw_closed_settings():
    surf = pygame.Surface((WIDTH, HEIGHT))
    surf.set_alpha(160)
    pygame.draw.rect(surf, 'white', (20, 20, 20, 20))
    pygame.draw.rect(surf, (150, 150, 150), (22, 28, 16, 4))
    pygame.draw.rect(surf, (150, 150, 150), (28, 22, 4, 16))
    ui.screen.blit(surf, (0, 0))


def print_text():
    font = pygame.font.SysFont(None, 20)
    small_font = pygame.font.SysFont(None, 12)
    medium_font = pygame.font.SysFont(None, 16)
    text_create = font.render('CREATE NEW WORLD', True, (0, 0, 0))
    text_close = font.render('CLOSE SETTINGS', True, (0, 0, 0))
    text_current = font.render('CURRENT WORLD SETTINGS', True, (0, 0, 0))
    text_new = font.render('NEW WORLD SETTINGS', True, (0, 0, 0))
    text_brush = font.render('PARTICLE BRUSH', True, (0, 0, 0))
    text_force = small_font.render('LINK FORCE:', True, (70, 70, 70))
    text_radius = small_font.render('PARTICLE RADIUS:', True, (70, 70, 70))
    text_speed = small_font.render('PARTICLE SPEED:', True, (70, 70, 70))
    text_frame = small_font.render('SIMULATIONS PER FRAME:', True, (70, 70, 70))
    text_types = small_font.render('PARTICLE TYPES AMOUNT:', True, (70, 70, 70))
    text_count = small_font.render('PARTICLE COUNT:', True, (70, 70, 70))
    text_connect = medium_font.render('DRAW CONNECTIONS', True, (0, 0, 0))
    ui.screen.blit(text_create, (70, 361))
    ui.screen.blit(text_close, (82, 53))
    ui.screen.blit(text_current, (30, 90))
    ui.screen.blit(text_new, (30, 261))
    ui.screen.blit(text_brush, (30, 400))
    ui.screen.blit(text_force, (30, 108))
    ui.screen.blit(text_radius, (30, 138))
    ui.screen.blit(text_speed, (30, 168))
    ui.screen.blit(text_frame, (30, 198))
    ui.screen.blit(text_types, (30, 280))
    ui.screen.blit(text_count, (30, 310))
    ui.screen.blit(text_connect, (60, 235))
