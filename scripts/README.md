
## h4-auto-alert

The script is using [Telegram Bot API -- sendMessage](https://core.telegram.org/bots/api#sendmessage) to send notifications to the chat channel.

To setup the script, create a config file at `~/.config/h4-scripts/config.json` with content like below:

```
{
	"TELEGRAM_CHATID": "@HackingThursday",
	"TELEGRAM_TOKEN": "57######43:AA###############################r8"
}
```

and then add a crontab setting like below:

```
# 10:30 every wednesday
30 10 * * 3  /THE_PATH_TO_THE_SCRIPT_FOLDER/h4-auto-alert
```
