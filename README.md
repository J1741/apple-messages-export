# apple-messages-export

Simple text-only export for Apple Messages.

# Overview

Command-line Python application that exports the text of all a user's
Apple Messages, with basic metadata, to a tab-delimited text file (TSV).

The export file has the following columns:

| col # | column name | description | example value
|-------|-------------|-------------|--
| 1 | export_id   | unique numeric id of exported row | 12187
| 2 | message_id| numeric id of message | 12188
| 3 | date | message datetime | 2015-03-14 15:09:26
| 4 | sender| message sender | +12223334444
| 5 | recipient | message recipient | me
| 6 | text | message text content | Sounds good 👍
| 7 | chat_identifier | identifier for thread | chat123456789908765432
| 8 | chat_members | members of thread |+12223334444,+15556667777,+18889990000

# Installation

## Requirements
(to-be-added)

## Steps
(to-be-added)

# Usage
(to-be-added)
