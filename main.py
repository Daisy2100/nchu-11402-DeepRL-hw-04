import numpy as np
import matplotlib.pyplot as plt
from cliff_walking import CliffWalkingEnv
from agents import QLearningAgent, SarsaAgent

def train(agent, env, episodes=500):
    rewards_per_episode = []
    
    for ep in range(episodes):
        state = env.reset()
        total_reward = 0
        done = False
        
        # For SARSA, we need to choose the next action in advance
        action = agent.choose_action(state)
        
        while not done:
            next_state, reward, done = env.step(action)
            total_reward += reward
            
            if isinstance(agent, QLearningAgent):
                agent.update(state, action, reward, next_state)
                state = next_state
                action = agent.choose_action(state)
            else: # SarsaAgent
                next_action = agent.choose_action(next_state)
                agent.update(state, action, reward, next_state, next_action)
                state = next_state
                action = next_action
                
        rewards_per_episode.append(total_reward)
        
    return rewards_per_episode

def get_optimal_path(agent, env):
    state = env.reset()
    path = [state]
    done = False
    
    # Use greedy policy for the final path
    # temporarly set epsilon to 0
    old_eps = agent.epsilon
    agent.epsilon = 0
    
    steps = 0
    while not done and steps < 100: # safety break
        action = agent.choose_action(state)
        state, reward, done = env.step(action)
        path.append(state)
        steps += 1
        
    agent.epsilon = old_eps
    return path

def visualize_path(path, rows, cols, title, cliff):
    grid = np.zeros((rows, cols))
    for r, c in cliff:
        grid[r, c] = -1 # Cliff
    
    path_grid = np.zeros((rows, cols))
    for i, (r, c) in enumerate(path):
        path_grid[r, c] = i + 1 # Path sequence
        
    plt.figure(figsize=(10, 4))
    plt.imshow(grid, cmap='RdYlGn', interpolation='nearest')
    
    # Plot path
    rows_p, cols_p = zip(*path)
    plt.plot(cols_p, rows_p, marker='o', color='blue', markersize=5, linestyle='-')
    
    # Annotate Start and Goal
    plt.text(0, rows-1, 'S', ha='center', va='center', fontweight='bold', color='white')
    plt.text(cols-1, rows-1, 'G', ha='center', va='center', fontweight='bold', color='white')
    
    plt.title(title)
    plt.grid(True)

if __name__ == "__main__":
    env = CliffWalkingEnv()
    episodes = 500
    
    # Q-Learning
    ql_agent = QLearningAgent(env.rows, env.cols, 4)
    ql_rewards = train(ql_agent, env, episodes)
    ql_path = get_optimal_path(ql_agent, env)
    
    # SARSA
    sarsa_agent = SarsaAgent(env.rows, env.cols, 4)
    sarsa_rewards = train(sarsa_agent, env, episodes)
    sarsa_path = get_optimal_path(sarsa_agent, env)
    
    # Plot Rewards
    plt.figure(figsize=(12, 6))
    # Smooth the curves for better visualization
    def smooth(y, box_pts):
        box = np.ones(box_pts)/box_pts
        y_smooth = np.convolve(y, box, mode='same')
        return y_smooth

    plt.plot(ql_rewards, label='Q-Learning', alpha=0.3)
    plt.plot(smooth(ql_rewards, 10), label='Q-Learning (Smoothed)', color='blue')
    plt.plot(sarsa_rewards, label='SARSA', alpha=0.3)
    plt.plot(smooth(sarsa_rewards, 10), label='SARSA (Smoothed)', color='red')
    
    plt.xlabel('Episodes')
    plt.ylabel('Sum of rewards per episode')
    plt.ylim(-100, 0) # Focus on the convergence area
    plt.legend()
    plt.title('Q-Learning vs SARSA Performance')
    plt.savefig('performance_comparison.png')
    
    # Plot Paths
    visualize_path(ql_path, env.rows, env.cols, 'Q-Learning Final Path', env.cliff)
    plt.savefig('ql_path.png')
    
    visualize_path(sarsa_path, env.rows, env.cols, 'SARSA Final Path', env.cliff)
    plt.savefig('sarsa_path.png')
    
    print("Experiment completed. Plots saved as performance_comparison.png, ql_path.png, and sarsa_path.png")
