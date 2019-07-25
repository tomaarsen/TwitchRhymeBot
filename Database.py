
import sqlite3, logging, random
logger = logging.getLogger(__name__)

class Database:
    def __init__(self, channel):
        self.db_name = f"MarkovChain_{channel.replace('#', '').lower()}.db"

        sql = "SELECT name FROM sqlite_master WHERE type='table';"
        # Get a flattened list of tables
        table_list = [items[0] for items in self.execute(sql, fetch=True)]
        if "MarkovGrammar" not in table_list or "MarkovStart" not in table_list:
            raise Exception("The Database generated by my TwitchMarkovChain program needs to be present in the current directory for this bot to run.")

    def execute(self, sql, values=None, fetch=False):
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            if values is None:
                cur.execute(sql)
            else:
                cur.execute(sql, values)
            conn.commit()
            if fetch:
                return cur.fetchall()
    
    def get_inputs(self, rhymes):
        if len(rhymes) > 1:
            return self.execute(f"SELECT word1, word2, word3 FROM MarkovGrammar WHERE word3 IN ({', '.join(['?' for _ in rhymes])});", values=(tuple(rhymes)), fetch=True)
        else:
            return self.execute(f"SELECT word1, word2, word3 FROM MarkovGrammar WHERE word3 = ?;", values=(list(rhymes)[0], ), fetch=True)
    
    def get_final_inputs(self, rhymes):
        # Modified version of get_inputs which only looks for cases where the sentence ends
        # TODO: Fix sqlite3.OperationalError: too many SQL variables
        if len(rhymes) > 1:
            return self.execute(f"SELECT word1, word2 FROM MarkovGrammar WHERE word2 IN ({', '.join(['?' for _ in rhymes])}) AND word3 = '<END>';", values=(tuple(rhymes)), fetch=True)
        else:
            return self.execute(f"SELECT word1, word2 FROM MarkovGrammar WHERE word2 = ? AND word3 = '<END>';", values=(list(rhymes)[0], ), fetch=True)
    
    def get_previous_double(self, word2, word3):
        return self.execute(f"SELECT word1 FROM MarkovGrammar WHERE word2 = ? AND word3 = ?;", values=(word2, word3), fetch=True)
    
    def get_previous_single(self, word3):
        return self.execute(f"SELECT word2 FROM MarkovGrammar WHERE word3 = ?;", values=(word3), fetch=True)
    
    def in_start(self, word1, word2):
        # Checks if word1 and word2 are the start of a sentence
        return len(self.execute(f"SELECT occurances FROM MarkovStart WHERE word1 = ? AND word2 = ?;", values=(word1, word2,), fetch=True)) > 0