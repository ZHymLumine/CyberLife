# CyberLife
![cover](assets/cover.png)

<p align="center">
  <a href="https://github.com/ZHymLumine/CyberLife/stargazers"><img src="https://img.shields.io/github/stars/ZHymLumine/CyberLife?color=cd7373&amp;logo=github&amp;style=for-the-badge" alt="Github stars"></a>
  <img src="https://img.shields.io/badge/Python-3.10.10-blue?style=for-the-badge&logo=Python&logoColor=white&color=cd7373" alt="Python">
  <a href="./LICENSE"><img src="https://img.shields.io/github/license/Syan-Lin/CyberWaifu?&amp;color=cd7373&amp;style=for-the-badge" alt="License"></a>
</p>


---

### 介绍🔎

CyberLife 是一个使用 LLM 和 TTS 实现的聊天机器人，探索真实的聊天体验。

该项目使用 [LangChain](https://github.com/hwchase17/langchain) 作为 LLM 主体框架，TTS 支持 vits、[edge-tts](https://github.com/rany2/edge-tts)。

语言模型支持：
- ChatGPT
- Claude

### 功能

✅ 预定义的思考链：使 AI 可以进行一定的逻辑思考，进行决策。例如在文本中添加 Emoji、发送表情包等等。

✅ 本地记忆数据库：自动总结对话内容并导入记忆数据库，根据用户的提问引入上下文，从而实现长时记忆。同时支持批量导入记忆，使人设更丰富、真实和可控。

✅ 向量数据库:总结的对话内容上传到Pinecone数据库

✅ 现实感知：AI 可以感知现实的时间并模拟自己的状态和行为，例如晚上会在睡觉、用户隔很久回复会有相应反馈（这部分表现暂时不稳定）。

✅ 联网搜索：根据用户的信息，自主构造搜索决策，并引入上下文。

✅ 人设模板、自定义人设

✅ edge-tts, azure 语音服务支持
  
⬜ vits, emotion-vits 支持

⬜ live2d 支持

⬜  GUI 支持

⬜ 多语言文本语音输入输出支持

⬜  机器人部署

⬜  表情支持

⬜ AI 绘图支持，将绘图引入思考链，使 AI 可以生成图片，例如 AI 自拍

### 安装💻

Python 版本：3.10.10

使用 conda:
```powershell
git clone https://github.com/ZHymLumine/CyberLife.git
cd CyberLife
conda create --name CyberLife python=3.10.10
conda activate CyberLife
pip install -r requirements.txt
```

#### ffmpeg 安装
为了支持任意格式的语音发送需安装ffmpeg

Mac: [Install ffmpeg on Mac OSX](https://macappstore.org/ffmpeg/) 或直接在terminal执行
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
brew install ffmpeg
```

Windows: [Download FFmpeg](https://ffmpeg.org/download.html#build-windows)

#### 记忆数据库向量计算模型
为了支持本地的文本向量计算，需要引入 text embedding 模型，这里使用 [Sentence Transformer](https://github.com/UKPLab/sentence-transformers)

首先 [下载模型](https://public.ukp.informatik.tu-darmstadt.de/reimers/sentence-transformers/v0.2/paraphrase-multilingual-MiniLM-L12-v2.zip)，然后解压到根目录的 `st_model` 文件夹，如果不存在请手动创建

### 配置✏️

按照 `template.ini` 进行配置，配置完成后改名为 `config.ini`

#### 大语言模型配置

- OpenAI：需要配置 `openai_key`，
- Claude：需要配置 `user_oauth_token` 和 `bot_id`，具体参考 [Claude API 接入教程](https://juejin.cn/post/7230366377705472060)

#### Pinecone
由于免费版只支持id字段为ASCII编码的向量插入，需要将总结后的对话翻译成英文。使用prompt让大语言模型翻译（这部分在使用ChatGPT实验时不能稳定地翻译成英文）
所以我们选择调用百度翻译的api，具体参考 [百度翻译API官方接入文档](https://fanyi-api.baidu.com/doc/13)
在config.ini配置appid和secret key。

#### 人设 Prompt 配置
根据 `presets/charactor/模板.txt` 进行编写，将编写好的人设 Prompt 丢到 `presets/charactor` 目录下即可，随后在 `config.ini` 配置文件中的 `charactor` 字段填写文件名（不包含后缀名）

记忆设定同样是丢到 `presets/charactor` 目录下，多段记忆用空行分开，并在配置文件中填写 `memory` 字段

#### 联网搜索配置
在 [Google Serper](https://serper.dev/) 中注册并创建一个 API key，在 `config.ini` 中配置并开启即可。Google Serper 可以免费使用 1000 次调用，实测可以使用很久。

由于上下文长度的限制，目前搜索引入的内容并不多，只能获取简单的事实信息。

### 使用🎉
运行 `main.py` 即可

```powershell
conda activate CyberLife
python main.py
```

### 鸣谢
- CyberWaifu(https://github.com/Syan-Lin/CyberWaifu)
