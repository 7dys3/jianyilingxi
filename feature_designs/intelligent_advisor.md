# 智能投顾与财富管理功能设计

## 功能概述

智能投顾与财富管理功能旨在为用户提供个性化的理财规划和投资建议，根据用户的资产状况、收入水平、家庭结构、风险偏好和投资目标，生成定制化的资产配置方案和投资组合推荐。该功能将结合现代投资组合理论、机器学习算法和YahooFinance API提供的金融数据，帮助用户实现财富增值，同时考虑中国用户对房产投资和传统理财产品的偏好，提供符合本地市场特点的投资建议。

## 系统架构

### 1. 用户画像模块

- **用户信息采集**：
  - 基本信息（年龄、收入、家庭结构等）
  - 资产负债情况（现金、房产、股票、债券、保险等）
  - 收入支出情况（月收入、固定支出、可投资金额等）
  - 投资经验和知识水平

- **风险偏好评估**：
  - 风险承受能力问卷
  - 投资目标和时间周期
  - 历史投资行为分析
  - 心理特征评估

- **投资目标设定**：
  - 短期目标（1-3年）
  - 中期目标（3-10年）
  - 长期目标（10年以上）
  - 特定目标（子女教育、养老规划等）

### 2. 资产配置引擎

- **资产类别分析**：
  - 股票（A股、港股、美股等）
  - 债券（国债、企业债、可转债等）
  - 基金（股票型、债券型、混合型、指数型等）
  - 房地产（住宅、商业地产、REITs等）
  - 现金及等价物（存款、货币基金等）
  - 另类投资（黄金、大宗商品等）

- **资产配置优化**：
  - 基于现代投资组合理论的有效前沿计算
  - 考虑用户风险偏好的效用最大化
  - 多目标优化（收益最大化、风险最小化、流动性需求等）
  - 考虑中国市场特点的资产配置调整

- **投资组合构建**：
  - 股票组合优化（基于行业、市值、风格等因素）
  - 基金筛选与组合（基于历史业绩、风险指标、基金经理等）
  - 债券组合构建（基于久期、信用等级、收益率等）
  - 现金管理策略

### 3. 投资产品推荐引擎

- **产品筛选模块**：
  - 基于用户风险偏好筛选适合产品
  - 基于历史表现评估产品质量
  - 基于费率和成本分析产品性价比
  - 考虑产品流动性和适合持有期

- **智能推荐算法**：
  - 协同过滤推荐（基于相似用户的选择）
  - 基于内容的推荐（基于产品特征匹配）
  - 基于知识的推荐（基于投资规则和专家知识）
  - 混合推荐策略

- **个性化定制**：
  - 考虑用户特定偏好和约束
  - 适应用户投资习惯和风格
  - 考虑现有投资组合的互补性
  - 提供多种可选方案

### 4. 投资组合管理与监控

- **绩效分析模块**：
  - 收益率计算（时间加权收益率、货币加权收益率）
  - 风险指标分析（波动率、最大回撤、夏普比率等）
  - 业绩归因分析（资产配置贡献、选股/选时贡献等）
  - 与基准比较分析

- **投资组合监控**：
  - 实时市场数据监控
  - 投资组合风险评估
  - 资产配置偏离度分析
  - 预警信号生成

- **再平衡建议**：
  - 定期再平衡提醒
  - 基于市场变化的动态再平衡
  - 税收优化的再平衡策略
  - 低成本实施方案

### 5. 财务规划与教育

- **财务规划工具**：
  - 退休规划计算器
  - 教育金规划工具
  - 税务优化建议
  - 保险需求分析

- **投资教育内容**：
  - 个性化学习路径
  - 投资知识库
  - 市场解读与分析
  - 投资策略指南

## 数据流设计

1. **用户画像构建流程**：
   ```
   用户输入 -> 问卷评估 -> 行为数据分析 -> 风险偏好计算 -> 用户画像生成
   ```

2. **资产配置流程**：
   ```
   用户画像 -> 资产类别分析 -> 历史数据获取 -> 风险收益计算 -> 有效前沿生成 -> 最优配置确定
   ```

3. **产品推荐流程**：
   ```
   资产配置方案 -> 产品库筛选 -> 推荐算法处理 -> 个性化调整 -> 推荐结果生成
   ```

4. **组合监控流程**：
   ```
   市场数据更新 -> 组合绩效计算 -> 风险指标更新 -> 偏离度分析 -> 再平衡建议生成
   ```

