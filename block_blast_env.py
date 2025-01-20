import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pygame

class block_blast_env(gym.Env):
    """
    Custom 1D environment where the agent moves along a 1D grid to reach the goal.
    """
    def __init__(self):
        super(block_blast_env, self).__init__()
        
        # What is needed to do
        '''
            the different block shapes need to be implemented 
            collision of blocks on the board
            randomly giving the ai random blocks
            rewarding the ai based on how much score it gets 
            there need to be a punishment but idk what that would be

            maybe this is not the stratigy I should be going for
        '''
        # Define action space: 0 = move left, 1 = move right
        self.action_space = spaces.Discrete(2)

        # Define observation space: The agent's position on a grid (0 to 10)
        self.observation_space = spaces.Box(low=0, high=10, shape=(1,), dtype=np.float32)

        # Environment parameters
        self.state = 0 # Current position of the agent
        self.board = np.zeros((8, 8))
        self.next_peices = np.array([])
        self.goal_position = 10  # Goal is to reach position 10


    def reset(self, seed=None, options=None):
        """
        Reset the environment to the initial state.
        Returns:
            - observation (np.array): The initial state as a NumPy array.
            - info (dict): Additional reset info (empty for now).
        """
        super().reset(seed=seed)
        self.state = 0  # Reset position to the starting point
        return np.array([self.state], dtype=np.float32), {}

    def step(self, action):
        # Update state based on action
        if action == 1:  # Move right
            self.state += 1
        elif action == 0:  # Move left
            self.state -= 1

        # Clip the state to remain within the valid range
        self.state = np.clip(self.state, 0, 10)

        # Check if the agent has reached the goal
        done = self.state == self.goal_position

        # Assign a reward
        reward = 1 if done else -0.1  # Encourage progress, reward for reaching the goal

        return np.array([self.state], dtype=np.float32), reward, done, False, {}

    def render(self, mode="human"):
        """
        Render the environment (e.g., print the current state).
        """
        print(f"Agent's Current Position: {self.state}")
        print(f"Board: {self.board}")

    def close(self):
        """
        Clean up resources if needed (optional).
        """
        print("Environment closed.")
