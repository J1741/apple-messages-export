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

# TODO: select only needed data
# TODO: add joins to other tables
# TODO: move query into separate file
sql_query = "SELECT * FROM message"


def main():

    # connect to database
    print(f"Connecting to {CHATDB_FILE} ..")
    conn = sqlite3.connect(CHATDB_FILE)

    # return results as Row objects (rather than tuples)
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    # set up file for message export
    with open(EXPORT_FILE, 'w') as tsv_file:
        tsv_writer = csv.writer(tsv_file,
                                delimiter='\t',
                                quoting=csv.QUOTE_NONE,
                                escapechar='\\',
                                lineterminator='\n')

        # select message info
        print("Exporting message data ..")
        for row in cur.execute(sql_query):

            id = row['ROWID']
            date = row['date']

            # render message content without newlines, but with emojis
            content = repr(row['text'])[1:-1]

            # TODO: write additional data to export file
            data = [id, date, content]
            tsv_writer.writerow(data)

        print(f"Exported messages to {EXPORT_FILE}")

    conn.close()


if __name__ == "__main__":
    main()
