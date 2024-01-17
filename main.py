import pygame
import sys
import os
import random


def load_image(name, directory=os.getcwd()):
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
        self.left = 10
        self.top = 10
        self.last = []
        self.score = 0
        self.show = 0
        self.images = list(range(1, self.height * self.width // 2 + 1)) + list(
            range(1, self.height * self.width // 2 + 1))
        self.images_show =[[0 for _ in range(self.height)] for _ in range(self.width)]
        random.shuffle(self.images)
        self.cell_size_x = 50
        self.cell_size_y = 50

    def set_view(self, width, height, left, top, cell_size_x, cell_size_y):
        self.width = width
        self.height = height
        self.images = list(range(1, self.height * self.width // 2 + 1)) + list(range(1, self.height * self.width // 2 + 1))
        random.shuffle(self.images)
        self.left = left
        self.top = top
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y

    def render(self, screen):
        if self.show != 5:
            text = pygame.font.Font(None, 50).render(f'Ваш счёт: {self.score}', True, (100, 255, 100))
            screen.blit(text, (20, 20))
            length = len(self.last) // 2 - 1 if self.show == 2 else len(self.last) // 2
            text = pygame.font.Font(None, 50).render(f'Ваши ходы: {length}', True, (100, 255, 100))
            screen.blit(text, (600, 20))
            for i in range(self.width):
                for j in range(self.height):
                    if self.images_show[i][j] != 2:
                        if self.images_show[i][j] == 1:
                            image = load_image(f'{self.images[self.width * j + i]}.jpg', directory=os.path.abspath('images1'))
                        else:
                            image = load_image('0.jpg', directory=os.path.abspath('images1'))
                        image = pygame.transform.scale(image, (self.cell_size_x - 4, self.cell_size_y - 4))
                        screen.blit(image, (self.left + self.cell_size_x * i + 2, self.top + self.cell_size_y * j + 2))
                        pygame.draw.rect(screen, 'orange',
                                         (self.left + self.cell_size_x * i + 2, self.top + self.cell_size_y * j + 2,
                                          self.cell_size_x - 4, self.cell_size_y - 4), 3)
        else:
            image = load_image('win.jpg', directory=os.getcwd())
            image = pygame.transform.scale(image, (300, 300))
            screen.blit(image, (100, 100))

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        if 0 < (x - self.left) / self.cell_size_x < self.width and 0 < (y - self.top) / self.cell_size_y < self.height:
            return ((x - self.left) // self.cell_size_x, (y - self.top) // self.cell_size_y)
        return None

    def on_click(self, cell_coords):
        cell = self.get_cell(cell_coords)
        if self.show == 0 or self.show == 1:
            if self.images_show[cell[0]][cell[1]] != 2:
                self.images_show[cell[0]][cell[1]] = 1
                self.last += [cell]
                self.show = (self.show + 1) % 3
        else:
            self.check()
            self.show = (self.show + 1) % 3
            self.images_show = [[0 if j != 2 else 2 for j in self.images_show[i]] for i in range(len(self.images_show))]



    def check(self):
        if self.images[self.width * self.last[-1][1] + self.last[-1][0]] \
                == self.images[self.width * self.last[-2][1] + self.last[-2][0]]:
            self.images_show[self.last[-1][0]][self.last[-1][1]] = 2
            self.images_show[self.last[-2][0]][self.last[-2][1]] = 2
            self.score += 1
            print('hey', self.score)
            if self.score == self.width * self.height // 2:
                self.win()

    def win(self):
        self.show = 5
        print('hey')
        # image = load_image('win.jpg', directory=os.getcwd())


pygame.init()
size = width, height = 1000, 600
screen = pygame.display.set_mode(size)
board = Board(10, 10)
board.set_view(6, 4, 20, 80, 160, 120)
running = True
clock = pygame.time.Clock()
v = 8
while running:
    screen.fill('white')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.on_click(event.pos)
    board.render(screen)
    clock.tick(v)
    pygame.display.flip()
pygame.quit()