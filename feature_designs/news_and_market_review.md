# 热点资讯与今日复盘功能设计

## 功能概述

热点资讯与今日复盘功能旨在为用户提供全面的市场动态和热点分析，帮助用户快速了解市场最新动向、热门板块和重要事件，并通过专业的市场复盘分析，帮助用户理解市场走势背后的原因。该功能将整合多种数据源，包括YahooFinance API提供的股票数据、新闻资讯和分析师观点，结合自然语言处理技术，为用户提供高质量的市场信息和分析内容。

## 系统架构

### 1. 数据采集层

- **市场数据获取**：
  - 使用YahooFinance API获取主要指数和板块数据
  - 获取个股涨跌幅排行
  - 获取成交量和换手率数据

- **新闻资讯获取**：
  - 使用YahooFinance/get_stock_insights API获取重大发展信息
  - 使用YahooFinance/get_stock_sec_filing API获取公司公告
  - 集成其他财经新闻API或网络爬虫获取最新资讯

- **分析师观点获取**：
  - 使用YahooFinance/get_stock_what_analyst_are_saying API获取分析师报告
  - 获取机构评级变动信息

### 2. 数据处理层

- **资讯分类模块**：
  - 按主题分类（公司新闻、行业动态、政策法规、市场评论等）
  - 按相关性分类（高、中、低影响力）
  - 按情感倾向分类（正面、中性、负面）

- **热点识别模块**：
  - 基于新闻提及频率识别热点股票和板块
  - 基于交易量和价格变动识别市场热点
  - 基于社交媒体讨论热度识别关注焦点

- **市场情绪分析**：
  - 基于新闻情感分析评估市场情绪
  - 计算市场恐慌/贪婪指数
  - 分析市场情绪与价格走势的关联

### 3. 内容生成层

- **热点资讯聚合**：
  - 按重要性排序展示热点新闻
  - 生成热点话题摘要
  - 关联相关股票和板块

- **今日复盘生成**：
  - 自动生成市场概览（指数表现、板块轮动、资金流向）
  - 分析市场主要影响因素
  - 总结交易特点和市场情绪
  - 预测可能的后市发展

- **个性化推荐**：
  - 基于用户关注的股票和板块推荐相关资讯
  - 根据用户阅读历史推荐感兴趣的内容
  - 为用户投资组合提供相关热点分析

### 4. 展示交互层

- **资讯展示模块**：
  - 热点资讯流
  - 专题聚合页
  - 资讯详情页

- **复盘展示模块**：
  - 每日市场复盘报告
  - 板块轮动分析
  - 技术面和基本面综合分析

- **交互功能**：
  - 资讯筛选和搜索
  - 收藏和分享
  - 个性化设置

## 数据流设计

1. **数据采集流程**：
   ```
   定时任务 -> 多源数据获取 -> 数据清洗 -> 结构化存储 -> 更新通知
   ```

2. **热点分析流程**：
   ```
   原始数据 -> 文本预处理 -> 主题提取 -> 情感分析 -> 热点识别 -> 结果生成
   ```

3. **复盘生成流程**：
   ```
   市场数据 -> 技术指标计算 -> 板块分析 -> 资金流向分析 -> 新闻关联 -> 复盘报告生成
   ```

4. **用户交互流程**：
   ```
   用户请求 -> 个性化过滤 -> 内容展示 -> 用户反馈 -> 推荐优化
   ```

## 关键算法实现

### 1. 新闻情感分析

```python
from transformers import pipeline

class NewsAnalyzer:
    def __init__(self):
        # 初始化情感分析模型
        self.sentiment_analyzer = pipeline("sentiment-analysis", model="finbert-sentiment")
        
    def analyze_sentiment(self, news_text):
        """分析新闻情感倾向"""
        result = self.sentiment_analyzer(news_text)
        return {
            'sentiment': result[0]['label'],  # positive, negative, neutral
            'score': result[0]['score']
        }
    
    def batch_analyze(self, news_list):
        """批量分析新闻情感"""
        results = []
        for news in news_list:
            sentiment = self.analyze_sentiment(news['content'])
            results.append({
                'id': news['id'],
                'title': news['title'],
                'sentiment': sentiment['sentiment'],
                'score': sentiment['score']
            })
        return results
```

