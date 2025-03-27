# 基于历史走势的股票推荐系统设计

## 功能概述

基于历史走势的股票推荐系统旨在通过分析股票的历史价格数据、技术指标和市场表现，识别出具有较高胜率的投资机会，并向用户提供智能化的股票推荐。该系统将结合GitHub参考项目中的推荐算法和YahooFinance API提供的金融数据，实现高质量的股票筛选和推荐功能。

## 系统架构

### 1. 数据采集层

- **历史价格数据获取**：
  - 使用YahooFinance/get_stock_chart API获取股票历史价格、交易量等数据
  - 支持不同时间周期（日、周、月）的数据获取
  - 实现定时更新机制，确保数据时效性

- **技术指标数据获取**：
  - 使用YahooFinance/get_stock_insights API获取技术展望数据
  - 获取短期、中期、长期技术指标评分

- **基本面数据获取**：
  - 使用YahooFinance/get_stock_holders API获取内部持股情况
  - 使用YahooFinance/get_stock_sec_filing API获取财务报告信息

### 2. 数据处理层

- **技术指标计算模块**：
  - 计算常用技术指标（MA、MACD、RSI、KDJ等）
  - 识别关键技术形态（头肩顶、双底、三角形等）
  - 计算支撑位和阻力位

- **数据标准化模块**：
  - 对不同股票的价格数据进行标准化处理
  - 处理缺失数据和异常值

- **特征工程模块**：
  - 提取价格走势特征
  - 构建时间序列特征
  - 生成技术指标组合特征

### 3. 推荐算法层

- **基于协同过滤的推荐**：
  - 实现基于用户的协同过滤（User-Based Collaborative Filtering）
  - 根据用户历史交互和偏好推荐相似用户喜欢的股票

- **基于内容的推荐**：
  - 实现基于股票特征的内容推荐
  - 根据股票的技术指标、行业、市值等特征推荐相似股票

- **基于历史胜率的推荐**：
  - 定义胜率计算规则（如N天内上涨X%的概率）
  - 基于历史数据计算不同条件下的胜率
  - 推荐满足高胜率条件的股票

- **混合推荐策略**：
  - 结合多种推荐算法的结果
  - 根据不同市场环境动态调整算法权重

### 4. 模型训练与评估

- **机器学习模型**：
  - 实现短期价格趋势预测模型
  - 使用随机森林、LSTM等算法预测股票走势
  - 定期重新训练模型以适应市场变化

- **回测系统**：
  - 实现历史数据回测功能
  - 评估推荐策略的历史表现
  - 计算关键绩效指标（收益率、最大回撤、夏普比率等）

- **模型评估**：
  - 设计评估指标（准确率、召回率、F1分数等）
  - 实现交叉验证机制
  - 比较不同模型和策略的表现

### 5. 推荐展示层

- **推荐结果生成**：
  - 生成每日/每周推荐股票列表
  - 为每个推荐提供理由和预期目标
  - 计算推荐的置信度和风险评级

- **用户个性化**：
  - 根据用户风险偏好调整推荐
  - 考虑用户投资风格和历史交互
  - 支持用户反馈和推荐调整

## 数据流设计

1. **数据采集流程**：
   ```
   定时任务 -> API请求 -> 数据解析 -> 数据存储 -> 数据更新通知
   ```

2. **推荐生成流程**：
   ```
   原始数据 -> 数据预处理 -> 特征工程 -> 模型预测 -> 推荐排序 -> 结果生成
   ```

3. **用户交互流程**：
   ```
   用户请求 -> 个性化过滤 -> 推荐展示 -> 用户反馈 -> 模型更新
   ```

## 关键算法实现

### 1. 股票相似度计算

```python
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def calculate_stock_similarity(stock_features):
    """计算股票之间的相似度"""
    # 使用余弦相似度计算股票特征的相似性
    similarity_matrix = cosine_similarity(stock_features)
    return similarity_matrix
```

### 2. 胜率计算算法

```python
def calculate_win_rate(price_data, n_days=5, target_return=0.03):
    """计算股票在n天内达到目标收益率的胜率"""
    total_samples = len(price_data) - n_days
    if total_samples <= 0:
        return 0
    
    win_count = 0
    for i in range(total_samples):
        start_price = price_data[i]
        end_prices = price_data[i+1:i+n_days+1]
        max_return = max([(p - start_price) / start_price for p in end_prices])
        if max_return >= target_return:
            win_count += 1
    
    return win_count / total_samples
```

