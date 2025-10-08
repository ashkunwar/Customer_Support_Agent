from langchain.tools import tool
import pandas as pd

# Global DataFrame reference
_df = None


def create_tools(df):
    """
    Create tools for DataFrame analysis.
    
    Args:
        df: pandas DataFrame
    
    Returns:
        List of tools
    """
    global _df
    _df = df
    
    @tool
    def show_summary() -> str:
        """Returns a string summary of the dataframe, including all columns."""
        return str(_df.describe(include='all'))
    
    @tool
    def list_columns() -> str:
        """Returns a comma-separated string of all column names in the dataframe."""
        return ", ".join(_df.columns)
    
    @tool
    def get_rows(n: int = 5) -> str:
        """Returns the first n rows of the dataframe as a markdown table."""
        # Convert to int if string is passed
        if isinstance(n, str):
            n = int(n)
        return _df.head(n).to_markdown()
    
    @tool
    def query_data(query: str = "") -> str:
        """Run a pandas .query() expression safely."""
        if not query:
            return "Error: query string is empty."
        try:
            result = _df.query(query)
            return result.head(10).to_markdown()
        except Exception as e:
            return f"Error: {e}"
    
    return [show_summary, list_columns, get_rows, query_data]
