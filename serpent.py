import pygame, sys, os,random
from pygame.locals import *



# DECLARATION OF  THE GAME SPEED
STARTING_FPS = 4
FPS_INCREMENT_FREQUENCY = 150


#  DECLARATION OF CONSTANTS FOR DIRECTION
DIRECTION_UP    = 1
DIRECTON_DOWN   = 2
DIRECTION_LEFT  = 3
DIRECTION_RIGHT = 4


# DECLARATION OF THE WORLD SIZE 
WORLD_SIZE_X = 40
WORLD_SIZE_Y = 40


# DECLARATION OF THE BASIC SNAKE LENGTH AND THE COLORS
SNAKE_START_LENGTH = 4
SNAKE_COLOR = (0, 10, 0)
fruit_COLOR = (133, 0, 0)


# Snake class
class Snake:

    # INITIALIZATION OF THE OBJECT
    def __init__(self, x, y, startLength):
        self.startLength = startLength
        self.startX = x
        self.startY = y
        self.reset()

    # RESET SNAKE TO GO BACK TO HIS ORIGINAL STATE
    def reset(self):
        self.pieces = []
        self.direction = 1

	#APPLY IT TO EVERY PART OF THE SNAKE
        for n in range(0, self.startLength):
            self.pieces.append((self.startX, self.startY + n))

    # FUNCTION TO CHANGE THE DIRECTION OF THE SNAKE
    def changeDirection(self, direction):
        # WE CAN NOT MOOVE FROM A DIRECTION TO AN OPPOSIT ONE
        if self.direction == 1 and direction == 2: return
        if self.direction == 2 and direction == 1: return
        if self.direction == 3 and direction == 4: return
        if self.direction == 4 and direction == 3: return

        self.direction = direction

    # FUNCTION TO GET THE COORDINATE OF THE HEAD OF THE SNAKE
    def getHead(self):
        return self.pieces[0]

    # FUNCTION TO GET THE COORTDINATE OF THE TAIL OF THE SNAKE
    def getTail(self):
        return self.pieces[len(self.pieces) - 1]

    # UPDATE THE SNAKE BY MOOVING EACH PART OF HIS BODY TO THE CURRENT DIRECTION
    def update(self):
        (headX, headY) = self.getHead()
        head = ()

        # CREATE A NEW PEACE OF THE SNAKE WHICH IS THE NEW HEAD OF THE SNAKE
        if   self.direction == 1: head = (headX, headY - 1)
        elif self.direction == 2: head = (headX, headY + 1)
        elif self.direction == 3: head = (headX - 1, headY)
        elif self.direction == 4: head = (headX + 1, headY)

        # REMOVE TAIL OF THE SNAKE AND ADD A NEW HEAD
        self.pieces.insert(0, head)
        self.pieces.pop()

    # ADD A NEW BLOCK AT THE TAIL OF THE SNAKE
    def grow(self):
        (tx, ty) = self.getTail()
        piece = ()

        if self.direction == 1: piece = (tx, ty + 1)
        elif self.direction == 2: piece = (tx, ty - 1)
        elif self.direction == 3: piece = (tx + 1, ty)
        elif self.direction == 4: piece = (tx - 1, ty)

        self.pieces.append(piece)

    # 2 PIECES OF THE SNAKE OCCUPING THE SAME BLOCK ? 
    def collidesWithSelf(self):

        return len([p for p in self.pieces if p == self.getHead()]) > 1


