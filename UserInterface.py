import pygame


class ToggleableButton:
    def __init__(self, position, image, command):
        self.position = position
        self.size = (60, 60)

        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.surface_rect = self.surface.get_rect()
        self.surface_rect.center = self.position

        self.image = image
        self.image_rect = image.get_rect()
        self.image_rect.center = (self.size[0]/2, self.size[1]/2)

        self.rect = pygame.Rect(0, 0, self.size[0], self.size[1])

        self.linked_with = []

        self.command = command

        self.is_active = False
        self.clicked = False

        self.background = ["#ff9966", "#ffbb99", "#33ff77", "#80ffaa"]
        self.border_color = ["#e64d00", "#ff7733", "#00cc44", "#00e64d"]
        self.border_width = 4
        self.border_radius = 15

    def draw(self, screen):
        screen.blit(self.surface, self.surface_rect)

    def update(self):
        if self.is_active:
            self.command()

        if self.surface_rect.collidepoint(pygame.mouse.get_pos()) and not pygame.mouse.in_use:
            if self.is_active:
                pygame.draw.rect(self.surface, self.background[3], self.rect, 0, self.border_radius)
                pygame.draw.rect(self.surface, self.border_color[3], self.rect, self.border_width, self.border_radius)
            else:
                pygame.draw.rect(self.surface, self.background[1], self.rect, 0, self.border_radius)
                pygame.draw.rect(self.surface, self.border_color[1], self.rect, self.border_width, self.border_radius)

            if pygame.mouse.get_pressed()[0] and not self.clicked:
                is_active = False
                if not self.is_active:
                    for btn in self.linked_with:
                        btn.is_active = False
                    is_active = True
                    pygame.mouse.in_use = True
                self.is_active = is_active
                self.clicked = True
        else:
            if self.is_active:
                pygame.draw.rect(self.surface, self.background[2], self.rect, 0, self.border_radius)
                pygame.draw.rect(self.surface, self.border_color[2], self.rect, self.border_width, self.border_radius)
            else:
                pygame.draw.rect(self.surface, self.background[0], self.rect, 0, self.border_radius)
                pygame.draw.rect(self.surface, self.border_color[0], self.rect, self.border_width, self.border_radius)

        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False
            pygame.mouse.in_use = False

        self.surface.blit(self.image, self.image_rect)


class Slider:
    def __init__(self, position, label, min_value, max_value, color):
        self.position = position

        self.font = pygame.font.Font("freesansbold.ttf", 20)
        self.label = label

        self.min_value = min_value
        self.max_value = max_value
        self.value = min_value

        self.blob_x = self.position[0]-4

        self.color = color

        self.clicked = False

        self.length = 170
        self.width = 6

    def set_value(self, value):
        self.value = value
        self.blob_x = self.position[0]-4+self.length*(value-self.min_value)/(self.max_value-self.min_value)

    def update(self):
        cdtn = pygame.Rect(self.position[0], self.position[1]-9, self.length, 15).collidepoint(pygame.mouse.get_pos())
        if cdtn and not pygame.mouse.in_use:
            if pygame.mouse.get_pressed()[0]:
                self.clicked = True
                pygame.mouse.in_use = True
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False
            pygame.mouse.in_use = False
        if self.clicked:
            self.blob_x = pygame.mouse.get_pos()[0]-4
            if self.blob_x < self.position[0]-4:
                self.blob_x = self.position[0]-4
            if self.blob_x > self.position[0]+self.length-4:
                self.blob_x = self.position[0]+self.length-4
        self.value = int(self.min_value+(self.max_value-self.min_value)*(self.blob_x-self.position[0]+4)/self.length)

    def draw(self, screen):
        text = self.font.render(self.label + ": " + str(self.value), True, self.color)
        screen.blit(text, (self.position[0], self.position[1]-self.font.get_height()-12))

        surface = pygame.Surface((self.length, self.width))
        pygame.draw.line(surface, self.color, (0, 0), (self.length, 0), self.width)
        surface.set_alpha(150)
        screen.blit(surface, self.position)

        pygame.draw.rect(screen, self.color, pygame.Rect(self.blob_x, self.position[1]-5, 8, 16))
        pygame.draw.circle(screen, self.color, (self.blob_x+4, self.position[1]-5), 4)
        pygame.draw.circle(screen, self.color, (self.blob_x+4, self.position[1]+11), 4)


