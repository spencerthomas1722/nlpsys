import sys, sqlite3
import spacy

SQL_CREATE = "CREATE TABLE entities (id INT PRIMARY KEY, entity TEXT, sent TEXT, label TEXT)"
SQL_SELECT = "SELECT * FROM entities"
SQL_INSERT = "INSERT INTO entities VALUES (?, ?, ?, ?)"


class DatabaseConnection(object):
    def __init__(self, filename):
        self.connection = sqlite3.connect(filename, check_same_thread=False)
        self.create_schema()

    def create_schema(self):
        try:
            self.connection.execute(SQL_CREATE)
        except sqlite3.OperationalError:
            print("Warning: table 'entities' was already created; ignoring.")

    def get(self, query=None):
        # get all entities
        # or all entities with the same name
        cursor = (self.connection.execute(f'{ SQL_SELECT } WHERE entity="{ query }"')
                  if query is not None else self.connection.execute(SQL_SELECT))
        return cursor.fetchall()

    def add(self, ent, ent_start, ent_label, sent):
        ent_id = hash((ent, ent_start, ent_label, sent))  # including the start index so each instance has a unique hash
        try:  # put ent in database
            self.connection.execute(SQL_INSERT, (ent_id, ent, sent, ent_label))
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
        connection.add(ent.text, ent.start_char, ent.label_, text)  # add to history
    # connection.add('jane', 'paella')
    # connection.add('john', 'wonton')
    print(connection.get())
