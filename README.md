# Opti-Resume: AI-Powered Resume Optimization Toolkit

An intelligent, open-source resume optimization tool powered by LLMs. Upload your resume, paste a job description, and get actionable AI-driven suggestions to make your resume stand out.

## What's New (Improved Version)

This fork includes significant enhancements over the original:

- **Multi-LLM Support**: Switch between OpenAI, DeepSeek, and local Ollama models
- **Chinese Resume Support**: Full Chinese prompt templates for resume optimization, ATS analysis, and more
- **Cover Letter Generator**: New tool to auto-generate tailored cover letters
- **Improved UI**: Modern dark-themed interface with smooth gradients and animations
- **Better PDF Output**: Unicode/Chinese character support via reportlab (with automatic fallback)
- **Error Handling**: Graceful error messages instead of crashes
- **Configurable Parameters**: Adjustable max tokens and temperature in sidebar

## Features

| Tool | Description |
|------|-------------|
| Resume Optimization | Rewrite your resume with strong action verbs, quantified achievements, and ATS-friendly keywords |
| ATS Score Analysis | Score your resume against a job description and get missing keywords + improvement suggestions |
| Bullet-Point Analysis | Transform weak bullet points into impactful, quantified achievements using the XYZ formula |
| Skills Analysis | Extract and categorize technical skills from any job description |
| Metric Suggestions | Get 5 quantifiable metrics for any bullet point you describe |
| Cover Letter Generator | Auto-generate a personalized cover letter from your resume + job description |

## Quick Start

### 1. Clone and Install

```bash
git clone https://github.com/YOUR_USERNAME/Opti-Resume.git
cd Opti-Resume
pip install -r requirements.txt
```

### 2. Configure API Keys

```bash
cp .env.example .env
```

Edit `.env` with at least one LLM provider's API key:

```env
# Option A: OpenAI
OPENAI_API_KEY=sk-your-key-here

# Option B: DeepSeek (cheaper alternative)
DEEPSEEK_API_KEY=sk-your-key-here

# Option C: Ollama (free, local)
OLLAMA_BASE_URL=http://localhost:11434/v1
```

### 3. Run

```bash
streamlit run app.py
```

## Supported LLM Providers

| Provider | Cost | Quality | Setup |
|----------|------|---------|-------|
| **OpenAI** (GPT-4o) | $$$ | Best | API key required |
| **DeepSeek** | $ | Good | API key required |
| **Ollama** (local) | Free | Varies | Install [Ollama](https://ollama.ai) + pull a model |

The app auto-detects which providers are configured and shows only available options.

## Project Structure

```
Opti-Resume/
├── app.py                    # Streamlit entry point
├── OptiResume/
│   ├── main.py               # Page logic for each tool
│   ├── utils.py              # PDF extraction & generation
│   └── llm.py                # Multi-provider LLM client
├── Prompts/
│   ├── Optimisation-Prompt.txt
│   ├── Optimisation-Prompt-CN.txt   # Chinese version
│   ├── ATS_Check.txt
│   ├── ATS_Check-CN.txt
│   ├── Bullet_Prompt.txt
│   ├── Bullet_Prompt-CN.txt
│   ├── Keyword_Prompt.txt
│   ├── Keyword_Prompt-CN.txt
│   ├── Metric_Prompt.txt
│   ├── Metric_Prompt-CN.txt
│   ├── CoverLetter_Prompt.txt       # New!
│   └── CoverLetter_Prompt-CN.txt    # New!
├── static/
│   └── styles.css
├── requirements.txt
├── .env.example
└── README.md
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Original project by [KalyanM45](https://github.com/KalyanM45/Opti-Resume)
- Improved with multi-LLM support, Chinese language support, and UI enhancements