## 关键算法实现

### 1. 风险偏好评估

```python
class RiskProfiler:
    def __init__(self):
        # 风险评分权重
        self.weights = {
            'age': 0.15,
            'income_stability': 0.10,
            'investment_horizon': 0.20,
            'financial_knowledge': 0.15,
            'loss_tolerance': 0.25,
            'investment_experience': 0.15
        }
        
        # 风险等级定义
        self.risk_levels = {
            1: {'name': '保守型', 'description': '追求资本保全，接受较低回报'},
            2: {'name': '稳健型', 'description': '追求稳定收益，接受有限波动'},
            3: {'name': '平衡型', 'description': '平衡风险与回报，接受适度波动'},
            4: {'name': '成长型', 'description': '追求较高回报，接受较大波动'},
            5: {'name': '进取型', 'description': '追求高回报，接受高风险和大幅波动'}
        }
    
    def calculate_risk_score(self, answers):
        """计算风险评分"""
        score = 0
        
        # 年龄评分（年轻得分高，年长得分低）
        age = answers.get('age', 40)
        if age < 30:
            age_score = 5
        elif age < 40:
            age_score = 4
        elif age < 50:
            age_score = 3
        elif age < 60:
            age_score = 2
        else:
            age_score = 1
        
        # 收入稳定性（越稳定越高）
        income_stability = answers.get('income_stability', 3)
        
        # 投资期限（越长得分越高）
        horizon = answers.get('investment_horizon', 5)  # 以年为单位
        if horizon < 1:
            horizon_score = 1
        elif horizon < 3:
            horizon_score = 2
        elif horizon < 5:
            horizon_score = 3
        elif horizon < 10:
            horizon_score = 4
        else:
            horizon_score = 5
        
        # 金融知识水平
        financial_knowledge = answers.get('financial_knowledge', 3)
        
        # 损失容忍度
        loss_tolerance = answers.get('loss_tolerance', 3)
        
        # 投资经验
        investment_experience = answers.get('investment_experience', 3)
        
        # 计算加权得分
        score = (
            self.weights['age'] * age_score +
            self.weights['income_stability'] * income_stability +
            self.weights['investment_horizon'] * horizon_score +
            self.weights['financial_knowledge'] * financial_knowledge +
            self.weights['loss_tolerance'] * loss_tolerance +
            self.weights['investment_experience'] * investment_experience
        )
        
        # 将得分映射到1-5的风险等级
        risk_level = min(5, max(1, round(score)))
        
        return {
            'score': score,
            'risk_level': risk_level,
            'risk_profile': self.risk_levels[risk_level]
        }
    
    def get_asset_allocation(self, risk_level):
        """根据风险等级获取推荐资产配置"""
        # 基础资产配置模板
        allocations = {
            1: {'stocks': 0.1, 'bonds': 0.6, 'cash': 0.2, 'alternatives': 0.1},
            2: {'stocks': 0.3, 'bonds': 0.5, 'cash': 0.1, 'alternatives': 0.1},
            3: {'stocks': 0.5, 'bonds': 0.3, 'cash': 0.1, 'alternatives': 0.1},
            4: {'stocks': 0.7, 'bonds': 0.2, 'cash': 0.05, 'alternatives': 0.05},
            5: {'stocks': 0.8, 'bonds': 0.1, 'cash': 0.05, 'alternatives': 0.05}
        }
        
        # 中国市场特点调整（增加房地产配置）
        china_adjusted = allocations[risk_level].copy()
        
        # 从股票和债券中各减少一部分配置给房地产
        real_estate_allocation = 0.1
        stock_reduction = real_estate_allocation * 0.7
        bond_reduction = real_estate_allocation * 0.3
        
        china_adjusted['stocks'] -= stock_reduction
        china_adjusted['bonds'] -= bond_reduction
        china_adjusted['real_estate'] = real_estate_allocation
        
        return china_adjusted
```

### 2. 投资组合优化

