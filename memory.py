import os
import openai
from langchain import OpenAI, ConversationChain

# openai key
os.environ["OPENAI_API_KEY"] = "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"
llm = OpenAI(temperature=0)
conversation = ConversationChain(llm=llm, verbose=True) # a kind of memory chain

output = conversation.predict(input="你好!")
print(output)
output = conversation.predict(input="我很好。我正在与人工智能对话")
print(output)