import numpy as np

from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import SubprocVecEnv
from stable_baselines3.common.results_plotter   import load_results, ts2xy
from stable_baselines3.common.utils import set_random_seed
from stable_baselines3.common.callbacks import CheckpointCallback
from stable_baselines3.common.vec_env import VecMonitor
from stable_baselines3.common.atari_wrappers import MaxAndSkipEnv

import os
# import gym
import gymnasium as gym

def make_env(env_id, rank, seed=0):
    def _init():
        env = gym.make(env_id)
        env = MaxAndSkipEnv(env, skip=4)
        env.seed(seed + rank)
        return env
    
    set_random_seed(seed)
    return _init
if __name__ == '__main__':
    log_dir = "tmp/"
    os.makedirs(log_dir, exist_ok=True)
    env_id = "ALE/Breakout-v5"
    num_cpu = 4  # Number of processes to use

    env= VecMonitor(SubprocVecEnv([make_env(env_id, i) for i in range(num_cpu)]), "tmp/monitor")

    model = PPO('CnnPolicy', env, verbose=1, tensorboard_log="./board/", )
    #model = PPO.load("", env = env)

    print("Training")
    callback = CheckpointCallback(save_freq=1000, save_path=log_dir)
    model.learn(total_timesteps=1000000, callback=callback, tb_log_name = "First round")
    model.save(env_id)
    print("Done")