```python
import numpy as np
import pandas as pd
from scipy.optimize import minimize

class PortfolioOptimizer:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def get_historical_data(self, symbols, period='1y', interval='1mo'):
        """获取历史价格数据"""
        price_data = {}
        
        for symbol in symbols:
            try:
                data = self.api_client.call_api('YahooFinance/get_stock_chart', 
                                               query={'symbol': symbol, 
                                                     'interval': interval, 
                                                     'range': period})
                
                if 'chart' in data and 'result' in data['chart'] and data['chart']['result']:
                    result = data['chart']['result'][0]
                    timestamps = result.get('timestamp', [])
                    quotes = result.get('indicators', {}).get('quote', [{}])[0]
                    
                    if timestamps and 'close' in quotes:
                        closes = quotes['close']
                        price_data[symbol] = closes
            except Exception as e:
                print(f"获取 {symbol} 数据时出错: {str(e)}")
        
        # 转换为DataFrame
        df = pd.DataFrame(price_data)
        return df
    
    def calculate_returns(self, prices):
        """计算收益率"""
        returns = prices.pct_change().dropna()
        return returns
    
    def optimize_portfolio(self, returns, risk_aversion=3, constraints=None):
        """优化投资组合"""
        n = len(returns.columns)
        
        # 计算预期收益和协方差矩阵
        mean_returns = returns.mean()
        cov_matrix = returns.cov()
        
        # 定义目标函数（效用函数 = 预期收益 - 风险厌恶系数 * 方差）
        def objective(weights):
            portfolio_return = np.sum(mean_returns * weights)
            portfolio_variance = np.dot(weights.T, np.dot(cov_matrix, weights))
            utility = portfolio_return - 0.5 * risk_aversion * portfolio_variance
            return -utility  # 最小化负效用 = 最大化效用
        
        # 约束条件
        constraints_list = [{'type': 'eq', 'fun': lambda x: np.sum(x) - 1}]  # 权重和为1
        
        # 添加自定义约束
        if constraints:
            for asset, (min_weight, max_weight) in constraints.items():
                asset_idx = list(returns.columns).index(asset)
                if min_weight is not None:
                    constraints_list.append({
                        'type': 'ineq', 
                        'fun': lambda x, idx=asset_idx, min_w=min_weight: x[idx] - min_w
                    })
                if max_weight is not None:
                    constraints_list.append({
                        'type': 'ineq', 
                        'fun': lambda x, idx=asset_idx, max_w=max_weight: max_w - x[idx]
                    })
        
        # 边界条件（所有权重在0和1之间）
        bounds = tuple((0, 1) for _ in range(n))
        
        # 初始猜测（平均分配）
        initial_weights = np.array([1/n] * n)
        
        # 优化
        result = minimize(
            objective,
            initial_weights,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints_list
        )
        
        # 提取结果
        optimal_weights = result['x']
        
        # 计算组合预期收益和风险
        expected_return = np.sum(mean_returns * optimal_weights)
        expected_volatility = np.sqrt(np.dot(optimal_weights.T, np.dot(cov_matrix, optimal_weights)))
        sharpe_ratio = expected_return / expected_volatility
        
        # 组合结果
        portfolio = {
            'weights': {asset: weight for asset, weight in zip(returns.columns, optimal_weights)},
            'expected_return': expected_return,
            'expected_volatility': expected_volatility,
            'sharpe_ratio': sharpe_ratio
        }
        
        return portfolio
    
    def generate_efficient_frontier(self, returns, points=20):
        """生成有效前沿"""
        n = len(returns.columns)
        
        # 计算预期收益和协方差矩阵
        mean_returns = returns.mean()
        cov_matrix = returns.cov()
        
        # 找到最小方差组合
        def min_variance_objective(weights):
            return np.dot(weights.T, np.dot(cov_matrix, weights))
        
        constraints = [{'type': 'eq', 'fun': lambda x: np.sum(x) - 1}]
        bounds = tuple((0, 1) for _ in range(n))
        initial_weights = np.array([1/n] * n)
        
        min_var_result = minimize(
            min_variance_objective,
            initial_weights,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )
        
        min_var_weights = min_var_result['x']
        min_var_return = np.sum(mean_returns * min_var_weights)
        min_var_volatility = np.sqrt(min_variance_objective(min_var_weights))
        
        # 找到最大收益组合
        def negative_return(weights):
            return -np.sum(mean_returns * weights)
        
        max_return_result = minimize(
            negative_return,
            initial_weights,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )
        
        max_return_weights = max_return_result['x']
        max_return = np.sum(mean_returns * max_return_weights)
        
        # 生成有效前沿
        target_returns = np.linspace(min_var_return, max_return, points)
        efficient_frontier = []
        
        for target in target_returns:
            # 添加目标收益约束
            target_constraints = constraints.copy()
            target_constraints.append({
                'type': 'eq',
                'fun': lambda x, target=target: np.sum(mean_returns * x) - target
            })
            
            # 最小化方差
            result = minimize(
                min_variance_objective,
                initial_weights,
                method='SLSQP',
                bounds=bounds,
                constraints=target_constraints
            )
            
            if result['success']:
                weights = result['x']
                volatility = np.sqrt(min_variance_objective(weights))
                sharpe = target / volatility if volatility > 0 else 0
                
                portfolio = {
                    'weights': {asset: weight for asset, weight in zip(returns.columns, weights)},
                    'expected_return': target,
                    'expected_volatility': volatility,
                    'sharpe_ratio': sharpe
                }
                
                efficient_frontier.append(portfolio)
        
        return efficient_frontier
```

