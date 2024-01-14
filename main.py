import pygame
import sys
import os


def load_image(name, directory=os.getcwd(), colorkey=None):
    fullname = os.path.join(directory, name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 20
        self.top = 20
        self.cell_size_x = 95
        self.cell_size_y = 55

    def set_view(self, width, height, left, top, cell_size_x, cell_size_y):
        self.width = width
        self.height = height
        self.left = left
        self.top = top
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y

    def render(self, screen):
        image = load_image("creature.png", directory=os.path.abspath('images1'))
        image = pygame.transform.scale(image, (self.cell_size_x - 4, self.cell_size_y - 4))
        for i in range(self.width):
            for j in range(self.height):
                screen.blit(image, (self.left + self.cell_size_x * i + 2, self.top + self.cell_size_y * j + 2))

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        if 0 < (x - self.left) / self.cell_size_x < self.width and 0 < (y - self.top) / self.cell_size_y < self.height:
            return ((x - self.left) // self.cell_size_x, (y - self.top) // self.cell_size_y)
        return None

    def on_click(self, cell_coords):
        print(cell_coords)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)



pygame.init()
size = width, height = 1000, 600
screen = pygame.display.set_mode(size)
board = Board(10, 10)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill('white')
    board.render(screen)
    pygame.display.flip()
pygame.quit()

#для карт
# set_view(10, 10, 20, 20, 95, 55)