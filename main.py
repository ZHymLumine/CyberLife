import configparser
from waifu.Waifu import Waifu
from waifu.StreamCallback import WaifuCallback
from waifu.llm.GPT import GPT
from waifu.llm.Claude import Claude
from waifu.Tools import load_prompt, load_emoticon, load_memory, str2bool, divede_sentences, translate
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
from vits.CNvoice import generateSound
import time 
import logging
import os
from pydub import AudioSegment
from pydub.playback import play

os.environ["TOKENIZERS_PARALLELISM"] = "true"
log_file_path = './LOG/waifu.log'
if not os.path.exists(log_file_path):
    with open(log_file_path, 'w') as f:
        f.write('log file created. %' % (time.time()))
else:
    pass

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
input_voice  = str2bool(config['CyberWaifu']['input_voice'])
use_emoji 	 = str2bool(config['Thoughts']['use_emoji'])
use_qqface   = str2bool(config['Thoughts']['use_qqface'])
use_emoticon = str2bool(config['Thoughts']['use_emoticon'])
use_search 	 = str2bool(config['Thoughts']['use_search'])
use_emotion  = str2bool(config['Thoughts']['use_emotion'])
search_api	 = config['Thoughts_GoogleSerperAPI']['search_api']
voice 		 = config['TTS']['voice']
pinecone_api = config['PINECONE']['api']
pinecone_env = config['PINECONE']['environment']
translate_platform = config['Translate']['platform']

if translate_platform == 'Baidu':
     baidu_appid = config['Translate_Baidu']['baidu_appid']
     baidu_secretKey = config['Translate_Baidu']['baidu_secretKey']
    

if pinecone_api != '':
    use_pinecone = True

# use_pinecone = False
# pinecone_api = ''

prompt = load_prompt(charactor)

# 语音配置
tts_model = config['TTS']['model']
if tts_model == 'Edge':
	tts = TTS(speak, voice)
	api = config['TTS_Edge']['azure_speech_key']
	if api == '':
		use_emotion = False

#-----------for debugging---------#
tts_model = ''


# vits configuration
vits_model = config['TTS_Vits']['model']
# speakerID = int(config['TTS_Vits']['speaker'])
speaker = config['TTS_Vits']['speaker']
language = config['TTS_Vits']['language']

# LLM 模型配置
model = config['LLM']['model']
if model == 'OpenAI':
    openai_api = config['LLM_OpenAI']['openai_key']
    #callback = WaifuCallback(tts, send_text, send_voice)
    callback=StreamingStdOutCallbackHandler()
    brain = GPT(openai_api, name, stream=True, callback=callback, vectorDB_api=pinecone_api, vectorDB_env=pinecone_env)
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
				use_emoticon=use_emoticon,
                use_pinecone=use_pinecone,
                translate_appid=baidu_appid,
                translate_secretKey=baidu_secretKey)

# load memory
filename = config['CyberWaifu']['memory']
if filename != '':
	memory = load_memory(filename, waifu.name)
	waifu.import_memory_dataset(memory)
        
stop = False
#send_voice = False
while not stop :
    if input_voice:
        content = input("Please Speak: ")
    else:
        content = input("Please type. You: ")

    if len(content) == 1 and content[0] == 'q':
        stop = True
        break

    reply = waifu.ask(content)
 
    if send_text:
        logging.info(f'发送信息: {reply}')
    if send_voice:
        emotion = waifu.analyze_emotion(reply)
        print(emotion)

        # tts
        if tts_model != '':
            # print("tts is speaking")
            tts.speak(reply, emotion)

        # vits
        if vits_model != '':
            # print('vits is speaking')
            text = reply
            if language == 'Chinese':
                text = '[ZH]' + reply + '[ZH]'
            elif language == 'Japanese':
                text = translate(text, 'zh', 'jp', appid=baidu_appid, secret_key=baidu_secretKey)
                print(text)
            generateSound(text, language=language, speaker=speaker)
        file_path = './output.wav'
        if use_emotion:
            file_path = './output.wav'
            audio = AudioSegment.from_file(file_path, "wav")
        else:
            file_path = './output.mp3'
            audio = AudioSegment.from_file(file_path, "mp3")
        abs_path = os.path.abspath(file_path)
        #audio = AudioSegment.from_wav(file_path)
        play(audio)
        mtime = os.path.getmtime(file_path)
        local_time = time.localtime(mtime)
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        #message.sender.send_message("%s" % record(file='file:///' + abs_path))
        logging.info(f'发送语音({emotion} {time_str}): {reply}')
    waifu.finish_ask(reply)

waifu.summarize_memory()
print("Bye bye!")