### 3. 产品推荐算法

```python
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class ProductRecommender:
    def __init__(self):
        # 产品特征数据库（示例）
        self.products = {
            'stock_funds': [],
            'bond_funds': [],
            'mixed_funds': [],
            'index_funds': [],
            'etfs': [],
            'stocks': []
        }
        
        # 用户-产品交互矩阵
        self.user_product_matrix = {}
    
    def load_products(self, api_client):
        """加载产品数据"""
        # 这里可以实现从API或数据库加载产品数据的逻辑
        pass
    
    def extract_product_features(self, product):
        """提取产品特征"""
        features = {}
        
        if product['type'] == 'fund':
            # 基金特征
            features = {
                'return_1y': product.get('return_1y', 0),
                'return_3y': product.get('return_3y', 0),
                'volatility': product.get('volatility', 0),
                'sharpe': product.get('sharpe', 0),
                'max_drawdown': product.get('max_drawdown', 0),
                'size': product.get('size', 0),
                'expense_ratio': product.get('expense_ratio', 0),
                'manager_experience': product.get('manager_experience', 0)
            }
        elif product['type'] == 'stock':
            # 股票特征
            features = {
                'market_cap': product.get('market_cap', 0),
                'pe_ratio': product.get('pe_ratio', 0),
                'pb_ratio': product.get('pb_ratio', 0),
                'dividend_yield': product.get('dividend_yield', 0),
                'volatility': product.get('volatility', 0),
                'beta': product.get('beta', 0),
                'sector': product.get('sector', ''),
                'growth_rate': product.get('growth_rate', 0)
            }
        
        return features
    
    def calculate_product_similarity(self, products):
        """计算产品之间的相似度"""
        # 提取特征向量
        feature_vectors = []
        for product in products:
            features = self.extract_product_features(product)
            # 将分类特征转换为数值
            # ...
            feature_vectors.append(list(features.values()))
        
        # 计算余弦相似度
        similarity_matrix = cosine_similarity(feature_vectors)
        
        return similarity_matrix
    
    def content_based_recommend(self, user_profile, product_type, top_n=5):
        """基于内容的推荐"""
        # 获取该类型的所有产品
        products = self.products.get(product_type, [])
        if not products:
            return []
        
        # 计算用户偏好向量
        user_preferences = {
            'return_preference': user_profile.get('return_preference', 0.5),
            'risk_tolerance': user_profile.get('risk_tolerance', 0.5),
            'cost_sensitivity': user_profile.get('cost_sensitivity', 0.5),
            'liquidity_need': user_profile.get('liquidity_need', 0.5)
        }
        
        # 计算每个产品的匹配分数
        scores = []
        for product in products:
            features = self.extract_product_features(product)
            
            # 计算匹配分数（示例逻辑）
            score = (
                user_preferences['return_preference'] * features.get('return_3y', 0) -
                (1 - user_preferences['risk_tolerance']) * features.get('volatility', 0) -
                user_preferences['cost_sensitivity'] * features.get('expense_ratio', 0)
            )
            
            scores.append((product, score))
        
        # 排序并返回top_n推荐
        scores.sort(key=lambda x: x[1], reverse=True)
        recommendations = [item[0] for item in scores[:top_n]]
        
        return recommendations
    
    def collaborative_filter_recommend(self, user_id, top_n=5):
        """协同过滤推荐"""
        if user_id not in self.user_product_matrix:
            return []
        
        # 用户-产品交互矩阵
        user_interactions = self.user_product_matrix
        
        # 计算用户相似度
        user_similarity = {}
        for other_user in user_interactions:
            if other_user == user_id:
                continue
                
            # 计算余弦相似度
            similarity = self._calculate_user_similarity(user_id, other_user)
            user_similarity[other_user] = similarity
        
        # 找到最相似的用户
        similar_users = sorted(user_similarity.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # 获取相似用户喜欢但当前用户未交互的产品
        recommendations = []
        user_products = set(user_interactions[user_id].keys())
        
        for similar_user, similarity in similar_users:
            similar_user_products = user_interactions[similar_user]
            
            for product, rating in similar_user_products.items():
                if product not in user_products and rating > 3:  # 假设评分范围是1-5
                    recommendations.append((product, rating * similarity))
        
        # 合并同一产品的得分
        product_scores = {}
        for product, score in recommendations:
            if product in product_scores:
                product_scores[product] += score
            else:
                product_scores[product] = score
        
        # 排序并返回top_n推荐
        sorted_products = sorted(product_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
        
        return [product for product, _ in sorted_products]
    
    def _calculate_user_similarity(self, user1, user2):
        """计算两个用户的相似度"""
        interactions1 = self.user_product_matrix[user1]
        interactions2 = self.user_product_matrix[user2]
        
        # 找到共同交互的产品
        common_products = set(interactions1.keys()) & set(interactions2.keys())
        if not common_products:
            return 0
        
        # 提取评分向量
        vector1 = [interactions1[product] for product in common_products]
        vector2 = [interactions2[product] for product in common_products]
        
        # 计算余弦相似度
        dot_product = sum(v1 * v2 for v1, v2 in zip(vector1, vector2))
        magnitude1 = np.sqrt(sum(v ** 2 for v in vector1))
        magnitude2 = np.sqrt(sum(v ** 2 for v in vector2))
        
        if magnitude1 * magnitude2 == 0:
            return 0
            
        return dot_product / (magnitude1 * magnitude2)
    
    def hybrid_recommend(self, user_id, user_profile, product_types, top_n=5):
        """混合推荐策略"""
        # 基于内容的推荐
        content_recs = []
        for product_type in product_types:
            recs = self.content_based_recommend(user_profile, product_type, top_n=3)
            content_recs.extend(recs)
        
        # 协同过滤推荐
        cf_recs = self.collaborative_filter_recommend(user_id, top_n=5)
        
        # 合并推荐结果
        all_recs = set()
        
        # 先添加协同过滤结果（较高权重）
        for product in cf_recs:
            all_recs.add(product)
            
        # 再添加基于内容的结果
        for product in content_recs:
            if len(all_recs) >= top_n:
                break
            all_recs.add(product)
        
        return list(all_recs)[:top_n]
```

