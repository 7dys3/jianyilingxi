# 图表分析标识功能设计

## 功能概述

图表分析标识功能旨在为用户提供专业的技术分析工具，通过自动识别和标注股票图表中的关键技术形态、支撑位/阻力位和趋势线，帮助用户更直观地理解市场走势，提高技术分析的效率和准确性。该功能将结合YahooFinance API提供的价格数据和先进的技术分析算法，为用户呈现可视化的分析结果。

## 系统架构

### 1. 数据获取层

- **价格数据获取**：
  - 使用YahooFinance/get_stock_chart API获取股票历史价格数据
  - 支持多种时间周期（分钟、小时、日、周、月）
  - 实现实时数据更新机制

- **技术指标数据获取**：
  - 使用YahooFinance/get_stock_insights API获取技术展望数据
  - 获取支撑位和阻力位数据

### 2. 技术分析引擎

- **基础技术指标计算**：
  - 移动平均线（MA）：短期、中期、长期
  - 相对强弱指标（RSI）
  - 移动平均收敛散度（MACD）
  - 布林带（Bollinger Bands）
  - 随机指标（KDJ）
  - 成交量指标（OBV、CMF）

- **形态识别模块**：
  - 头肩顶/底形态
  - 双顶/双底形态
  - 三角形整理
  - 旗形和三角旗形
  - 楔形
  - 杯柄形态
  - 岛形反转

- **趋势分析模块**：
  - 趋势线自动绘制
  - 支撑位和阻力位识别
  - 突破点检测
  - 趋势强度评估

- **波浪理论分析**：
  - 艾略特波浪计数
  - 斐波那契回调水平
  - 斐波那契扩展水平
  - 斐波那契时间区域

### 3. 可视化引擎

- **图表渲染模块**：
  - 蜡烛图/K线图绘制
  - 技术指标叠加显示
  - 形态标注和高亮
  - 趋势线和通道绘制

- **交互控制模块**：
  - 缩放和平移控制
  - 时间周期切换
  - 指标参数调整
  - 自定义标注工具

- **警报系统**：
  - 形态完成警报
  - 突破警报
  - 指标交叉警报
  - 价格目标警报

### 4. 分析结果解释

- **形态解释引擎**：
  - 提供形态的历史成功率
  - 解释形态的技术含义
  - 预测可能的价格目标
  - 建议的交易策略

- **风险评估模块**：
  - 计算形态的风险/回报比
  - 提供止损位建议
  - 评估当前市场环境对形态的影响

## 数据流设计

1. **数据获取流程**：
   ```
   用户选择股票 -> API请求价格数据 -> 数据预处理 -> 存储处理后的数据
   ```

2. **技术分析流程**：
   ```
   处理后的数据 -> 计算技术指标 -> 形态识别 -> 趋势分析 -> 生成分析结果
   ```

3. **可视化流程**：
   ```
   分析结果 -> 图表渲染 -> 标注添加 -> 用户交互响应 -> 动态更新
   ```

## 关键算法实现

### 1. 移动平均线计算

```python
import numpy as np
import pandas as pd

def calculate_ma(prices, window):
    """计算移动平均线"""
    return pd.Series(prices).rolling(window=window).mean().values
```

### 2. 支撑位和阻力位识别

```python
def identify_support_resistance(prices, window=20, threshold=0.02):
    """识别支撑位和阻力位"""
    supports = []
    resistances = []
    
    # 使用局部最小值识别支撑位
    for i in range(window, len(prices) - window):
        if all(prices[i] <= prices[i-j] for j in range(1, window+1)) and \
           all(prices[i] <= prices[i+j] for j in range(1, window+1)):
            supports.append((i, prices[i]))
    
    # 使用局部最大值识别阻力位
    for i in range(window, len(prices) - window):
        if all(prices[i] >= prices[i-j] for j in range(1, window+1)) and \
           all(prices[i] >= prices[i+j] for j in range(1, window+1)):
            resistances.append((i, prices[i]))
    
    # 合并相近的支撑位和阻力位
    supports = merge_levels(supports, threshold)
    resistances = merge_levels(resistances, threshold)
    
    return supports, resistances

def merge_levels(levels, threshold):
    """合并相近的价格水平"""
    if not levels:
        return []
    
    levels.sort(key=lambda x: x[1])
    merged = [levels[0]]
    
    for i in range(1, len(levels)):
        last = merged[-1]
        current = levels[i]
        
        # 如果当前水平与上一个水平相差不超过阈值，则合并
        if abs(current[1] - last[1]) / last[1] <= threshold:
            # 取平均位置和价格
            merged[-1] = ((last[0] + current[0]) // 2, (last[1] + current[1]) / 2)
        else:
            merged.append(current)
    
    return merged
```

### 3. 形态识别算法（以头肩顶为例）

