import sys
import pygame.mouse
from GUI import *


class Canvas:
    def __init__(self):
        self.size = (700, 700)
        self.position = (25, 25)

        self.surface = pygame.Surface(self.size)
        self.surface_rect = self.surface.get_rect()
        self.surface_rect.topleft = self.position

        self.color = "#ffffff"
        self.surface.fill(self.color)

        self.canvas = pygame.Surface(self.size, pygame.SRCALPHA)
        self.surface.blit(self.canvas, (0, 0))

        self.m_pos = (0, 0)
        self.o_pos = (0, 0)

        self.mouse_over = False
        self.clicked = False
        self.clicked_ = False

    def draw(self, _screen_):
        pygame.draw.rect(
            _screen_, "#000000",
            pygame.Rect(self.position[0]-10, self.position[1]-10, self.size[0]+20, self.size[1]+20), 10
        )
        _screen_.blit(self.surface, self.surface_rect)

    def update(self):
        global mouse_in_use
        self.surface.fill(self.color)
        self.surface.blit(self.canvas, (0, 0))
        self.clicked_ = False

        self.mouse_over = self.surface_rect.collidepoint(pygame.mouse.get_pos())
        if self.mouse_over and pygame.mouse.get_pressed()[0] and not self.clicked and not mouse_in_use:
            mouse_in_use = True
            self.clicked = True
            self.m_pos = (pygame.mouse.get_pos()[0]-self.position[0], pygame.mouse.get_pos()[1]-self.position[1])
            self.o_pos = self.m_pos
            self.clicked_ = True
        if not pygame.mouse.get_pressed()[0]:
            pygame.mouse.in_use = False
            self.clicked = False


class Pixel:
    def __init__(self, position, from_clr, to_clr):
        self.position = position
        self.from_clr = from_clr
        self.to_clr = to_clr
        self.can_clone = False
        try:
            if pygame.Color(canvas.surface.get_at(self.position)) == pygame.Color(self.from_clr):
                canvas.surface.set_at(self.position, self.to_clr)
                self.can_clone = True
        except IndexError:
            pass

    def do_thing(self):
        if self.can_clone:
            fill_tool_pixels[-1].append(Pixel((self.position[0] + 1, self.position[1]), self.from_clr, self.to_clr))
            fill_tool_pixels[-1].append(Pixel((self.position[0] - 1, self.position[1]), self.from_clr, self.to_clr))
            fill_tool_pixels[-1].append(Pixel((self.position[0], self.position[1] + 1), self.from_clr, self.to_clr))
            fill_tool_pixels[-1].append(Pixel((self.position[0], self.position[1] - 1), self.from_clr, self.to_clr))


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
    global fill_tool_pixels
    start = False
    if canvas.clicked_:
        fill_tool_pixels.clear()
        fill_tool_pixels.append([])
        if pygame.Color(canvas.surface.get_at(canvas.m_pos)) != pygame.Color(color):
            fill_tool_pixels[0].append(Pixel(canvas.m_pos, canvas.surface.get_at(canvas.m_pos), color))
        start = True
    while start:
        fill_tool_pixels.append([])
        for guy in fill_tool_pixels[-2]:
            guy.do_thing()
        if len(fill_tool_pixels[-1]) == 0:
            fill_tool_pixels.clear()
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
    global files_screen
    files_screen = FilesScreen((520, 500), (250, 100), "MyPaintings", "save")


def load():
    global files_screen
    files_screen = FilesScreen((520, 500), (250, 100), "MyPaintings", "open")