### 4. 投资组合绩效分析

```python
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

class PortfolioAnalyzer:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def calculate_portfolio_performance(self, portfolio, start_date, end_date=None):
        """计算投资组合绩效"""
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
            
        # 获取投资组合中所有资产的历史价格
        symbols = list(portfolio['weights'].keys())
        prices = self._get_historical_prices(symbols, start_date, end_date)
        
        if prices.empty:
            return None
            
        # 计算每日投资组合价值
        portfolio_values = self._calculate_portfolio_values(prices, portfolio['weights'])
        
        # 计算收益率
        returns = portfolio_values.pct_change().dropna()
        
        # 计算累计收益
        cumulative_return = (portfolio_values.iloc[-1] / portfolio_values.iloc[0]) - 1
        
        # 计算年化收益率
        days = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days
        annualized_return = (1 + cumulative_return) ** (365 / days) - 1
        
        # 计算波动率
        volatility = returns.std() * np.sqrt(252)  # 年化波动率
        
        # 计算最大回撤
        max_drawdown = self._calculate_max_drawdown(portfolio_values)
        
        # 计算夏普比率（假设无风险利率为3%）
        risk_free_rate = 0.03
        sharpe_ratio = (annualized_return - risk_free_rate) / volatility if volatility > 0 else 0
        
        # 汇总结果
        performance = {
            'start_date': start_date,
            'end_date': end_date,
            'initial_value': portfolio_values.iloc[0],
            'final_value': portfolio_values.iloc[-1],
            'cumulative_return': cumulative_return,
            'annualized_return': annualized_return,
            'volatility': volatility,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio,
            'daily_values': portfolio_values.to_dict(),
            'daily_returns': returns.to_dict()
        }
        
        return performance
    
    def _get_historical_prices(self, symbols, start_date, end_date):
        """获取历史价格数据"""
        # 转换日期格式
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        
        # 获取足够长的历史数据
        range_days = (end - start).days
        range_param = '1mo'
        if range_days > 365:
            range_param = '2y'
        elif range_days > 180:
            range_param = '1y'
        elif range_days > 90:
            range_param = '6mo'
        elif range_days > 30:
            range_param = '3mo'
        
        all_prices = {}
        
        for symbol in symbols:
            try:
                data = self.api_client.call_api('YahooFinance/get_stock_chart', 
                                               query={'symbol': symbol, 
                                                     'interval': '1d', 
                                                     'range': range_param})
                
                if 'chart' in data and 'result' in data['chart'] and data['chart']['result']:
                    result = data['chart']['result'][0]
                    
                    # 提取时间和价格数据
                    timestamps = result.get('timestamp', [])
                    quotes = result.get('indicators', {}).get('quote', [{}])[0]
                    
                    if timestamps and 'close' in quotes:
                        # 转换时间戳为日期
                        dates = [datetime.fromtimestamp(ts).strftime('%Y-%m-%d') for ts in timestamps]
                        closes = quotes['close']
                        
                        # 创建价格序列
                        price_series = pd.Series(closes, index=dates)
                        
                        # 筛选日期范围
                        price_series = price_series[(price_series.index >= start_date) & 
                                                   (price_series.index <= end_date)]
                        
                        all_prices[symbol] = price_series
            except Exception as e:
                print(f"获取 {symbol} 历史价格时出错: {str(e)}")
        
        # 合并所有价格数据
        if all_prices:
            prices_df = pd.DataFrame(all_prices)
            return prices_df
        else:
            return pd.DataFrame()
    
    def _calculate_portfolio_values(self, prices, weights):
        """计算投资组合每日价值"""
        # 假设初始投资为1
        initial_investment = 1.0
        
        # 计算每个资产的初始份额
        initial_prices = prices.iloc[0]
        shares = {}
        for symbol, weight in weights.items():
            if symbol in initial_prices:
                price = initial_prices[symbol]
                if price > 0:
                    shares[symbol] = weight * initial_investment / price
        
        # 计算每日投资组合价值
        portfolio_values = pd.Series(index=prices.index)
        
        for date in prices.index:
            daily_prices = prices.loc[date]
            portfolio_value = sum(shares.get(symbol, 0) * daily_prices.get(symbol, 0) 
                                 for symbol in shares)
            portfolio_values[date] = portfolio_value
        
        return portfolio_values
    
    def _calculate_max_drawdown(self, portfolio_values):
        """计算最大回撤"""
        # 计算累计最大值
        running_max = portfolio_values.cummax()
        
        # 计算回撤
        drawdown = (portfolio_values - running_max) / running_max
        
        # 最大回撤
        max_drawdown = drawdown.min()
        
        return abs(max_drawdown)
    
    def compare_with_benchmark(self, portfolio_performance, benchmark_symbol='SPY'):
        """与基准比较"""
        start_date = portfolio_performance['start_date']
        end_date = portfolio_performance['end_date']
        
        # 获取基准数据
        benchmark_prices = self._get_historical_prices([benchmark_symbol], start_date, end_date)
        
        if benchmark_prices.empty:
            return None
            
        # 计算基准收益率
        benchmark_returns = benchmark_prices[benchmark_symbol].pct_change().dropna()
        
        # 计算基准累计收益
        benchmark_cumulative_return = (benchmark_prices[benchmark_symbol].iloc[-1] / 
                                      benchmark_prices[benchmark_symbol].iloc[0]) - 1
        
        # 计算相对收益
        relative_return = portfolio_performance['cumulative_return'] - benchmark_cumulative_return
        
        # 计算跟踪误差
        portfolio_returns = pd.Series(portfolio_performance['daily_returns'])
        tracking_error = (portfolio_returns - benchmark_returns).std() * np.sqrt(252)
        
        # 计算信息比率
        information_ratio = relative_return / tracking_error if tracking_error > 0 else 0
        
        # 计算Beta
        covariance = portfolio_returns.cov(benchmark_returns)
        benchmark_variance = benchmark_returns.var()
        beta = covariance / benchmark_variance if benchmark_variance > 0 else 1
        
        # 计算Alpha
        risk_free_rate = 0.03 / 252  # 日化无风险利率
        portfolio_avg_return = portfolio_returns.mean()
        benchmark_avg_return = benchmark_returns.mean()
        alpha = portfolio_avg_return - (risk_free_rate + beta * (benchmark_avg_return - risk_free_rate))
        alpha = alpha * 252  # 年化Alpha
        
        # 汇总比较结果
        comparison = {
            'benchmark_symbol': benchmark_symbol,
            'benchmark_cumulative_return': benchmark_cumulative_return,
            'relative_return': relative_return,
            'tracking_error': tracking_error,
            'information_ratio': information_ratio,
            'beta': beta,
            'alpha': alpha,
            'benchmark_daily_values': benchmark_prices[benchmark_symbol].to_dict(),
            'benchmark_daily_returns': benchmark_returns.to_dict()
        }
        
        return comparison
```

