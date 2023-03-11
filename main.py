import sys

import pygame.draw

from UserInterface import *
from Canvas import *


class Guy:
    def __init__(self, position, f_clr, t_clr):
        self.position = position
        self.f_clr = f_clr
        self.t_clr = t_clr
        self.can_reproduce = False
        try:
            if pygame.Color(canvas.surface.get_at(self.position)) == pygame.Color(self.f_clr):
                canvas.surface.set_at(self.position, self.t_clr)
                self.can_reproduce = True
        except IndexError:
            pass

    def do_thing(self):
        if self.can_reproduce:
            guys[-1].append(Guy((self.position[0]+1, self.position[1]), self.f_clr, self.t_clr))
            guys[-1].append(Guy((self.position[0]-1, self.position[1]), self.f_clr, self.t_clr))
            guys[-1].append(Guy((self.position[0], self.position[1]+1), self.f_clr, self.t_clr))
            guys[-1].append(Guy((self.position[0], self.position[1]-1), self.f_clr, self.t_clr))


def paint():
    if canvas.mouse_over:
        m_pos = (pygame.mouse.get_pos()[0]-canvas.position[0], pygame.mouse.get_pos()[1]-canvas.position[1])
        pygame.draw.circle(canvas.surface, color, m_pos, width_slider.value/2)
        pygame.draw.circle(canvas.surface, "#444444", m_pos, width_slider.value/2, 2)
    if canvas.clicked:
        canvas.o_pos = canvas.m_pos
        canvas.m_pos = (pygame.mouse.get_pos()[0]-canvas.position[0], pygame.mouse.get_pos()[1]-canvas.position[1])
        pygame.draw.circle(canvas.canvas, color, canvas.m_pos, width_slider.value/2)
        pygame.draw.line(canvas.canvas, color, canvas.m_pos, canvas.o_pos, width_slider.value+2)


def erase():
    if canvas.mouse_over:
        m_pos = (pygame.mouse.get_pos()[0]-canvas.position[0], pygame.mouse.get_pos()[1]-canvas.position[1])
        pygame.draw.circle(canvas.surface, canvas.color, m_pos, width_slider.value/2)
        pygame.draw.circle(canvas.surface, "#444444", m_pos, width_slider.value/2, 2)
    if canvas.clicked:
        canvas.o_pos = canvas.m_pos
        canvas.m_pos = (pygame.mouse.get_pos()[0]-canvas.position[0], pygame.mouse.get_pos()[1]-canvas.position[1])
        pygame.draw.line(canvas.canvas, canvas.color, canvas.m_pos, canvas.o_pos, width_slider.value+2)
        pygame.draw.circle(canvas.canvas, canvas.color, canvas.m_pos, width_slider.value/2)


def fill():
    global guys
    start = False
    if canvas.clicked_:
        guys.clear()
        guys.append([])
        if pygame.Color(canvas.surface.get_at(canvas.m_pos)) != pygame.Color(color):
            guys[0].append(Guy(canvas.m_pos, canvas.surface.get_at(canvas.m_pos), color))
        start = True
    while start:
        guys.append([])
        for guy in guys[-2]:
            guy.do_thing()
        if len(guys[-1]) == 0:
            guys.clear()
            start = False
    cc = canvas.surface.copy()
    cc.set_colorkey(canvas.color)
    canvas.canvas = cc


def pick_color():
    if canvas.mouse_over:
        m_pos = (pygame.mouse.get_pos()[0]-canvas.position[0], pygame.mouse.get_pos()[1]-canvas.position[1])
        try:
            pygame.draw.circle(canvas.surface, canvas.surface.get_at(m_pos), (m_pos[0]+20, m_pos[1]-20), 20)
        except IndexError:
            pass
        pygame.draw.circle(canvas.surface, "#444444", (m_pos[0]+20, m_pos[1]-20), 20, 2)
    if canvas.clicked:
        clr = canvas.surface.get_at(canvas.m_pos)
        red_slider.set_value(clr[0])
        green_slider.set_value(clr[1])
        blue_slider.set_value(clr[2])


