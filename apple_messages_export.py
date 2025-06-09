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

# TODO: move queries into separate files
sql_query_1 = "SELECT DISTINCT chat_identifier from chat LIMIT 5"

sql_query_2 = """SELECT
    c.chat_identifier,
    group_concat(h.id) AS chat_members
FROM chat c
JOIN chat_handle_join ch on c.ROWID=ch.chat_id
JOIN handle h on ch.handle_id=h.ROWID
WHERE c.chat_identifier = ?
"""

sql_query_3 = """SELECT
    m.ROWID AS message_id,
    datetime(m.date + strftime('%s', '2001-01-01'), 'unixepoch', 'localtime') AS date,
    m.text as text,
    CASE WHEN m.is_from_me=1 THEN 'me' ELSE h.id END AS 'sender'
FROM message m
LEFT JOIN handle h ON m.handle_id=h.ROWID
WHERE
    m.ROWID=42226"""


def main():

    # connect to database
    print(f"Connecting to {CHATDB_FILE} ..")
    conn = sqlite3.connect(CHATDB_FILE)

    # return results as Row objects (rather than tuples)
    conn.row_factory = sqlite3.Row

    # get list of chat identifiers
    cursor1 = conn.cursor()

    res = cursor1.execute(sql_query_1)
    res_list = res.fetchall()

    chat_identifiers = [item['chat_identifier'] for item in res_list]
    print(chat_identifiers)

    # TODO: get dictionary of chat identifiers -- members
    cursor2 = conn.cursor()

    cursor3 = conn.cursor()

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
        for row in cursor3.execute(sql_query_3):

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
