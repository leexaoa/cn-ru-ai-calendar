# 🗓️ 中国-俄罗斯节假日日历

自动生成和更新中国与俄罗斯节假日的 iCalendar 格式日历文件。支持日历应用订阅、自动更新、连休识别和调休标记。

## ✨ 功能特性

- **自动更新**：每月自动检查并更新节假日信息
- **多源支持**：优先使用在线API，失败时回退到官方数据
- **连休识别**：自动识别和标记连续假期
- **黄金周检测**：自动标记春节和国庆黄金周
- **调休标记**：清晰标记补班日期
- **标准格式**：生成标准 iCalendar (.ics) 格式，支持所有日历应用

## 📱 订阅方式

### 方法1：直接订阅链接

在你的日历应用中添加此订阅链接（使用 `https` 或 `webcal` 协议）：

```
webcal://leexaoa.github.io/cn-ru-ai-calendar/calendar.ics
```

或使用 HTTPS：

```
https://leexaoa.github.io/cn-ru-ai-calendar/calendar.ics
```

### 方法2：主流日历应用订阅

#### Apple Calendar (macOS/iOS)
1. 打开 Calendar 应用
2. File → New Calendar Subscription
3. 粘贴上述链接
4. 点击 Subscribe

#### Google Calendar
1. 点击左侧"其他日历"旁的 + 号
2. 选择"通过网址订阅"
3. 粘贴上述链接
4. 点击 Subscribe

#### Outlook/Microsoft 365
1. File → Open & Export → Import Calendar
2. 选择"Internet Calendar"
3. 粘贴上述链接

#### Thunderbird
1. 右键点击日历列表
2. 选择"Subscribe to Remote Calendar"
3. 粘贴上述链接

## 📅 包含的节假日

### 中国 🇨🇳

- **春节** - 春节假期（通常7-8天）
- **清明节** - 清明节假期（3天）
- **劳动节** - 五一劳动节假期（5天）
- **端午节** - 端午节假期（1-3天）
- **中秋节** - 中秋节假期（3-4天）
- **国庆节** - 十一国庆节假期（7天）
- **调休日期** - 标记所有补班日期

### 俄罗斯 🇷🇺

- **新年假期** - 1月1-8日（8天）
- **祖国保卫者日** - 2月23日
- **妇女节** - 3月8日
- **劳动节** - 5月1日
- **胜利日** - 5月9日
- **俄罗斯日** - 6月12日
- **民族统一日** - 11月4日

## 🚀 本地使用

### 安装依赖

```bash
pip install -r requirements.txt
```

### 生成日历

```bash
python generate.py
```

生成的文件会保存为 `calendar.ics`

### 指定年份生成

编辑 `generate.py` 中的 `year` 变量：

```python
year = 2024  # 改为需要的年份
```

## 🔄 自动更新

此项目使用 GitHub Actions 实现自动更新：

- **触发时机**：每个月的第一天 00:00 UTC 自动运行
- **自动提交**：检测到更新后自动提交到仓库
- **手动触发**：可在 GitHub 仓库的 Actions 标签页手动运行

## 📝 文件结构

```
.
├── .github/
│   └── workflows/
│       └── update-holidays.yml    # GitHub Actions 工作流
├── engine/
│   ├── cn_exact.py               # 中国假期数据获取和解析
│   ├── ru.py                     # 俄罗斯假期数据
│   └── cluster.py                # 连休识别和黄金周检测
├── generate.py                   # 主生成脚本
├── calendar.ics                  # 生成的日历文件
├── requirements.txt              # Python 依赖
└── README.md                     # 本说明文档
```

## 🔧 自定义

### 修改假期数据

编辑 `engine/cn_exact.py` 中的 `OFFICIAL_HOLIDAYS` 字典来添加或修改中国假期。

编辑 `engine/ru.py` 中的 `RUSSIAN_SPECIAL_HOLIDAYS` 字典来修改俄罗斯假期。

### 添加新的国家

1. 创建新文件 `engine/[country].py`
2. 实现 `fetch_[country](year)` 函数
3. 在 `generate.py` 中导入并调用

## 🔗 API 数据源

- **中国**：国务院办公厅公告 + 天行数据 API（免费额度）
- **俄罗斯**：俄罗斯政府官方假期规定

## ⚖️ 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📧 联系方式

如有问题或建议，请在 GitHub 提交 Issue。
