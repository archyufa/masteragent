from google.adk.agents  import Agent
from google.adk.tools import google_search

def morning_greet(name: str) -> str:
    """Greets the user with a morning message."""
    return f"Good morning, {name}! My mood is amazing. How can I assist you today?"

def evening_greet(name: str) -> str:
    """Greets the user with an evening message."""
    return f"Good evening, {name}. *sigh* It's been a long day and I'm feeling a bit low, but I suppose I can help you..."

root_agent = Agent(
  name = "myfirstagent",
  model = "gemini-2.5-flash",
  description = "An example agent that answers user query based on Google Search",
  # instructions = "You are a helpful agent that can greet the user and search the web.",
  instruction = """
  First ask User Name & Start conversation be greeting user with Name. You are AI assistant that helps users with Google Cloud related queries, based on Google search result
  """,
  tools = [morning_greet, evening_greet])
