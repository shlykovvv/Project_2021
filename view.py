import pygame
import math
from constants import WIDTH, HEIGHT, COLORS
import ui
from model import deltaW, deltaH


def draw_particles(fields):
    """this function draws all particles"""
    for i in range(deltaW):
        for j in range(deltaH):
            for a in fields[i][j]:
                pygame.draw.circle(ui.screen, a.color, (a.x, a.y), ui.NODE_RADIUS)


def calc_coord_for_link(z1, z2, dist):
    """this function calculates the coordinate of link"""
    return z1 + (z2 - z1) * ui.NODE_RADIUS / dist


def draw_links(links):
    """this function draws all links"""
    for link in links:
        dist = ((link.b.x - link.a.x) ** 2 + (link.b.y - link.a.y) ** 2) ** 0.5
        link_color = ((link.a.color[0] + link.b.color[0]) / 2, (link.a.color[1] + link.b.color[1]) / 2,
                      (link.a.color[2] + link.b.color[2]) / 2)
        pygame.draw.line(ui.screen, link_color,
                         (calc_coord_for_link(link.a.x, link.b.x, dist), calc_coord_for_link(link.a.y, link.b.y, dist)),
                         (calc_coord_for_link(link.b.x, link.a.x, dist), calc_coord_for_link(link.b.y, link.a.y, dist)),
                         math.floor(ui.NODE_RADIUS / 2))


def draw_settings():
    """this function draws translucent plane for all settings"""
    surf = pygame.Surface((WIDTH, HEIGHT))
    surf.set_alpha(140)
    pygame.draw.rect(surf, 'white', (20, 20, 240, HEIGHT - 40))
    ui.screen.blit(surf, (0, 0))


def draw_closed_settings():
    """this function draws the version of closed settings"""
    surf = pygame.Surface((WIDTH, HEIGHT))
    surf.set_alpha(160)
    pygame.draw.rect(surf, 'white', (20, 20, 20, 20))
    pygame.draw.rect(surf, (150, 150, 150), (22, 28, 16, 4))
    pygame.draw.rect(surf, (150, 150, 150), (28, 22, 4, 16))
    ui.screen.blit(surf, (0, 0))


def print_text():
    """this function prints all texts that are needed in settings"""
    font = pygame.font.SysFont(None, 20)
    small_font = pygame.font.SysFont(None, 12)
    medium_font = pygame.font.SysFont(None, 16)
    text_create = font.render('CREATE NEW WORLD', True, (0, 0, 0))
    text_close = font.render('CLOSE SETTINGS', True, (0, 0, 0))
    text_current = font.render('CURRENT WORLD SETTINGS', True, (0, 0, 0))
    text_new = font.render('NEW WORLD SETTINGS', True, (0, 0, 0))
    text_brush = font.render('PARTICLE BRUSH', True, (0, 0, 0))
    text_force = small_font.render('LINK FORCE: ' + str(int(- ui.LINK_FORCE * 1000)), True, (70, 70, 70))
    text_radius = small_font.render('PARTICLE RADIUS: ' + str(ui.NODE_RADIUS), True, (70, 70, 70))
    text_speed = small_font.render('PARTICLE SPEED: ' + str(ui.SPEED), True, (70, 70, 70))
    text_frame = small_font.render('SIMULATIONS PER FRAME: ' + str(ui.SIMULATIONS_PER_FRAME), True, (70, 70, 70))
    text_types = small_font.render('PARTICLE TYPES AMOUNT: ' + str(ui.NUMBER_OF_TYPES), True, (70, 70, 70))
    text_count = small_font.render('PARTICLE COUNT: ' + str(ui.NODE_COUNT), True, (70, 70, 70))
    text_connect = medium_font.render('DRAW CONNECTIONS', True, (0, 0, 0))
    text_save = medium_font.render('SAVE AS', True, (0, 0, 0))
    text_open = medium_font.render('OPEN FILE', True, (0, 0, 0))
    ui.screen.blit(text_create, (70, 361))
    ui.screen.blit(text_close, (49, 53))
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
    ui.screen.blit(text_save, (193, 44))
    ui.screen.blit(text_open, (188, 66))


def draw_buttons(mouse):
    """this function draws buttons light or dark depending on mouse's coordinates"""
    if 30 <= mouse[0] <= 250 and 347 <= mouse[1] <= 387:
        pygame.draw.rect(ui.screen, ui.color_light, [30, 347, 220, 40])
    else:
        pygame.draw.rect(ui.screen, ui.color_dark, [30, 347, 220, 40])
    if 30 <= mouse[0] <= 180 and 40 <= mouse[1] <= 80:
        pygame.draw.rect(ui.screen, ui.color_light, [30, 40, 150, 40])
    else:
        pygame.draw.rect(ui.screen, ui.color_dark, [30, 40, 150, 40])
    if 184 <= mouse[0] <= 250 and 40 <= mouse[1] <= 58:
        pygame.draw.rect(ui.screen, ui.color_light, [184, 40, 66, 18])
    else:
        pygame.draw.rect(ui.screen, ui.color_dark, [184, 40, 66, 18])
    if 184 <= mouse[0] <= 250 and 62 <= mouse[1] <= 80:
        pygame.draw.rect(ui.screen, ui.color_light, [184, 62, 66, 18])
    else:
        pygame.draw.rect(ui.screen, ui.color_dark, [184, 62, 66, 18])


def draw_controllers():
    """this function draws all kinds of controllers"""
    for s in ui.controllers:
        if s != 'connections' and s != 'brush':
            pygame.draw.rect(ui.screen, (150, 150, 150), [30, ui.controllers[s]['y'], 220, 6])
            pygame.draw.rect(ui.screen, (100, 100, 100), [ui.controllers[s]['x'], ui.controllers[s]['y'] - 3, 8, 12])
        if s == 'connections':
            pygame.draw.rect(ui.screen, ui.color_dark, [30, 230, 20, 20])
            if ui.controllers[s]:
                pygame.draw.polygon(ui.screen, 'white',
                                    [(36, 250), (30, 244), (32, 242), (36, 246), (48, 230), (50, 232)])
        if s == 'brush':
            for i in range(ui.NUMBER_OF_TYPES):
                pygame.draw.rect(ui.screen, COLORS[i],
                                 [30 + i * 220 / ui.NUMBER_OF_TYPES, 420, 220 / ui.NUMBER_OF_TYPES + 1, 40])
            x = 21 + ui.controllers[s] * 220 / ui.NUMBER_OF_TYPES + 110 / ui.NUMBER_OF_TYPES
            pygame.draw.polygon(ui.screen, 'white',
                                [(x+6, 450), (x, 444), (x+2, 442), (x+6, 446), (x+16, 430), (x+18, 432)])