### 3. 混合推荐算法

```python
class HybridRecommender:
    def __init__(self, cf_recommender, content_recommender, win_rate_recommender, 
                 cf_weight=0.3, content_weight=0.3, win_rate_weight=0.4):
        self.cf_recommender = cf_recommender
        self.content_recommender = content_recommender
        self.win_rate_recommender = win_rate_recommender
        self.cf_weight = cf_weight
        self.content_weight = content_weight
        self.win_rate_weight = win_rate_weight
    
    def recommend(self, user_id=None, top_n=5):
        # 获取各推荐器的结果
        cf_recs = self.cf_recommender.recommend(user_id, top_n=top_n*2) if user_id else []
        content_recs = self.content_recommender.recommend(top_n=top_n*2)
        win_rate_recs = self.win_rate_recommender.recommend(top_n=top_n*2)
        
        # 合并推荐结果
        all_recs = {}
        
        # 处理协同过滤推荐
        for stock, score in cf_recs:
            all_recs[stock] = score * self.cf_weight
        
        # 处理基于内容的推荐
        for stock, score in content_recs:
            if stock in all_recs:
                all_recs[stock] += score * self.content_weight
            else:
                all_recs[stock] = score * self.content_weight
        
        # 处理基于胜率的推荐
        for stock, score in win_rate_recs:
            if stock in all_recs:
                all_recs[stock] += score * self.win_rate_weight
            else:
                all_recs[stock] = score * self.win_rate_weight
        
        # 排序并返回top_n推荐
        sorted_recs = sorted(all_recs.items(), key=lambda x: x[1], reverse=True)
        return sorted_recs[:top_n]
```

## 用户界面设计

### 1. 推荐股票列表页面

- **展示内容**：
  - 推荐股票列表（股票代码、名称、当前价格、推荐理由）
  - 每只股票的胜率指标和预期目标
  - 技术形态标识和关键支撑/阻力位
  - 推荐置信度评级（高、中、低）

- **交互功能**：
  - 点击股票查看详细分析
  - 筛选功能（按行业、市值、胜率等）
  - 自定义推荐参数（时间周期、目标收益等）

### 2. 股票详细分析页面

- **展示内容**：
  - 价格走势图（带技术指标和形态标识）
  - 历史胜率统计和回测结果
  - 相似股票推荐
  - 技术指标详解和预测目标

- **交互功能**：
  - 调整技术指标参数
  - 切换不同时间周期
  - 添加到自选或投资组合
  - 设置价格提醒

## 实现计划

### 阶段一：基础架构搭建

1. 实现数据采集模块，对接YahooFinance API
2. 构建数据处理管道，实现技术指标计算
3. 搭建基本的推荐算法框架

### 阶段二：算法实现与优化

1. 实现协同过滤、基于内容和基于胜率的推荐算法
2. 开发混合推荐策略
3. 构建回测系统和模型评估框架

### 阶段三：用户界面开发

1. 设计并实现推荐股票列表页面
2. 开发股票详细分析页面
3. 实现用户交互和个性化功能

### 阶段四：系统集成与测试

1. 将推荐系统集成到现有平台
2. 进行系统测试和性能优化
3. 收集用户反馈并迭代改进

## 技术栈选择

- **后端**：Python、Pandas、NumPy、scikit-learn
- **机器学习**：TensorFlow/PyTorch（用于深度学习模型）
- **数据存储**：SQLite/PostgreSQL
- **前端**：Streamlit、Plotly（与现有平台保持一致）

## 评估指标

- **推荐质量**：准确率、召回率、F1分数
- **投资表现**：胜率、平均收益率、最大回撤
- **用户体验**：用户满意度、点击率、留存率

## 风险与挑战

1. **数据质量**：历史数据可能存在缺失或不准确
2. **市场变化**：市场环境变化可能导致模型失效
3. **计算资源**：实时推荐可能需要较高的计算资源
4. **用户接受度**：用户可能对算法推荐持怀疑态度

## 缓解措施

1. 实现数据质量检查和异常处理机制
2. 定期重新训练模型并监控市场环境变化
3. 实现批处理推荐和缓存机制
4. 提供推荐理由和透明的决策过程，增强用户信任
