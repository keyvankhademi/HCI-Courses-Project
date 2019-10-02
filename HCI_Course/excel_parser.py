import json

import pandas

excel_file = pandas.ExcelFile("C:\\Users\\ricksonre\\Documents\\GitHub\\HCI-Courses-Project\\HCI_Course\\course_list.xlsx")
print(excel_file.sheet_names)

data = []

#verifies if the cell has a value
def has_value(cell):
    return cell is not None and cell != "" and cell == cell
        
def import_sheet(sheet):
    df = pandas.read_excel(excel_file, sheet)


    name = df.columns[1]
    description = df.iloc[0][1]
    core_for_major = (df.iloc[2][1] == 'Yes')
    last_taught = df.iloc[3][1]
    instructor = df.iloc[4][1]
    url = df.iloc[5][1]

    criteria = []

    headers_index = []
    #find indexes
    for i in range(7,50):
        try:
            if(df.iloc[i][0] == "Learning outcomes/goals:"):
                headers_index.append(i)
            if(df.iloc[i][0] == "List of topics covered from most recent course offering:"):
                headers_index.append(i)
        except IndexError:
            continue

    for i in range(7,headers_index[0]):
        try:
            Cname, weight = df.iloc[i][1], df.iloc[i][2]
        except IndexError:
            continue
        if has_value(Cname):
            criteria.append({
                "name": Cname,
                "weight": weight,
            })

    learning_goal = ""

    for i in range(headers_index[0], headers_index[1]):
        try:
            if has_value(df.iloc[i][1]):
                learning_goal += df.iloc[i][1]
        except IndexError:
            continue

    topics = []

    for i in range(headers_index[1], 40):
        try:
            week, title = df.iloc[i][1], df.iloc[i][2]
        except IndexError:
           continue

        if week is None:  week = ""
        
        if has_value(title):
        #if week is not None and week != "" and week == week:
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
