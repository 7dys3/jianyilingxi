import os
import sys
import pandas as pd
import numpy as np
import json
import datetime
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
from PIL import Image
import io
import base64

# 设置页面配置
st.set_page_config(
    page_title="金融智能分析平台",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 添加CSS样式
def add_custom_css():
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #0D47A1;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: #f8f9fa;
        box-shadow: 0 0.25rem 0.75rem rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
    }
    .highlight {
        color: #E53935;
        font-weight: bold;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        color: #757575;
        font-size: 0.8rem;
    }
    </style>
    """, unsafe_allow_html=True)

add_custom_css()

# 模拟数据生成函数
def generate_stock_data(symbol, days=30):
    np.random.seed(42)  # 确保可重复性
    date_today = datetime.datetime.now()
    dates = [date_today - datetime.timedelta(days=i) for i in range(days)]
    dates.reverse()
    
    # 生成初始价格和波动
    initial_price = np.random.uniform(50, 200)
    prices = [initial_price]
    for i in range(1, days):
        change = np.random.normal(0, 1) * 2  # 每日变化
        new_price = max(prices[-1] + change, 1)  # 确保价格为正
        prices.append(new_price)
    
    # 生成成交量
    volumes = np.random.randint(100000, 1000000, size=days)
    
    # 创建DataFrame
    df = pd.DataFrame({
        'date': dates,
        'open': prices,
        'high': [p * (1 + np.random.uniform(0, 0.02)) for p in prices],
        'low': [p * (1 - np.random.uniform(0, 0.02)) for p in prices],
        'close': [p * (1 + np.random.normal(0, 0.01)) for p in prices],
        'volume': volumes
    })
    
    return df

# 生成技术指标
def calculate_technical_indicators(df):
    # 计算移动平均线
    df['MA5'] = df['close'].rolling(window=5).mean()
    df['MA10'] = df['close'].rolling(window=10).mean()
    df['MA20'] = df['close'].rolling(window=20).mean()
    
    # 计算MACD
    df['EMA12'] = df['close'].ewm(span=12, adjust=False).mean()
    df['EMA26'] = df['close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = df['EMA12'] - df['EMA26']
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['Histogram'] = df['MACD'] - df['Signal']
    
    # 计算RSI
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    return df

# 股票推荐系统
class StockRecommendationSystem:
    def __init__(self):
        self.stock_universe = [
            {"symbol": "AAPL", "name": "苹果公司", "sector": "科技", "industry": "消费电子"},
            {"symbol": "MSFT", "name": "微软公司", "sector": "科技", "industry": "软件"},
            {"symbol": "GOOGL", "name": "Alphabet公司", "sector": "科技", "industry": "互联网"},
            {"symbol": "AMZN", "name": "亚马逊公司", "sector": "消费者服务", "industry": "电子商务"},
            {"symbol": "TSLA", "name": "特斯拉公司", "sector": "汽车", "industry": "电动汽车"},
            {"symbol": "NVDA", "name": "英伟达公司", "sector": "科技", "industry": "半导体"},
            {"symbol": "META", "name": "Meta平台公司", "sector": "科技", "industry": "社交媒体"},
            {"symbol": "BABA", "name": "阿里巴巴集团", "sector": "消费者服务", "industry": "电子商务"},
            {"symbol": "TCEHY", "name": "腾讯控股", "sector": "科技", "industry": "互联网"},
            {"symbol": "TSM", "name": "台积电", "sector": "科技", "industry": "半导体"}
        ]
    
    def get_stock_data(self, symbol, days=30):
        return generate_stock_data(symbol, days)
    
    def calculate_win_rate(self, symbol, lookback_period=30, holding_period=5):
        """计算股票的历史胜率"""
        stock_data = self.get_stock_data(symbol, lookback_period + holding_period)
        stock_data = calculate_technical_indicators(stock_data)
        
        # 模拟胜率计算
        np.random.seed(hash(symbol) % 100)  # 使不同股票有不同的随机性
        win_rate = np.random.uniform(40, 85)
        
        return win_rate
    
    def get_recommendations(self, sector=None, min_win_rate=50):
        """获取股票推荐"""
        recommendations = []
        
        for stock in self.stock_universe:
            if sector and stock["sector"] != sector:
                continue
                
            win_rate = self.calculate_win_rate(stock["symbol"])
            
            if win_rate >= min_win_rate:
                stock_data = self.get_stock_data(stock["symbol"])
                last_price = stock_data["close"].iloc[-1]
                price_change = ((last_price / stock_data["close"].iloc[0]) - 1) * 100
                
                recommendations.append({
                    "symbol": stock["symbol"],
                    "name": stock["name"],
                    "sector": stock["sector"],
                    "industry": stock["industry"],
                    "win_rate": win_rate,
                    "last_price": last_price,
                    "price_change": price_change,
                    "recommendation_reason": self.generate_recommendation_reason(stock["symbol"], win_rate)
                })
        
        # 按胜率排序
        recommendations.sort(key=lambda x: x["win_rate"], reverse=True)
        
        return recommendations
    
    def generate_recommendation_reason(self, symbol, win_rate):
        """生成推荐理由"""
        reasons = [
            f"技术指标显示强势上涨趋势，历史胜率{win_rate:.1f}%",
            f"突破关键阻力位，短期有望继续上涨，历史胜率{win_rate:.1f}%",
            f"MACD金叉形成，买入信号明确，历史胜率{win_rate:.1f}%",
            f"量价配合良好，上涨动能强劲，历史胜率{win_rate:.1f}%",
            f"RSI指标从超卖区回升，反弹信号明确，历史胜率{win_rate:.1f}%"
        ]
        
        np.random.seed(hash(symbol) % 100)
        return np.random.choice(reasons)

# 图表分析系统
class ChartAnalysisSystem:
    def __init__(self):
        pass
    
    def get_stock_data(self, symbol, days=60):
        return generate_stock_data(symbol, days)
    
    def identify_patterns(self, symbol):
        """识别股票图表中的技术形态"""
        patterns = []
        
        # 模拟识别结果
        possible_patterns = [
            {"name": "头肩顶", "type": "看跌反转", "confidence": 0.85, "description": "价格形成三个高点，中间高点最高，两侧高点大致相等，预示着上升趋势即将结束。"},
            {"name": "头肩底", "type": "看涨反转", "confidence": 0.78, "description": "价格形成三个低点，中间低点最低，两侧低点大致相等，预示着下降趋势即将结束。"},
            {"name": "双顶", "type": "看跌反转", "confidence": 0.82, "description": "价格两次触及相似的高点后回落，预示着上升趋势即将结束。"},
            {"name": "双底", "type": "看涨反转", "confidence": 0.75, "description": "价格两次触及相似的低点后反弹，预示着下降趋势即将结束。"},
            {"name": "三角形整理", "type": "持续", "confidence": 0.68, "description": "价格波动幅度逐渐减小，形成三角形，通常是当前趋势的短暂休整。"},
            {"name": "旗形", "type": "持续", "confidence": 0.72, "description": "在强劲的趋势中出现的小型矩形整理，通常预示着趋势将继续。"},
            {"name": "楔形", "type": "反转", "confidence": 0.65, "description": "价格通道逐渐收窄，与当前趋势方向相反，通常预示着趋势即将反转。"}
        ]
        
        # 根据股票代码选择1-3个模式
        np.random.seed(hash(symbol) % 100)
        num_patterns = np.random.randint(1, 4)
        selected_patterns = np.random.choice(possible_patterns, num_patterns, replace=False)
        
        for pattern in selected_patterns:
            patterns.append(pattern)
        
        return patterns
    
    def identify_support_resistance(self, symbol):
        """识别支撑位和阻力位"""
        stock_data = self.get_stock_data(symbol)
        
        # 模拟支撑位和阻力位
        close_prices = stock_data["close"].values
        min_price = np.min(close_prices)
        max_price = np.max(close_prices)
        current_price = close_prices[-1]
        
        # 生成支撑位
        supports = []
        for i in range(1, 4):
            level = current_price * (1 - 0.05 * i) + np.random.uniform(-2, 2)
            if level > min_price * 0.95:
                strength = np.random.uniform(0.6, 0.9)
                supports.append({"level": level, "strength": strength})
        
        # 生成阻力位
        resistances = []
        for i in range(1, 4):
            level = current_price * (1 + 0.05 * i) + np.random.uniform(-2, 2)
            if level < max_price * 1.05:
                strength = np.random.uniform(0.6, 0.9)
                resistances.append({"level": level, "strength": strength})
        
        return {"supports": supports, "resistances": resistances}
    
    def identify_trend_lines(self, symbol):
        """识别趋势线"""
        # 模拟趋势线识别结果
        np.random.seed(hash(symbol) % 100)
        
        trend_types = ["上升趋势", "下降趋势", "横盘整理"]
        trend_type = np.random.choice(trend_types, p=[0.4, 0.3, 0.3])
        
        strength = np.random.uniform(0.6, 0.95)
        duration = np.random.randint(10, 50)
        
        return {
            "trend_type": trend_type,
            "strength": strength,
            "duration_days": duration,
            "description": f"{trend_type}已持续{duration}天，趋势强度为{strength:.2f}"
        }
    
    def generate_analysis_report(self, symbol):
        """生成综合分析报告"""
        patterns = self.identify_patterns(symbol)
        support_resistance = self.identify_support_resistance(symbol)
        trend_line = self.identify_trend_lines(symbol)
        
        # 根据分析结果生成投资建议
        if trend_line["trend_type"] == "上升趋势" and trend_line["strength"] > 0.7:
            if any(p["type"] == "看涨反转" for p in patterns):
                recommendation = "强烈买入"
                reason = "上升趋势强劲，同时出现看涨反转形态"
            else:
                recommendation = "买入"
                reason = "上升趋势明确，可以考虑买入"
        elif trend_line["trend_type"] == "下降趋势" and trend_line["strength"] > 0.7:
            if any(p["type"] == "看跌反转" for p in patterns):
                recommendation = "强烈卖出"
                reason = "下降趋势强劲，同时出现看跌反转形态"
            else:
                recommendation = "卖出"
                reason = "下降趋势明确，建议规避风险"
        else:
            recommendation = "观望"
            reason = "趋势不明确，建议等待更清晰的信号"
        
        return {
            "patterns": patterns,
            "support_resistance": support_resistance,
            "trend_line": trend_line,
            "recommendation": recommendation,
            "reason": reason
        }

# 热点资讯与市场复盘系统
class NewsAndMarketReviewSystem:
    def __init__(self):
        self.news_data = []
        self.generate_mock_news()
    
    def generate_mock_news(self):
        """生成模拟新闻数据"""
        news_templates = [
            {"title": "{公司}发布新一代{产品}，{特点}引发市场关注", "category": "公司新闻"},
            {"title": "{公司}第{季度}季度财报超预期，{增长点}表现亮眼", "category": "财报"},
            {"title": "{分析师}：{行业}行业迎来拐点，{原因}将推动长期增长", "category": "行业分析"},
            {"title": "{国家}宣布新的{政策}，{影响}引发市场波动", "category": "政策"},
            {"title": "{指数}创{时间段}新高，{板块}板块领涨", "category": "市场动态"}
        ]
        
        companies = ["苹果", "微软", "谷歌", "亚马逊", "特斯拉", "阿里巴巴", "腾讯", "百度", "京东", "美团"]
        products = ["智能手机", "云服务", "人工智能平台", "电动汽车", "芯片", "操作系统", "支付服务"]
        features = ["创新设计", "性能提升", "价格优势", "用户体验改进", "技术突破"]
        quarters = ["一", "二", "三", "四"]
        growth_points = ["营收", "利润", "用户增长", "海外市场", "新业务"]
        analysts = ["高盛", "摩根士丹利", "中金公司", "华泰证券", "野村证券"]
        industries = ["科技", "新能源", "医疗健康", "消费", "金融", "制造业"]
        reasons = ["政策支持", "技术创新", "需求增长", "产业升级", "全球化布局"]
        countries = ["中国", "美国", "欧盟", "日本", "印度"]
        policies = ["财政刺激计划", "货币政策调整", "产业支持政策", "监管措施", "税收改革"]
        impacts = ["利好科技股", "提振市场信心", "引发通胀担忧", "加剧市场波动", "改变行业格局"]
        indices = ["上证指数", "深证成指", "创业板指", "道琼斯指数", "纳斯达克指数"]
        time_periods = ["年内", "三年来", "历史", "近五年", "季度"]
        sectors = ["科技", "金融", "医药", "消费", "新能源", "半导体"]
        
        # 生成30条模拟新闻
        for i in range(30):
            template = news_templates[i % len(news_templates)]
            title = template["title"]
            category = template["category"]
            
            # 替换占位符
            if "{公司}" in title:
                title = title.replace("{公司}", np.random.choice(companies))
            if "{产品}" in title:
                title = title.replace("{产品}", np.random.choice(products))
            if "{特点}" in title:
                title = title.replace("{特点}", np.random.choice(features))
            if "{季度}" in title:
                title = title.replace("{季度}", np.random.choice(quarters))
            if "{增长点}" in title:
                title = title.replace("{增长点}", np.random.choice(growth_points))
            if "{分析师}" in title:
                title = title.replace("{分析师}", np.random.choice(analysts))
            if "{行业}" in title:
                title = title.replace("{行业}", np.random.choice(industries))
            if "{原因}" in title:
                title = title.replace("{原因}", np.random.choice(reasons))
            if "{国家}" in title:
                title = title.replace("{国家}", np.random.choice(countries))
            if "{政策}" in title:
                title = title.replace("{政策}", np.random.choice(policies))
            if "{影响}" in title:
                title = title.replace("{影响}", np.random.choice(impacts))
            if "{指数}" in title:
                title = title.replace("{指数}", np.random.choice(indices))
            if "{时间段}" in title:
                title = title.replace("{时间段}", np.random.choice(time_periods))
            if "{板块}" in title:
                title = title.replace("{板块}", np.random.choice(sectors))
            
            # 生成日期（最近7天内的随机日期）
            days_ago = np.random.randint(0, 7)
            date = datetime.datetime.now() - datetime.timedelta(days=days_ago)
            date_str = date.strftime("%Y-%m-%d")
            
            # 生成来源
            sources = ["财经网", "证券时报", "经济日报", "华尔街日报", "彭博社", "路透社"]
            source = np.random.choice(sources)
            
            # 生成内容摘要
            summary = f"这是关于{title}的新闻摘要。详细内容包括相关背景、影响分析和未来展望。"
            
            self.news_data.append({
                "title": title,
                "date": date_str,
                "source": source,
                "category": category,
                "summary": summary,
                "url": "#"  # 模拟URL
            })
        
        # 按日期排序，最新的在前
        self.news_data.sort(key=lambda x: x["date"], reverse=True)
    
    def get_latest_news(self, category=None, limit=10):
        """获取最新新闻"""
        if category:
            filtered_news = [news for news in self.news_data if news["category"] == category]
            return filtered_news[:limit]
        else:
            return self.news_data[:limit]
    
    def get_hot_topics(self):
        """获取热点话题"""
        topics = [
            {"keyword": "人工智能", "heat": 95, "related_news": self.news_data[:3]},
            {"keyword": "新能源车", "heat": 88, "related_news": self.news_data[3:6]},
            {"keyword": "半导体", "heat": 82, "related_news": self.news_data[6:9]},
            {"keyword": "元宇宙", "heat": 75, "related_news": self.news_data[9:12]},
            {"keyword": "数字货币", "heat": 70, "related_news": self.news_data[12:15]}
        ]
        return topics
    
    def generate_market_review(self):
        """生成市场复盘"""
        # 模拟指数表现
        indices = [
            {"name": "上证指数", "change_percent": np.random.uniform(-1.5, 1.5)},
            {"name": "深证成指", "change_percent": np.random.uniform(-1.8, 1.8)},
            {"name": "创业板指", "change_percent": np.random.uniform(-2.0, 2.0)},
            {"name": "科创50", "change_percent": np.random.uniform(-2.2, 2.2)}
        ]
        
        # 模拟板块表现
        sectors = [
            {"name": "科技", "change_percent": np.random.uniform(-2.5, 2.5)},
            {"name": "金融", "change_percent": np.random.uniform(-1.5, 1.5)},
            {"name": "医药", "change_percent": np.random.uniform(-2.0, 2.0)},
            {"name": "消费", "change_percent": np.random.uniform(-1.8, 1.8)},
            {"name": "新能源", "change_percent": np.random.uniform(-3.0, 3.0)},
            {"name": "半导体", "change_percent": np.random.uniform(-3.5, 3.5)}
        ]
        
        # 模拟市场情绪
        sentiment_options = ["乐观", "谨慎", "中性", "悲观", "恐慌"]
        sentiment_weights = [0.2, 0.3, 0.3, 0.15, 0.05]
        market_sentiment = np.random.choice(sentiment_options, p=sentiment_weights)
        
        # 生成复盘摘要
        summary_templates = [
            "今日市场{走势}，{表现最好板块}板块表现最佳，{表现最差板块}板块跌幅居前。{市场情绪}情绪占据主导，{原因}是主要影响因素。",
            "{主要指数}今日{走势}，成交量{成交量变化}。{涨跌原因}，市场情绪{市场情绪}。后市关注{关注点}。",
            "受{影响因素}影响，今日市场{走势}。板块方面，{表现最好板块}领涨，{表现最差板块}领跌。市场整体情绪{市场情绪}。"
        ]
        
        # 选择模板并填充
        template = np.random.choice(summary_templates)
        
        # 计算表现最好和最差的板块
        sectors.sort(key=lambda x: x["change_percent"], reverse=True)
        best_sector = sectors[0]["name"]
        worst_sector = sectors[-1]["name"]
        
        # 确定市场走势
        avg_change = np.mean([idx["change_percent"] for idx in indices])
        if avg_change > 1.0:
            trend = "大幅上涨"
        elif avg_change > 0.3:
            trend = "小幅上涨"
        elif avg_change > -0.3:
            trend = "基本平稳"
        elif avg_change > -1.0:
            trend = "小幅下跌"
        else:
            trend = "大幅下跌"
        
        # 生成成交量变化
        volume_changes = ["明显放大", "小幅放大", "基本持平", "小幅萎缩", "明显萎缩"]
        volume_change = np.random.choice(volume_changes)
        
        # 生成涨跌原因
        reasons = [
            "受海外市场影响", 
            "政策面利好刺激", 
            "经济数据超预期", 
            "资金面趋紧", 
            "获利盘回吐压力增大",
            "市场情绪谨慎"
        ]
        reason = np.random.choice(reasons)
        
        # 生成关注点
        focus_points = [
            "政策动向", 
            "资金面变化", 
            "海外市场波动", 
            "重要经济数据", 
            "板块轮动",
            "热点持续性"
        ]
        focus = np.random.choice(focus_points)
        
        # 填充模板
        summary = template
        if "{走势}" in summary:
            summary = summary.replace("{走势}", trend)
        if "{表现最好板块}" in summary:
            summary = summary.replace("{表现最好板块}", best_sector)
        if "{表现最差板块}" in summary:
            summary = summary.replace("{表现最差板块}", worst_sector)
        if "{市场情绪}" in summary:
            summary = summary.replace("{市场情绪}", market_sentiment)
        if "{原因}" in summary:
            summary = summary.replace("{原因}", reason)
        if "{主要指数}" in summary:
            summary = summary.replace("{主要指数}", indices[0]["name"])
        if "{成交量变化}" in summary:
            summary = summary.replace("{成交量变化}", volume_change)
        if "{涨跌原因}" in summary:
            summary = summary.replace("{涨跌原因}", reason)
        if "{关注点}" in summary:
            summary = summary.replace("{关注点}", focus)
        if "{影响因素}" in summary:
            summary = summary.replace("{影响因素}", reason)
        
        return {
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "indices": indices,
            "sectors": sectors,
            "market_sentiment": market_sentiment,
            "summary": summary
        }

# 智能投顾系统
class IntelligentAdvisorSystem:
    def __init__(self):
        pass
    
    def assess_risk_tolerance(self, answers):
        """评估风险承受能力"""
        # 简单的风险评分计算
        score = sum(answers.values())
        
        if score < 10:
            risk_profile = "保守型"
            description = "您倾向于稳健的投资策略，更注重资金安全，对投资波动的容忍度较低。"
        elif score < 20:
            risk_profile = "稳健型"
            description = "您能够接受适度的投资波动，在追求收益的同时也重视资金安全。"
        elif score < 30:
            risk_profile = "平衡型"
            description = "您能够平衡风险和收益，可以接受中等程度的投资波动。"
        elif score < 40:
            risk_profile = "成长型"
            description = "您更注重长期收益，能够接受较大的投资波动。"
        else:
            risk_profile = "进取型"
            description = "您追求高收益，能够承受较大的投资风险和市场波动。"
        
        return {
            "risk_profile": risk_profile,
            "score": score,
            "description": description
        }
    
    def generate_asset_allocation(self, risk_profile):
        """生成资产配置建议"""
        if risk_profile == "保守型":
            allocation = {
                "现金及等价物": 20,
                "债券": 50,
                "股票": 20,
                "另类投资": 10
            }
            expected_return = "4%-6%"
            volatility = "低"
        elif risk_profile == "稳健型":
            allocation = {
                "现金及等价物": 15,
                "债券": 40,
                "股票": 35,
                "另类投资": 10
            }
            expected_return = "5%-8%"
            volatility = "中低"
        elif risk_profile == "平衡型":
            allocation = {
                "现金及等价物": 10,
                "债券": 30,
                "股票": 50,
                "另类投资": 10
            }
            expected_return = "7%-10%"
            volatility = "中等"
        elif risk_profile == "成长型":
            allocation = {
                "现金及等价物": 5,
                "债券": 20,
                "股票": 65,
                "另类投资": 10
            }
            expected_return = "9%-12%"
            volatility = "中高"
        else:  # 进取型
            allocation = {
                "现金及等价物": 5,
                "债券": 10,
                "股票": 75,
                "另类投资": 10
            }
            expected_return = "10%以上"
            volatility = "高"
        
        return {
            "allocation": allocation,
            "expected_return": expected_return,
            "volatility": volatility
        }
    
    def generate_investment_recommendations(self, risk_profile):
        """生成投资产品推荐"""
        recommendations = []
        
        if risk_profile in ["保守型", "稳健型"]:
            recommendations.extend([
                {"name": "国债ETF", "type": "债券", "risk_level": "低", "expected_return": "3%-4%", "description": "追踪国债指数的ETF，波动小，收益稳定。"},
                {"name": "货币市场基金", "type": "现金等价物", "risk_level": "极低", "expected_return": "2%-3%", "description": "投资于短期货币市场工具，流动性高，风险极低。"},
                {"name": "高等级信用债基金", "type": "债券", "risk_level": "低", "expected_return": "4%-5%", "description": "投资于高信用等级的企业债券，收益相对稳定。"}
            ])
        
        if risk_profile in ["稳健型", "平衡型"]:
            recommendations.extend([
                {"name": "混合型基金", "type": "混合", "risk_level": "中", "expected_return": "6%-8%", "description": "同时投资股票和债券，平衡风险和收益。"},
                {"name": "蓝筹股ETF", "type": "股票", "risk_level": "中高", "expected_return": "7%-9%", "description": "追踪大型蓝筹股指数，长期表现稳健。"},
                {"name": "REITs", "type": "另类投资", "risk_level": "中", "expected_return": "5%-7%", "description": "房地产投资信托，提供稳定的租金收入和潜在的资本增值。"}
            ])
        
        if risk_profile in ["平衡型", "成长型", "进取型"]:
            recommendations.extend([
                {"name": "科技行业ETF", "type": "股票", "risk_level": "高", "expected_return": "10%-15%", "description": "追踪科技行业指数，高增长潜力但波动较大。"},
                {"name": "新兴市场ETF", "type": "股票", "risk_level": "高", "expected_return": "9%-14%", "description": "投资新兴市场国家的股票，提供多元化的国际市场敞口。"},
                {"name": "小盘成长股基金", "type": "股票", "risk_level": "高", "expected_return": "12%-18%", "description": "投资于小市值高增长公司，潜在回报高但风险也高。"}
            ])
        
        if risk_profile in ["成长型", "进取型"]:
            recommendations.extend([
                {"name": "区块链ETF", "type": "股票", "risk_level": "极高", "expected_return": "15%以上", "description": "投资于区块链相关公司，高风险高回报。"},
                {"name": "人工智能主题基金", "type": "股票", "risk_level": "高", "expected_return": "12%-20%", "description": "投资于人工智能领域的公司，长期增长潜力大。"},
                {"name": "私募股权基金", "type": "另类投资", "risk_level": "极高", "expected_return": "15%-25%", "description": "投资于非上市公司，流动性低但潜在回报高。"}
            ])
        
        return recommendations
    
    def generate_financial_plan(self, user_info, risk_profile):
        """生成财务规划"""
        # 根据用户信息和风险偏好生成财务规划
        monthly_income = user_info.get("monthly_income", 10000)
        monthly_expenses = user_info.get("monthly_expenses", 5000)
        savings = user_info.get("savings", 100000)
        debt = user_info.get("debt", 0)
        age = user_info.get("age", 30)
        retirement_age = user_info.get("retirement_age", 60)
        
        # 计算每月可投资金额
        monthly_investment = monthly_income - monthly_expenses
        
        # 计算紧急备用金建议
        emergency_fund = monthly_expenses * 6
        
        # 计算退休所需资金
        years_to_retirement = retirement_age - age
        retirement_years = 85 - retirement_age  # 假设寿命85岁
        monthly_retirement_need = monthly_expenses * 0.8  # 退休后支出可能降低
        annual_retirement_need = monthly_retirement_need * 12
        
        # 简单计算退休所需总资金（不考虑通胀和投资回报）
        total_retirement_need = annual_retirement_need * retirement_years
        
        # 根据风险偏好确定投资回报率
        if risk_profile == "保守型":
            expected_return_rate = 0.05
        elif risk_profile == "稳健型":
            expected_return_rate = 0.07
        elif risk_profile == "平衡型":
            expected_return_rate = 0.08
        elif risk_profile == "成长型":
            expected_return_rate = 0.1
        else:  # 进取型
            expected_return_rate = 0.12
        
        # 计算达到退休目标所需的每月投资金额
        # 使用简化的计算方法
        monthly_investment_needed = (total_retirement_need - savings * (1 + expected_return_rate) ** years_to_retirement) / (((1 + expected_return_rate) ** years_to_retirement - 1) / expected_return_rate * 12)
        
        # 确保计算结果合理
        monthly_investment_needed = max(0, monthly_investment_needed)
        
        # 生成投资建议
        if monthly_investment >= monthly_investment_needed:
            investment_advice = f"您当前的每月可投资金额（{monthly_investment}元）足以满足退休目标。建议按照资产配置方案进行投资，并定期检查投资组合表现。"
        else:
            gap = monthly_investment_needed - monthly_investment
            investment_advice = f"您当前的每月可投资金额（{monthly_investment}元）与达成退休目标所需的金额（{monthly_investment_needed:.2f}元）有{gap:.2f}元的差距。建议增加收入或减少支出，提高投资金额。"
        
        # 债务管理建议
        if debt > 0:
            debt_advice = "您有未偿还的债务。建议优先偿还高利率债务，然后再增加投资金额。"
        else:
            debt_advice = "您没有债务负担，可以专注于投资增值。"
        
        return {
            "emergency_fund_recommendation": emergency_fund,
            "monthly_investment_current": monthly_investment,
            "monthly_investment_needed": monthly_investment_needed,
            "total_retirement_need": total_retirement_need,
            "investment_advice": investment_advice,
            "debt_advice": debt_advice
        }

# 客服服务系统
class CustomerServiceSystem:
    def __init__(self):
        self.faqs = [
            {"question": "如何开始使用股票推荐功能？", "answer": "您可以在左侧导航栏选择\"股票推荐\"功能，然后根据自己的偏好设置筛选条件，系统会为您推荐符合条件的股票。"},
            {"question": "图表分析系统支持哪些技术形态识别？", "answer": "我们的图表分析系统支持多种技术形态识别，包括头肩顶/底、双顶/双底、三角形整理、旗形、楔形等常见形态，以及支撑位/阻力位和趋势线的自动识别。"},
            {"question": "如何查看最新的市场热点？", "answer": "您可以在\"热点资讯\"页面查看最新的市场热点话题和相关新闻，我们会每日更新市场热点分析和词云图，帮助您把握市场脉搏。"},
            {"question": "智能投顾功能如何使用？", "answer": "首先在\"智能投顾\"页面完成风险评估问卷，系统会根据您的风险偏好和投资目标，为您生成个性化的资产配置方案和投资建议。"},
            {"question": "平台的数据来源是什么？", "answer": "我们的数据来源包括雅虎财经、东方财富、新浪财经等多个权威金融数据提供商，确保数据的准确性和及时性。"}
        ]
    
    def get_answer(self, question):
        """获取问题的答案"""
        # 简单的关键词匹配
        for faq in self.faqs:
            if any(keyword in question for keyword in faq["question"].split()):
                return faq["answer"]
        
        # 如果没有匹配到FAQ，返回默认回答
        return "感谢您的提问。这个问题可能需要更专业的解答，建议您联系我们的客服专员获取帮助。您可以通过页面右上角的"联系客服"按钮与客服专员取得联系。"
    
    def get_all_faqs(self):
        """获取所有FAQ"""
        return self.faqs

# 主应用
def main():
    # 初始化系统
    stock_recommendation_system = StockRecommendationSystem()
    chart_analysis_system = ChartAnalysisSystem()
    news_system = NewsAndMarketReviewSystem()
    advisor_system = IntelligentAdvisorSystem()
    customer_service_system = CustomerServiceSystem()
    
    # 设置页面标题
    st.markdown('<h1 class="main-header">金融智能分析平台</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center;">集成AI驱动的股票分析、市场资讯和智能投顾服务</p>', unsafe_allow_html=True)
    
    # 侧边栏导航
    st.sidebar.title("功能导航")
    page = st.sidebar.radio(
        "选择功能",
        ["首页", "股票推荐", "图表分析", "热点资讯", "智能投顾", "人工客服"]
    )
    
    # 根据选择的页面显示不同内容
    if page == "首页":
        render_home_page(news_system, stock_recommendation_system, customer_service_system)
    elif page == "股票推荐":
        render_stock_recommendation_page(stock_recommendation_system)
    elif page == "图表分析":
        render_chart_analysis_page(chart_analysis_system)
    elif page == "热点资讯":
        render_news_page(news_system)
    elif page == "智能投顾":
        render_advisor_page(advisor_system)
    elif page == "人工客服":
        render_customer_service_page(customer_service_system)
    
    # 页脚
    st.markdown('<div class="footer">© 2025 金融智能分析平台 | 版权所有</div>', unsafe_allow_html=True)

# 首页
def render_home_page(news_system, stock_recommendation_system, customer_service_system):
    # 欢迎信息
    st.markdown('<h2 class="sub-header">欢迎使用金融智能分析平台</h2>', unsafe_allow_html=True)
    
    # 平台介绍
    st.markdown("""
    金融智能分析平台是一个集成了多种金融分析工具的综合性平台，旨在帮助投资者做出更明智的投资决策。
    平台利用人工智能技术，提供股票推荐、图表分析、热点资讯、智能投顾等功能，为用户提供全方位的金融分析和决策支持。
    """)
    
    # 功能概览
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h3>今日市场概览</h3>', unsafe_allow_html=True)
        
        # 获取市场复盘数据
        market_review = news_system.generate_market_review()
        
        # 显示指数表现
        st.markdown("**主要指数表现**")
        for idx in market_review["indices"]:
            color = "green" if idx["change_percent"] > 0 else "red"
            st.markdown(f"{idx['name']}: <span style='color:{color}'>{idx['change_percent']:.2f}%</span>", unsafe_allow_html=True)
        
        # 显示市场复盘摘要
        st.markdown("**市场复盘**")
        st.markdown(market_review["summary"])
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h3>热门推荐股票</h3>', unsafe_allow_html=True)
        
        # 获取推荐股票
        recommendations = stock_recommendation_system.get_recommendations(min_win_rate=70)[:3]
        
        for stock in recommendations:
            color = "green" if stock["price_change"] > 0 else "red"
            st.markdown(f"**{stock['name']}** ({stock['symbol']})")
            st.markdown(f"胜率: {stock['win_rate']:.1f}% | 涨跌幅: <span style='color:{color}'>{stock['price_change']:.2f}%</span>", unsafe_allow_html=True)
            st.markdown(f"推荐理由: {stock['recommendation_reason']}")
            st.markdown("---")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 热点话题
    st.markdown('<h2 class="sub-header">热点话题</h2>', unsafe_allow_html=True)
    hot_topics = news_system.get_hot_topics()[:3]
    
    topic_cols = st.columns(3)
    for i, topic in enumerate(hot_topics):
        with topic_cols[i]:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(f"<h3>{topic['keyword']}</h3>", unsafe_allow_html=True)
            st.markdown(f"热度: {topic['heat']}/100")
            st.markdown("相关新闻:")
            for news in topic["related_news"][:2]:
                st.markdown(f"- {news['title']}")
            st.markdown('</div>', unsafe_allow_html=True)
    
    # 常见问题
    st.markdown('<h2 class="sub-header">常见问题</h2>', unsafe_allow_html=True)
    faqs = customer_service_system.get_all_faqs()
    
    for i, faq in enumerate(faqs):
        with st.expander(faq["question"]):
            st.markdown(faq["answer"])

# 股票推荐页面
def render_stock_recommendation_page(stock_recommendation_system):
    st.markdown('<h2 class="sub-header">股票推荐</h2>', unsafe_allow_html=True)
    
    # 筛选条件
    st.markdown("### 设置筛选条件")
    col1, col2 = st.columns(2)
    
    with col1:
        sector = st.selectbox(
            "行业选择",
            ["全部", "科技", "消费者服务", "汽车", "金融"]
        )
        
        min_win_rate = st.slider(
            "最低胜率",
            min_value=0,
            max_value=100,
            value=50,
            step=5
        )
    
    with col2:
        st.markdown("### 排序方式")
        sort_by = st.radio(
            "排序依据",
            ["胜率", "价格变化", "行业"]
        )
    
    # 获取推荐股票
    sector_param = None if sector == "全部" else sector
    recommendations = stock_recommendation_system.get_recommendations(sector=sector_param, min_win_rate=min_win_rate)
    
    # 排序
    if sort_by == "胜率":
        recommendations.sort(key=lambda x: x["win_rate"], reverse=True)
    elif sort_by == "价格变化":
        recommendations.sort(key=lambda x: x["price_change"], reverse=True)
    elif sort_by == "行业":
        recommendations.sort(key=lambda x: x["sector"])
    
    # 显示推荐结果
    st.markdown("### 推荐股票")
    
    if not recommendations:
        st.warning("没有符合条件的推荐股票，请尝试调整筛选条件。")
    else:
        for stock in recommendations:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"### {stock['name']} ({stock['symbol']})")
                st.markdown(f"**行业**: {stock['sector']} | **子行业**: {stock['industry']}")
                st.markdown(f"**胜率**: {stock['win_rate']:.1f}%")
                
                color = "green" if stock["price_change"] > 0 else "red"
                st.markdown(f"**最新价格**: {stock['last_price']:.2f} | **涨跌幅**: <span style='color:{color}'>{stock['price_change']:.2f}%</span>", unsafe_allow_html=True)
                
                st.markdown(f"**推荐理由**: {stock['recommendation_reason']}")
            
            with col2:
                # 生成股票数据并绘制图表
                stock_data = stock_recommendation_system.get_stock_data(stock["symbol"])
                
                # 使用Plotly绘制K线图
                fig = go.Figure(data=[go.Candlestick(
                    x=stock_data['date'],
                    open=stock_data['open'],
                    high=stock_data['high'],
                    low=stock_data['low'],
                    close=stock_data['close']
                )])
                
                fig.update_layout(
                    title=f"{stock['symbol']} 近期走势",
                    xaxis_title="日期",
                    yaxis_title="价格",
                    height=300,
                    margin=dict(l=0, r=0, t=30, b=0)
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")

# 图表分析页面
def render_chart_analysis_page(chart_analysis_system):
    st.markdown('<h2 class="sub-header">图表分析</h2>', unsafe_allow_html=True)
    
    # 股票选择
    stock_options = [
        {"symbol": "AAPL", "name": "苹果公司"},
        {"symbol": "MSFT", "name": "微软公司"},
        {"symbol": "GOOGL", "name": "Alphabet公司"},
        {"symbol": "AMZN", "name": "亚马逊公司"},
        {"symbol": "TSLA", "name": "特斯拉公司"}
    ]
    
    stock_selection = st.selectbox(
        "选择股票",
        options=[f"{stock['name']} ({stock['symbol']})" for stock in stock_options],
        index=0
    )
    
    # 提取股票代码
    selected_symbol = stock_selection.split("(")[1].split(")")[0]
    
    # 时间范围选择
    time_range = st.radio(
        "选择时间范围",
        ["1个月", "3个月", "6个月", "1年"],
        horizontal=True
    )
    
    # 转换时间范围为天数
    if time_range == "1个月":
        days = 30
    elif time_range == "3个月":
        days = 90
    elif time_range == "6个月":
        days = 180
    else:  # 1年
        days = 365
    
    # 获取股票数据
    stock_data = chart_analysis_system.get_stock_data(selected_symbol, days)
    stock_data = calculate_technical_indicators(stock_data)
    
    # 绘制K线图
    st.markdown("### 价格走势")
    
    fig = go.Figure()
    
    # 添加K线图
    fig.add_trace(go.Candlestick(
        x=stock_data['date'],
        open=stock_data['open'],
        high=stock_data['high'],
        low=stock_data['low'],
        close=stock_data['close'],
        name="价格"
    ))
    
    # 添加移动平均线
    fig.add_trace(go.Scatter(
        x=stock_data['date'],
        y=stock_data['MA5'],
        mode='lines',
        name='MA5',
        line=dict(color='blue', width=1)
    ))
    
    fig.add_trace(go.Scatter(
        x=stock_data['date'],
        y=stock_data['MA10'],
        mode='lines',
        name='MA10',
        line=dict(color='orange', width=1)
    ))
    
    fig.add_trace(go.Scatter(
        x=stock_data['date'],
        y=stock_data['MA20'],
        mode='lines',
        name='MA20',
        line=dict(color='green', width=1)
    ))
    
    fig.update_layout(
        title=f"{selected_symbol} 价格走势",
        xaxis_title="日期",
        yaxis_title="价格",
        height=500,
        margin=dict(l=0, r=0, t=30, b=0)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 技术指标
    st.markdown("### 技术指标")
    
    indicator_tabs = st.tabs(["MACD", "RSI", "成交量"])
    
    with indicator_tabs[0]:
        # MACD图表
        fig = go.Figure()
        
        # 添加MACD线
        fig.add_trace(go.Scatter(
            x=stock_data['date'],
            y=stock_data['MACD'],
            mode='lines',
            name='MACD',
            line=dict(color='blue', width=1)
        ))
        
        # 添加信号线
        fig.add_trace(go.Scatter(
            x=stock_data['date'],
            y=stock_data['Signal'],
            mode='lines',
            name='Signal',
            line=dict(color='red', width=1)
        ))
        
        # 添加柱状图
        colors = ['green' if val >= 0 else 'red' for val in stock_data['Histogram']]
        fig.add_trace(go.Bar(
            x=stock_data['date'],
            y=stock_data['Histogram'],
            name='Histogram',
            marker_color=colors
        ))
        
        fig.update_layout(
            title="MACD指标",
            xaxis_title="日期",
            yaxis_title="值",
            height=400,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with indicator_tabs[1]:
        # RSI图表
        fig = go.Figure()
        
        # 添加RSI线
        fig.add_trace(go.Scatter(
            x=stock_data['date'],
            y=stock_data['RSI'],
            mode='lines',
            name='RSI',
            line=dict(color='purple', width=2)
        ))
        
        # 添加超买超卖线
        fig.add_trace(go.Scatter(
            x=stock_data['date'],
            y=[70] * len(stock_data),
            mode='lines',
            name='超买线 (70)',
            line=dict(color='red', width=1, dash='dash')
        ))
        
        fig.add_trace(go.Scatter(
            x=stock_data['date'],
            y=[30] * len(stock_data),
            mode='lines',
            name='超卖线 (30)',
            line=dict(color='green', width=1, dash='dash')
        ))
        
        fig.update_layout(
            title="RSI指标",
            xaxis_title="日期",
            yaxis_title="RSI值",
            height=400,
            margin=dict(l=0, r=0, t=30, b=0),
            yaxis=dict(range=[0, 100])
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with indicator_tabs[2]:
        # 成交量图表
        fig = go.Figure()
        
        # 添加成交量柱状图
        colors = ['green' if stock_data['close'].iloc[i] >= stock_data['open'].iloc[i] else 'red' 
                 for i in range(len(stock_data))]
        
        fig.add_trace(go.Bar(
            x=stock_data['date'],
            y=stock_data['volume'],
            name='成交量',
            marker_color=colors
        ))
        
        fig.update_layout(
            title="成交量",
            xaxis_title="日期",
            yaxis_title="成交量",
            height=400,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # 技术形态识别
    st.markdown("### 技术形态识别")
    
    # 获取技术形态识别结果
    patterns = chart_analysis_system.identify_patterns(selected_symbol)
    
    if patterns:
        for pattern in patterns:
            col1, col2 = st.columns([1, 3])
            
            with col1:
                confidence_color = "green" if pattern["confidence"] > 0.8 else "orange" if pattern["confidence"] > 0.6 else "red"
                st.markdown(f"**形态**: {pattern['name']}")
                st.markdown(f"**类型**: {pattern['type']}")
                st.markdown(f"**置信度**: <span style='color:{confidence_color}'>{pattern['confidence']:.2f}</span>", unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"**描述**: {pattern['description']}")
            
            st.markdown("---")
    else:
        st.info("未检测到明显的技术形态。")
    
    # 支撑位和阻力位
    st.markdown("### 支撑位和阻力位")
    
    # 获取支撑位和阻力位
    support_resistance = chart_analysis_system.identify_support_resistance(selected_symbol)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**支撑位**")
        if support_resistance["supports"]:
            for support in support_resistance["supports"]:
                strength_color = "green" if support["strength"] > 0.8 else "orange" if support["strength"] > 0.6 else "red"
                st.markdown(f"价格: {support['level']:.2f} | 强度: <span style='color:{strength_color}'>{support['strength']:.2f}</span>", unsafe_allow_html=True)
        else:
            st.info("未检测到明显的支撑位。")
    
    with col2:
        st.markdown("**阻力位**")
        if support_resistance["resistances"]:
            for resistance in support_resistance["resistances"]:
                strength_color = "green" if resistance["strength"] > 0.8 else "orange" if resistance["strength"] > 0.6 else "red"
                st.markdown(f"价格: {resistance['level']:.2f} | 强度: <span style='color:{strength_color}'>{resistance['strength']:.2f}</span>", unsafe_allow_html=True)
        else:
            st.info("未检测到明显的阻力位。")
    
    # 趋势线分析
    st.markdown("### 趋势线分析")
    
    # 获取趋势线分析结果
    trend_line = chart_analysis_system.identify_trend_lines(selected_symbol)
    
    trend_color = "green" if trend_line["trend_type"] == "上升趋势" else "red" if trend_line["trend_type"] == "下降趋势" else "gray"
    
    st.markdown(f"**趋势类型**: <span style='color:{trend_color}'>{trend_line['trend_type']}</span>", unsafe_allow_html=True)
    st.markdown(f"**趋势强度**: {trend_line['strength']:.2f}")
    st.markdown(f"**持续时间**: {trend_line['duration_days']}天")
    st.markdown(f"**描述**: {trend_line['description']}")
    
    # 综合分析报告
    st.markdown("### 综合分析报告")
    
    # 获取综合分析报告
    analysis_report = chart_analysis_system.generate_analysis_report(selected_symbol)
    
    recommendation_color = "green" if analysis_report["recommendation"] in ["买入", "强烈买入"] else "red" if analysis_report["recommendation"] in ["卖出", "强烈卖出"] else "gray"
    
    st.markdown(f"**投资建议**: <span style='color:{recommendation_color}'>{analysis_report['recommendation']}</span>", unsafe_allow_html=True)
    st.markdown(f"**理由**: {analysis_report['reason']}")
    
    # 详细分析
    with st.expander("查看详细分析"):
        st.markdown("**技术形态分析**")
        if analysis_report["patterns"]:
            for pattern in analysis_report["patterns"]:
                st.markdown(f"- {pattern['name']} ({pattern['type']}): 置信度 {pattern['confidence']:.2f}")
        else:
            st.markdown("未检测到明显的技术形态。")
        
        st.markdown("**支撑位和阻力位分析**")
        st.markdown("支撑位:")
        for support in analysis_report["support_resistance"]["supports"]:
            st.markdown(f"- 价格: {support['level']:.2f}, 强度: {support['strength']:.2f}")
        
        st.markdown("阻力位:")
        for resistance in analysis_report["support_resistance"]["resistances"]:
            st.markdown(f"- 价格: {resistance['level']:.2f}, 强度: {resistance['strength']:.2f}")
        
        st.markdown("**趋势分析**")
        st.markdown(f"- 趋势类型: {analysis_report['trend_line']['trend_type']}")
        st.markdown(f"- 趋势强度: {analysis_report['trend_line']['strength']:.2f}")
        st.markdown(f"- 持续时间: {analysis_report['trend_line']['duration_days']}天")

# 热点资讯页面
def render_news_page(news_system):
    st.markdown('<h2 class="sub-header">热点资讯</h2>', unsafe_allow_html=True)
    
    # 创建标签页
    tabs = st.tabs(["最新资讯", "热点话题", "市场复盘"])
    
    # 最新资讯标签页
    with tabs[0]:
        st.markdown("### 最新财经资讯")
        
        # 分类筛选
        categories = ["全部", "公司新闻", "财报", "行业分析", "政策", "市场动态"]
        selected_category = st.selectbox("选择分类", categories)
        
        # 获取新闻
        category_param = None if selected_category == "全部" else selected_category
        news_list = news_system.get_latest_news(category=category_param, limit=20)
        
        # 显示新闻列表
        for news in news_list:
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.markdown(f"#### {news['title']}")
                st.markdown(f"**来源**: {news['source']} | **日期**: {news['date']} | **分类**: {news['category']}")
                st.markdown(news['summary'])
            
            with col2:
                st.markdown(f"<a href='{news['url']}' target='_blank'>查看详情</a>", unsafe_allow_html=True)
            
            st.markdown("---")
    
    # 热点话题标签页
    with tabs[1]:
        st.markdown("### 热点话题分析")
        
        # 获取热点话题
        hot_topics = news_system.get_hot_topics()
        
        # 生成热度条形图
        topic_names = [topic["keyword"] for topic in hot_topics]
        topic_heats = [topic["heat"] for topic in hot_topics]
        
        fig = px.bar(
            x=topic_heats,
            y=topic_names,
            orientation='h',
            labels={"x": "热度", "y": "话题"},
            title="热点话题热度排行",
            color=topic_heats,
            color_continuous_scale="Reds"
        )
        
        fig.update_layout(
            height=400,
            margin=dict(l=0, r=0, t=30, b=0),
            yaxis=dict(autorange="reversed")
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 显示热点话题详情
        for topic in hot_topics:
            with st.expander(f"{topic['keyword']} (热度: {topic['heat']}/100)"):
                st.markdown("**相关新闻**")
                for news in topic["related_news"]:
                    st.markdown(f"- {news['title']} ({news['source']}, {news['date']})")
    
    # 市场复盘标签页
    with tabs[2]:
        st.markdown("### 今日市场复盘")
        
        # 获取市场复盘数据
        market_review = news_system.generate_market_review()
        
        st.markdown(f"**日期**: {market_review['date']}")
        st.markdown(f"**市场情绪**: {market_review['market_sentiment']}")
        st.markdown(f"**复盘摘要**: {market_review['summary']}")
        
        # 指数表现
        st.markdown("### 指数表现")
        
        # 生成指数表现条形图
        index_names = [idx["name"] for idx in market_review["indices"]]
        index_changes = [idx["change_percent"] for idx in market_review["indices"]]
        
        colors = ["green" if change >= 0 else "red" for change in index_changes]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=index_names,
            y=index_changes,
            marker_color=colors,
            text=[f"{change:.2f}%" for change in index_changes],
            textposition="auto"
        ))
        
        fig.update_layout(
            title="主要指数涨跌幅",
            xaxis_title="指数",
            yaxis_title="涨跌幅 (%)",
            height=400,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 板块表现
        st.markdown("### 板块表现")
        
        # 生成板块表现热力图
        sector_names = [sector["name"] for sector in market_review["sectors"]]
        sector_changes = [sector["change_percent"] for sector in market_review["sectors"]]
        
        # 按涨跌幅排序
        sorted_indices = sorted(range(len(sector_changes)), key=lambda i: sector_changes[i], reverse=True)
        sorted_sectors = [sector_names[i] for i in sorted_indices]
        sorted_changes = [sector_changes[i] for i in sorted_indices]
        
        colors = ["green" if change >= 0 else "red" for change in sorted_changes]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=sorted_sectors,
            y=sorted_changes,
            marker_color=colors,
            text=[f"{change:.2f}%" for change in sorted_changes],
            textposition="auto"
        ))
        
        fig.update_layout(
            title="行业板块涨跌幅",
            xaxis_title="板块",
            yaxis_title="涨跌幅 (%)",
            height=400,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)

# 智能投顾页面
def render_advisor_page(advisor_system):
    st.markdown('<h2 class="sub-header">智能投顾</h2>', unsafe_allow_html=True)
    
    # 创建标签页
    tabs = st.tabs(["风险评估", "资产配置", "投资推荐", "财务规划"])
    
    # 风险评估标签页
    with tabs[0]:
        st.markdown("### 风险承受能力评估")
        st.markdown("请回答以下问题，帮助我们了解您的风险承受能力。")
        
        # 风险评估问卷
        q1 = st.slider("1. 您计划的投资期限是多久？", 1, 10, 5, 
                       help="1分表示短期（1年以内），10分表示长期（10年以上）")
        
        q2 = st.slider("2. 当您的投资出现10%的亏损时，您会怎么做？", 1, 10, 5,
                      help="1分表示立即全部卖出，10分表示坚定持有甚至加仓")
        
        q3 = st.slider("3. 您对金融投资的了解程度如何？", 1, 10, 5,
                      help="1分表示几乎不了解，10分表示非常了解")
        
        q4 = st.slider("4. 您的收入来源稳定性如何？", 1, 10, 5,
                      help="1分表示非常不稳定，10分表示非常稳定")
        
        q5 = st.slider("5. 您希望获得的年化收益率是多少？", 1, 10, 5,
                      help="1分表示期望低收益（3%以下），10分表示期望高收益（15%以上）")
        
        # 计算风险评分
        if st.button("提交评估"):
            answers = {
                "q1": q1,
                "q2": q2,
                "q3": q3,
                "q4": q4,
                "q5": q5
            }
            
            risk_assessment = advisor_system.assess_risk_tolerance(answers)
            
            st.session_state.risk_profile = risk_assessment["risk_profile"]
            st.session_state.risk_score = risk_assessment["score"]
            st.session_state.risk_description = risk_assessment["description"]
            
            st.success("评估完成！")
            
            # 显示评估结果
            st.markdown("### 评估结果")
            st.markdown(f"**风险偏好**: {st.session_state.risk_profile}")
            st.markdown(f"**风险评分**: {st.session_state.risk_score}/50")
            st.markdown(f"**描述**: {st.session_state.risk_description}")
    
    # 资产配置标签页
    with tabs[1]:
        st.markdown("### 资产配置建议")
        
        if "risk_profile" not in st.session_state:
            st.warning("请先完成风险评估问卷。")
        else:
            # 获取资产配置建议
            asset_allocation = advisor_system.generate_asset_allocation(st.session_state.risk_profile)
            
            # 显示资产配置建议
            st.markdown(f"**风险偏好**: {st.session_state.risk_profile}")
            st.markdown(f"**预期年化收益率**: {asset_allocation['expected_return']}")
            st.markdown(f"**波动性**: {asset_allocation['volatility']}")
            
            # 绘制资产配置饼图
            fig = px.pie(
                values=list(asset_allocation["allocation"].values()),
                names=list(asset_allocation["allocation"].keys()),
                title="建议资产配置比例",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            
            fig.update_layout(
                height=500,
                margin=dict(l=0, r=0, t=30, b=0)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # 资产配置说明
            st.markdown("### 配置说明")
            
            for asset_class, percentage in asset_allocation["allocation"].items():
                st.markdown(f"**{asset_class}**: {percentage}%")
            
            # 资产配置建议
            st.markdown("### 配置建议")
            
            if st.session_state.risk_profile == "保守型":
                st.markdown("""
                - **现金及等价物**: 保持充足的流动性，应对紧急需求
                - **债券**: 以国债和高等级信用债为主，追求稳定收益
                - **股票**: 选择大型蓝筹股和高股息股票，降低波动性
                - **另类投资**: 少量配置REITs等稳定收益类资产
                """)
            elif st.session_state.risk_profile == "稳健型":
                st.markdown("""
                - **现金及等价物**: 保持适度流动性，应对短期需求
                - **债券**: 平衡配置国债和信用债，兼顾安全性和收益性
                - **股票**: 以蓝筹股为主，适当配置成长股，追求稳健增长
                - **另类投资**: 配置REITs和黄金等资产，增加多元化
                """)
            elif st.session_state.risk_profile == "平衡型":
                st.markdown("""
                - **现金及等价物**: 保持基本流动性储备
                - **债券**: 配置中短期债券，平衡风险和收益
                - **股票**: 均衡配置价值股和成长股，国内外市场均有布局
                - **另类投资**: 适当配置商品、REITs等另类资产，提高组合效率
                """)
            elif st.session_state.risk_profile == "成长型":
                st.markdown("""
                - **现金及等价物**: 保持最低限度的流动性储备
                - **债券**: 少量配置高收益债券，提高组合收益
                - **股票**: 以成长股为主，加大对科技、医疗等高增长行业的配置
                - **另类投资**: 配置私募股权、商品等高风险高收益资产
                """)
            else:  # 进取型
                st.markdown("""
                - **现金及等价物**: 仅保留应急资金
                - **债券**: 极少量配置，主要用于战术性调整
                - **股票**: 重点配置高增长行业和新兴市场，追求高回报
                - **另类投资**: 积极配置私募股权、风险投资等高风险资产
                """)
    
    # 投资推荐标签页
    with tabs[2]:
        st.markdown("### 投资产品推荐")
        
        if "risk_profile" not in st.session_state:
            st.warning("请先完成风险评估问卷。")
        else:
            # 获取投资产品推荐
            recommendations = advisor_system.generate_investment_recommendations(st.session_state.risk_profile)
            
            # 显示推荐产品
            st.markdown(f"基于您的风险偏好（{st.session_state.risk_profile}），我们为您推荐以下投资产品：")
            
            for product in recommendations:
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    risk_color = "green" if product["risk_level"] in ["极低", "低"] else "orange" if product["risk_level"] == "中" else "red"
                    st.markdown(f"**{product['name']}**")
                    st.markdown(f"**类型**: {product['type']}")
                    st.markdown(f"**风险等级**: <span style='color:{risk_color}'>{product['risk_level']}</span>", unsafe_allow_html=True)
                    st.markdown(f"**预期收益**: {product['expected_return']}")
                
                with col2:
                    st.markdown(f"**描述**: {product['description']}")
                
                st.markdown("---")
    
    # 财务规划标签页
    with tabs[3]:
        st.markdown("### 个人财务规划")
        
        if "risk_profile" not in st.session_state:
            st.warning("请先完成风险评估问卷。")
        else:
            st.markdown("请提供您的基本财务信息，帮助我们为您制定个性化的财务规划。")
            
            col1, col2 = st.columns(2)
            
            with col1:
                monthly_income = st.number_input("月收入（元）", min_value=0, value=10000)
                monthly_expenses = st.number_input("月支出（元）", min_value=0, value=5000)
                savings = st.number_input("当前储蓄（元）", min_value=0, value=100000)
            
            with col2:
                debt = st.number_input("当前债务（元）", min_value=0, value=0)
                age = st.number_input("年龄", min_value=18, max_value=80, value=30)
                retirement_age = st.number_input("计划退休年龄", min_value=age, max_value=80, value=60)
            
            if st.button("生成财务规划"):
                # 收集用户信息
                user_info = {
                    "monthly_income": monthly_income,
                    "monthly_expenses": monthly_expenses,
                    "savings": savings,
                    "debt": debt,
                    "age": age,
                    "retirement_age": retirement_age
                }
                
                # 生成财务规划
                financial_plan = advisor_system.generate_financial_plan(user_info, st.session_state.risk_profile)
                
                # 显示财务规划
                st.markdown("### 财务规划结果")
                
                # 紧急备用金
                st.markdown("#### 紧急备用金")
                st.markdown(f"建议的紧急备用金金额: **{financial_plan['emergency_fund_recommendation']:,.2f}元**")
                st.markdown("紧急备用金应该保持高流动性，可以存放在货币市场基金或活期储蓄账户中。")
                
                # 每月投资
                st.markdown("#### 每月投资")
                st.markdown(f"当前每月可投资金额: **{financial_plan['monthly_investment_current']:,.2f}元**")
                st.markdown(f"达成退休目标所需每月投资金额: **{financial_plan['monthly_investment_needed']:,.2f}元**")
                
                # 退休规划
                st.markdown("#### 退休规划")
                st.markdown(f"预计退休所需总资金: **{financial_plan['total_retirement_need']:,.2f}元**")
                
                # 投资建议
                st.markdown("#### 投资建议")
                st.markdown(financial_plan['investment_advice'])
                
                # 债务管理
                if debt > 0:
                    st.markdown("#### 债务管理")
                    st.markdown(financial_plan['debt_advice'])
                
                # 财务规划图表
                st.markdown("#### 财务状况可视化")
                
                # 收入与支出饼图
                income_expense_data = {
                    "类别": ["每月支出", "每月储蓄/投资"],
                    "金额": [monthly_expenses, monthly_income - monthly_expenses]
                }
                
                fig = px.pie(
                    income_expense_data,
                    values="金额",
                    names="类别",
                    title="月收入分配",
                    color_discrete_sequence=["#FF6B6B", "#4ECDC4"]
                )
                
                fig.update_layout(
                    height=400,
                    margin=dict(l=0, r=0, t=30, b=0)
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # 退休规划条形图
                retirement_data = {
                    "类别": ["当前储蓄", "退休所需总资金"],
                    "金额": [savings, financial_plan['total_retirement_need']]
                }
                
                fig = px.bar(
                    retirement_data,
                    x="类别",
                    y="金额",
                    title="退休规划进度",
                    color="类别",
                    color_discrete_sequence=["#FFD166", "#118AB2"]
                )
                
                fig.update_layout(
                    height=400,
                    margin=dict(l=0, r=0, t=30, b=0),
                    showlegend=False
                )
                
                st.plotly_chart(fig, use_container_width=True)

# 人工客服页面
def render_customer_service_page(customer_service_system):
    st.markdown('<h2 class="sub-header">人工客服</h2>', unsafe_allow_html=True)
    
    # 创建标签页
    tabs = st.tabs(["智能问答", "常见问题", "联系客服"])
    
    # 智能问答标签页
    with tabs[0]:
        st.markdown("### 智能问答")
        st.markdown("请输入您的问题，我们的智能客服将为您解答。")
        
        # 初始化聊天历史
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        
        # 显示聊天历史
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f"<div style='background-color:#E8F4F8; padding:10px; border-radius:5px; margin-bottom:10px;'><strong>您:</strong> {message['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='background-color:#F0F0F0; padding:10px; border-radius:5px; margin-bottom:10px;'><strong>客服:</strong> {message['content']}</div>", unsafe_allow_html=True)
        
        # 用户输入
        user_question = st.text_input("请输入您的问题")
        
        if st.button("发送") and user_question:
            # 添加用户问题到聊天历史
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_question
            })
            
            # 获取回答
            answer = customer_service_system.get_answer(user_question)
            
            # 添加回答到聊天历史
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": answer
            })
            
            # 刷新页面显示新消息
            st.experimental_rerun()
    
    # 常见问题标签页
    with tabs[1]:
        st.markdown("### 常见问题")
        
        # 获取所有FAQ
        faqs = customer_service_system.get_all_faqs()
        
        # 显示FAQ
        for faq in faqs:
            with st.expander(faq["question"]):
                st.markdown(faq["answer"])
    
    # 联系客服标签页
    with tabs[2]:
        st.markdown("### 联系客服")
        st.markdown("如果您的问题无法通过智能问答解决，请通过以下方式联系我们的人工客服：")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**在线客服**")
            st.markdown("工作时间: 周一至周五 9:00-18:00")
            st.markdown("点击下方按钮连接人工客服")
            st.button("连接人工客服", disabled=True)
        
        with col2:
            st.markdown("**电话客服**")
            st.markdown("客服热线: 400-123-4567")
            st.markdown("工作时间: 周一至周日 8:00-20:00")
            
        st.markdown("**邮件支持**")
        st.markdown("客服邮箱: support@financial-platform.com")
        st.markdown("我们将在1个工作日内回复您的邮件")

if __name__ == "__main__":
    main()
