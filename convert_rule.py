import pandas as pd
import re
import os
import xlsxwriter


filepath = "D:\\VPX\\UAS.KBS"

def get_file_extension(file_path):
    _, file_extension = os.path.splitext(file_path)
    return file_extension



extension = get_file_extension(filepath)
print(extension)

with open(filepath, 'r') as file:
    text = file.read()

# print(text)

# Define a regular expression pattern to match rules
rule_pattern = re.compile(r'RULE (\d+)\s+IF(.+?)THEN\s+(.+?);', re.DOTALL)

# Find all matches of the pattern in the content
matches = rule_pattern.findall(text)

rules_data = {
    'Rule Number': [],
    'Rule Status': [],
    'Premise Clause Number': [],
    'Result': [],
    'Ans': [],
    'status': [],
}

# Extract and print the rules
for match in matches:
    rule_number = match[0].strip()
    conditions = match[1].strip()
    actions = match[2].strip()

    match = re.match(r'(\w+)\s*=\s*(\w+)', actions)
    condition_list = re.findall(r'\w+\s*=\s*.+?(?=\s+and|\s+or|\s*;|$)', conditions)

    for condition in condition_list:
        match2 = re.match(r'(\w+)\s*=\s*(\w+)', condition)

        rules_data['Rule Number'].append(rule_number)
        rules_data['Rule Status'].append('au')
        rules_data['Premise Clause Number'].append(f"{match2.group(1)},{match2.group(2)}")
        rules_data['Result'].append(match.group(1))
        rules_data['Ans'].append(match.group(2))
        rules_data['status'].append('free')

df2 = pd.DataFrame(rules_data)
df2['Rule Number'] = pd.to_numeric(df2['Rule Number'], errors='coerce')

# Use ExcelWriter to create a multi-sheet Excel file
with pd.ExcelWriter("output.xlsx", engine='xlsxwriter') as writer:
    df2.to_excel(writer, sheet_name="Sheet1", index=False)

    ask_lines = [line.strip() for line in text.split("\n") if
                 line.strip().startswith("ASK") or line.strip().startswith("CHOICES")]

    data = {
        "Question": [],
        "Variable": []
    }

    for i in range(0, len(ask_lines), 2):
        ask = ask_lines[i].split(":")
        choices = ask_lines[i + 1].split(":")

        variable = ask[0].split(" ")[1]
        q_index = ask[1].index('"')
        q_index_2 = ask[1].index('?', q_index + 1)
        question = f"{ask[1][q_index + 1:q_index_2 + 1]}({choices[1].strip().replace(';', '')})"
        data['Question'].append(question)
        data['Variable'].append(variable)

    df_ask = pd.DataFrame(data)
    df_ask.to_excel(writer, sheet_name="ask", index=False)