```python
def identify_head_and_shoulders(prices, window=5):
    """识别头肩顶形态"""
    patterns = []
    
    for i in range(2*window, len(prices) - 2*window):
        # 找到局部高点
        left_shoulder_idx = find_local_maximum(prices, i - 2*window, i - window)
        head_idx = find_local_maximum(prices, i - window, i + window)
        right_shoulder_idx = find_local_maximum(prices, i + window, i + 2*window)
        
        if left_shoulder_idx is None or head_idx is None or right_shoulder_idx is None:
            continue
        
        left_shoulder = prices[left_shoulder_idx]
        head = prices[head_idx]
        right_shoulder = prices[right_shoulder_idx]
        
        # 检查头肩顶条件
        if head > left_shoulder and head > right_shoulder and \
           abs(left_shoulder - right_shoulder) / left_shoulder < 0.1:
            
            # 找到颈线
            neckline_left = find_minimum_between(prices, left_shoulder_idx, head_idx)
            neckline_right = find_minimum_between(prices, head_idx, right_shoulder_idx)
            
            if neckline_left is not None and neckline_right is not None:
                neckline = (prices[neckline_left] + prices[neckline_right]) / 2
                
                # 添加识别到的形态
                patterns.append({
                    'type': 'head_and_shoulders',
                    'left_shoulder': (left_shoulder_idx, left_shoulder),
                    'head': (head_idx, head),
                    'right_shoulder': (right_shoulder_idx, right_shoulder),
                    'neckline': neckline,
                    'target': neckline - (head - neckline)  # 价格目标
                })
    
    return patterns

def find_local_maximum(prices, start, end):
    """在指定范围内找到局部最大值"""
    if start < 0 or end >= len(prices) or start >= end:
        return None
    
    max_idx = start
    for i in range(start + 1, end):
        if prices[i] > prices[max_idx]:
            max_idx = i
    
    return max_idx

def find_minimum_between(prices, start, end):
    """在两点之间找到最小值"""
    if start < 0 or end >= len(prices) or start >= end:
        return None
    
    min_idx = start
    for i in range(start + 1, end):
        if prices[i] < prices[min_idx]:
            min_idx = i
    
    return min_idx
```

### 4. 趋势线自动绘制

```python
def draw_trendline(prices, window=20, is_support=True):
    """自动绘制趋势线"""
    x = np.array(range(len(prices)))
    y = np.array(prices)
    
    # 找到局部极值点
    extrema = []
    for i in range(window, len(prices) - window):
        if is_support:
            # 支撑线使用局部最小值
            if all(prices[i] <= prices[i-j] for j in range(1, window+1)) and \
               all(prices[i] <= prices[i+j] for j in range(1, window+1)):
                extrema.append((i, prices[i]))
        else:
            # 阻力线使用局部最大值
            if all(prices[i] >= prices[i-j] for j in range(1, window+1)) and \
               all(prices[i] >= prices[i+j] for j in range(1, window+1)):
                extrema.append((i, prices[i]))
    
    if len(extrema) < 2:
        return None
    
    # 使用RANSAC算法找到最佳拟合线
    from sklearn.linear_model import RANSACRegressor
    
    X = np.array([p[0] for p in extrema]).reshape(-1, 1)
    Y = np.array([p[1] for p in extrema])
    
    ransac = RANSACRegressor()
    ransac.fit(X, Y)
    
    # 获取趋势线参数
    slope = ransac.estimator_.coef_[0]
    intercept = ransac.estimator_.intercept_
    
    # 计算趋势线上的点
    line_x = np.array(range(len(prices)))
    line_y = slope * line_x + intercept
    
    return {
        'slope': slope,
        'intercept': intercept,
        'points': list(zip(line_x, line_y)),
        'is_support': is_support
    }
```

## 用户界面设计

### 1. 主图表区域

- **展示内容**：
  - 股票价格K线图/蜡烛图
  - 自动标注的技术形态（用不同颜色和图案标识）
  - 支撑位和阻力位（水平线）
  - 趋势线（斜线）
  - 成交量柱状图

- **交互功能**：
  - 缩放和平移图表
  - 鼠标悬停显示详细信息
  - 点击形态查看详细分析
  - 自定义时间范围

### 2. 技术指标区域

- **展示内容**：
  - 可选择的技术指标图表（RSI、MACD、KDJ等）
  - 指标信号标注（如金叉、死叉）
  - 超买/超卖区域标识

- **交互功能**：
  - 添加/移除技术指标
  - 调整指标参数
  - 切换指标显示样式

### 3. 形态分析面板

- **展示内容**：
  - 已识别形态的列表
  - 每个形态的详细信息（类型、位置、成功率）
  - 形态完成后的预期目标价格
  - 建议的交易策略和止损位

- **交互功能**：
  - 点击形态在图表上高亮显示
  - 调整形态识别的敏感度
  - 设置形态完成提醒

### 4. 控制面板

- **展示内容**：
  - 时间周期选择（分钟、小时、日、周、月）
  - 图表类型选择（K线图、蜡烛图、线图）
  - 形态识别开关
  - 趋势线绘制开关

- **交互功能**：
  - 自定义显示设置
  - 保存/加载用户偏好
  - 导出图表和分析结果

## 实现计划

### 阶段一：基础功能实现

1. 实现数据获取和预处理模块
2. 开发基础技术指标计算功能
3. 实现基本的图表渲染功能

### 阶段二：形态识别实现

1. 开发主要技术形态的识别算法
2. 实现支撑位/阻力位识别
3. 开发趋势线自动绘制功能

### 阶段三：可视化增强

1. 实现形态标注和高亮功能
2. 开发交互控制功能
3. 设计并实现形态分析面板

### 阶段四：系统集成与优化

1. 将图表分析功能集成到现有平台
2. 优化算法性能和识别准确率
3. 完善用户界面和交互体验

## 技术栈选择

- **后端**：Python、NumPy、Pandas、scikit-learn
- **图表库**：Plotly（与现有平台保持一致）
- **前端框架**：Streamlit（与现有平台保持一致）
- **数据存储**：SQLite/PostgreSQL（用于缓存分析结果）

## 评估指标

- **识别准确率**：形态识别的准确率和召回率
- **用户体验**：用户满意度、功能使用频率
- **性能指标**：图表渲染速度、分析计算时间

## 风险与挑战

1. **识别准确性**：技术形态识别可能存在误判
2. **计算性能**：复杂形态识别可能需要较高计算资源
3. **用户期望**：专业用户可能对分析结果有较高期望

## 缓解措施

1. 提供形态识别的置信度评分，允许用户调整敏感度
2. 实现结果缓存和异步计算机制，优化性能
3. 清晰说明算法局限性，提供专业用户自定义分析工具