### 2. 热点话题提取

```python
import jieba.analyse
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN

class HotTopicExtractor:
    def __init__(self):
        self.tfidf_vectorizer = TfidfVectorizer(max_features=1000)
        
    def extract_keywords(self, text, top_k=5):
        """提取文本关键词"""
        keywords = jieba.analyse.extract_tags(text, topK=top_k)
        return keywords
    
    def cluster_news(self, news_list, eps=0.5, min_samples=3):
        """聚类相似新闻为热点话题"""
        # 提取每条新闻的文本内容
        texts = [news['content'] for news in news_list]
        
        # 转换为TF-IDF特征
        tfidf_matrix = self.tfidf_vectorizer.fit_transform(texts)
        
        # 使用DBSCAN聚类
        clustering = DBSCAN(eps=eps, min_samples=min_samples, metric='cosine').fit(tfidf_matrix)
        
        # 获取聚类结果
        labels = clustering.labels_
        
        # 整理聚类结果
        clusters = {}
        for i, label in enumerate(labels):
            if label == -1:  # 噪声点
                continue
                
            if label not in clusters:
                clusters[label] = []
                
            clusters[label].append(news_list[i])
        
        # 为每个聚类提取主题
        topics = []
        for label, cluster_news in clusters.items():
            # 合并该聚类的所有文本
            combined_text = " ".join([news['title'] + " " + news['content'] for news in cluster_news])
            
            # 提取关键词作为主题
            keywords = self.extract_keywords(combined_text, top_k=5)
            
            topics.append({
                'id': label,
                'keywords': keywords,
                'news': cluster_news,
                'size': len(cluster_news)  # 话题热度
            })
        
        # 按热度排序
        topics.sort(key=lambda x: x['size'], reverse=True)
        
        return topics
```

