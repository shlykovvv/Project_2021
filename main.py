import pygame
import pygame.draw
import model
from constants import WIDTH, HEIGHT, FPS, BACKGROUND_COLOR
import view
import ui

model.create_new_world()

pygame.init()
pygame.display.update()
clock = pygame.time.Clock()
finished = False
opened = True

while not finished:
    clock.tick(FPS)
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mouse[0] <= WIDTH and mouse[1] <= HEIGHT:
                model.Particle(ui.type_for_click, mouse[0], mouse[1])
            if 30 <= mouse[0] <= 250:
                ui.controllers_info(mouse)
                if 40 <= mouse[1] <= 80 and opened:
                    opened = False
                if 347 <= mouse[1] <= 387:
                    model.create_new_world()
            if 20 <= mouse[0] <= 40 and 20 <= mouse[1] <= 40 and not opened:
                opened = True
    ui.screen.fill(BACKGROUND_COLOR)
    for i in range(ui.SIMULATIONS_PER_FRAME):
        model.mmmodel()
    view.draw_particles(model.fields)
    if ui.DRAW_CONNECTIONS:
        view.draw_links(model.links)
    if opened:
        view.draw_settings()
        ui.draw_controllers()
        ui.draw_buttons(mouse)
        view.print_text()
    else:
        view.draw_closed_settings()
    pygame.display.update()
pygame.quit()
