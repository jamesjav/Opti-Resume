import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))


def get_available_providers():
    """Return list of available LLM providers based on configured API keys."""
    providers = []
    if os.getenv("OPENAI_API_KEY"):
        providers.append("OpenAI")
    if os.getenv("DEEPSEEK_API_KEY"):
        providers.append("DeepSeek")
    if os.getenv("OLLAMA_BASE_URL"):
        providers.append("Ollama")
    return providers if providers else ["OpenAI"]


def _build_client(provider: str):
    """Build an OpenAI-compatible client for the given provider."""
    if provider == "DeepSeek":
        return OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
        )
    elif provider == "Ollama":
        return OpenAI(
            api_key="ollama",
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
        )
    else:
        return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def _get_model(provider: str) -> str:
    """Return the default model name for each provider."""
    if provider == "DeepSeek":
        return os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    elif provider == "Ollama":
        return os.getenv("OLLAMA_MODEL", "llama3")
    else:
        return os.getenv("OPENAI_MODEL", "gpt-4o")


def SendRequest(prompt_filename: str, text: str, provider: str = "OpenAI",
                language: str = "English", max_tokens: int = 2000,
                temperature: float = 0) -> str:
    """
    Send a prompt + user text to the selected LLM provider and return the response.

    Args:
        prompt_filename: Name of the prompt file under Prompts/
        text: The user-provided text (resume, bullet point, job desc, etc.)
        provider: One of "OpenAI", "DeepSeek", "Ollama"
        language: "English" or "Chinese" — appended to prompt for output language
        max_tokens: Maximum tokens for the completion
        temperature: Sampling temperature
    """
    prompts_dir = os.path.join(os.path.dirname(__file__), '..', 'Prompts')
    prompt_path = os.path.join(prompts_dir, prompt_filename)
    with open(prompt_path, 'r', encoding='utf-8') as f:
        prompt = f.read()

    # Append language instruction
    if language == "Chinese":
        prompt += "\n\nPlease respond entirely in Chinese (简体中文)."

    prompt = prompt + "\n\n" + text

    client = _build_client(provider)
    model = _get_model(provider)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert resume optimization assistant. "
                        "Provide clear, actionable, and professional advice."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        result = response.choices[0].message.content.strip()
        return result
    except Exception as e:
        return f"[Error] Failed to get response from {provider}: {str(e)}"
