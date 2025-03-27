# 金融智能分析平台

## 项目概述

金融智能分析平台是一个集成了多种智能化功能的金融分析工具，旨在帮助用户做出更明智的投资决策。平台集成了DeepSeek、智谱AI、文心一言、讯飞星火和通义千问五大中国顶级AI模型，提供专业金融终端、简约现代、中国传统和高对比度四种主题风格，针对A股市场特点和中国金融政策进行了优化。

## 核心功能

1. **人工客服服务功能**：结合AI智能问答和人工专业服务，为用户提供全方位支持
2. **图表分析标识功能**：自动识别股票图表中的关键技术形态和趋势
3. **基于历史走势的股票推荐功能**：利用历史数据分析预测未来走势，推荐高胜率股票
4. **热点资讯板块**：整合市场动态和热点信息，分析市场情绪
5. **今日复盘和热点分析功能**：提供市场回顾和热点解读
6. **智能投顾与财富管理功能**：根据用户资产和目标提供个性化理财规划

## 文件结构

```
financial_platform/
├── api_analysis.py                  # 金融API能力分析
├── chart_analysis_system.py         # 图表分析系统
├── comprehensive_report.md          # 综合功能改进报告
├── demo_presentation.md             # 详细演示文档
├── deployment_guide.md              # 部署指南
├── enhanced_multi_model_service.py  # 多模型服务
├── feature_designs/                 # 功能设计文档
│   ├── chart_analysis_system.md
│   ├── customer_service.md
│   ├── intelligent_advisor.md
│   ├── news_and_market_review.md
│   └── stock_recommendation_system.md
├── improvement_opportunities.md     # 改进机会分析
├── news_and_market_review_system.py # 热点资讯与市场复盘系统
├── presentation.md                  # 简要演示文档
├── requirements.txt                 # 依赖包列表
├── stock_recommendation_system.py   # 股票推荐系统
├── todo.md                          # 任务清单
└── ui_optimization.py               # UI优化系统
```

## 安装指南

详细的安装和部署步骤请参考 [deployment_guide.md](deployment_guide.md)。

### 快速开始

1. 克隆代码仓库或解压下载的ZIP文件
2. 安装依赖：`pip install -r requirements.txt`
3. 创建配置文件：参考deployment_guide.md中的配置说明
4. 启动应用：`streamlit run ui_optimization.py`

## 功能演示

详细的功能演示和用例分析请参考 [demo_presentation.md](demo_presentation.md)。

## 系统要求

- **操作系统**：Windows 10/11、Ubuntu 20.04/22.04 LTS、macOS 11.0+
- **Python环境**：Python 3.10+
- **内存**：至少4GB RAM，推荐8GB或更高
- **存储空间**：至少1GB可用空间，推荐5GB以上
- **网络**：稳定的互联网连接，推荐带宽≥10Mbps

## 技术栈

- **数据分析**：pandas, numpy, matplotlib, plotly
- **机器学习**：scikit-learn, tensorflow/keras
- **Web界面**：Streamlit
- **金融数据API**：YahooFinance API
- **自然语言处理**：transformers, jieba, nltk

## 联系与支持

如有任何问题或需要技术支持，请联系：

- 技术支持邮箱：support@example.com
- 技术支持电话：400-123-4567

## 许可证

本项目采用 [MIT 许可证](LICENSE)。

---

*最后更新：2025年3月27日*
