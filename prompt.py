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
llm = OpenAI(temperature=0.9)

# define prompt template
prompt = PromptTemplate(
    input_variables=["product"],
    template="What is a good name for a company that makes {product}?",
)

chain = LLMChain(llm=llm, prompt=prompt) # llmchains
message = chain.run("colorful socks")
print(message)