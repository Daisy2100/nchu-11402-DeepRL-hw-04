import numpy as np

class BaseAgent:
    def __init__(self, rows, cols, actions, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.rows = rows
        self.cols = cols
        self.n_actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = np.zeros((rows, cols, actions))
        
    def choose_action(self, state):
        r, c = state
        if np.random.uniform(0, 1) < self.epsilon:
            return np.random.randint(0, self.n_actions)
        else:
            # If multiple actions have the same max value, randomly choose one to avoid bias
            action_values = self.q_table[r, c, :]
            return np.random.choice(np.where(action_values == np.max(action_values))[0])

    def update(self, state, action, reward, next_state, next_action=None):
        raise NotImplementedError

class QLearningAgent(BaseAgent):
    def update(self, state, action, reward, next_state, next_action=None):
        r, c = state
        nr, nc = next_state
        
        # Off-policy: update based on the best possible action in next_state
        best_next_action = np.max(self.q_table[nr, nc, :])
        
        td_target = reward + self.gamma * best_next_action
        td_error = td_target - self.q_table[r, c, action]
        self.q_table[r, c, action] += self.alpha * td_error

class SarsaAgent(BaseAgent):
    def update(self, state, action, reward, next_state, next_action=None):
        r, c = state
        nr, nc = next_state
        
        # On-policy: update based on the action actually chosen (next_action)
        q_next = self.q_table[nr, nc, next_action]
        
        td_target = reward + self.gamma * q_next
        td_error = td_target - self.q_table[r, c, action]
        self.q_table[r, c, action] += self.alpha * td_error
