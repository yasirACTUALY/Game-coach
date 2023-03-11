import pygame
from snake_game import Game
import neat
import os
import pickle
import time
import multiprocessing
import random


class SnakeGame:
    def __init__(self, window, width, height, dela = True):
        #makes a game for the ai
        self.game = Game(window, width, height, dela)
        self.top = False
        self.bottom = False
        self.left = False
        self.right = False

    def test_ai(self,genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        run = True
        while run :
            if(not self.game.game_loop()): 
                run = False
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    break
            pygame.display.update()
            
           #trying to give the 4 possible spots around the snake to see if it can learn to avoid itself
            self.updatelocations()
            #gives inputs to the gnome to get outputs
            output = net.activate((self.game.food_x - self.game.x, self.game.food_y - self.game.y, self.top, self.bottom, self.left, self.right))

            decision = output.index(max(output))
            if decision == 0:
                self.game.turn_around("left")
            elif decision == 1:
                self.game.turn_around("right")
            elif decision == 2:
                self.game.turn_around("up")
            elif decision == 3:
                self.game.turn_around("down")
    
    def train_ai(self,genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        run = True
        genome.fitness = self.game.snake_length
        start = time.time()
        while run :
            if(not self.game.game_loop()): 
                run = False
                break
            # if genome.fitness < (self.game.snake_size ):
                
            #     #add a small intiative to move towards the food
            #     genome.fitness += (distance(self.game.x, self.game.y, self.game.food_x, self.game.food_y)*10)
            #     start = time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    quit()

            # pygame.display.update()
            
            #gives inputs to the gnome to get outputs(trying multiple ones to see which combination works best)
            # output = net.activate(( self.game.snake_length, self.game.x,self.game.y , self.game.food_x, self.game.food_y))
            #output = net.activate(( self.game.snake_length, self.game.x,self.game.y , self.game.x_velocity, self.game.y_velocity, self.game.food_x, self.game.food_y))
            # output = net.activate(( self.game.x_velocity, self.game.y_velocity, self.game.food_x - self.game.x, self.game.food_y - self.game.y ))

            self.updatelocations()
            output = net.activate((self.game.food_x - self.game.x, self.game.food_y - self.game.y, self.top, self.bottom, self.left, self.right))

            decision = output.index(max(output))
            if decision == 0:
                self.game.turn_around("left")
            elif decision == 1:
                self.game.turn_around("right")
            elif decision == 2:
                self.game.turn_around("up")
            elif decision == 3:
                self.game.turn_around("down")

            #if too much time passes without scoring assume
            # its stuck and then stops the game
            if time.time() - start > .1:
                run = False
                #punsih them for stalling
                genome.fitness = -10
                break
            if(genome.fitness != self.game.snake_length):
                start = time.time()
                genome.fitness = self.game.snake_length 
            
            #incase we want to reward the snake for moving towards the food
            # genome.fitness += (distance(self.game.x, self.game.y, self.game.food_x, self.game.food_y))
            
    #function to update the locations around the snake
    def updatelocations(self):
        self.top = 1
        if([self.game.x,self.game.y+10] in self.game.snake_list or self.game.y+10 >= self.game.window_height):
            self.top=  0
        self.bottom =  1
        if([self.game.x,self.game.y-10] in self.game.snake_list or self.game.y-10 < 0):
            self.bottom =  0
        self.left =  1
        if([self.game.x-10,self.game.y] in self.game.snake_list or self.game.x-10 < 0):
            self.left =  0
        self.right =  1
        if([self.game.x+10,self.game.y] in self.game.snake_list or self.game.x+10 >= self.game.window_width):
            self.right =  0
        
#making a function to reset the game instead 
# of closing and reopening since that takes too much time
def reset( game):
        # Set up game variables
        game.snake_size = 10
        game.food_size = 10
        game.game_over = False
        
        # Set up initial snake position and velocity
        game.x = game.window_width/2
        game.y = game.window_height/2
        
        game.snake_list = []
        game.snake_length = 1
        game.x_velocity = 0
        game.y_velocity = 0
        game.x_velocity += game.snake_size
        
        # Set up initial food position
        game.food_x = round(random.randrange(0, game.window_width - game.food_size)/10.0)*10.0
        game.food_y = round(random.randrange(0, game.window_height - game.food_size)/10.0)*10.0
        
#a function to make multiple processes easier
def eval(genome,config, game):
    game.train_ai(genome, config)

def eval_genomes(genomes, config, draw = False):
    width, height = 300, 300
    window = pygame.display.set_mode((width, height))
    game = SnakeGame(window, width, height, False)
    
    # proccessed_genomes = []
    # num = 0
    for i, (genome_id, genome) in enumerate(genomes):
        genome.fitness = 0
        reset(game.game)
        game.train_ai(genome, config)

        #stuff for multiprocessing trials
        # p1 = multiprocessing.Process(target =eval, args =[genome, config, game])
        # p1.start()
        # proccessed_genomes.append(p1)
        # num+=1
        # if(num == 5):
        #     num = 0
        #     for pro in  proccessed_genomes:
        #         pro.join()
        #     proccessed_genomes = []

    # for pro in  proccessed_genomes:
    #     pro.join()

def run_neat(config,tries,num = 0):
    #checks if we want to start from a previous checkpoint
    if num != 0:
        p = neat.Checkpointer.restore_checkpoint(f'neat-checkpoint-{num}')
    else: p = neat.Population(config)
    
    #adds reporters to show progress
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(10)) 

    #trains the ai
    winner = p.run(eval_genomes, tries)
    #saves the winner ai
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)

def test_ai(config):
    #loads the best ai
    with open("best.pickle", "rb") as f:
        genome = pickle.load(f)
    width, height = 300, 300
    window = pygame.display.set_mode((width, height))
    game = SnakeGame(window, width, height, True)
    game.test_ai(genome, config)

#calculates a value from 0-1 based on how close the snake is to the food
#the value is closer to 1 if the snake is closer to the food
def distance(x1, y1, x2, y2):
    dist = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
    #limits it to a value between 0 and 1
    maxim = ((700)**2 + (500)**2)**0.5
    minim =0 
    val = (dist - minim)/(maxim - minim)
    #now returns the opposite of the value since a smaller value is better
    return (1- val)

if __name__ == "__main__":
    print("\n\n\nstart\n\n")
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,
                        config_path)
    # run_neat(config, 30)
    # run_neat(config, 501, 879)
    test_ai(config)