### 3. 市场复盘生成

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class MarketReview:
    def __init__(self, api_client):
        self.api_client = api_client
        
    def generate_daily_review(self, date=None):
        """生成每日市场复盘"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
            
        # 获取主要指数数据
        indices = self._get_indices_data(date)
        
        # 获取板块表现
        sectors = self._get_sectors_performance(date)
        
        # 获取市场资金流向
        fund_flows = self._get_fund_flows(date)
        
        # 获取市场热点新闻
        hot_news = self._get_hot_news(date)
        
        # 生成市场复盘报告
        review = self._generate_review_text(date, indices, sectors, fund_flows, hot_news)
        
        return {
            'date': date,
            'indices': indices,
            'sectors': sectors,
            'fund_flows': fund_flows,
            'hot_news': hot_news,
            'review_text': review
        }
    
    def _get_indices_data(self, date):
        """获取主要指数数据"""
        indices = ['SPY', '000001.SS', '399001.SZ', 'HSI']  # 示例：标普500、上证指数、深证成指、恒生指数
        indices_data = []
        
        for index in indices:
            try:
                # 获取指数当日数据
                data = self.api_client.call_api('YahooFinance/get_stock_chart', 
                                               query={'symbol': index, 
                                                     'interval': '1d', 
                                                     'range': '5d'})
                
                if 'chart' in data and 'result' in data['chart'] and data['chart']['result']:
                    result = data['chart']['result'][0]
                    
                    # 提取最新交易日数据
                    timestamps = result.get('timestamp', [])
                    quotes = result.get('indicators', {}).get('quote', [{}])[0]
                    
                    if timestamps and 'close' in quotes:
                        latest_idx = -1
                        latest_close = quotes['close'][latest_idx]
                        prev_close = quotes['close'][latest_idx-1] if len(quotes['close']) > 1 else latest_close
                        
                        change_pct = (latest_close - prev_close) / prev_close * 100
                        
                        indices_data.append({
                            'symbol': index,
                            'name': self._get_index_name(index),
                            'close': latest_close,
                            'change_pct': change_pct,
                            'volume': quotes.get('volume', [0])[latest_idx]
                        })
            except Exception as e:
                print(f"获取指数 {index} 数据时出错: {str(e)}")
        
        return indices_data
    
    def _get_sectors_performance(self, date):
        """获取板块表现"""
        # 这里可以实现获取各行业板块表现的逻辑
        # 示例数据
        sectors = [
            {'name': '科技', 'change_pct': 1.2, 'leaders': ['AAPL', 'MSFT']},
            {'name': '金融', 'change_pct': -0.5, 'leaders': ['JPM', 'BAC']},
            {'name': '医疗', 'change_pct': 0.8, 'leaders': ['JNJ', 'PFE']},
            {'name': '能源', 'change_pct': -1.3, 'leaders': ['XOM', 'CVX']},
            {'name': '消费', 'change_pct': 0.3, 'leaders': ['PG', 'KO']}
        ]
        
        # 按涨跌幅排序
        sectors.sort(key=lambda x: x['change_pct'], reverse=True)
        
        return sectors
    
    def _get_fund_flows(self, date):
        """获取市场资金流向"""
        # 这里可以实现获取资金流向的逻辑
        # 示例数据
        fund_flows = {
            'net_inflow': 1250000000,  # 净流入金额
            'sectors': [
                {'name': '科技', 'flow': 580000000},
                {'name': '医疗', 'flow': 320000000},
                {'name': '消费', 'flow': 150000000},
                {'name': '金融', 'flow': -120000000},
                {'name': '能源', 'flow': -180000000}
            ]
        }
        
        return fund_flows
    
    def _get_hot_news(self, date):
        """获取市场热点新闻"""
        # 这里可以实现获取热点新闻的逻辑
        # 示例数据
        hot_news = [
            {'title': '美联储维持利率不变，暗示年内可能降息', 'impact': 'high'},
            {'title': '科技巨头财报超预期，带动板块上涨', 'impact': 'medium'},
            {'title': '原油价格下跌，能源股承压', 'impact': 'medium'},
            {'title': '新冠疫苗研发取得突破，医药股走强', 'impact': 'high'}
        ]
        
        return hot_news
    
    def _generate_review_text(self, date, indices, sectors, fund_flows, hot_news):
        """生成复盘文本"""
        # 市场概览
        market_overview = self._generate_market_overview(indices)
        
        # 板块分析
        sector_analysis = self._generate_sector_analysis(sectors, fund_flows)
        
        # 热点分析
        hot_analysis = self._generate_hot_analysis(hot_news)
        
        # 市场展望
        market_outlook = self._generate_market_outlook(indices, sectors, hot_news)
        
        # 组合完整复盘报告
        review = f"""# {date} 市场复盘

## 市场概览
{market_overview}

## 板块分析
{sector_analysis}

## 今日热点
{hot_analysis}

