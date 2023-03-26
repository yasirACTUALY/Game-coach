import gym
from stable_baselines3.common.atari_wrappers import MaxAndSkipEnv
from gym.utils.play import PlayPlot
from gym.utils.play import play
import numpy as np
import os
import time
import pickle
import neat
import itertools

def train(genome, obs, env):
    run = True
    #measure how long the game is going on for
    start_time  = time.time()
    creat = time.time()
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    print("time to create net:  ", time.time() - creat)

    #a max score to end the game on
    max_score = 100 
    done = False
    truncated = False
    
    while True:
        loop = time.time()
        if done or truncated:
            break

        #makes a 1-dimensional tuple for the image ovbservation
        l = tuple(itertools.chain.from_iterable(itertools.chain.from_iterable(obs)))

        #let the ai decides
        starting = time.time()
        output = net.activate(l)
        print("time to pick:  ", time.time() - starting)
        starting = time.time()
        decision = output.index(max(output))
        print("time to find max:  ", time.time() - starting)
        starting = time.time()
        obs, reward, done, truncated, info = env.step(decision)
        print("time to step:  ", time.time() - starting)
        
        # env.render()
        # print("redering")

        if reward != genome.fitness:
            genome.fitness = reward
            start_time  = time.time()
        #pusnish them if they dont score for a while and end the game
        elif time.time() - start_time > 5:
            genome.fitness -= 10
            break
        print("time to loop:  ", time.time() - loop)
        
    

def run_neat(config):
    # p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    winner = p.run(eval_genomes, 2)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)
def eval_genomes(genomes, config):
    for i, (genome_id, genome) in enumerate(genomes):
        print(round(i/len(genomes) * 100), end=" ")
        genome.fitness = 0
        env = gym.make("ALE/AirRaid-v5", render_mode="rgb_array")
        obs, info = env.reset()
        train(genome, obs, env)


local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'config.txt')

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,
                        config_path)

run_neat(config)



# env = gym.make("ALE/AirRaid-v5", render_mode="rgb_array")
# obs, info = env.reset()
# obs, reward, done, truncated, info = env.step(1)
