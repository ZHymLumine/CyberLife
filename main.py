import configparser
from waifu.Waifu import Waifu
from waifu.StreamCallback import WaifuCallback
from waifu.llm.GPT import GPT
from waifu.llm.Claude import Claude
from waifu.Tools import load_prompt, load_emoticon, load_memory, str2bool, divede_sentences
from tts.TTS import TTS
from tts.edge.edge import speak
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
import time 
import logging
import os
from playsound import playsound
from pydub import AudioSegment
from pydub.playback import play

os.environ["TOKENIZERS_PARALLELISM"] = "true"
log_file_path = './LOG/waifu.log'
if not os.path.exists(log_file_path):
    with open(log_file_path, 'w') as f:
        print('log file created.')
else:
    print('log already exists.')

logging.basicConfig(level=logging.INFO, filename='./LOG/waifu.log')
logging.info("This is an info message.")


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

# 语音配置
tts_model = config['TTS']['model']
if tts_model == 'Edge':
	tts = TTS(speak, voice)
	api = config['TTS_Edge']['azure_speech_key']
	if api == '':
		use_emotion = False


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
 
    if send_text:
        logging.info(f'发送信息: {reply}')
    if send_voice:
        emotion = waifu.analyze_emotion(reply)
        tts.speak(reply, emotion)
        file_path = './output.mp3'
        abs_path = os.path.abspath(file_path)
        mp3_audio = AudioSegment.from_file(abs_path, format="mp3")
        play(mp3_audio)
        mtime = os.path.getmtime(file_path)
        local_time = time.localtime(mtime)
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        #message.sender.send_message("%s" % record(file='file:///' + abs_path))
        logging.info(f'发送语音({emotion} {time_str}): {reply}')
    sentences = divede_sentences(reply)
    # for st in sentences:
    #     time.sleep(0.5)
    #     if st == '' or st == ' ':
    #         continue
    #     if send_text:
    #         logging.info(f'发送信息: {st}')
    #     if send_voice:
    #         emotion = waifu.analyze_emotion(st)
    #         tts.speak(st, emotion)
    #         file_path = './output.wav'
    #         abs_path = os.path.abspath(file_path)
    #         wave_obj = sa.WaveObject.from_wave_file(abs_path)
    #         play_obj = wave_obj.play()
    #         play_obj.wait_done()  
    #         mtime = os.path.getmtime(file_path)
    #         local_time = time.localtime(mtime)
    #         time_str = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    #         #message.sender.send_message("%s" % record(file='file:///' + abs_path))
    #         logging.info(f'发送语音({emotion} {time_str}): {st}')
    waifu.finish_ask(reply)

waifu.summarize_memory()
print("Bye bye!")
