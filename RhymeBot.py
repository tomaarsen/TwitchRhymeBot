
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
        # Set up rhyming backend
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

                # Get the rhyming sentence, if one exists
                sentence = self.s.attempt_to_rhyme(m.message)

                if sentence is not None:
                    # If the previous message has been "self.cooldown" seconds ago,
                    # and the initial message and rhyming message are not both less than 4 words
                    # and the initial message and rhyming message are not both larger than 9 words
                    if self.prev_message_t + self.cooldown < time.time() and not (len(m.message.split(" ")) < 4 or len(sentence.split(" ")) < 4 or len(m.message.split(" ")) > 9 or len(sentence.split(" ")) > 9):
                        # Reply with the rhyming sentence with the SingsNote emote attached
                        self.ws.send_message(sentence + " SingsNote")
                        # Reset time for previous message
                        self.prev_message_t = time.time()
                        # Logging
                        logging.info(f"Input:  \"{m.message}\"")
                        logging.info(f"Output: \"{sentence}\"")
                        logging.info("")
                    else:
                        # Logging under debug
                        logging.debug(f"Input:  \"{m.message}\"" + " will be ignored")
                        logging.debug(f"Output: \"{sentence}\"")
                        logging.debug("")

        except Exception as e:
            logging.exception(e)

if __name__ == "__main__": 
    RhymeBot()
