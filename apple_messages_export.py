#!/usr/bin/env python3

import csv
import os
import os.path
import sqlite3
import time
from dotenv import load_dotenv

load_dotenv()

ts = time.localtime()
EXPORT_TIME = time.strftime('%Y%m%d_%H%M%S', ts)

# get input and output files and locations
CHATDB_FILE = os.getenv("CHATDB_FILE")
EXPORT_DIR = os.getenv("EXPORT_DIR")
EXPORT_FILE = os.path.join(EXPORT_DIR,
                           "apple_messages_export_" + EXPORT_TIME + ".tsv")

# TODO: move queries into separate files
sql_query_1 = "SELECT DISTINCT chat_identifier FROM chat"

sql_query_2 = """SELECT
    c.chat_identifier,
    group_concat(h.id) AS chat_members
FROM chat c
    JOIN chat_handle_join ch ON c.ROWID=ch.chat_id
    JOIN handle h ON ch.handle_id=h.ROWID
WHERE c.chat_identifier = ?
"""

sql_query_3 = """SELECT
    m.ROWID AS message_id,
    datetime(m.date + strftime('%s', '2001-01-01'), 'unixepoch', 'localtime') AS date,
    m.text AS text,
    CASE WHEN m.is_from_me=1 THEN 'me' ELSE coalesce(nullif(h.id, ''), 'none') END AS 'sender',
    CASE WHEN m.is_from_me=0 THEN 'me' ELSE coalesce(nullif(h.id, ''), 'none') END AS 'recipient',
    coalesce(nullif(c.chat_identifier, ''), 'none') as chat_identifier
FROM message m
    LEFT JOIN handle h ON m.handle_id=h.ROWID
    LEFT JOIN chat_message_join cm on m.ROWID=cm.message_id
    LEFT JOIN chat c ON cm.chat_id=c.ROWID
"""

def main():

    print(f"Connecting to {CHATDB_FILE} ..")

    # connect to database and return results as Row objects (rather than tuples)
    conn = sqlite3.connect(CHATDB_FILE)
    conn.row_factory = sqlite3.Row

    # get list of chat identifiers
    cursor1 = conn.cursor()

    res1 = cursor1.execute(sql_query_1)
    res1_list = res1.fetchall()

    # pull chat identifiers out of tuples
    chat_identifiers = [item['chat_identifier'] for item in res1_list]

    # get mapping of chat identifiers to members
    cursor2 = conn.cursor()
    chat_dict = {}

    for chat_identifier in chat_identifiers:
        for res2_row in cursor2.execute(sql_query_2, (chat_identifier,)):
            chat_dict[res2_row['chat_identifier']] = res2_row['chat_members']

    cursor3 = conn.cursor()

    # set up file for message export
    with open(EXPORT_FILE, 'w') as tsv_file:
        tsv_writer = csv.writer(tsv_file,
                                delimiter='\t',
                                quoting=csv.QUOTE_NONE,
                                escapechar='\\',
                                lineterminator='\n')

        fieldnames = ["message_id", "date", "sender", "recipient", "text",
                      "chat_identifier", "chat_members"]

        # add header
        tsv_writer.writerow(fieldnames)

        # select message info
        print("Exporting message data ..")

        export_counter = 0

        for res3_row in cursor3.execute(sql_query_3):

            message_id = res3_row['message_id']
            date = res3_row['date']
            sender = res3_row['sender']
            recipient = res3_row['recipient']

            # render message text without newlines or extra quotes, but keep emojis
            text = repr(res3_row['text'])[1:-1]

            chat_identifier = res3_row['chat_identifier']

            # add chat members to export file
            if chat_identifier == "none":
                chat_members = "NA"
            else:
                chat_members = chat_dict[chat_identifier]

            export_data = [message_id, date, sender, recipient, text,
                    chat_identifier, chat_members]

            # output data
            tsv_writer.writerow(export_data)
            export_counter += 1

        print(f"Success! Exported {export_counter} messages to: {EXPORT_FILE}")

    conn.close()


if __name__ == "__main__":
    main()
