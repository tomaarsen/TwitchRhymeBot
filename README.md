# TwitchRhymeBot
Twitch bot that periodically responds to messages with a rhyme   

---
# Explanation

When the bot has started, it will start listening to chat messages in the channel listed in the settings.txt file. Every "cooldown" seconds, as listed in the settings.txt file, the bot will respond to a message with a rhyme. The bot will try to ensure that the sound of the final word of the input message from the random chat user and the output message from the bot have the same sound. It will also try to match the syllable count of both messages.

---

# Example
<pre><b>
Input:  "its kinda useless"
Output: "Good job regardless"

Input:  "Face your crimes!"
Output: "were great times"

Input:  "bloody and stuff"
Output: "This game is tough"
</b></pre>

---

# Settings
This bot is controlled by a settings.txt file, which looks like:
```
{
    "Host": "irc.chat.twitch.tv",
    "Port": 6667,
    "Channel": "#<channel>",
    "Nickname": "<name>",
    "Authentication": "oauth:<auth>",
    "Cooldown": 300
}
```

| **Parameter**        | **Meaning** | **Example** |
| -------------------- | ----------- | ----------- |
| Host                 | The URL that will be used. Do not change.                         | "irc.chat.twitch.tv" |
| Port                 | The Port that will be used. Do not change.                        | 6667 |
| Channel              | The Channel that will be connected to.                            | "#CubieDev" |
| Nickname             | The Username of the bot account.                                  | "CubieB0T" |
| Authentication       | The OAuth token for the bot account.                              | "oauth:pivogip8ybletucqdz4pkhag6itbax" |
| Cooldown | The cooldown between rhymes in seconds. | 300 |


*Note that the example OAuth token is not an actual token, but merely a generated string to give an indication what it might look like.*

I got my real OAuth token from https://twitchapps.com/tmi/.

---

# Usage
<b>Run the RhymeBot.py file</b>

---

# Dependencies
<b>This bot relies on having a MarkovChain_xxx.db file being in the same folder as the .py files.</b>
More generally, this bot relies on the <b>TwitchMarkovChain</b> bot being run in the same folder, to create a database of sentences.

---

# Requirements
* Python 3+ (Only tested on 3.6)

Download Python online.

* nltk module
* json module
* sqlite3 module

Install these using `pip install ...`
Note that the NLTK module might require you to download some additional information. 

* TwitchWebsocket

Install this using `pip install git+https://github.com/CubieDev/TwitchWebsocket.git`

This last library is my own [TwitchWebsocket](https://github.com/CubieDev/TwitchWebsocket) wrapper, which makes making a Twitch chat bot a lot easier.
This repository can be seen as an implementation using this wrapper.

---

# Other Twitch Bots

* [TwitchGoogleTranslate](https://github.com/CubieDev/TwitchGoogleTranslate)
* [TwitchMarkovChain](https://github.com/CubieDev/TwitchMarkovChain)
* [TwitchCubieBotGUI](https://github.com/CubieDev/TwitchCubieBotGUI)
* [TwitchCubieBot](https://github.com/CubieDev/TwitchCubieBot)
* [TwitchDeathCounter](https://github.com/CubieDev/TwitchDeathCounter)
* [TwitchSuggestDinner](https://github.com/CubieDev/TwitchSuggestDinner)
* [TwitchPickUser](https://github.com/CubieDev/TwitchPickUser)
* [TwitchSaveMessages](https://github.com/CubieDev/TwitchSaveMessages)
* [TwitchMMLevelPickerGUI](https://github.com/CubieDev/TwitchMMLevelPickerGUI) (Mario Maker 2 specific bot)
* [TwitchMMLevelQueueGUI](https://github.com/CubieDev/TwitchMMLevelQueueGUI) (Mario Maker 2 specific bot)
* [TwitchPackCounter](https://github.com/CubieDev/TwitchPackCounter) (Streamer specific bot)
* [TwitchDialCheck](https://github.com/CubieDev/TwitchDialCheck) (Streamer specific bot)
* [TwitchSendMessage](https://github.com/CubieDev/TwitchSendMessage) (Not designed for non-programmers)
