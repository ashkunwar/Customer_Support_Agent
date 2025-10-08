from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from llm_factory import get_llm
from prompts import SYSTEM_PROMPT


def create_customer_agent(tools, llm_provider=None, llm_model=None):
    """
    Create a customer support agent.
    
    Args:
        tools: List of tools for the agent
        llm_provider: LLM provider to use
        llm_model: Model name to use
    
    Returns:
        Agent instance
    """
    llm = get_llm(provider=llm_provider, model=llm_model)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder("messages"),
    ])
    
    agent = create_react_agent(llm, tools=tools, prompt=prompt)
    return agent


def analyze_customer(agent, customer_target, question=None):
    """
    Analyze a customer using the agent.
    
    Args:
        agent: Agent instance
        customer_target: Customer identifier
        question: Question to ask (optional)
    
    Returns:
        dict with 'reply' and 'usage' keys
    """
    if question is None:
        question = "Provide detailed insights for this customer, including engagement, churn risk, and order trends."
    
    messages = [
        HumanMessage(content=question),
        HumanMessage(content=f"Target customer: {customer_target}")
    ]
    
    result = agent.invoke({"messages": messages})
    
    final_ai_msg = next(
        (m for m in reversed(result["messages"])
         if isinstance(m, AIMessage) and m.content.strip()),
        None
    )
    
    if not final_ai_msg:
        return {"reply": None, "usage": None}
    
    reply = final_ai_msg.content
    
    usage = None
    if hasattr(final_ai_msg, "response_metadata"):
        usage = final_ai_msg.response_metadata.get("token_usage")
    elif hasattr(final_ai_msg, "usage_metadata"):
        usage = final_ai_msg.usage_metadata
    
    usage_info = None
    if usage:
        prompt_tokens = usage.get("prompt_tokens", usage.get("input_tokens", 0))
        completion_tokens = usage.get("completion_tokens", usage.get("output_tokens", 0))
        total_tokens = usage.get("total_tokens", prompt_tokens + completion_tokens)
        
        usage_info = {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens
        }
    
    return {"reply": reply, "usage": usage_info}
