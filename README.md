# NCHU Deep RL Homework 04: Q-Learning vs SARSA

This repository contains the implementation and analysis of two classic reinforcement learning algorithms: **Q-learning** and **SARSA**, applied to the **Cliff Walking** Gridworld environment.

本專案實作並比較了兩種經典的強化學習演算法：**Q-learning** (離策略) 與 **SARSA** (同策略)，並在經典的 **Cliff Walking (懸崖尋路)** 環境中進行測試與行為分析。

---

## 🏗️ 項目架構 (Project Architecture)

| 檔案名稱 | 說明 |
| :--- | :--- |
| `cliff_walking.py` | 自定義 Gridworld 環境 (4x12)，包含懸崖懲罰機制 (-100)。 |
| `agents.py` | 強化學習代理人模組，實作 Q-learning 與 SARSA 更新邏輯。 |
| `main.py` | 實驗執行腳本，負責訓練循環、數據收集與結果視覺化。 |
| `scripts/` | 自動化管理腳本 (`startup.sh`, `ending.sh`)。 |
| `openspec/` | OpenSpec 規範化開發配置資料夾。 |

---

## 📊 實驗結果分析與討論 (Analysis & Discussion)

### 1. 學習表現 (Learning Performance)
下圖展示了兩種演算法在 500 回合內每一回合的累積獎勵（Total Reward）曲線。

![Performance Comparison](performance_comparison.png)

- **收斂速度**：
    - **Q-learning** 通常能在較少的回合內尋找到路徑，但訓練過程波動極大。由於其「離策略」特性，它會嘗試在懸崖邊緣行走，導致頻繁掉入懸崖。
    - **SARSA** 的曲線相對平滑，且能較快到達一個穩定的區間。雖然學習到的路徑較長，但其整體訓練過程的累積獎勵高於 Q-learning。

### 2. 策略行為 (Strategy Behavior)
最終學習到的路徑視覺化比較：

| Q-Learning (冒險策略) | SARSA (保守策略) |
| :---: | :---: |
| ![Q-Learning Path](ql_path.png) | ![SARSA Path](sarsa_path.png) |
| **路徑最優 (13 步)**，緊貼懸崖邊緣。 | **路徑次優 (15 步)**，遠離懸崖邊緣。 |
| 忽略探索帶來的風險。 | 考慮到隨機探索可能導致的災難。 |

### 3. 穩定性與探索 (Stability & Exploration)
- **波動程度**：SARSA 的表現顯著比 Q-learning 穩定。
- **探索影響**：在帶有隨機性（$\epsilon$-greedy）的訓練環境下，SARSA 會將「可能掉入懸崖」的風險納入價值更新，從而學會规避風險；Q-learning 則一味追求理論最短路徑，不畏懼探索時的懲罰。

---

## 📖 理論比較與分析

1.  **Q-learning (Off-policy)**：
    - 更新基於「下一狀態的最佳行動」：$Q(S, A) \leftarrow Q(S, A) + \alpha [R + \gamma \max_a Q(S', a) - Q(S, A)]$。
    - 學習的是理論上的最優策略 $\pi^*$。
2.  **SARSA (On-policy)**：
    - 更新基於「實際採取的下一行動」：$Q(S, A) \leftarrow Q(S, A) + \alpha [R + \gamma Q(S', A') - Q(S, A)]$。
    - 學習的是在當前探索策略下的安全行為。

---

## 📝 結論 (Conclusion)

- **收斂速度**：Q-learning 尋找最優解較快，但 SARSA 達到穩定獎勵的速度較快。
- **穩定性**：SARSA 遠比 Q-learning 穩定。
- **應用場景**：
    - 若追求環境極致效能且無視訓練成本，選 **Q-learning**。
    - 若環境懲罰代價極高（如硬體損壞風險），選 **SARSA**。

---

## 🔄 工作流系統 (OpenSpec Workflow)

本項目採用 **OpenSpec** 框架進行規範化管理：

- **`npm run dev:start`**: 同步代碼，讀取 `handover.md` 並初始化開發環境。
- **`npm run dev:ending`**: 總結當前開發階段，更新任務狀態與交接文檔，並推送至 GitHub。

---

## 🚀 如何運行 (How to Run)

1. **執行實驗與繪圖**：
   ```bash
   python main.py
   ```
2. **開啟 OpenSpec 開發會話**：
   ```bash
   npm run dev:start
   ```
3. **結束會話並自動備份**：
   ```bash
   npm run dev:ending
   ```