class Button:
    def __init__(self, position, text, command):
        size = (110, 25)

        self.button = pygame.Surface(size, pygame.SRCALPHA)
        self.button_rect = self.button.get_rect()
        self.button_rect.topleft = position
        self.rect = pygame.Rect(0, 0, size[0], size[1])

        self.background = ["#efefef", "#e5e5e5", "#f5f5f5"]
        self.foreground = ["#000000", "#000000", "#000000"]
        self.border_color = ["#000000", "#000000", "#000000"]

        self.border_width = 2

        self.font = pygame.font.Font("freesansbold.ttf", int(size[1] * 3 // 5))
        self.txt = text
        self.command = command

        self.clicked = False

    def draw(self, screen: pygame.Surface):
        screen.blit(self.button, self.button_rect)

    def update(self):
        mouse_position = pygame.mouse.get_pos()
        if self.button_rect.collidepoint(mouse_position):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                txt = self.font.render(self.txt, True, self.foreground[2])
                txt_rect = txt.get_rect()
                txt_rect.center = (self.rect.width / 2, self.rect.height / 2)
                pygame.draw.rect(self.button, self.background[2], self.rect, 0, 4)
                pygame.draw.rect(self.button, self.border_color[2], self.rect, self.border_width, 4)
                self.button.blit(txt, txt_rect)

                self.command()
                self.clicked = True

            if not pygame.mouse.get_pressed()[0]:
                txt = self.font.render(self.txt, True, self.foreground[1])
                txt_rect = txt.get_rect()
                txt_rect.center = (self.rect.width / 2, self.rect.height / 2)
                pygame.draw.rect(self.button, self.background[1], self.rect, 0, 4)
                pygame.draw.rect(self.button, self.border_color[1], self.rect, self.border_width, 4)
                self.button.blit(txt, txt_rect)

                self.clicked = False
        else:
            txt = self.font.render(self.txt, True, self.foreground[0])
            txt_rect = txt.get_rect()
            txt_rect.center = (self.rect.width / 2, self.rect.height / 2)
            pygame.draw.rect(self.button, self.background[0], self.rect, 0, 4)
            pygame.draw.rect(self.button, self.border_color[0], self.rect, self.border_width, 4)
            self.button.blit(txt, txt_rect)


class TextInput:
    def __init__(self, position):
        self.font = pygame.font.Font("freesansbold.ttf", 15)

        self.position = position

        self.width = 170
        self.height = self.font.get_height()*1.5
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.surface_rect = self.surface.get_rect()
        self.surface_rect.topleft = self.position

        self.unavailable_unicodes = [
            '\b', '\t', '\x7f', '\x08', '\r', '\x1b', "/", "\\", ":", "*", "<", ">", "?", "|", "\"", ""
        ]

        self.background = "#e7e7e7"
        self.foreground = "#000000"
        self.border_color = "#000000"
        self.border_width = 1

        self.text = ""

        self.is_active = False
        self.cursor_position = 0

    def draw(self, screen: pygame.Surface):
        screen.blit(self.surface, self.surface_rect)

    def update(self, event):
        pygame.draw.rect(self.surface, self.background, pygame.Rect(0, 0, self.width, self.height), 0, 4)
        pygame.draw.rect(
            self.surface, self.border_color, pygame.Rect(0, 0, self.width, self.height), self.border_width, 4
        )

        if self.surface_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
            if pygame.mouse.get_pressed()[0]:
                self.is_active = True
                self.cursor_position = len(self.text)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            if pygame.mouse.get_pressed()[0]:
                self.is_active = False

        txt = self.font.render(self.text, True, self.foreground)
        txt_rect = txt.get_rect()
        txt_rect.midleft = (3, self.height / 2)

        if self.is_active:
            if event.type == pygame.KEYDOWN:
                if event.unicode not in self.unavailable_unicodes:
                    self.text += event.unicode
                    self.cursor_position += 1

                if event.key == pygame.K_LEFT:
                    if self.cursor_position != 0:
                        self.cursor_position -= 1
                if event.key == pygame.K_RIGHT:
                    if self.cursor_position != len(self.text):
                        self.cursor_position += 1

                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:self.cursor_position-1]+self.text[self.cursor_position:]
                    if self.cursor_position != 0:
                        self.cursor_position -= 1
                if event.key == pygame.K_DELETE:
                    self.text = self.text[:self.cursor_position]+self.text[self.cursor_position+1:]
                if event.key == pygame.K_RETURN:
                    self.is_active = False

            pygame.draw.rect(
                self.surface, self.border_color, pygame.Rect(0, 0, self.width, self.height), self.border_width+1, 4
            )
            x = self.font.render(self.text[:self.cursor_position], True, "#000000").get_rect().width+3
            x_ = x
            if x > self.width:
                txt = self.font.render(self.text[:self.cursor_position], True, self.foreground)
                txt_rect = txt.get_rect()
                txt_rect.midright = (self.width-5, self.height/2)
                x_ = self.width - 5
            pygame.draw.line(self.surface, "#000000", (x_, self.height/7), (x_, 6*self.height/7), 1)

        self.surface.blit(txt, txt_rect)

