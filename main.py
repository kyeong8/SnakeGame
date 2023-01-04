import pygame
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
H_RED = (240, 80, 80)
H_BLUE = (80, 80, 240)
RED = (240, 40, 40)
BLUE = (40, 40, 240)
ORANGE = (255, 128, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

class GridObject:
    def __init__(self, x, y, game, color):
        self.game = game
        self.active = True
        self.color = color
        self.x = x
        self.y = y
        self.count = 0
        self.position = [[0, 0]]
        self.lose = 0

    def handle_event(self, event):
        pass

    def tick(self):
        pass

    def draw(self):
        pass

    def interact(self, other):
        pass

    def generate(self):
        pass

class Player1(GridObject):
    color = RED
    dx = 0
    dy = 0
    mem_x = []
    mem_y = []

    def __init__(self, x, y, game):
        super().__init__(x, y, game, self.color)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_LEFT:
                self.dx = -1
                self.dy = 0
            elif event.key == pygame.K_RIGHT:
                self.dx = 1
                self.dy = 0
            elif event.key == pygame.K_UP:
                self.dx = 0
                self.dy = -1
            elif event.key == pygame.K_DOWN:
                self.dx = 0
                self.dy = 1

    def draw(self):
        block_size = self.game.block_size
        pygame.draw.rect(self.game.display, H_RED,
                         [self.position[0][0] * block_size, self.position[0][1] * block_size, block_size,
                          block_size])

        for i in range(len(self.position)-1):
            pygame.draw.rect(self.game.display, self.color,
                             [self.position[i+1][0] * block_size, self.position[i+1][1] * block_size, block_size,
                              block_size])

    def tick(self):

        self.x += self.dx
        self.y += self.dy

        self.position[0][0] = self.x
        self.position[0][1] = self.y

        self.mem_x.append(self.x)
        self.mem_y.append(self.y)

        for i in range(1, self.count + 1):
            self.position[i][0] = self.mem_x[-i-1]
            self.position[i][1] = self.mem_y[-i-1]

    def interact(self, other):
        if isinstance(other, Food):
            if self.x == other.x and self.y == other.y:
                other.active = False

                if other.color == YELLOW:
                    self.count += 3
                    for _ in range(3):
                        self.position.append([0, 0])
                elif other.color == ORANGE:
                    self.count += 2
                    for _ in range(2):
                        self.position.append([0, 0])
                elif other.color == GREEN:
                    self.count += 1
                    self.position.append([0, 0])
                self.tick()

        elif isinstance(other, Player2):
            if other.x == self.x and other.y == self.y:
                if len(self.position) < len(other.position):
                    self.lose = 0
                elif len(self.position) > len(other.position):
                    self.lose = 1
                elif len(self.position) == len(other.position):
                    self.lose = 2

            if len(other.position) > 1:
                for res in other.position[1:]:
                    if self.x == res[0] and self.y == res[1]:
                        self.lose = 1

class Player2(GridObject):
    color = BLUE
    dx = 0
    dy = 0
    mem_x = []
    mem_y = []

    def __init__(self, x, y, game):
        super().__init__(x, y, game, self.color)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN :
            if event.key == ord('a'):
                self.dx = -1
                self.dy = 0
            elif event.key == ord('d'):
                self.dx = 1
                self.dy = 0
            elif event.key == ord('w'):
                self.dx = 0
                self.dy = -1
            elif event.key == ord('s'):
                self.dx = 0
                self.dy = 1

    def draw(self):
        block_size = self.game.block_size
        pygame.draw.rect(self.game.display, H_BLUE,
                         [self.position[0][0] * block_size, self.position[0][1] * block_size, block_size,
                          block_size])

        for i in range(len(self.position)-1):
            pygame.draw.rect(self.game.display, self.color,
                             [self.position[i+1][0] * block_size, self.position[i+1][1] * block_size, block_size,
                              block_size])

    def tick(self):

        self.x += self.dx
        self.y += self.dy

        self.position[0][0] = self.x
        self.position[0][1] = self.y

        self.mem_x.append(self.x)
        self.mem_y.append(self.y)

        for i in range(1, self.count + 1):
            self.position[i][0] = self.mem_x[-i-1]
            self.position[i][1] = self.mem_y[-i-1]

    def interact(self, other):
        if isinstance(other, Food):
            if self.x == other.x and self.y == other.y:
                other.active = False

                if other.color == YELLOW:
                    self.count += 3
                    for _ in range(3):
                        self.position.append([0, 0])
                elif other.color == ORANGE:
                    self.count += 2
                    for _ in range(2):
                        self.position.append([0, 0])
                elif other.color == GREEN:
                    self.count += 1
                    self.position.append([0, 0])
                self.tick()

        elif isinstance(other, Player1):

            if other.x == self.x and other.y == self.y:
                if len(self.position) < len(other.position):
                    self.lose = 0
                elif len(self.position) > len(other.position):
                    self.lose = 1
                elif len(self.position) == len(other.position):
                    self.lose = 2

            if len(other.position) > 1:
                for res in other.position[1:]:
                    if self.x == res[0] and self.y == res[1]:
                        self.lose = 1

class Food(GridObject):

    def __init__(self, game):
        self.color_choice()
        x = random.randint(6, game.n_cols - 7)
        y = random.randint(6, game.n_rows - 7)
        super().__init__(x, y, game, self.color)

    def draw(self):
        block_size = self.game.block_size

        pygame.draw.rect(self.game.display, self.color, [self.x * block_size, self.y * block_size, block_size, block_size])

    def color_choice(self):
        choice = random.randint(0, 2)

        if choice == 0:
            self.color = GREEN
        elif choice == 1:
            self.color = ORANGE
        elif choice == 2:
            self.color = YELLOW

    def generate(self):
        self.color_choice()
        self.x = random.randint(5, self.game.n_cols - 6)
        self.y = random.randint(5, self.game.n_rows - 6)

    def interact(self, other):
        if isinstance(other, Food):
            if self.x == other.x and self.y == other.y:
                other.active = False

        elif isinstance(other, Player1) or isinstance(other, Player2):
            if self.x == other.x and self.y == other.y:
                self.active = False


class Game:
    block_size = 10
    circle = 0

    def __init__(self, n_rows, n_cols):
        pygame.init()
        pygame.display.set_caption('DCCP Snake Game')

        self.display = pygame.display.set_mode((n_cols * self.block_size, n_rows * self.block_size))

        self.n_rows = n_rows
        self.n_cols = n_cols
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.objects = []
        self.winner1 = 0
        self.winner2 = 0
        self.res = 0

    def active_objects(self):
        for obj in self.objects:
            if obj.active:
                yield obj

    def show_winner(self, winner1, winner2):
        self.winner1 = winner1
        self.winner2 = winner2

        font = pygame.font.SysFont(None, 100)

        if self.winner1 == 1 and self.winner2 == 0:
            text = font.render("Player 1 Win!", True, WHITE)
        elif self.winner2 == 1 and self.winner1 == 0:
            text = font.render("Player 2 Win!", True, WHITE)
        elif self.winner1 == 1 and self.winner2 == 1:
            text = font.render("Tie!", True, WHITE)
            self.n_cols += 30
        else :
            text = font.render("Error!", True, WHITE)

        self.display.blit(text,
                          (self.n_cols / 2 * self.block_size - 200, self.n_rows / 2 * self.block_size - 50))
        pygame.display.update()
        pygame.time.wait(1000)

    def play(self, n_foods):

        self.objects = [Player1(40, 40, self), Player2(80, 40, self), *[Food(self) for _ in range(n_foods)]]

        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                    break

                for obj in self.active_objects():
                    obj.handle_event(event)

            for obj in self.active_objects():
                obj.tick()

            for obj1 in self.objects:
                for obj2 in self.objects:
                    if not obj1 == obj2:
                        if obj1.active and obj2.active:
                            obj1.interact(obj2)
                            obj2.interact(obj1)

            font = pygame.font.SysFont(None, 22)

            self.display.fill(BLACK)
            pygame.draw.rect(self.display, WHITE, [5 * self.block_size, 5 * self.block_size,
                                                   (self.n_cols - 10) * self.block_size, (self.n_rows - 10) * self.block_size],2)

            text = font.render("LEFT : ", True, WHITE)
            self.display.blit(text,
                              ((self.n_cols / 2 - 11) * self.block_size, 1.5 * self.block_size))

            text = font.render("RIGHT : ", True, WHITE)
            self.display.blit(text,
                              ((self.n_cols / 2 + 10) * self.block_size, 1.5 * self.block_size))

            pygame.draw.rect(self.display, GREEN, [(self.n_cols/2 - 20) * self.block_size, (self.n_rows - 3)* self.block_size,
                                                   self.block_size, self.block_size])
            text = font.render(": 1",True, WHITE)
            self.display.blit(text, ((self.n_cols/2 - 19) * self.block_size + 5, (self.n_rows - 3) * self.block_size - 1))

            pygame.draw.rect(self.display, ORANGE, [(self.n_cols/2) * self.block_size, (self.n_rows - 3)* self.block_size,
                                                   self.block_size, self.block_size])
            text = font.render(": 2",True, WHITE)
            self.display.blit(text, ((self.n_cols/2 + 1) * self.block_size + 5, (self.n_rows - 3) * self.block_size - 1))

            pygame.draw.rect(self.display, YELLOW, [(self.n_cols/2 + 20) * self.block_size, (self.n_rows - 3)* self.block_size,
                                                   self.block_size, self.block_size])
            text = font.render(": 3",True, WHITE)
            self.display.blit(text, ((self.n_cols/2 + 21) * self.block_size + 5, (self.n_rows - 3) * self.block_size - 1))

            for obj in self.active_objects():
                obj.draw()

            for obj in self.objects:
                if isinstance(obj, Player1):
                    text = font.render(str(len(obj.position)), True, WHITE)
                    self.display.blit(text,
                                      ((self.n_cols / 2 - 6) * self.block_size, 1.5 * self.block_size))

                    if len(obj.position) >= 24:
                        text = font.render(str(self.res), True, WHITE)
                        self.display.blit(text,
                                          ((self.n_cols / 2 + 16.2) * self.block_size, 1.5 * self.block_size))
                        self.winner1 = 1
                        self.game_over = True


                elif isinstance(obj, Player2):
                    text = font.render(str(len(obj.position)), True, WHITE)
                    self.display.blit(text,
                                      ((self.n_cols / 2 + 16.2) * self.block_size, 1.5 * self.block_size))
                    self.res = len(obj.position)
                    if len(obj.position) >= 24:
                        self.winner2 = 1
                        self.game_over = True

            for obj in self.objects:
                if isinstance(obj, Food) and not obj.active:
                    obj.generate()
                    obj.active = True

                elif isinstance(obj, Player1):
                    if not (5 <= obj.x < self.n_cols - 5 and 5 <= obj.y < self.n_rows - 5):
                        self.winner2 = 1
                        self.game_over = True
                    elif obj.lose >= 1:
                        self.winner2 = 1
                        if obj.lose == 2:
                            self.winner1 = 1
                        self.game_over = True

                elif isinstance(obj, Player2):
                    if not (5 <= obj.x < self.n_cols - 5 and 5 <= obj.y < self.n_rows - 5):
                        self.winner1 = 1
                        self.game_over = True

                    elif obj.lose >= 1:
                        self.winner1 = 1
                        if obj.lose == 2:
                            self.winner2 = 1
                        self.game_over = True

            pygame.display.update()

            self.circle += 1

            if self.circle % 51 == 0:
                for obj in self.objects:
                    if (isinstance(obj, Player1) or isinstance(obj, Player2)) and len(obj.position) > 1:
                        del obj.position[-1]
                        obj.count -= 1

            if not (self.winner1 == 0 and self.winner2 == 0):
                self.show_winner(self.winner1, self.winner2)

            self.clock.tick(10)

if __name__ == "__main__":
    Game(n_rows=80, n_cols=120).play(n_foods=20)
