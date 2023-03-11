import pygame
import random

# Initialize Pygame
pygame.init()

# Set up colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

class Game:
    def __init__(self, window, window_width, window_height, dela = True):
        self.dela = dela
        self.window_width = window_width
        self.window_height = window_height
        self.window = window
        self.game_over = False
        
        # Set up game variables
        self.snake_size = 10
        self.food_size = 10
        self.clock = pygame.time.Clock()
        # self.font = pygame.font.SysFont(None, 25)
    
        
        # Set up initial snake position and velocity
        self.x = window_width/2
        self.y = window_height/2
        
        self.snake_list = []
        self.snake_length = 1
        self.x_velocity = 0
        self.y_velocity = 0
        self.x_velocity += self.snake_size

        
        # Set up initial food position
        self.food_x = round(random.randrange(0, window_width - self.food_size)/10.0)*10.0
        self.food_y = round(random.randrange(0, window_height - self.food_size)/10.0)*10.0

    # Define functions
    def draw_snake(self,snake_list):
        """
        Draws the snake on the game screen
        """
        for x in snake_list:
            pygame.draw.rect(self.window, black, [x[0], x[1], self.snake_size, self.snake_size])

    #turns the snake around 
    def turn_around(self, direction):
        if direction == "left":
            self.x_velocity = -self.snake_size
            self.y_velocity = 0
        elif direction == "right":
            self.x_velocity = self.snake_size
            self.y_velocity = 0
        elif direction == "up":
            self.x_velocity = 0
            self.y_velocity = -self.snake_size
        elif direction == "down":
            self.x_velocity = 0
            self.y_velocity = self.snake_size

    
    def game_loop(self):
        """
        Main game loop
        """
        if not self.game_over:
            
            self.x += self.x_velocity
            self.y += self.y_velocity
            self.window.fill(white)
            pygame.draw.rect(self.window, red, [self.food_x, self.food_y, self.food_size, self.food_size])
            snake_head = []
            snake_head.append(self.x)
            snake_head.append(self.y)
            self.snake_list.append(snake_head)
            if len(self.snake_list) > self.snake_length:
                del self.snake_list[0]
            for i in self.snake_list[:-1]:
                if i == snake_head:
                    self.game_over = True
            self.draw_snake(self.snake_list)
            # pygame.display.update()

            # Check for collision with food
            if self.x == self.food_x and self.y == self.food_y:
                self.food_x = round(random.randrange(0, self.window_width - self.food_size)/10.0)*10.0
                self.food_y = round(random.randrange(0, self.window_height - self.food_size)/10.0)*10.0
                self.snake_length += 5

            # Check for collision with wall or self
            if self.x < 0 or self.x >= self.window_width or self.y < 0 or self.y >= self.window_height:
                self.game_over = True
            if self.dela:   
                self.clock.tick(10)
        else:
            return False
        return True

#code to test it
if __name__ == "__main__":
    window_width = 300
    window_height = 300
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Snake Game")
    game = Game(window, window_width, window_height,True)
    cont  = True
    while cont:
        if(not game.game_loop()): break
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                cont = False
                break
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.turn_around("left")
                elif event.key == pygame.K_RIGHT:
                    game.turn_around("right")
                elif event.key == pygame.K_UP:
                    game.turn_around("up")
                elif event.key == pygame.K_DOWN:
                    game.turn_around("down")

        top = 1
        if([game.x,game.y+10] in game.snake_list or game.y+10 >= game.window_height):
            print("bottom")
        bottom =  1
        if([game.x,game.y-10] in game.snake_list or game.y-10 < 0):
            print("top")
        left =  1
        if([game.x-10,game.y] in game.snake_list or game.x-10 < 0):
            print("left")
        right =  1
        if([game.x+10,game.y] in game.snake_list or game.x+10 >= game.window_width):
            print("right")
                
