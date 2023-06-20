import configparser
from waifu.Waifu import Waifu
#from waifu.StreamCallback import WaifuCallback
from waifu.llm.GPT import GPT
from waifu.llm.Claude import Claude
from waifu.Tools import load_prompt, load_emoticon, load_memory, str2bool
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

prompt = load_prompt(charactor)

# LLM 模型配置
model = config['LLM']['model']
if model == 'OpenAI':
    openai_api = config['LLM_OpenAI']['openai_key']
    #callback = WaifuCallback(tts, send_text, send_voice)
    callback=StreamingStdOutCallbackHandler()
    brain = GPT(openai_api, name, stream=True, callback=callback)
elif model == 'Claude':
	callback = None
	user_oauth_token = config['LLM_Claude']['user_oauth_token']
	bot_id = config['LLM_Claude']['bot_id']
	brain = Claude(bot_id, user_oauth_token, name)

waifu = Waifu(brain=brain,
				prompt=prompt,
				name=name,
                username=username,
				use_search=use_search,
				search_api=search_api,
				use_emoji=use_emoji,
				use_qqface=use_qqface,
                use_emotion=use_emotion,
				use_emoticon=use_emoticon)

# load memory
filename = config['CyberWaifu']['memory']
if filename != '':
	memory = load_memory(filename, waifu.name)
	waifu.import_memory_dataset(memory)
        
        

stop = False
while not stop :
    content = input("You: ")
    if len(content) == 1 and content[0] == 'q':
        stop = True
        break
    reply = waifu.ask(content)
    waifu.finish_ask(reply)
    
waifu.summarize_memory()
print("Bye bye!")
