
from TwitchWebsocket import TwitchWebsocket
import logging, time

from Log import Log
Log(__file__)

from Settings import Settings
from Syllables import Syllables

class RhymeBot:
    def __init__(self):
        self.host = None
        self.port = None
        self.chan = None
        self.nick = None
        self.auth = None
        self.cooldown = 60
        self.prev_message_t = 0
        
        # Fill previously initialised variables with data from the settings.txt file
        Settings(self)
        self.s = Syllables(self.chan)

        self.ws = TwitchWebsocket(host=self.host, 
                                  port=self.port,
                                  chan=self.chan,
                                  nick=self.nick,
                                  auth=self.auth,
                                  callback=self.message_handler,
                                  capability=None,
                                  live=True)
        self.ws.start_bot()

    def set_settings(self, host, port, chan, nick, auth, cooldown):
        self.host = host
        self.port = port
        self.chan = chan
        self.nick = nick
        self.auth = auth
        self.cooldown = cooldown
    
    def message_handler(self, m):
        try:
            if m.type == "366":
                logging.info(f"Successfully joined channel: #{m.channel}")

            elif m.type == "PRIVMSG":
                # Don't do anything with commands
                if m.message.startswith(("!", "/", ".")):
                    return

                sentence = self.s.attempt_to_rhyme(m.message)

                if sentence is not None:
                    logging.info(f"Input:  \"{m.message}\"" + " will be ignored" * ((len(m.message.split(" ")) < 3 and len(sentence.split(" ")) < 3) or len(m.message.split(" ")) > 8))
                    logging.info(f"Output: \"{sentence}\"")
                    logging.info("")
                    if self.prev_message_t + self.cooldown < time.time():
                        self.ws.send_message(sentence)
                        self.prev_message_t = time.time()

        except Exception as e:
            logging.exception(e)

if __name__ == "__main__": 
    RhymeBot()