## 用户界面设计

### 1. 风险评估问卷页面

- **展示内容**：
  - 风险评估问卷（年龄、收入、投资经验等）
  - 投资目标设定（短期、中期、长期）
  - 资产负债情况输入
  - 投资偏好设置

- **交互功能**：
  - 问卷填写和提交
  - 进度保存
  - 结果预览

### 2. 资产配置建议页面

- **展示内容**：
  - 风险偏好分析结果
  - 推荐资产配置比例（饼图）
  - 预期收益和风险指标
  - 有效前沿图表

- **交互功能**：
  - 调整资产配置比例
  - 查看不同风险水平的配置方案
  - 比较自定义配置与推荐配置
  - 保存和应用配置方案

### 3. 投资产品推荐页面

- **展示内容**：
  - 推荐产品列表（按资产类别分组）
  - 产品详细信息（历史表现、风险指标、费率等）
  - 产品比较视图
  - 推荐理由说明

- **交互功能**：
  - 产品筛选和排序
  - 添加到投资组合
  - 查看产品详情
  - 调整推荐参数

### 4. 投资组合管理页面

- **展示内容**：
  - 当前投资组合概览
  - 资产配置比例（实际vs目标）
  - 绩效分析图表（收益率、回撤等）
  - 与基准比较分析

