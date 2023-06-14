import os
import openai
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType

# openai key
os.environ["OPENAI_API_KEY"] = "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"
os.environ["SERPAPI_API_KEY"] = "1804f4033ec7003c8c1065234e8b35b14c631da8e1cfdc5f1f0da080a44c0a21"

# First, let's load the language model we're going to use to control the agent.
llm = OpenAI(temperature=0)

# Next, let's load some tools to use. Note that the `llm-math` tool uses an LLM, so we need to pass that in.
tools = load_tools(["serpapi", "llm-math"], llm=llm)


# Finally, let's initialize an agent with the tools, the language model, and the type of agent we want to use.
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# Now let's test it out!
message = agent.run("What was the high temperature in SF yesterday in Fahrenheit? What is that number raised to the .023 power?")
print(message)