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
        self.left = 10
        self.top = 10
        self.last = []
        #счет в игре
        self.score = 0
        #количество открылых на поле карточек
        #зависит от режима
        self.show = 0
        #общее состояние приложение(play, start, win)
        self.play = 'start'
        #карточки на эту игру
        self.images = list(range(1, self.height * self.width // 2 + 1)) + list(
            range(1, self.height * self.width // 2 + 1))
        random.shuffle(self.images)
        #состояние каждой карточки(0-закрыта, 1-открыта, 2-выиграна(убрана с поля))
        self.images_show =[[0 for _ in range(self.height)] for _ in range(self.width)]
        self.cell_size_x = 50
        self.cell_size_y = 50

    def set_view(self, width, height, left, top, cell_size_x, cell_size_y):
        self.width = width
        self.height = height
        self.images = list(range(1, self.height * self.width // 2 + 1)) +\
                      list(range(1, self.height * self.width // 2 + 1))
        random.shuffle(self.images)
        self.images_show = [[0 for _ in range(self.height)] for _ in range(self.width)]
        self.score = 0
        self.show = 0
        self.last = []
        self.left = left
        self.top = top
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y

    def draw(self, screen):
        if self.play == 'play':
            self.render(screen)
        if self.play == 'win':
            self.win(screen)
        if self.play == 'start':
            self.start(screen)

    #рисование в процессе игры
    def render(self, screen):
        text = pygame.font.Font(None, 50).render(f'Ваш счёт: {self.score}', True, (100, 255, 100))
        screen.blit(text, (20, 20))
        length = len(self.last) // 2 - 1 if self.show == 2 else len(self.last) // 2
        text = pygame.font.Font(None, 50).render(f'Ваши ходы: {length}', True, (100, 255, 100))
        screen.blit(text, (600, 20))
        for i in range(self.width):
            for j in range(self.height):
                if self.images_show[i][j] != 2:
                    if self.images_show[i][j] == 1:
                        image = load_image(f'{self.images[self.width * j + i]}.jpg',
                                           directory=os.path.abspath('images1'))
                    else:
                        image = load_image('0.jpg', directory=os.path.abspath('images1'))
                    image = pygame.transform.scale(image, (self.cell_size_x - 4, self.cell_size_y - 4))
                    screen.blit(image, (self.left + self.cell_size_x * i + 2,
                                        self.top + self.cell_size_y * j + 2))
                    pygame.draw.rect(screen, 'orange',
                                     (self.left + self.cell_size_x * i + 2, self.top + self.cell_size_y * j + 2,
                                      self.cell_size_x - 4, self.cell_size_y - 4), 3)

    #рисовка для победы
    def win(self, screen):
        image = load_image('win.jpg', directory=os.getcwd())
        image = pygame.transform.scale(image, (800, 550))
        screen.blit(image, (100, 0))
        text = pygame.font.Font(None, 100).render('Начать сначала', True, (100, 255, 100))
        screen.blit(text, (50, 500))
        pygame.draw.rect(screen, 'orange', (45, 475, 545, 110), 3)
        text = pygame.font.Font(None, 100).render('Повторить', True, (100, 255, 100))
        screen.blit(text, (610, 500))
        pygame.draw.rect(screen, 'orange', (600, 475, 370, 110), 3)

    #отрисовка начала игры
    def start(self, screen):
        if self.show == 0:
            text = pygame.font.Font(None, 150).render('Начать игру', True, (100, 255, 100))
            screen.blit(text, (200, 200))
        if self.show == 1:
            text = pygame.font.Font(None, 150).render('Выберите уровень', True, (100, 255, 100))
            screen.blit(text, (20, 20))
            text = pygame.font.Font(None, 100).render('Сложный', True, (100, 255, 100))
            screen.blit(text, (150, 300))
            pygame.draw.rect(screen, 'orange', (135, 275, 350, 130), 3)
            text = pygame.font.Font(None, 100).render('Простой', True, (100, 255, 100))
            screen.blit(text, (550, 300))
            pygame.draw.rect(screen, 'orange', (525, 275, 330, 130), 3)
        if self.show == 2:
            self.set_view(6, 4, 20, 80, 160, 120)
            self.play = 'play'
            self.show = 0
        if self.show == 3:
            self.set_view(6, 4, 20, 80, 160, 120)
            self.play = 'play'
            self.show = 0


    def on_click(self, cell_coords):
        if self.play == 'play':
            cell = self.get_cell(cell_coords)
            if cell != None:
                if self.show == 0 or self.show == 1:
                    if self.images_show[cell[0]][cell[1]] != 2:
                        if self.last == [] or self.show == 0 or\
                                not (self.last[-1][0] == cell[0] and self.last[-1][1] == cell[1]):
                            self.images_show[cell[0]][cell[1]] = 1
                            self.last += [cell]
                            self.show = (self.show + 1) % 3
                else:
                    self.check()
                    self.show = (self.show + 1) % 3
                    self.images_show = [[0 if j != 2 else 2 for j in self.images_show[i]]
                                        for i in range(len(self.images_show))]
        if self.play == 'start':
            if self.show == 0:
                self.show += 1
            elif self.show == 1:
                self.images = list(range(1, self.height * self.width // 2 + 1)) + list(
                    range(1, self.height * self.width // 2 + 1))
                random.shuffle(self.images)
                self.images_show = [[0 for _ in range(self.height)] for _ in range(self.width)]
                if 135 < cell_coords[0] < 485 and 275 < cell_coords[1] < 405:
                    self.show = 2
                if 525 < cell_coords[0] < 855 and 275 < cell_coords[1] < 405:
                    self.show = 3
        if self.play == 'win':
            self.show = 0
            if 45 < cell_coords[0] < 590 and 475 < cell_coords[1] < 585:
                self.play = 'start'
            if 600 < cell_coords[0] < 970 and 475 < cell_coords[1] < 585:
                self.play = 'play'
                self.images = list(range(1, self.height * self.width // 2 + 1)) + list(
                    range(1, self.height * self.width // 2 + 1))
                random.shuffle(self.images)
                self.images_show = [[0 for _ in range(self.height)] for _ in range(self.width)]


    def check(self):
        if self.images[self.width * self.last[-1][1] + self.last[-1][0]] \
                == self.images[self.width * self.last[-2][1] + self.last[-2][0]]:
            self.images_show[self.last[-1][0]][self.last[-1][1]] = 2
            self.images_show[self.last[-2][0]][self.last[-2][1]] = 2
            self.score += 1
            if self.score == self.width * self.height // 2:
                self.play = 'win'

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        if 0 < (x - self.left) / self.cell_size_x < self.width and\
                0 < (y - self.top) / self.cell_size_y < self.height:
            return ((x - self.left) // self.cell_size_x, (y - self.top) // self.cell_size_y)
        return None


pygame.init()
size = width, height = 1000, 600
screen = pygame.display.set_mode(size)
board = Board(10, 10)
board.set_view(6, 4, 20, 80, 160, 120)
running = True
clock = pygame.time.Clock()
pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)
v = 8
while running:
    screen.fill('white')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.on_click(event.pos)
    board.draw(screen)
    clock.tick(v)
    pygame.display.flip()
pygame.quit()