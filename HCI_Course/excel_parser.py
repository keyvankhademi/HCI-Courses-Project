import json

import pandas

excel_file = pandas.ExcelFile("course_list.xlsx")
print(excel_file.sheet_names)

data = []


def import_sheet(sheet):
    df = pandas.read_excel(excel_file, sheet)

    print(df.items())


for sheet in excel_file.sheet_names:
    if sheet != 'top20':
        import_sheet(sheet)

f = open("data.json", "w")
f.write(json.dumps(data))
f.close()
