import pygame.draw
import model
from constants import FPS, BACKGROUND_COLOR
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
            if opened and not (20 <= mouse[0] <= 260 and 20 <= mouse[1] <= 480):
                model.Particle(ui.type_for_click, mouse[0], mouse[1])
            elif not opened and not (20 <= mouse[0] <= 40 and 20 <= mouse[1] <= 40):
                model.Particle(ui.type_for_click, mouse[0], mouse[1])
            if 30 <= mouse[0] <= 250:
                if 40 <= mouse[1] <= 80 and 30 <= mouse[0] <= 180 and opened:
                    opened = False
                if 347 <= mouse[1] <= 387 and opened:
                    model.create_new_world()
            if 184 <= mouse[0] <= 250 and 62 <= mouse[1] <= 80 and opened:
                model.open_world()
            if 184 <= mouse[0] <= 250 and 40 <= mouse[1] <= 58:
                ui.write_laws_to_file("output.txt", model.LINKS, model.LINKS_POSSIBLE, model.COUPLING)
            if 20 <= mouse[0] <= 40 and 20 <= mouse[1] <= 40 and not opened:
                opened = True
        pressed = pygame.mouse.get_pressed()
        if pressed[0] and opened:
            if 30 <= mouse[0] <= 250:
                ui.change_controllers(mouse)
            ui.change_characteristics()
    ui.screen.fill(BACKGROUND_COLOR)
    for i in range(ui.SIMULATIONS_PER_FRAME):
        model.central_modeling()
    view.draw_particles(model.fields)
    if ui.controllers['connections']:
        view.draw_links(model.links)
    if opened:
        view.draw_settings()
        view.draw_controllers()
        view.draw_buttons(mouse)
        view.print_text()
    else:
        view.draw_closed_settings()
    pygame.display.update()
pygame.quit()
