import os
import sys, sqlite3
import spacy


SQL_CREATE = "CREATE TABLE entities (id INT PRIMARY KEY, entity TEXT, ent_label TEXT, count INT)"
SQL_SELECT = "SELECT * FROM entities"
SQL_INSERT = "INSERT INTO entities VALUES (?, ?, ?, ?)"


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

    def add(self, ent, ent_label):
        ent_id = hash((ent, ent_label))  # create a hash so the same string with different labels will get stored separately
        cursor = (self.connection.execute(f'{ SQL_SELECT } WHERE id="{ ent_id }"'))
        item = cursor.fetchone()
        # print(f'item={ item }, type = { type(item) }')
        if item is not None:
            self.connection.execute(f'UPDATE entities SET count = count + 1 WHERE id="{ ent_id }"')
            self.connection.commit()
        else:
            self.connection.execute(SQL_INSERT, (ent_id, ent, ent_label, 1))
            self.connection.commit()


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
