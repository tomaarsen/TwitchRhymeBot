
import sqlite3, logging, random
logger = logging.getLogger(__name__)

class Database:
    def __init__(self, channel):
        self.db_name = f"MarkovChain_{channel.replace('#', '').lower()}.db"

        sql = """
        CREATE TABLE IF NOT EXISTS MarkovGrammar (
            input1 TEXT,
            input2 TEXT,
            output1 TEXT,
            count INTEGER,
            PRIMARY KEY (input1, input2, output1)
        )
        """
        self.create_db(sql)
    
    def create_db(self, sql):
        logger.debug("Creating Database...")
        self.execute(sql)
        logger.debug("Database created.")

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
            return self.execute(f"SELECT input1, input2, output1 FROM MarkovGrammar WHERE output1 IN {tuple(rhymes)};", fetch=True)
        else:
            return self.execute(f"SELECT input1, input2, output1 FROM MarkovGrammar WHERE output1 = ?;", values=(list(rhymes)[0], ), fetch=True)
    
    def get_previous_double(self, input2, output1):
        return self.execute(f"SELECT input1 FROM MarkovGrammar WHERE input2 = ? AND output1 = ?;", values=(input2, output1), fetch=True)
    
    def get_previous_single(self, output1):
        return self.execute(f"SELECT input1 FROM MarkovGrammar WHERE output1 = ?;", values=(output1), fetch=True)