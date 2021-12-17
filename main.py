import pygame
import pygame.draw
import model
from constants import w, h, FPS
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
            if mouse[0] <= w and mouse[1] <= h:
                model.add_particle(ui.type_for_click, mouse[0], mouse[1])
            if mouse[0] >= w and mouse[1] <= h / 5:
                model.new_world()

    for i in range(ui.SIMULATIONS_PER_FRAME):
        model.mmmodel()
    view.draw_background()
    view.draw_particles(model.fields)
    if ui.DRAW_CONNECTIONS:
        view.draw_links(model.links)

    ui.draw_button(mouse)
    pygame.display.update()
pygame.quit()
