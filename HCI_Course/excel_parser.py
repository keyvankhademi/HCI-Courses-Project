import json

import pandas

excel_file = pandas.ExcelFile("course_list.xlsx")
print(excel_file.sheet_names)

data = []


def import_sheet(sheet):
    df = pandas.read_excel(excel_file, sheet)

    name = df.columns[1]
    description = df.iloc[0][1]
    core_for_major = (df.iloc[2][1] == 'Yes')
    last_taught = df.iloc[3][1]
    instructor = df.iloc[4][1]
    url = df.iloc[5][1]

    criteria = []

    for i in range(7,13):
        try:
            Cname, weight = df.iloc[i][1], df.iloc[i][2]
        except:
            continue
        if Cname is not None and Cname != "" and Cname == Cname:
            criteria.append({
                "name": Cname,
                "weight": weight,
            })

    learning_goal = ""

    for i in range(14, 19):
        try:
            learning_goal += df.iloc[i][1]
        except:
            continue

    topics = []

    for i in range(20, 40):
        try:
            week, title = df.iloc[i][1], df.iloc[i][2]
        except:
            continue
        if week is not None and week != "" and week == week:
            topics.append({
                "week": week,
                "title": title,
            })

    data.append({
        "name": name,
        "description": description,
        "core_for_major": core_for_major,
        "last_taught": last_taught,
        "instructor": instructor,
        "url": url,
        "criteria": criteria,
        "learning_goals": learning_goal,
        "topics": topics,
    })


for sheet in excel_file.sheet_names:
    if sheet != 'top20':
        import_sheet(sheet)

f = open("data.json", "w")
f.write(json.dumps(data))
f.close()