## 市场展望
{market_outlook}
"""
        return review
    
    def _generate_market_overview(self, indices):
        """生成市场概览文本"""
        if not indices:
            return "今日无交易数据。"
            
        # 计算平均涨跌幅
        avg_change = sum(idx['change_pct'] for idx in indices) / len(indices)
        
        # 判断市场整体表现
        if avg_change > 1.5:
            tone = "大幅上涨"
        elif avg_change > 0.5:
            tone = "普遍上涨"
        elif avg_change > -0.5:
            tone = "基本持平"
        elif avg_change > -1.5:
            tone = "普遍下跌"
        else:
            tone = "大幅下跌"
            
        # 生成概览文本
        text = f"今日市场{tone}，"
        
        # 添加各指数表现
        for idx in indices:
            direction = "上涨" if idx['change_pct'] > 0 else "下跌"
            text += f"{idx['name']}({idx['symbol']}) {direction} {abs(idx['change_pct']):.2f}%，"
            
        text = text[:-1] + "。"  # 替换最后一个逗号为句号
        
        return text
    
    def _generate_sector_analysis(self, sectors, fund_flows):
        """生成板块分析文本"""
        if not sectors:
            return "无板块数据。"
            
        # 领涨板块
        leading_sectors = [s for s in sectors if s['change_pct'] > 0]
        leading_sectors.sort(key=lambda x: x['change_pct'], reverse=True)
        
        # 领跌板块
        lagging_sectors = [s for s in sectors if s['change_pct'] <= 0]
        lagging_sectors.sort(key=lambda x: x['change_pct'])
        
        text = ""
        
        # 领涨板块分析
        if leading_sectors:
            text += "**领涨板块**：\n\n"
            for sector in leading_sectors[:3]:  # 取前三个领涨板块
                text += f"- {sector['name']}板块上涨{sector['change_pct']:.2f}%，"
                if sector['leaders']:
                    text += f"其中{', '.join(sector['leaders'][:2])}表现强势。\n"
                else:
                    text += "\n"
            text += "\n"
        
        # 领跌板块分析
        if lagging_sectors:
            text += "**领跌板块**：\n\n"
            for sector in lagging_sectors[:3]:  # 取前三个领跌板块
                text += f"- {sector['name']}板块下跌{abs(sector['change_pct']):.2f}%，"
                if sector['leaders']:
                    text += f"其中{', '.join(sector['leaders'][:2])}跌幅明显。\n"
                else:
                    text += "\n"
            text += "\n"
        
        # 资金流向分析
        if fund_flows:
            net_flow = fund_flows['net_inflow']
            if net_flow > 0:
                text += f"今日市场资金净流入{net_flow/1e8:.2f}亿元，"
            else:
                text += f"今日市场资金净流出{abs(net_flow)/1e8:.2f}亿元，"
                
            # 资金流入前两个板块
            inflow_sectors = sorted(fund_flows['sectors'], key=lambda x: x['flow'], reverse=True)[:2]
            if inflow_sectors:
                text += f"主要流入{inflow_sectors[0]['name']}"
                if len(inflow_sectors) > 1:
                    text += f"和{inflow_sectors[1]['name']}"
                text += "板块。"
        
        return text
    
    def _generate_hot_analysis(self, hot_news):
        """生成热点分析文本"""
        if not hot_news:
            return "今日无重大市场热点。"
            
        text = ""
        
        # 高影响力热点
        high_impact_news = [news for news in hot_news if news['impact'] == 'high']
        if high_impact_news:
            text += "**重要热点**：\n\n"
            for news in high_impact_news:
                text += f"- {news['title']}\n"
            text += "\n"
        
        # 中等影响力热点
        medium_impact_news = [news for news in hot_news if news['impact'] == 'medium']
        if medium_impact_news:
            text += "**次要热点**：\n\n"
            for news in medium_impact_news:
                text += f"- {news['title']}\n"
        
        return text
    
    def _generate_market_outlook(self, indices, sectors, hot_news):
        """生成市场展望文本"""
        # 这里可以实现更复杂的逻辑，基于当前市场状况生成展望
        # 示例简单实现
        
        # 计算平均涨跌幅
        avg_change = sum(idx['change_pct'] for idx in indices) / len(indices) if indices else 0
        
        if avg_change > 1:
            outlook = "市场情绪偏向乐观，短期可能继续保持强势。建议关注成交量能否持续配合，以及市场领涨板块的轮动情况。"
        elif avg_change > 0:
            outlook = "市场呈现温和上涨，整体趋势向好。建议关注市场热点的持续性，以及外部因素对市场的潜在影响。"
        elif avg_change > -1:
            outlook = "市场表现平淡，方向不明确。建议等待更明确的市场信号，关注成交量和主力资金动向。"
        else:
            outlook = "市场承压下行，短期可能继续调整。建议关注重要支撑位的表现，以及是否出现超跌反弹机会。"
            
        return outlook
    
    def _get_index_name(self, symbol):
        """获取指数名称"""
        index_names = {
            'SPY': '标普500',
            '000001.SS': '上证指数',
            '399001.SZ': '深证成指',
            'HSI': '恒生指数',
            '^DJI': '道琼斯工业',
            '^IXIC': '纳斯达克',
            '^N225': '日经225'
        }
        return index_names.get(symbol, symbol)
```

## 用户界面设计

### 1. 热点资讯页面

- **展示内容**：
  - 热点资讯列表（标题、来源、发布时间、情感标签）
  - 热点话题聚合区（按主题分类的相关新闻）
  - 热门股票关联区（与热点相关的股票）
  - 市场情绪指标（恐慌/贪婪指数）

- **交互功能**：
  - 资讯筛选（按类别、时间、相关性）
  - 资讯搜索
  - 收藏和分享
  - 点击查看详情

### 2. 今日复盘页面

- **展示内容**：
  - 市场概览（主要指数表现、成交量、涨跌家数）
  - 板块轮动分析（各板块涨跌幅、资金流向）
  - 热点分析（重要新闻及其影响）
  - 技术面分析（大盘技术指标、形态分析）
  - 市场展望（短期趋势判断）

- **交互功能**：
  - 历史复盘查看
  - 自定义复盘内容
  - 复盘报告导出
  - 相关股票查询

### 3. 个股热点页面

- **展示内容**：
  - 个股相关新闻
  - 分析师评级变动
  - 相关板块热点
  - 公司公告和重大事件

- **交互功能**：
  - 添加到自选
  - 设置新闻提醒
  - 查看历史新闻
  - 相关股票推荐

### 4. 热点日历

- **展示内容**：
  - 重要经济数据发布日程
  - 财报发布日程
  - 重要会议和事件
  - 节假日信息

- **交互功能**：
  - 日历视图切换
  - 事件提醒设置
  - 自定义事件添加
  - 历史事件查询

## 实现计划

### 阶段一：数据采集与处理

1. 实现多源数据采集模块
2. 开发新闻分类和情感分析功能
3. 实现热点话题提取算法

### 阶段二：内容生成

1. 开发热点资讯聚合功能
2. 实现市场复盘报告生成
3. 开发个性化推荐算法

### 阶段三：用户界面开发

1. 设计并实现热点资讯页面
2. 开发今日复盘页面
3. 实现个股热点和热点日历功能

### 阶段四：系统集成与优化

1. 将热点资讯与复盘功能集成到现有平台
2. 优化内容生成质量和性能
3. 完善用户交互和个性化体验

## 技术栈选择

- **后端**：Python、Pandas、NumPy
- **NLP工具**：Transformers、jieba、NLTK
- **前端框架**：Streamlit（与现有平台保持一致）
- **数据存储**：SQLite/PostgreSQL
- **可视化**：Plotly、Matplotlib

## 评估指标

- **内容质量**：资讯准确性、复盘分析质量
- **用户体验**：页面加载速度、交互流畅度
- **用户参与度**：阅读时长、访问频率、互动率

## 风险与挑战

1. **数据质量**：新闻源可能存在质量和可靠性问题
2. **内容生成**：自动生成的复盘内容可能缺乏深度
3. **实时性**：热点资讯需要及时更新
4. **个性化**：不同用户对内容的需求差异较大

## 缓解措施

1. 实现多源数据交叉验证，提高数据可靠性
2. 结合模板和AI生成技术，提升内容质量
3. 优化数据更新机制，确保内容时效性
4. 加强用户画像和个性化推荐算法