# SnakeGame class
class SnakeGame:

    # INITIALIZE SNAKE GAME OBJECT
    def __init__(self, window, screen, clock, font):
        self.window = window
        self.screen = screen
        self.clock = clock
        self.font = font

        self.fps = STARTING_FPS
        self.ticks = 0
        self.playing = True
        self.score = 0

        self.nextDirection = DIRECTION_UP
        self.sizeX = WORLD_SIZE_X
        self.sizeY = WORLD_SIZE_Y
        self.fruit = []
        self.snake = Snake(WORLD_SIZE_X / 2, WORLD_SIZE_Y / 2, SNAKE_START_LENGTH)

        self.addfruit()

    # ADD A PIECE OF fruit IN A RANDOM POSITION
    def addfruit(self):
        fx = None
        fy = None

        while fx is None or fy is None or (fx, fy) in self.fruit:
            fx = random.randint(1, self.sizeX)
            fy = random.randint(1, self.sizeY)

        self.fruit.append((fx, fy))

    # GET INPUT FROM KEYBOARD
    def input(self, events):
        for e in events:
            if e.type == QUIT:
                return False

            elif e.type == KEYUP:
                if   e.key == K_w: self.nextDirection = 1
                elif e.key == K_s: self.nextDirection = 2
                elif e.key == K_a: self.nextDirection = 3
                elif e.key == K_d: self.nextDirection = 4
                elif e.key == K_SPACE and not self.playing: 
                    self.reset()
		#elif e.key == K_ESCAPE and self.playing: 
                 #   sys.exit()


        return True

    # UPDATE THE STATE OF THE GAME AND VERIFY IF THE SNAKE IS DEAD OR NOT
    def update(self):
        self.snake.changeDirection(self.nextDirection)
        self.snake.update()

        # IF THE SNAKE EAT A FRUIT, IT WILL ADD A NEW FRUIT, GROW THE SNAKE
        for fruit in self.fruit: 
            if self.snake.getHead() == fruit:
                self.fruit.remove(fruit)
                self.addfruit()
                self.snake.grow()
                self.score += 10

        # IF THE SNAKE HIT HIMSELF OR THE BOUNDARIES THEN YOU LOOSE
        (hx, hy) = self.snake.getHead()
        if self.snake.collidesWithSelf() or hx < 1 or hy < 1 or hx > self.sizeX or hy > self.sizeY:
            self.playing = False

    # RESET THE GAME TO THE INITIAL STATE
    def reset(self):
        self.playing = True
        self.nextDirection = DIRECTION_UP
        self.fps = STARTING_FPS
        self.score = 0
        self.snake.reset()

    # FUNCTION TO DRAW THE SNAKE/fruit ON THE SCREEN
    def draw(self):
        self.screen.fill((45, 45, 45))

        (width, height) = self.window.get_size()
        blockWidth = int(width / self.sizeX)
        blockHeight = int(height / self.sizeY)

        # DRAWS PIECES OF SNAKE
        for (px, py) in self.snake.pieces: 
            pygame.draw.rect(self.screen, SNAKE_COLOR, (blockWidth * (px-1), blockHeight * (py-1), blockWidth, blockHeight))

        # DRAWS FRUITS
        for (fx, fy) in self.fruit:
            pygame.draw.rect(self.screen, fruit_COLOR, (blockWidth * (fx-1), blockHeight * (fy-1), blockWidth, blockHeight))

        pygame.display.flip()

    # DRAWS THE END MESSAGE ON THE SCREEN
    def drawDeath(self):
        self.screen.fill((255, 0, 0))
        self.screen.blit(self.font.render("Game over! Press Space to start a new game", 1, (255, 255, 255)), (20, 150))
        self.screen.blit(self.font.render("Your score is: %d" % self.score, 1, (255, 255, 255)), (140, 180))
        pygame.display.flip()

    # MAIN LOOP
    def run(self, events):
        if not self.input(events): return False

        if self.playing: 
            self.update()
            self.draw()
        else: self.drawDeath()

        self.clock.tick(self.fps)

        self.ticks += 1
        if self.ticks % FPS_INCREMENT_FREQUENCY == 0: self.fps += 1

        return True


def main():
	#INITIALIZE THE PYGAME CONTEXT
    pygame.init()
	#GIVING HIM A NAME
    pygame.display.set_caption('Our (beautiful)(or not ) snake game')

	#SETTING DATAS ABOUT THE WINDOW/SCREEN
    window = pygame.display.set_mode((600, 600))
    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()
    font = pygame.font.Font('freesansbold.ttf', 20)

    game = SnakeGame(window, screen, clock, font)

    while game.run(pygame.event.get()):
        pass

    pygame.quit()
    sys.exit()


# INITIALIZE THE MAIN OBJECT IF IT IS NOT DONE
if __name__ == '__main__':
    main()

