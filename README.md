# Opti-Resume 🚀 AI 智能简历优化工具

一款基于大语言模型的开源简历优化工具。上传简历、粘贴职位描述，即可获得 AI 驱动的专业优化建议，让你的简历脱颖而出。

---

## ✨ 核心功能

| 工具 | 说明 |
|------|------|
| 📝 简历优化 | 用强动词、量化成果和 ATS 友好关键词重写简历 |
| 🎯 ATS 评分分析 | 对照职位描述打分，找出缺失关键词和改进方向 |
| 💡 要点分析 | 将薄弱的要点描述转化为有冲击力的量化成果（XYZ 公式） |
| 🔑 技能关键词提取 | 从职位描述中提取并分类技术技能 |
| 📊 量化指标建议 | 为任意要点描述生成 5 个可量化的指标 |
| ✉️ 求职信生成器 | 根据简历 + 职位描述自动生成个性化求职信 |

---

## 🆕 主要特性

- **多 LLM 后端支持** — 一键切换 OpenAI / DeepSeek / Ollama 本地模型
- **中文简历全支持** — 所有工具均有中文 Prompt 模板，sidebar 语言切换
- **求职信生成器** — 新增工具，自动生成针对性求职信
- **现代深色 UI** — 渐变主题风格，流畅的交互体验
- **PDF 中文导出** — 基于 reportlab，完美支持中文/Unicode，自动降级兼容
- **完善的错误处理** — 友好提示，告别直接崩溃
- **参数可配置** — sidebar 可调 max_tokens / temperature

---

## 🚀 快速开始

### 1. 克隆并安装

```bash
git clone https://github.com/jamesjav/Opti-Resume.git
cd Opti-Resume
pip install -r requirements.txt
```

### 2. 配置 API 密钥

```bash
cp .env.example .env
```

编辑 `.env`，至少配置一个 LLM 服务商的密钥：

```env
# 方案 A：OpenAI
OPENAI_API_KEY=sk-your-key-here

# 方案 B：DeepSeek（性价比之选）
DEEPSEEK_API_KEY=sk-your-key-here

# 方案 C：Ollama（免费本地部署）
OLLAMA_BASE_URL=http://localhost:11434/v1
```

### 3. 启动

```bash
streamlit run app.py
```

---

## 🤖 支持的 LLM 服务商

| 服务商 | 费用 | 质量 | 配置方式 |
|--------|------|------|----------|
| **OpenAI**（GPT-4o） | $$$ | 最佳 | 需要 API Key |
| **DeepSeek** | $ | 良好 | 需要 API Key |
| **Ollama**（本地） | 免费 | 取决于模型 | 安装 [Ollama](https://ollama.ai) + 拉取模型 |

应用会自动检测已配置的服务商，仅显示可用选项。

---

## 📁 项目结构

```
Opti-Resume/
├── app.py                          # Streamlit 入口
├── OptiResume/
│   ├── main.py                     # 各工具页面逻辑
│   ├── utils.py                    # PDF 提取与生成
│   └── llm.py                      # 多 LLM 客户端
├── Prompts/
│   ├── Optimisation-Prompt.txt     # 简历优化（英文）
│   ├── Optimisation-Prompt-CN.txt  # 简历优化（中文）
│   ├── ATS_Check.txt               # ATS 分析（英文）
│   ├── ATS_Check-CN.txt            # ATS 分析（中文）
│   ├── Bullet_Prompt.txt           # 要点分析（英文）
│   ├── Bullet_Prompt-CN.txt        # 要点分析（中文）
│   ├── Keyword_Prompt.txt          # 关键词提取（英文）
│   ├── Keyword_Prompt-CN.txt       # 关键词提取（中文）
│   ├── Metric_Prompt.txt           # 量化指标（英文）
│   ├── Metric_Prompt-CN.txt        # 量化指标（中文）
│   ├── CoverLetter_Prompt.txt      # 求职信（英文）
│   └── CoverLetter_Prompt-CN.txt   # 求职信（中文）
├── static/
│   └── styles.css                  # 深色主题样式
├── requirements.txt
├── .env.example
└── README.md
```

---

## 📄 开源协议

本项目基于 MIT 协议开源，详见 [LICENSE](LICENSE)。