def canvas_():
    if canvas.clicked:
        cc = canvas.surface.copy()
        cc.set_colorkey(canvas.color)
        canvas.canvas = cc
        canvas.color = color


def save():
    pygame.image.save(canvas.surface, "C:/Users/dell/Documents/MyPaint/"+text_input.text+".png")


def load():
    global warning_visible
    try:
        canvas.canvas = pygame.image.load("C:/Users/dell/Documents/MyPaint/"+text_input.text+".png").copy()
        warning_visible = False
    except FileNotFoundError:
        warning_visible = True


pygame.init()

screen = pygame.display.set_mode((995, 750))
pygame.display.set_caption("My Paint")
pygame.display.set_icon(pygame.image.load("images/icon.png"))

pygame.mouse.in_use = False

clock = pygame.time.Clock()
FPS = 60

canvas = Canvas()

paint_button = ToggleableButton((820, 95), pygame.image.load("images/paint.png"), paint)
fill_button = ToggleableButton((900, 95), pygame.image.load("images/fill bucket.png"), fill)
eraser_button = ToggleableButton((820, 165), pygame.image.load("images/eraser.png"), erase)
colorPicker_button = ToggleableButton((900, 165), pygame.image.load("images/color picker.png"), pick_color)
canvas_button = ToggleableButton((865, 235), pygame.image.load("images/canvas.png"), canvas_)

paint_button.linked_with = [fill_button, eraser_button, colorPicker_button, canvas_button]
fill_button.linked_with = [paint_button, eraser_button, colorPicker_button, canvas_button]
eraser_button.linked_with = [fill_button, paint_button, colorPicker_button, canvas_button]
colorPicker_button.linked_with = [fill_button, eraser_button, paint_button, canvas_button]
canvas_button.linked_with = [paint_button, fill_button, eraser_button, colorPicker_button]

width_slider = Slider((780, 315), "Width", 0, 50, "#000000")
red_slider = Slider((780, 365), "Red", 0, 255, "#ff0000")
green_slider = Slider((780, 415), "Green", 0, 255, "#00ff00")
blue_slider = Slider((780, 465), "Blue", 0, 255, "#0000ff")

save_button = Button((810, 600), "save", save)
load_button = Button((810, 630), "load", load)

text_input = TextInput((780, 680))

warning = pygame.font.Font("freesansbold.ttf", 10).render("! FILE NOT FOUND", True, "#ff0000")
warning_visible = False

color = (0, 0, 0)

guys = []

if __name__ == '__main__':
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            text_input.update(event)

        screen.fill("#2b2b2b")

        pygame.draw.rect(screen, "#000000", pygame.Rect(750, 15, 230, 720), 10)
        pygame.draw.rect(screen, "darkslategray", pygame.Rect(760, 25, 210, 700))

        paint_button.draw(screen)
        fill_button.draw(screen)
        eraser_button.draw(screen)
        colorPicker_button.draw(screen)
        canvas_button.draw(screen)

        width_slider.draw(screen)
        red_slider.draw(screen)
        green_slider.draw(screen)
        blue_slider.draw(screen)

        save_button.draw(screen)
        load_button.draw(screen)

        text_input.draw(screen)

        if warning_visible:
            screen.blit(warning, (780, 703))

        color = (red_slider.value, green_slider.value, blue_slider.value)

        pygame.draw.rect(screen, "black", pygame.Rect(815, 485, 100, 100), 5)
        pygame.draw.rect(screen, color, pygame.Rect(820, 490, 90, 90))

        paint_button.update()
        fill_button.update()
        eraser_button.update()
        colorPicker_button.update()
        canvas_button.update()

        width_slider.update()
        red_slider.update()
        green_slider.update()
        blue_slider.update()

        save_button.update()
        load_button.update()

        canvas.draw(screen)
        canvas.update()

        clock.tick(FPS)
        pygame.display.flip()
