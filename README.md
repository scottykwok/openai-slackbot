## Usage
1. Create your own `.env` based on `.env.sample` . The following keys must be configured:
```shell
# See https://api.slack.com/start/building/bolt-python
SLACK_BOT_TOKEN=xoxb-your-Bot-User-OAuth-Token
SLACK_SIGNING_SECRET=your-signing-secret

# See https://beta.openai.com/account/api-keys
OPENAI_API_KEY=your-openai-api-key

# NGROK
NGROK_AUTHTOKEN=your-ngrok-token
```

2. Then docker compose up: 
```shell
docker compose up -d
```

3. Get the Ngrok URL:
```shell
python3 get_ngrok_url.py
#Output: https://xxxx-xxx-xxx-xxx-xx.xx.ngrok.io
```

4. Goto your Slack App "Event Subscriptions" page and put the Ngrok URL into the "Request URL". And add "Subscribe to bot events". If verified successfully, you will be able to "Save Changes".
   
<img src="img/slack_event.jpg" width="500" />

5. Done! You can now direct message the bot or add the bot to your channel(s). It will reply to the conversation thread.

## Slack App Setup
To create Slack App, see [this example](https://github.com/slackapi/python-slack-events-api/blob/main/example/README.rst). Refer to the sections from "**Create a Slack app**" to "**Save your apps credentials**".

For this particular app, it need the following Bot Token Scopes:

<img src="img/slack_scope.jpg" width="500" />

If you want to direct message the bot, enable the followings:

<img src="img/slack_app_home.jpg" width="500" />

Remember to "Reinstall to Workspace".

<img src="img/slack_install.jpg" width="500" />

## Ngrok Authtoken
<img src="img/key_ngrok.jpg" width="500" />

## OpenAPI API keys
<img src="img/key_openai.jpg" width="500" />

## More
You can also play around with other settings:
```shell
# Some of the OpenAI params
OPENAI_API_ENGINE=text-davinci-003
OPENAI_API_MAX_TOKENS=1024
OPENAI_API_TEMPERATURE=0
OPENAI_API_TOP_P=1
OPENAI_API_N=1

# Set to 1 and the bot will reply in raw json
BOT_REPLY_IN_JSON=1
```
## Local development using venv
```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
ngrok http 3000
python3 bot.py
```

## Screenshots
Here is an example of asking the bot to generate a login page.

<img src="img/output_sample1.jpg"/>

After removing the wrong integrity checksum, the generated HTML looks pretty decent:

<img src="img/output_sample1_render.jpg"/>



## Disclaimer
This is a personal project for fun and is not affiliated with OpenAI or Slack in any way.