- **交互功能**：
  - 添加/移除投资产品
  - 调整持仓比例
  - 设置再平衡提醒
  - 导出投资组合报告

### 5. 财务规划工具页面

- **展示内容**：
  - 退休规划计算器
  - 教育金规划工具
  - 税务优化建议
  - 保险需求分析

- **交互功能**：
  - 输入财务目标和参数
  - 调整规划假设
  - 查看模拟结果
  - 保存和导出规划方案

## 实现计划

### 阶段一：用户画像与风险评估

1. 开发风险评估问卷
2. 实现风险偏好计算算法
3. 设计用户画像存储结构

### 阶段二：资产配置引擎

1. 实现历史数据获取和处理
2. 开发投资组合优化算法
3. 构建有效前沿生成功能

### 阶段三：产品推荐系统

1. 建立产品数据库
2. 实现基于内容的推荐算法
3. 开发协同过滤推荐功能
4. 构建混合推荐策略

### 阶段四：投资组合管理

1. 实现投资组合绩效分析
2. 开发再平衡建议功能
3. 构建与基准比较分析

### 阶段五：用户界面开发

1. 设计并实现风险评估页面
2. 开发资产配置建议页面
3. 实现产品推荐和组合管理界面
4. 构建财务规划工具页面

## 技术栈选择

- **后端**：Python、Pandas、NumPy、SciPy
- **机器学习**：scikit-learn（用于推荐算法）
- **数据存储**：SQLite/PostgreSQL
- **前端框架**：Streamlit（与现有平台保持一致）
- **可视化**：Plotly、Matplotlib

## 评估指标

- **推荐质量**：产品推荐的准确性和相关性
- **投资表现**：推荐组合的风险调整收益
- **用户满意度**：用户反馈和使用频率
- **功能完整性**：覆盖用户需求的程度

## 风险与挑战

1. **数据质量**：历史数据可能存在缺失或不准确
2. **市场变化**：市场环境变化可能影响模型有效性
3. **个性化需求**：用户需求和偏好差异较大
4. **监管合规**：需要符合金融监管要求

## 缓解措施

1. 实现数据质量检查和异常处理机制
2. 定期更新模型和参数，适应市场变化
3. 提供高度可定制的界面和参数设置
4. 明确免责声明，强调投资决策最终由用户负责
