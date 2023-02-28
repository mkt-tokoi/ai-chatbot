# OpenAI API + linebot

## Setup AWS SecretManager

- secret_name : `prod/openai_linebot`

```json
{
  "/linebot/davinci3/CHANNEL_ACCESS_TOKEN":"xxxxxxxxxxxxxxxxx",
  "/linebot/davinci3/CHANNEL_SECRET":"xxxxxxxxxxxxxxxxx",
  "/linebot/dalle2/CHANNEL_ACCESS_TOKEN":"xxxxxxxxxxxxxxxxx",
  "/linebot/dalle2/CHANNEL_SECRET":"xxxxxxxxxxxxxxxxx",
  "/openai/apikey":"xxxxxxxxxxxxxxxxx"}
```

- Replace `xxxxxxxxxxxxxxxxx` with your own values.


## Requirements

- Python 3.8
- `pip install -r src/requirements.txt`

## start server
```
cd ./src
python run_server.py
```

## start ngrok (optional)
```
ngrok http 5000
```

## register your webhook url to LINE developer console

- https://developers.line.biz/console/
