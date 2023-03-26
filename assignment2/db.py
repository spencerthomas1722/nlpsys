import os
import sys, sqlite3
import spacy


SQL_CREATE = "CREATE TABLE entities (id INT PRIMARY KEY, entity TEXT, label TEXT, start_token INT, end_token INT, start_char INT, end_char INT, sent TEXT)"
# start token INT, end token INT, start char INT, end char INT,
SQL_SELECT = "SELECT * FROM entities"
SQL_INSERT = "INSERT INTO entities VALUES (?, ?, ?, ?, ?, ?, ?, ?)"


class DatabaseConnection(object):
    def __init__(self, filename):
        self.path = os.path.join(os.getcwd(), filename)
        self.connection = sqlite3.connect(filename, check_same_thread=False)
        self.create_schema()

    def create_schema(self):
        try:
            self.connection.execute(SQL_CREATE)
        except sqlite3.OperationalError:
            print("Warning: table 'entities' was already created; ignoring.")

    def get(self, query=None):
        # get all entities with the same name
        if query is not None:
            cursor = (self.connection.execute(f'{SQL_SELECT} WHERE entity="{query}"'))
            # pattern = query + '%'
            # cursor = (self.connection.execute(f'{ SQL_SELECT } WHERE entity LIKE "{ pattern }"')
        # or get all entities (when no query)
        else:
            cursor = self.connection.execute(SQL_SELECT)
        fetched = cursor.fetchall()
        return fetched

    def add(self, ent, ent_label, start_token, end_token, start_char, end_char, sent):
        ent_id = hash((ent, start_char, ent_label, sent))  # including the start index so each instance within a sentence has a unique hash
        try:  # put ent in database
            # text, label, start token, end token, start char, end char, sent
            self.connection.execute(SQL_INSERT, (ent_id, ent, ent_label, start_token, end_token, start_char, end_char, sent))
            # self.connection.execute(SQL_INSERT, (ent_id, ent, ent_label, start_char, end_char, sent))
            self.connection.commit()
        except sqlite3.IntegrityError:
            print(f'Warning: sentence with ID { ent_id } is already in the database; ignoring...')
            self.connection.rollback()


if __name__ == '__main__':
    dbname = sys.argv[1] if len(sys.argv) > 1 else 'entities'
    connection = DatabaseConnection(f'{ dbname }.sqlite')
    connection.create_schema()

    nlp = spacy.load('en_core_web_lg')
    text = 'Andrew Hussie is best known as the creator of the webcomic Homestuck.'
    doc = nlp(text)
    # get entity
    for ent in doc.ents:
        # connection.add(ent.text, ent.label_, ent.start, ent.end, ent.start_char, ent.end_char, text)  # add to history
        connection.add(ent.text, ent.label_, text)  # add to history
    # connection.add('jane', 'paella')
    # connection.add('john', 'wonton')
    print(connection.get())
