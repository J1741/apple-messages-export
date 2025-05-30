#!/usr/bin/env python3

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
# TODO: add joins to other tables
sql_query = "SELECT * FROM message"


def main():

    # connect to database
    print(f"Connecting to {CHATDB_FILE} ..")
    conn = sqlite3.connect(CHATDB_FILE)

    # return results as Row objects
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    # select message info
    for row in cur.execute(sql_query):

        # TODO: write row data export file
        print(row['ROWID'])

    conn.close()


if __name__ == "__main__":
    main()
