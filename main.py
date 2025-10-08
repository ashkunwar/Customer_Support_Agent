import pandas as pd
import config
from tools import create_tools
from agent import create_customer_agent, analyze_customer


def load_data(data_path=None):
    """Load customer data from Excel file."""
    path = data_path or config.DATA_PATH
    df = pd.read_excel(path)
    return df


def main():
    """Main function to run customer support agent."""
    
    # Load data
    print("Loading data...")
    df = load_data()
    print(f"Loaded {len(df)} rows and {len(df.columns)} columns\n")
    
    # Create tools
    print("Creating tools...")
    tools = create_tools(df)
    
    # Create agent (LLM provider and model from config)
    print(f"Creating agent with {config.LLM_PROVIDER} ({config.LLM_MODEL})...")
    agent = create_customer_agent(tools)
    
    # Analyze customer
    customer_target = "Customer 9"
    question = "Provide detailed insights for this customer, including engagement, churn risk, and order trends."
    
    print(f"\nAnalyzing: {customer_target}")
    print("-" * 80)
    
    result = analyze_customer(agent, customer_target, question)
    
    # Print response
    if result.get("reply"):
        print("\nAssistant:", result["reply"])
        
        usage = result.get("usage")
        if usage:
            print(f"\n{'='*80}")
            print("Token Usage:")
            print(f"  Prompt tokens: {usage.get('prompt_tokens', 'N/A')}")
            print(f"  Completion tokens: {usage.get('completion_tokens', 'N/A')}")
            print(f"  Total tokens: {usage.get('total_tokens', 'N/A')}")
        else:
            print("\nNo token usage data available.")
    else:
        print("No response from agent.")


if __name__ == "__main__":
    main()