if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode((995, 750))
    pygame.display.set_caption("My Paint")
    pygame.display.set_icon(pygame.image.load("images/icon.png"))

    pygame.mouse.in_use = False

    clock = pygame.time.Clock()
    FPS = 20

    canvas = Canvas()
    # __________________________________________________________________________________________________________________

    paint_button = ToggleableButton(
        (60, 60), (820, 95), image=pygame.image.load("images/paint.png"),
        background=["#ff9966", "#ffbb99", "#33ff77", "#80ffaa"],
        border_color=["#e64d00", "#ff7733", "#00cc44", "#00e64d"],
        border_width=4, border_radius=15, command=paint
    )
    fill_button = ToggleableButton(
        (60, 60), (900, 95), image=pygame.image.load("images/fill bucket.png"),
        background=["#ff9966", "#ffbb99", "#33ff77", "#80ffaa"],
        border_color=["#e64d00", "#ff7733", "#00cc44", "#00e64d"],
        border_width=4, border_radius=15, command=fill
    )
    eraser_button = ToggleableButton(
        (60, 60), (820, 165), image=pygame.image.load("images/eraser.png"),
        background=["#ff9966", "#ffbb99", "#33ff77", "#80ffaa"],
        border_color=["#e64d00", "#ff7733", "#00cc44", "#00e64d"],
        border_width=4, border_radius=15, command=erase
    )
    colorPicker_button = ToggleableButton(
        (60, 60), (900, 165), image=pygame.image.load("images/color picker.png"),
        background=["#ff9966", "#ffbb99", "#33ff77", "#80ffaa"],
        border_color=["#e64d00", "#ff7733", "#00cc44", "#00e64d"],
        border_width=4, border_radius=15, command=pick_color
    )
    canvas_button = ToggleableButton(
        (60, 60), (865, 235), image=pygame.image.load("images/canvas.png"),
        background=["#ff9966", "#ffbb99", "#33ff77", "#80ffaa"],
        border_color=["#e64d00", "#ff7733", "#00cc44", "#00e64d"],
        border_width=4, border_radius=15, command=canvas_
    )

    paint_button.linked_with = [fill_button, eraser_button, colorPicker_button, canvas_button]
    fill_button.linked_with = [paint_button, eraser_button, colorPicker_button, canvas_button]
    eraser_button.linked_with = [fill_button, paint_button, colorPicker_button, canvas_button]
    colorPicker_button.linked_with = [fill_button, eraser_button, paint_button, canvas_button]
    canvas_button.linked_with = [paint_button, fill_button, eraser_button, colorPicker_button]
    # __________________________________________________________________________________________________________________

    width_slider = Slider((780, 315), label="Width", min_value=0, max_value=50, color="#000000")
    red_slider = Slider((780, 365), label="Red", min_value=0, max_value=255, color="#ff0000")
    green_slider = Slider((780, 415), label="Green", min_value=0, max_value=255, color="#00ff00")
    blue_slider = Slider((780, 465), label="Blue", min_value=0, max_value=255, color="#0000ff")
    color = (0, 0, 0)
    # __________________________________________________________________________________________________________________

    save_button = Button((110, 25), (865, 612), text="save", command=save)
    load_button = Button((110, 25), (865, 642), text="load", command=load)
    # __________________________________________________________________________________________________________________

    files_screen: Union[FilesScreen, None] = None

    fill_tool_pixels = []
    while True:
        screen.fill("#2b2b2b")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if files_screen is not None:
                files_screen.update(pygame.mouse.get_pos(), event)
                if files_screen.return_value.split("|")[0] == "open":
                    try:
                        canvas.canvas = pygame.transform.scale(
                            pygame.image.load("MyPaintings/" + files_screen.return_value.split("|")[1]),
                            (700, 700))
                    except FileNotFoundError:
                        pass
                if files_screen.return_value.split("|")[0] == "save":
                    if files_screen.return_value.split("|")[1] != "" and os.path.splitext(files_screen.return_value) in [".png", ".jpg", ".jpeg"]:
                        pygame.image.save(canvas.surface, "MyPaintings/" + files_screen.return_value.split("|")[1])
                if files_screen.quit:
                    files_screen = None

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

        color = (red_slider.value, green_slider.value, blue_slider.value)

        pygame.draw.rect(screen, "black", pygame.Rect(815, 485, 100, 100), 5)
        pygame.draw.rect(screen, color, pygame.Rect(820, 490, 90, 90))
        if files_screen is None:
            paint_button.update(pygame.mouse.get_pos())
            fill_button.update(pygame.mouse.get_pos())
            eraser_button.update(pygame.mouse.get_pos())
            colorPicker_button.update(pygame.mouse.get_pos())
            canvas_button.update(pygame.mouse.get_pos())

            width_slider.update(pygame.mouse.get_pos())
            red_slider.update(pygame.mouse.get_pos())
            green_slider.update(pygame.mouse.get_pos())
            blue_slider.update(pygame.mouse.get_pos())

            save_button.update(pygame.mouse.get_pos())
            load_button.update(pygame.mouse.get_pos())

            canvas.update()

        canvas.draw(screen)

        if files_screen is not None:
            files_screen.draw(screen)

        update_mouse()

        clock.tick(FPS)
        pygame.display.flip()
