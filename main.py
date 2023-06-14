import configparser
from waifu.llm.GPT import GPT
from waifu.Tools import str2bool
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts.chat import (
    ChatPromptTemplate,
    MessagesPlaceholder, 
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)


config = configparser.ConfigParser()

config_files = config.read('config.ini', 'utf-8')
if len(config_files) == 0:
    raise FileNotFoundError("can't find config.ini !")

# CyberWaifu 配置
name 		 = config['CyberWaifu']['name']
username     = config['CyberWaifu']['username']
charactor 	 = config['CyberWaifu']['charactor']
send_text    = str2bool(config['CyberWaifu']['send_text'])
send_voice   = str2bool(config['CyberWaifu']['send_voice'])
use_emoji 	 = str2bool(config['Thoughts']['use_emoji'])
use_qqface   = str2bool(config['Thoughts']['use_qqface'])
use_emoticon = str2bool(config['Thoughts']['use_emoticon'])
use_search 	 = str2bool(config['Thoughts']['use_search'])
use_emotion  = str2bool(config['Thoughts']['use_emotion'])
search_api	 = config['Thoughts_GoogleSerperAPI']['search_api']
voice 		 = config['TTS']['voice']

# LLM 模型配置
model = config['LLM']['model']
if model == 'OpenAI':
    openai_api = config['LLM_OpenAI']['openai_key']
    #callback = WaifuCallback(tts, send_text, send_voice)
    callback=StreamingStdOutCallbackHandler()
    brain = GPT(openai_api, name, stream=True, callback=callback)
elif model == 'Claude':
	callback = None
	#user_oauth_token = config['LLM_Claude']['user_oauth_token']
	#bot_id = config['LLM_Claude']['bot_id']
	#brain = Claude(bot_id, user_oauth_token, name)

# messages = [
#     SystemMessage(content="You are a helpful assistant that translates English to French."),
#     HumanMessage(content="I love programming.")
# ]

stop = False
system_message = SystemMessage(content="You are a helpful assistant that translates English to Chinese."),
print(type(system_message))
while not stop :
    content = input("You: ")
    if len(content) == 1 and content[0] == 'q':
        stop = True
        break
    human_message = HumanMessage(content=f"{content}")
    messages = [
        SystemMessage(content="You are a helpful assistant that translates English to Chinese."),
        HumanMessage(content=content)
    ]
    response = brain.think((messages))
    print()

print("Bye bye!")
