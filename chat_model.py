import os
import openai
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

from langchain.prompts.chat import (
    ChatPromptTemplate,
    MessagesPlaceholder, 
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

os.environ["SERPAPI_API_KEY"] = "1804f4033ec7003c8c1065234e8b35b14c631da8e1cfdc5f1f0da080a44c0a21"
os.environ["OPENAI_API_KEY"] = "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"

# chat = ChatOpenAI(temperature=0)

# template = "You are a helpful assistant that translates {input_language} to {output_language}."
# system_message_prompt = SystemMessagePromptTemplate.from_template(template)
# human_template = "{text}"
# human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

# chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

# # get a chat completion from the formatted messages
# response = chat(chat_prompt.format_prompt(input_language="English", output_language="French", text="I love programming.").to_messages())
# # -> AIMessage(content="J'aime programmer.", additional_kwargs={})
# print(response)

# # First, let's load the language model we're going to use to control the agent.
# chat = ChatOpenAI(temperature=0)

# # Next, let's load some tools to use. Note that the `llm-math` tool uses an LLM, so we need to pass that in.
# llm = OpenAI(temperature=0)
# tools = load_tools(["serpapi", "llm-math"], llm=llm)


# # Finally, let's initialize an agent with the tools, the language model, and the type of agent we want to use.
# agent = initialize_agent(tools, chat, agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# # Now let's test it out!
# response = agent.run("Who is Olivia Wilde's boyfriend? What is his current age raised to the 0.23 power?")
# print(response)

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know."),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}")
])

llm = ChatOpenAI(temperature=0)
memory = ConversationBufferMemory(return_messages=True)
conversation = ConversationChain(memory=memory, prompt=prompt, llm=llm)

response = conversation.predict(input="Hi there!")
print(response)
# -> 'Hello! How can I assist you today?'


response = conversation.predict(input="I'm doing well! Just having a conversation with an AI.")
print(response)
# -> "That sounds like fun! I'm happy to chat with you. Is there anything specific you'd like to talk about?"

response = conversation.predict(input="Tell me about yourself.")
print(response)