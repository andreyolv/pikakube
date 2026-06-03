import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--instancia", help="Database name, has to be the same as config file", action='append', nargs='+')

args = parser.parse_args()

if args.database:
    for db_names in args.database:
        for db_name in db_names:
            print("Database:", db_name)
