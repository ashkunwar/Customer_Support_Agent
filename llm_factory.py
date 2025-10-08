from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
import config


def get_llm(provider=None, model=None):
    """
    Factory function to get LLM instance based on provider.
    
    Args:
        provider: LLM provider ('groq', 'openai', 'anthropic', 'gemini')
        model: Model name to use
    
    Returns:
        LLM instance
    """
    provider = provider or config.LLM_PROVIDER
    model = model or config.LLM_MODEL
    
    if provider == "groq":
        if not config.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not found in environment")
        return ChatGroq(api_key=config.GROQ_API_KEY, model=model)
    
    elif provider == "openai":
        if not config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not found in environment")
        return ChatOpenAI(api_key=config.OPENAI_API_KEY, model=model)
    
    elif provider == "anthropic":
        if not config.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")
        return ChatAnthropic(api_key=config.ANTHROPIC_API_KEY, model=model)
    
    elif provider == "gemini":
        if not config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment")
        return ChatGoogleGenerativeAI(api_key=config.GEMINI_API_KEY, model=model)
    
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}. Supported: groq, openai, anthropic, gemini")
