import pygame


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

    def draw(self, screen):
        pygame.draw.rect(
            screen, "#000000",
            pygame.Rect(self.position[0]-10, self.position[1]-10, self.size[0]+20, self.size[1]+20), 10
        )
        screen.blit(self.surface, self.surface_rect)

    def update(self):
        self.surface.fill(self.color)
        self.surface.blit(self.canvas, (0, 0))
        self.clicked_ = False

        self.mouse_over = self.surface_rect.collidepoint(pygame.mouse.get_pos())
        if self.mouse_over and pygame.mouse.get_pressed()[0] and not self.clicked and not pygame.mouse.in_use:
            pygame.mouse.in_use = True
            self.clicked = True
            self.m_pos = (pygame.mouse.get_pos()[0]-self.position[0], pygame.mouse.get_pos()[1]-self.position[1])
            self.o_pos = self.m_pos
            self.clicked_ = True
        if not pygame.mouse.get_pressed()[0]:
            pygame.mouse.in_use = False
            self.clicked = False
