import pygame
from pygame.locals import *
import time
import random

SIZE = 40
BACKGROUND_COLOR = (70, 51, 89)
class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.play_background_music()
        self.surface = pygame.display.set_mode((1366,768))
        self.surface.fill(BACKGROUND_COLOR)
        self.snake = Snake(self.surface,1)
        self.snake.draw()
        self.apple = Apple(self.surface)

    def collision(self,x1,y1,x2,y2):
        if x1 >= x2 and x1 < x2+SIZE :
            if y1 >= y2 and y1<y2+SIZE:
                return True
        return False
    
    def play_background_music(self):
        pygame.mixer.music.load("resources/bg_music_1.mp3")
        pygame.mixer.music.play()
    
    def playSound(self,sound):
            sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
            pygame.mixer.Sound.play(sound)

    def play(self):
        self.snake.move()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        #collision of sanke with apple
        if self.collision(self.snake.x[0],self.snake.y[0],self.apple.x,self.apple.y):
            self.playSound('ding')
            self.snake.increase_length()
            self.apple.move()

        #collision of snake with its body
        for i in range(3,self.snake.length):
            if self.collision(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i]):
                self.playSound('crash')
                raise "Game Over"
        
    
    def show_game_over(self):
        self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('arial',30)
        line1 = font.render("Game Over!",True,(255,255,255))
        self.surface.blit(line1,(500,350))
        line2 = font.render(f" Score:{self.snake.length}",True,(255,255,255))
        self.surface.blit(line2,(500,400))
        line3 = font.render("Press Enter to play Again. Press Esc to Exit",True,(255,255,255))
        self.surface.blit(line3,(500,450))
        pygame.display.flip()
        pygame.mixer.music.pause()


    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score:{self.snake.length}",True,(255,255,255))
        self.surface.blit(score,(1240,10))

    
    def reset(self):
        self.snake = Snake(self.surface,1)
        self.apple = Apple(self.surface)


    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    
                    if event.key == K_RETURN:
                        pause = False
                        pygame.mixer.music.unpause()
                    
                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False
            
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
            time.sleep(0.2)

class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [SIZE] * length
        self.y = [SIZE] * length
        self.direction = 'right'
    
    def draw(self):
        self.parent_screen.fill((70, 51, 89))
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()
    
    def increase_length(self):
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)


    def move_up(self):
        self.direction = 'up'
    
    def move_down(self):
        self.direction = 'down'
    
    def move_left(self):
        self.direction = 'left'
    
    def move_right(self):
        self.direction = 'right'
    
    def move(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE

        self.draw()

class Apple:
    def __init__(self,parent_screen):
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = SIZE*3
        self.y = SIZE*3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = SIZE*random.randint(0,33)
        self.y = SIZE*random.randint(0,18)


if __name__ == "__main__":
    game = Game()
    game.run()
