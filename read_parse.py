import ast
from datetime import datetime, timedelta, date
import csv


with open("data.txt", "r") as ins:
    """Opens data file, which is poorly formatted version of JSON data"""
    data = []
    for line in ins:
        this_line = ast.literal_eval(line)
        # Individual lines are Dict items, this converts the string format of the text file to a useable Dict

        date = datetime.strptime(this_line["submission_datetime"].split(".")[0], "%Y-%m-%dT%H:%M:%S") - timedelta(hours=7)
        # UTC date in the file has some unnecssary data and is in the wrong timezome, this shifts the time, removes unnecessary data and converts to datetime
        if date.isocalendar()[1] - 28 == 0:
            # Were looking at data for a specific set of weeks, if the data is before that it's ignored
            continue
        else:
            r_ID = this_line["submission_id"]
            status = this_line["status"]
            week_number = date.isocalendar()[1] - 28
            date = datetime.strftime(date, "%Y-%m-%d")
            data = {"ID": r_ID, "status": status, "date": date, "week_number": week_number}
            data.append(data)

file_name = "data_" + str(date.today()) + ".csv"

with open(file_name, mode='w') as csv_file:
    fieldnames = ['ID', 'status', 'date', 'week_number']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    for item in data:
        writer.writerow(item)
