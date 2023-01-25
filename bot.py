import os
import dotenv
import openai
from concurrent.futures import ThreadPoolExecutor
from slackeventsapi import SlackEventAdapter
from slack_sdk.web import WebClient
from html import unescape

dotenv.load_dotenv()

# Slack
SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
slackRecevier = SlackEventAdapter(SLACK_SIGNING_SECRET, endpoint="/")
slackSender = WebClient(SLACK_BOT_TOKEN)

# OpenAI
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
openai.api_key = OPENAI_API_KEY

# OpenAI - Config
OPENAI_API_ENGINE = os.environ["OPENAI_API_ENGINE"]
OPENAI_API_TEMPERATURE = float(os.environ["OPENAI_API_TEMPERATURE"])
OPENAI_API_MAX_TOKENS = int(os.environ["OPENAI_API_MAX_TOKENS"])
OPENAI_API_TOP_P = float(os.environ["OPENAI_API_TOP_P"])
OPENAI_API_N = int(os.environ["OPENAI_API_N"])

# Threads
BOT_MAX_WORKERS = int(os.environ["BOT_MAX_WORKERS"])
BOT_PORT = int(os.environ["BOT_PORT"])
BOT_REPLY_IN_JSON = int(os.environ["BOT_REPLY_IN_JSON"])
executor = ThreadPoolExecutor(max_workers=BOT_MAX_WORKERS)


def ask(text):
    return openai.Completion.create(
        engine=OPENAI_API_ENGINE,
        prompt=text,
        max_tokens=OPENAI_API_MAX_TOKENS,
        temperature=OPENAI_API_TEMPERATURE,
        top_p=OPENAI_API_TOP_P,
        n=OPENAI_API_N,
        stream=False,
        # logprobs=None,
        # stop=["Q:", "A:"],
    )


def isSentByBot(event):
    return "bot_id" in event


@slackRecevier.on("message")
def onMessage(data):
    print("onMessage")
    event = data["event"]
    if not isSentByBot(event):
        executor.submit(onEventAsync, event)
        print(f"task submitted")


def onEventAsync(event):
    try:
        request = unescape(event["text"])
        if request.startswith(">"):
            print("Ignored << ", request)
            return
        print("OpenAI << ", request)
        response = ask(request)
        print("OpenAI >> ", response)

        if BOT_REPLY_IN_JSON:
            answer = str(response)
        else:
            answer = "```" + response["choices"][0]["text"] + "```"
    except Exception as e:
        answer = "```" + str(e) + "```"
        print(e)

    slackSender.chat_postMessage(
        channel=event["channel"],
        text=answer,
        thread_ts=event["ts"],
    )

# Flask server on port 3000, endpoint: /slack/events
slackRecevier.start(host="0.0.0.0", port=BOT_PORT)
