# 金融智能分析平台部署指南

## 1. 系统要求

### 1.1 硬件要求
- **处理器**：推荐4核心及以上
- **内存**：至少4GB RAM，推荐8GB或更高
- **存储空间**：至少1GB可用空间，推荐5GB以上（用于数据缓存和日志）
- **网络**：稳定的互联网连接，推荐带宽≥10Mbps

### 1.2 软件要求
- **操作系统**：
  - Windows 10/11
  - Ubuntu 20.04/22.04 LTS
  - macOS 11.0+
- **Python环境**：Python 3.10+
- **浏览器**：Chrome 90+、Firefox 90+、Edge 90+（用于访问Web界面）

## 2. 环境准备

### 2.1 安装Python
根据您的操作系统，按照以下步骤安装Python 3.10或更高版本：

#### Windows
1. 访问 [Python官网](https://www.python.org/downloads/)
2. 下载Python 3.10+安装包
3. 运行安装程序，勾选"Add Python to PATH"
4. 完成安装后，打开命令提示符验证：
   ```bash
   python --version
   ```

#### Ubuntu
```bash
sudo apt update
sudo apt install python3.10 python3.10-venv python3-pip
```

#### macOS
```bash
brew update
brew install python@3.10
```

### 2.2 创建虚拟环境
推荐使用虚拟环境隔离项目依赖：

```bash
# 创建虚拟环境
python -m venv financial_env

# 激活虚拟环境
# Windows
financial_env\Scripts\activate
# Linux/macOS
source financial_env/bin/activate
```

## 3. 安装步骤

### 3.1 获取代码
```bash
# 克隆代码仓库
git clone https://github.com/your-repo/financial-platform-improved.git
cd financial-platform-improved

# 或解压下载的ZIP文件
unzip financial_platform_improved.zip -d financial_platform
cd financial_platform
```

### 3.2 安装依赖
```bash
pip install -r requirements.txt
```

如果requirements.txt不存在，请安装以下核心依赖：
```bash
pip install pandas numpy matplotlib plotly streamlit scikit-learn tensorflow jieba requests beautifulsoup4 transformers torch
```

### 3.3 配置API密钥

#### 3.3.1 创建配置文件
在项目根目录创建`config.json`文件：

```json
{
  "yahoo_finance_api_key": "your_yahoo_finance_api_key",
  "news_api_key": "your_news_api_key",
  "ai_model_keys": {
    "deepseek": "your_deepseek_api_key",
    "zhipu": "your_zhipu_api_key",
    "baidu": "your_baidu_api_key",
    "xunfei": "your_xunfei_api_key",
    "aliyun": "your_aliyun_api_key"
  },
  "database": {
    "host": "localhost",
    "port": 3306,
    "user": "financial_user",
    "password": "your_password",
    "database": "financial_platform"
  }
}
```

#### 3.3.2 获取API密钥
- **Yahoo Finance API**：访问 [RapidAPI](https://rapidapi.com/apidojo/api/yahoo-finance1/) 注册并订阅
- **News API**：访问 [NewsAPI](https://newsapi.org/) 注册获取密钥
- **中文AI模型API**：
  - DeepSeek：[官网](https://www.deepseek.com/)
  - 智谱AI：[官网](https://www.zhipuai.cn/)
  - 文心一言：[官网](https://yiyan.baidu.com/)
  - 讯飞星火：[官网](https://xinghuo.xfyun.cn/)
  - 通义千问：[官网](https://qianwen.aliyun.com/)

### 3.4 初始化数据目录
```bash
mkdir -p data/stocks data/news data/charts data/ui data/user_profiles data/logs
```

### 3.5 数据库设置（可选）
如果您选择使用数据库存储用户数据和分析结果：

#### MySQL
```bash
# 安装MySQL
# Ubuntu
sudo apt install mysql-server

# 创建数据库和用户
mysql -u root -p
```

在MySQL提示符下执行：
```sql
CREATE DATABASE financial_platform;
CREATE USER 'financial_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON financial_platform.* TO 'financial_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

#### 初始化数据库表
```bash
python scripts/init_database.py
```

## 4. 启动应用

### 4.1 基本启动
```bash
streamlit run ui_optimization.py
```

### 4.2 高级启动选项
```bash
# 指定端口
streamlit run ui_optimization.py --server.port 8501

# 允许外部访问
streamlit run ui_optimization.py --server.address 0.0.0.0

# 启用缓存
streamlit run ui_optimization.py --server.enableCORS false --server.enableXsrfProtection false
```

### 4.3 使用脚本启动（推荐）
我们提供了启动脚本，自动处理环境变量和配置：

```bash
# Windows
start.bat

# Linux/macOS
./start.sh
```

## 5. 功能模块配置

### 5.1 股票推荐系统配置
编辑`config/stock_recommendation_config.json`：

```json
{
  "default_market": "CN",  // 默认市场：CN(中国)、US(美国)
  "max_stocks": 20,        // 最大推荐股票数量
  "lookback_period": 252,  // 回测周期（交易日）
  "holding_period": 20,    // 默认持有期（交易日）
  "technical_indicators": ["MACD", "RSI", "KDJ", "BOLL"],  // 使用的技术指标
  "win_rate_threshold": 60.0,  // 胜率阈值（百分比）
  "data_update_interval": 3600  // 数据更新间隔（秒）
}
```

### 5.2 图表分析系统配置
编辑`config/chart_analysis_config.json`：

```json
{
  "patterns_to_detect": ["HEAD_SHOULDERS", "DOUBLE_TOP", "DOUBLE_BOTTOM", "TRIANGLE", "CHANNEL"],
  "confidence_threshold": 0.7,  // 形态识别置信度阈值
  "support_resistance_levels": 5,  // 识别的支撑/阻力位数量
  "trend_line_lookback": 90,  // 趋势线识别回看期（天）
  "chart_theme": "professional"  // 图表主题：professional, simple, traditional, high_contrast
}
```

### 5.3 热点资讯系统配置
编辑`config/news_config.json`：

```json
{
  "news_sources": ["sina", "eastmoney", "cnstock", "yicai"],  // 新闻来源
  "update_interval": 1800,  // 更新间隔（秒）
  "max_news_items": 100,  // 最大新闻条目
  "hot_topics_count": 20,  // 热点话题数量
  "sentiment_analysis": true  // 是否启用情感分析
}
```

### 5.4 智能投顾系统配置
编辑`config/advisor_config.json`：

```json
{
  "risk_levels": 5,  // 风险等级数量
  "asset_classes": ["stocks", "bonds", "cash", "gold", "realestate"],  // 资产类别
  "simulation_runs": 1000,  // 蒙特卡洛模拟次数
  "planning_horizon": 30,  // 规划周期（年）
  "tax_consideration": true  // 是否考虑税收因素
}
```

### 5.5 人工客服系统配置
编辑`config/customer_service_config.json`：

```json
{
  "ai_confidence_threshold": 0.8,  // AI回答置信度阈值
  "service_hours": {  // 人工服务时间
    "weekday": {"start": "9:00", "end": "21:00"},
    "weekend": {"start": "10:00", "end": "18:00"}
  },
  "max_waiting_users": 20,  // 最大等待人数
  "knowledge_base_path": "data/knowledge_base"  // 知识库路径
}
```

## 6. 生产环境部署

### 6.1 使用Docker部署

#### 6.1.1 安装Docker
根据您的操作系统安装Docker：
- [Windows安装指南](https://docs.docker.com/desktop/install/windows-install/)
- [Ubuntu安装指南](https://docs.docker.com/engine/install/ubuntu/)
- [macOS安装指南](https://docs.docker.com/desktop/install/mac-install/)

#### 6.1.2 构建Docker镜像
在项目根目录创建`Dockerfile`：

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "ui_optimization.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

构建镜像：
```bash
docker build -t financial-platform:latest .
```

#### 6.1.3 运行Docker容器
```bash
docker run -d -p 8501:8501 --name financial-platform financial-platform:latest
```

### 6.2 使用Nginx作为反向代理

#### 6.2.1 安装Nginx
```bash
# Ubuntu
sudo apt install nginx

# CentOS
sudo yum install nginx
```

#### 6.2.2 配置Nginx
创建配置文件`/etc/nginx/sites-available/financial-platform`：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

启用配置：
```bash
sudo ln -s /etc/nginx/sites-available/financial-platform /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 6.3 使用Supervisor管理进程
安装Supervisor：
```bash
sudo apt install supervisor
```

创建配置文件`/etc/supervisor/conf.d/financial-platform.conf`：

```ini
[program:financial-platform]
command=/path/to/financial_env/bin/streamlit run /path/to/financial_platform/ui_optimization.py --server.port=8501 --server.address=0.0.0.0
directory=/path/to/financial_platform
autostart=true
autorestart=true
stderr_logfile=/var/log/financial-platform.err.log
stdout_logfile=/var/log/financial-platform.out.log
user=your_username
environment=HOME="/home/your_username",USER="your_username"
```

启用配置：
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start financial-platform
```

## 7. 数据备份与恢复

### 7.1 数据备份
创建备份脚本`backup.sh`：

```bash
#!/bin/bash
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="/path/to/backups"
APP_DIR="/path/to/financial_platform"

# 创建备份目录
mkdir -p $BACKUP_DIR

# 备份配置文件
tar -czf $BACKUP_DIR/config_$TIMESTAMP.tar.gz $APP_DIR/config

# 备份数据目录
tar -czf $BACKUP_DIR/data_$TIMESTAMP.tar.gz $APP_DIR/data

# 如果使用数据库，备份数据库
mysqldump -u financial_user -p financial_platform > $BACKUP_DIR/db_$TIMESTAMP.sql

echo "备份完成: $BACKUP_DIR"
```

设置定时任务：
```bash
chmod +x backup.sh
crontab -e
```

添加以下行设置每日备份：
```
0 2 * * * /path/to/backup.sh
```

### 7.2 数据恢复
创建恢复脚本`restore.sh`：

```bash
#!/bin/bash
BACKUP_DIR="/path/to/backups"
APP_DIR="/path/to/financial_platform"
BACKUP_DATE=$1

# 检查参数
if [ -z "$BACKUP_DATE" ]; then
    echo "请提供备份日期，格式：YYYYMMDD_HHMMSS"
    exit 1
fi

# 恢复配置文件
tar -xzf $BACKUP_DIR/config_$BACKUP_DATE.tar.gz -C /

# 恢复数据目录
tar -xzf $BACKUP_DIR/data_$BACKUP_DATE.tar.gz -C /

# 如果使用数据库，恢复数据库
mysql -u financial_user -p financial_platform < $BACKUP_DIR/db_$BACKUP_DATE.sql

echo "恢复完成"
```

使用方法：
```bash
chmod +x restore.sh
./restore.sh 20250327_120000
```

## 8. 故障排除

### 8.1 常见问题

#### 8.1.1 应用无法启动
- 检查Python版本是否为3.10+
- 确认所有依赖已正确安装
- 检查配置文件格式是否正确
- 查看日志文件中的错误信息

#### 8.1.2 API连接失败
- 验证API密钥是否正确
- 检查网络连接
- 确认API服务是否可用
- 检查API调用频率是否超限

#### 8.1.3 数据加载缓慢
- 考虑增加服务器内存
- 优化数据缓存策略
- 检查网络带宽
- 减少同时处理的数据量

### 8.2 日志文件位置
- 应用日志：`data/logs/app.log`
- 错误日志：`data/logs/error.log`
- API调用日志：`data/logs/api.log`
- 用户操作日志：`data/logs/user.log`

### 8.3 获取支持
如遇到无法解决的问题，请通过以下方式获取支持：
- 提交GitHub Issue
- 发送邮件至support@example.com
- 在工作时间拨打技术支持热线：400-123-4567

## 9. 更新与维护

### 9.1 更新应用
```bash
# 拉取最新代码
git pull

# 更新依赖
pip install -r requirements.txt

# 重启应用
supervisorctl restart financial-platform
```

### 9.2 数据清理
定期运行数据清理脚本，删除过期缓存和日志：
```bash
python scripts/cleanup.py --days 30
```

### 9.3 性能监控
使用Prometheus和Grafana监控应用性能：

1. 安装Prometheus和Grafana
2. 配置Prometheus抓取应用指标
3. 创建Grafana仪表板显示关键指标

## 10. 安全建议

### 10.1 API密钥保护
- 不要在代码中硬编码API密钥
- 使用环境变量或加密的配置文件
- 定期轮换API密钥

### 10.2 用户数据保护
- 加密存储敏感用户数据
- 实施最小权限原则
- 定期备份用户数据

### 10.3 网络安全
- 使用HTTPS加密传输
- 配置防火墙限制访问
- 实施IP白名单（适用于内部部署）

## 11. 多环境部署

### 11.1 开发环境
```bash
# 使用开发配置启动
streamlit run ui_optimization.py --config.env=dev
```

### 11.2 测试环境
```bash
# 使用测试配置启动
streamlit run ui_optimization.py --config.env=test
```

### 11.3 生产环境
```bash
# 使用生产配置启动
streamlit run ui_optimization.py --config.env=prod
```

## 12. 集成指南

### 12.1 作为独立应用部署
按照上述步骤部署为独立Web应用。

### 12.2 作为API服务集成
1. 启动FastAPI服务：
   ```bash
   python api_server.py
   ```

2. API端点示例：
   - `GET /api/stock/recommendation` - 获取股票推荐
   - `POST /api/chart/analyze` - 分析股票图表
   - `GET /api/news/hot-topics` - 获取热点话题
   - `POST /api/advisor/portfolio` - 获取投资组合建议

### 12.3 作为模块集成到现有系统
1. 将项目作为Python包安装：
   ```bash
   pip install -e .
   ```

2. 在现有系统中导入模块：
   ```python
   from financial_platform.stock_recommendation_system import StockRecommender
   from financial_platform.chart_analysis_system import ChartAnalyzer
   # 使用模块功能
   ```

## 13. 性能优化建议

### 13.1 数据缓存策略
- 使用Redis缓存频繁访问的数据
- 实现定时数据预加载
- 优化数据库查询

### 13.2 计算资源优化
- 使用多进程处理计算密集型任务
- 考虑使用GPU加速机器学习模型
- 实现任务队列处理批量请求

### 13.3 前端优化
- 实现懒加载和分页
- 优化图表渲染
- 减少不必要的API调用

## 14. 扩展功能指南

### 14.1 添加新数据源
1. 在`data_sources`目录创建新数据源模块
2. 实现标准接口方法
3. 在配置文件中注册新数据源

### 14.2 开发新分析模型
1. 在`models`目录创建新模型模块
2. 实现训练和预测方法
3. 在相应系统中集成新模型

### 14.3 自定义UI组件
1. 在`ui/components`目录创建新组件
2. 实现Streamlit组件接口
3. 在UI布局中使用新组件

## 15. 参考资源

- [Streamlit文档](https://docs.streamlit.io/)
- [Pandas文档](https://pandas.pydata.org/docs/)
- [Plotly文档](https://plotly.com/python/)
- [Yahoo Finance API文档](https://rapidapi.com/apidojo/api/yahoo-finance1/)
- [金融技术分析指南](https://www.investopedia.com/technical-analysis-4689657)
- [Docker文档](https://docs.docker.com/)
- [Nginx文档](https://nginx.org/en/docs/)

## 16. 联系与支持

如有任何问题或需要技术支持，请联系：

- 技术支持邮箱：support@example.com
- 技术支持电话：400-123-4567
- 项目GitHub：https://github.com/your-repo/financial-platform-improved
- 官方网站：https://financial-platform.example.com

---

*本部署指南最后更新于2025年3月27日*
