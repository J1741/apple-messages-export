#!/usr/bin/env python3

import os
from dotenv import load_dotenv

load_dotenv()

# get chat.db and message export locations
CHATDB_FILE = os.getenv("CHATDB_FILE")
EXPORT_DIR = os.getenv("EXPORT_DIR")


def main():

    print(CHATDB_FILE)
    print(EXPORT_DIR)


if __name__ == "__main__":
    main()
