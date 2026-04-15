import numpy as np

class CliffWalkingEnv:
    def __init__(self, rows=4, cols=12):
        self.rows = rows
        self.cols = cols
        self.start_state = (self.rows - 1, 0)
        self.goal_state = (self.rows - 1, self.cols - 1)
        self.current_state = self.start_state
        
        # Cliff is the bottom row except for start and goal
        self.cliff = [(self.rows - 1, i) for i in range(1, self.cols - 1)]
        
    def reset(self):
        self.current_state = self.start_state
        return self.current_state
    
    def step(self, action):
        """
        Actions: 0=Up, 1=Down, 2=Left, 3=Right
        """
        r, c = self.current_state
        
        if action == 0: # Up
            r = max(0, r - 1)
        elif action == 1: # Down
            r = min(self.rows - 1, r + 1)
        elif action == 2: # Left
            c = max(0, c - 1)
        elif action == 3: # Right
            c = min(self.cols - 1, c + 1)
            
        next_state = (r, c)
        self.current_state = next_state
        
        reward = -1
        done = False
        
        if next_state in self.cliff:
            reward = -100
            self.current_state = self.start_state # Fall off cliff, return to start
            # In some versions, done is True, but the standard problem resets it
            # We will follow the requirement "回到起點" and continue the episode
            # but usually it's counted as a reset within the episode.
        elif next_state == self.goal_state:
            reward = 0
            done = True
            
        return self.current_state, reward, done

    def get_all_states(self):
        states = []
        for r in range(self.rows):
            for c in range(self.cols):
                states.append((r, c))
        return states
