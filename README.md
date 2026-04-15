# NCHU Deep RL Homework 04: Q-Learning vs SARSA

This repository contains the implementation and analysis of two classic reinforcement learning algorithms: **Q-learning** and **SARSA**, applied to the **Cliff Walking** Gridworld environment.

## 📝 Assignment Objectives
- Implement Q-learning (Off-policy) and SARSA (On-policy).
- Analyze learning behavior, convergence, and risk-taking strategies.
- Compare safety versus optimality in the Cliff Walking environment.

---

## 🏗️ Project Architecture
- `cliff_walking.py`: Custom Gridworld environment (4x12) with cliff penalty (-100).
- `agents.py`: Modular RL agents implementing Temporal Difference (TD) updates.
- `main.py`: Training loop and visualization suite.
- `scripts/`: Automation scripts for session management (startup/ending).
- `openspec/`: Specification-driven development configuration.

---

---

## 📊 實驗結果分析與討論

### 1. 學習表現 (Learning Performance)
下圖展示了兩種演算法在 500 回合內每一回合的累積獎勵（Total Reward）曲線。

![Performance Comparison](performance_comparison.png)

- **收斂速度**：
    - **Q-learning** 通常能在較少的回合內到達目標，但其在訓練過程中的波動極大。由於其「離策略」特性，它會嘗試在懸崖邊緣行走，導致頻繁掉入懸崖（獎勵 -100）。
    - **SARSA** 的曲線則相對平滑且上升較快到達一個穩定的區間。雖然它學習到的路径較長，但因為它在訓練中學會了如何避免極端懲罰，其整體累積獎勵明顯高於 Q-learning。

### 2. 策略行為 (Strategy Behavior)
我們目測並視覺化了最終學習到的路徑：

#### Q-Learning (冒險策略)
![Q-Learning Path](ql_path.png)
- **路徑描述**：Q-learning 最終學習到了理論上的最優路徑（13 步），即緊貼懸崖邊緣（Row 2）行走。
- **特點分析**：這是一種**冒險型**策略。它假設在未來執行的是最優行動，完全忽略了訓練過程中 $\epsilon$-greedy 帶來的隨機探索風險。

#### SARSA (保守策略)
![SARSA Path](sarsa_path.png)
- **路徑描述**：SARSA 學習到的是一條繞遠路的路徑（至少 15 步），遠離懸崖邊緣。
- **特點分析**：這是一種**保守型**策略。因為它是「同策略」，在更新 Q 值時會考慮到下一個實際採取的行動。如果待在懸崖邊緣，隨機探索有 10% 的機率會掉下去，SARSA 會把這個風險更新到狀態價值中，從而選擇更安全的路線。

### 3. 穩定性分析 (Stability Analysis)
- **波動程度**：SARSA 的波動明顯小於 Q-learning。在訓練過程中，SARSA 的代理人表現得更為謹慎，大幅減少了掉入懸崖的次數。
- **探索的影響**：探索（Exploration）對 Q-learning 來說是一把雙面刃，它幫助找到最短路徑，但也導致訓練中的低分；對 SARSA 來說，探索的風險被直接反映在學習到的策略中，使其選擇更穩定的路徑。

---

## 📖 理論比較與討論

1.  **Q-learning (Off-policy)**：
    - 其更新基於「下一個狀態的最佳可能行動」：$Q(S, A) \leftarrow Q(S, A) + \alpha [R + \gamma \max_a Q(S', a) - Q(S, A)]$。
    - 即使當前策略還在探索（隨機亂走），更新時依然假設未來會走最完美的步法。這使得它傾向於學習到理論最優解，但在實際執行（含探索）時非常危險。
2.  **SARSA (On-policy)**：
    - 其更新基於「實際採取的行動」：$Q(S, A) \leftarrow Q(S, A) + \alpha [R + \gamma Q(S', A') - Q(S, A)]$。
    - 它會忠實反映當前策略的行為。如果策略帶有隨機性（探索），SARSA 就會學到「在隨機性存在的情況下，哪一條路最安全」。

---

## 📝 結論

在本實驗的 Cliff Walking 環境中：
- **收斂速度**：Q-learning 在尋找最優路徑上收斂較快（理論最優），但 SARSA 在獲得穩定獎勵的速度上更快。
- **穩定性**：**SARSA 遠比 Q-learning 穩定**，其訓練過程中的懲罰次數顯著較少。

**選擇建議**：
- 在**模擬環境**或探索成本較低的場景下，可選擇 **Q-learning** 以求得最短路徑。
- 在**真實物理環境**（如無人車、機器人）中，掉入「懸崖」意味著硬體損毀，此時應選擇 **SARSA** 以保證訓練過程中的安全性與穩定性。

---

## 🔄 Workflow System (OpenSpec)

## 🔄 Workflow System (OpenSpec)
This project uses the **OpenSpec** framework for synchronized development and handover management.

### Commands:
- **`npm run dev:start`**: Syncs code, reads the latest `handover.md`, and initializes the environment.
- **`npm run dev:ending`**: Summarizes the session, updates the handover doc, and pushes progress to GitHub.

---

## 🚀 How to Run
1. **Experiment**:
   ```bash
   python main.py
   ```
2. **Start Development Session**:
   ```bash
   npm run dev:start
   ```
3. **End Development Session**:
   ```bash
   npm run dev:ending
   ```
