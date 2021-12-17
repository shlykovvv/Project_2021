import pygame
import pygame.draw
import model
import color
from view import w, h, FPS, screen
import view
import ui


model.new_world()

pygame.init()
pygame.display.update()
clock = pygame.time.Clock()
finished = False
ui.create_button()

while not finished:
    clock.tick(FPS)
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mouse[0] >= w and mouse[1] <= h / 5:
                model.new_world()
    for i in range(ui.SIMULATIONS_PER_FRAME):
        model.mmmodel()
    pygame.draw.rect(screen, color.DARK_BACKGROUND, (0, 0, w, h))
    for i in range(model.fw):
        for j in range(model.fh):
            for a in model.fields[i][j]:
                pygame.draw.circle(screen, a.color, (a.x, a.y), model.NODE_RADIUS)
    if ui.DRAW_CONNECTIONS:
        for l in model.links:
            view.draw_link(l, model.NODE_RADIUS)
    ui.draw_button(mouse)
    pygame.display.update()
pygame.quit()
