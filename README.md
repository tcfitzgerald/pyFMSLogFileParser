# pyFMSLogFileParser

Parses Access.log file from FileMaker Server.

# Notes
FileMaker Server Log parsing regex

date: r"\d{4}-\d{2}-\d{2}"

r"opening database"

2014-12-07 08:00:07.335 -0600	Information	98	filemakerserver.host	Client "user (computer-001) [123.45.67.89]" closing database "finance" as "user1".

database and user: r"database \"[a-zA-z0-9_\- ]{0,}\" as \"[a-zA-z0-9_\-@ ]{0,}\""

a bit more comprehensive on the db name...: r"database \"[a-zA-z0-9!@#$%^&()+=:'.,\[\]\{\}_\- ]{0,}\" as \"[a-zA-z0-9_\-@ ]{0,}\""


2014-12-07 08:10:00.026 -0600	Information	638	filemakerserver.host	Client "user" opening a connection from "computer-001 (123.45.67.89)" using "ProAdvanced 13.0v4 [fmapp]".

Client: r"using \"[a-zA-z0-9.\[\]\{\}_\- ]{0,}\""



2014-12-07 08:10:00.026 -0600	Information	638	filemakerserver.host	Client "user" opening a connection from "computer-001 (123.45.67.89)" using "ProAdvanced 13.0v4 [fmapp]".

2014-12-07 08:00:07.335 -0600	Information	98	filemakerserver.host	Client "user (computer-001 [123.45.67.89]" closing database "finance" as "user1".



r"opening a connection from"
