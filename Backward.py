import pandas as pd

premise_table = pd.read_excel("output.xlsx", sheet_name='Sheet1')
global memory_table
memory_table = {

}
global rule_q
rule_q = list()
rule_q_back = list()
reason_variable = dict()
goal = dict()


attribute_q_table = []


with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    def convert_au_to_list(value):
        if value == "au":
            return ["a", "u"]
        else:
            return value


    def convert_clause_number(value):
        return tuple(value.split(sep=","))

    # ubah rule status dan premise clause number jadi list
    premise_table["Rule Status"] = premise_table["Rule Status"].apply(convert_au_to_list)
    premise_table["Premise Clause Number"] = premise_table["Premise Clause Number"].apply(convert_clause_number)


    def checkIntermediary(rule):
        df_ans = set(premise_table["Result"])
        if rule in df_ans:
            return True
        else:
            return False


    def why():
        pass

    def ask(rule, rule_num):
        if rule_num not in rule_q:
            rule_q.append(rule_num)
        if rule not in memory_table:
            if not checkIntermediary(rule):
                print(premise_table)
                df = pd.read_excel("testing_Copy.xlsx", sheet_name='ask')

                row_index = df[df['Variable'] == str(rule)].index[0]
                question = df.iloc[row_index]['Question']

                ans = str(input(question)).strip()
                while ans == 'why' or ans == 'how':
                    if ans == 'why':
                        print("the question asked because rule: ", end="")
                        print(rule_q[-1])
                    elif ans == 'how':
                        variables = df['Variable'].tolist()
                        variables2 = premise_table['Result'].tolist()

                        variables2 = list(set(variables2))
                        variables.extend(variables2)

                        for i in variables:
                            print(i, end=" ")

                        print()
                        ask2 = input("variable apa yang mau anda tanya?:")
                        if ask2 in variables:
                            if ask2 in memory_table and not checkIntermediary(ask2):
                                print(f"{ask2} : {memory_table[ask2]}")
                                print("reason: you said so")
                            elif ask2 in memory_table and checkIntermediary(ask2):
                                print(f"variable {ask2} : {memory_table[ask2]} comes from rule {reason_variable[ask2]}")
                            else:
                                print("no value in that variable")

                    ans = input(question)

                memory_table[str(df.iloc[row_index]['Variable'])] = ans

                update_status()
                update_false()

                check_all_tu()

                update_status()
                update_false()

                check_all_tu()

            else:
                result_premise_table = premise_table.loc[premise_table['Result'].apply(lambda x: rule in x)]
                most_frequent_rule_number = result_premise_table['Rule Number'].value_counts().idxmax()
                filtered_rows = premise_table[premise_table['Rule Number'] == most_frequent_rule_number]
                for index, row in filtered_rows.iterrows():
                    ask(row['Premise Clause Number'][0], row['Rule Number'])
                    if 'Solution' in memory_table:
                        return


    def check_ans(rule, premise):
        if memory_table[rule] == premise:
            return True
        else:
            return False


    def update_false():
        rule_num_fix = []
        for index, row in premise_table.iterrows():
            if row['Premise Clause Number'][0] in memory_table and not row['Rule Status'][len(row['Rule Status']) - 1] == 'd':
                # kalau jawaban salah
                if not row['Premise Clause Number'][1] == (memory_table[row['Premise Clause Number'][0]]):
                    premise_table.at[index, 'Rule Status'].append('d')
                    rule_num_fix.append(row['Rule Number'])

        for index, row in premise_table.iterrows():
            if not rule_num_fix == [] and row['Rule Number'] in rule_num_fix and not row['Rule Status'][len(row['Rule Status']) - 1] == 'd':
                premise_table.at[index, 'Rule Status'].append('d')
                if premise_table.at[index, 'status'] == 'free':
                    premise_table.at[index, 'status'] = 'FA'


    def update_status():
        for index, row in premise_table.iterrows():
            if row['Premise Clause Number'][0] in memory_table:
                if premise_table.at[index, 'status'] == 'free':
                    if not row['Premise Clause Number'][1] == (memory_table[row['Premise Clause Number'][0]]):
                        premise_table.at[index, 'status'] = 'FA'
                    else:
                        premise_table.at[index, 'status'] = 'TU'

    # kalau rule di data diganti rule disini harus diganti
    def check_solution(rule_num):
        df = premise_table[premise_table['Rule Number'] == rule_num]
        res = df.iloc[0]['Result']
        ans = df.iloc[0]['Ans']
        if ans == 'Solution':
            reason_variable[res] = rule_num
            memory_table['Solution'] = ans
        else:
            reason_variable[res] = rule_num
            memory_table[res] = ans

        attribute_q_table.append("")

    def backward(variable):
        if not checkIntermediary(variable):
            df = pd.read_excel("testing_Copy.xlsx", sheet_name='ask')

            row_index = df[df['Variable'] == str(variable)].index[0]
            question = df.iloc[row_index]['Question']

            ans = input(question)
            while ans == 'why' or ans == 'how':
                if ans == 'why':
                    print("the question asked because rule: ", end="")
                    print(rule_q[-1])
                elif ans == 'how':
                    variables = df['Variable'].tolist()
                    variables2 = premise_table['Result'].tolist()

                    variables2 = list(set(variables2))
                    variables.extend(variables2)

                    for i in variables:
                        print(i, end=" ")

                    print()
                    ask2 = input("variable apa yang mau anda tanya?:")
                    if ask2 in variables:
                        if ask2 in memory_table and not checkIntermediary(ask2):
                            print(f"{ask2} : {memory_table[ask2]}")
                            print("reason: you said so")
                        elif ask2 in memory_table and checkIntermediary(ask2):
                            print(f"variable {ask2} : {memory_table[ask2]} comes from rule {reason_variable[ask2]}")
                        else:
                            print("no value in that variable")

                ans = input(question)
            memory_table[str(df.iloc[row_index]['Variable'])] = ans

            update_status()
            update_false()

            check_all_tu()

            update_status()
            update_false()

            check_all_tu()
        else:
            df2 = premise_table[premise_table['Result'] == variable]
            # cari yang rule numbernya terlalu banyak
            most_frequent_rule_number = df2['Rule Number'].value_counts().idxmax()
            filtered_rows = premise_table[premise_table['Rule Number'] == most_frequent_rule_number]
            for index, row in filtered_rows.iterrows():
                backward(row['Premise Clause Number'][0])
                if 'Solution' in memory_table:
                    return


    def check_all_tu():
        rule_numbers = premise_table['Rule Number'].unique()

        for rule_number in rule_numbers:

            all_tu = True
            rows_with_rule_number = premise_table[premise_table['Rule Number'] == rule_number]
            if not (rows_with_rule_number['status'] == 'TU').all():
                all_tu = False
            else:
                # print(rule_number)
                check_solution(rule_number)



    # main program
    counter = 0
    evaluate_rule_number = 0
    previous_evaluated_rule_number = 0
    # set goal
    goal_df = premise_table[premise_table['Result'] == 'Solution']
    print(goal_df)
    for index, row in goal_df.iterrows():
        variable = row['Premise Clause Number'][0]
        backward(variable)
        if 'Solution' in memory_table:
            break

    print(memory_table['Solution'])

