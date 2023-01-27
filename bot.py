import os
import traceback
import re
import sys
import dotenv
import openai
from concurrent.futures import ThreadPoolExecutor
from slackeventsapi import SlackEventAdapter
from slack_sdk.web import WebClient
from html import unescape
from history import ConversationHistory

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
BOT_REPLY_IN_JSON = os.getenv('BOT_REPLY_IN_JSON', 'False').lower() == 'true'
BOT_REPLY_SHOW_META = os.getenv('BOT_REPLY_SHOW_META', 'False').lower() == 'true'
BOT_MAX_HISTORY_CHARS = int(os.environ["BOT_MAX_HISTORY_CHARS"])
executor = ThreadPoolExecutor(max_workers=BOT_MAX_WORKERS)
reCodeBlock = re.compile(r"```([^`]*)```")
history = ConversationHistory(size=50)

# Stops
HUMAN = "Q:"
BOT = "A:"


def ask(text):
    return openai.Completion.create(
        engine=OPENAI_API_ENGINE,
        prompt=text,
        max_tokens=OPENAI_API_MAX_TOKENS,
        temperature=OPENAI_API_TEMPERATURE,
        top_p=OPENAI_API_TOP_P,
        n=OPENAI_API_N,
        stream=False,
        # frequency_penalty=0,
        # presence_penalty=0
        # logprobs=None,
        stop=[HUMAN],
    )


def isSentByBot(event):
    return "bot_id" in event


def containsCodeBlock(s):
    return bool(reCodeBlock.search(s))


def reformat(text, meta):
    if len(text) < 1:
        return ":man-shrugging:" + meta
    if containsCodeBlock(text):
        return text + meta
    return "``` " + text + meta + " ```"

def parseMeta(response):
    total_tokens = int(response["usage"]["total_tokens"])
    # model = response["model"]
    # objective = response["object"]
    # return f"\n ({total_tokens} tokens | {model} | {objective})"
    return f"\n ({total_tokens} tokens)"

@slackRecevier.on("message")
def onMessage(data):
    print("onMessage")
    event = data["event"]
    if not isSentByBot(event):
        executor.submit(onEventAsync, event)
        print(f"task submitted")


def onEventAsync(event):
    if "text" in event:
        try:
            print(str(event))
            request = unescape(event["text"])
            if request.startswith(">"):
                print("Ignored << ", request)
                return

            # History
            ts = event["thread_ts"] if "thread_ts" in event else event["ts"]
            history.appendMessage(ts, f"{HUMAN} {request}\n")
            request = "\n".join(
                history.retrieveMessages(ts, max_length=BOT_MAX_HISTORY_CHARS)
            )

            print("OpenAI << ", request)
            response = ask(request)
            print("OpenAI >> ", response)

            if BOT_REPLY_IN_JSON:
                answer = str(response)
            else:
                # Response
                text = response["choices"][0]["text"]
                # Remove bot name
                text = text.replace(BOT, "").lstrip().rstrip()
                history.appendMessage(ts, f"{BOT} {text}\n")
                # Summary
                meta = parseMeta(response) if BOT_REPLY_SHOW_META else ""
                answer = reformat(text, meta)
        except Exception as e:
            answer = ":confounded: :" + str(e)
            print(traceback.format_exc())

        slackSender.chat_postMessage(
            channel=event["channel"],
            text=answer,
            thread_ts=event["ts"],
        )
    else:
        # E.g. when user edit a message
        print("No 'text' in this event:", event)


# Flask server on port 3000, endpoint: /slack/events
slackRecevier.start(host="0.0.0.0", port=BOT_PORT)
