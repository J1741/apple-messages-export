#!/usr/bin/env python3

import csv
import os
import os.path
import sqlite3
from dotenv import load_dotenv

load_dotenv()

# get input and output files and locations
CHATDB_FILE = os.getenv("CHATDB_FILE")
EXPORT_DIR = os.getenv("EXPORT_DIR")
EXPORT_FILE = os.path.join(EXPORT_DIR, "messages_export.tsv")

# TODO: move query into separate file
sql_query = """SELECT
    m.ROWID AS message_id,
    datetime(m.date + strftime('%s', '2001-01-01'), 'unixepoch', 'localtime') AS date,
    m.text as text,
    CASE WHEN m.is_from_me=1 THEN 'me' ELSE h.id END AS 'sender'
FROM message m
LEFT JOIN handle h ON m.handle_id=h.ROWID
WHERE
    m.ROWID=42226"""

# TODO: add query to get chat members

def main():

    # connect to database
    print(f"Connecting to {CHATDB_FILE} ..")
    conn = sqlite3.connect(CHATDB_FILE)

    # return results as Row objects (rather than tuples)
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    # TODO: add cursor to get chat members
    # TODO: store chat members as dictionary

    # set up file for message export
    with open(EXPORT_FILE, 'w') as tsv_file:
        tsv_writer = csv.writer(tsv_file,
                                delimiter='\t',
                                quoting=csv.QUOTE_NONE,
                                escapechar='\\',
                                lineterminator='\n')

        # add header
        fieldnames = ["message_id", "date", "sender", "text"]
        tsv_writer.writerow(fieldnames)

        # select message info
        print("Exporting message data ..")
        for row in cur.execute(sql_query):

            message_id = row['message_id']
            date = row['date']
            sender = row['sender']

            # render message content without newlines, but with emojis
            text = repr(row['text'])[1:-1]

            # TODO: add chat identifier to export file
            # TODO: add chat members to export file

            data = [message_id, date, sender, text]
            tsv_writer.writerow(data)

        print(f"Exported messages to {EXPORT_FILE}")

    conn.close()


if __name__ == "__main__":
    main()
