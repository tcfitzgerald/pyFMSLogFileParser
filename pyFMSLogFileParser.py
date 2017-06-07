import argparse
import re
import csv

parser = argparse.ArgumentParser(description='Python script to parse results of Access.log file from FileMaker Server.')
parser.add_argument('input_file', metavar='input_file', type=str, help='Full path to file list you want to process.')
parser.add_argument('fmp_server', metavar='server', type=str, help='FileMaker server FQDN (e.g. filemaker.example.com)')
parser.add_argument('output_file', metavar='output_file', type=str, help='Name of file you want to render output to.')

args = parser.parse_args()

list_file = args.input_file
server = args.fmp_server
output_file = args.output_file

with open(list_file, 'r') as f:
    lines = f.readlines()

date_regex = r"\d{4}-\d{2}-\d{2}"
account_name_regex = r"\"[a-zA-z0-9_.\-@ ]{0,}\""
account_name_regex_end = r"\"[a-zA-z0-9_.\-@ ]{0,}\".$"
client_regex = r"\"[a-zA-z0-9.\[\]\{\}_\- ]{0,}\".$"
database_search_regex = r"database \"[a-zA-z0-9!@#$%^&()+=:'.,\[\]\{\}_\- ]{0,}\""
database_regex = r"\"[a-zA-z0-9!@#$%^&()+=:'.,\[\]\{\}_\- ]{0,}\""

is_client_line_regex = r"opening a connection from"
is_database_line_regex = r"opening database"

output_lines = []

for line in lines:
    client_line_matches = re.search(is_client_line_regex, line)
    database_line_matches = re.search(is_database_line_regex, line)

    if database_line_matches:
        # if "opening database" was found, line looks like this 2016-09-27 15:03:43.082 -0500
        # Information	94	FileMaker-Server	Client "username (ComputerName) [000.000.00.00]"
        #  opening database "the_database" as "username".
        # we want to extract date, account name and database name

        date = re.search(date_regex, line).group()
        database_search = re.search(database_search_regex, line).group()
        database = re.search(database_regex, database_search).group().lstrip('"').rstrip('"')

        account_name = re.search(account_name_regex_end, line, re.MULTILINE).group().lstrip('"').rstrip('".')

        newline = [server, date, account_name, database]
        output_lines.append(newline)

    # if client_line_matches:
    #     # if "opening a connection" was found, line looks like this 2014-12-07 08:10:00.026 -0600
    #     # Information	638	FileMaker-Server	Client "username" opening a connection from
    #     #  "ComputerName (000.000.00.00)" using "ProAdvanced 13.0v4 [fmapp]".
    #     # we want to extract the date, account name and client version info
    #
    #     date = re.search(date_regex, line).group()
    #     account_name = re.search(account_name_regex, line).group().lstrip('"').rstrip('"')
    #     client = re.search(client_regex, line, re.MULTILINE).group().lstrip('"').rstrip('".')
    #
    #     newline = [server, date, account_name, client]
    #     output_lines.append(newline)

    else:
        pass

with open(output_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(output_lines)
