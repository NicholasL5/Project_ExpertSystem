import tkinter as tk

import pandas as pd
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import customtkinter

global premise_table
FILE_PATH = None
no_solution_flag = False
SOLUTION_VAR = 'BidMethodology'
memory_table = dict()
rule_q = list()
reason_variable = dict()
attribute_q_table = []
FONT = ('Times New Roman', 15)
q_label_list = []
memory_label_list = []
global newWindow
newWindow = None

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    def convert_au_to_list(value):
        if value == "au":
            return ["a", "u"]
        else:
            return value


    def convert_clause_number(value):
        return tuple(value.split(sep=","))


    def checkIntermediary(rule):
        df_ans = set(premise_table["Result"])
        if rule in df_ans:
            return True
        else:
            return False


    def on_button_click(button_id):
        print(f"Button {button_id} Clicked!")
        root.user_clicked.set(button_id)


    def openNewWindow():
        global newWindow
        # Toplevel object which will
        # be treated as a new window
        newWindow = Toplevel(root)

        # sets the title of the
        # Toplevel widget
        newWindow.title("New Window")

        # sets the geometry of toplevel
        newWindow.geometry("200x200")

    def why():
        if rule_q[-1] is not None:
            if newWindow is not None:
                newWindow.destroy()
            openNewWindow()
            Label(newWindow, text=f"the question asked because rule: {rule_q[-1]}").pack()

    def how():
        if newWindow is not None:
            newWindow.destroy()
        openNewWindow()
        df = pd.read_excel(FILE_PATH, sheet_name='ask')
        variables = df['Variable'].tolist()
        variables2 = premise_table['Result'].tolist()

        variables2 = list(set(variables2))
        variables.extend(variables2)

        def button_click(answer):
            for j in range(len(btn_lists)):
                btn_lists[j].destroy()

            Label(newWindow, text=answer).pack()
            root.another_var.set(answer)

        btn_lists = []
        for i in variables:
            var_btn = Button(newWindow, text=i,
                             command=lambda choosen=i: button_click(choosen))
            btn_lists.append(var_btn)
            var_btn.pack()

        root.wait_variable(root.another_var)
        my_var = root.another_var.get().strip()

        root.another_var = tk.StringVar()

        if my_var in memory_table and not checkIntermediary(my_var):
            Label(newWindow, text=f"{my_var} : {memory_table[my_var]}").pack()
            Label(newWindow, text=f"reason: you said so").pack()
        elif my_var in memory_table and checkIntermediary(my_var):
            Label(newWindow, text=f"{my_var} : {memory_table[my_var]}, comes from rule {reason_variable[my_var]}").pack()
        else:
            Label(newWindow, text="no value in that variable").pack()


    def ask(rule, rule_num):
        global q_label_list
        global no_solution_flag
        global memory_label_list
        if rule_num not in rule_q:
            rule_q.append(rule_num)
        if rule not in memory_table:
            if not checkIntermediary(rule):
                button_list = []
                # print(premise_table)
                df = pd.read_excel(FILE_PATH, sheet_name='ask')

                row_index = df[df['Variable'] == str(rule)].index[0]
                question = df.iloc[row_index]['Question']
                index_temp_1 = question.rfind("(")
                index_temp_2 = question.rfind(")")
                possible_ans = question[index_temp_1+1:index_temp_2]
                possible_ans = possible_ans.split(',')
                print(possible_ans)

                qa_frame = ttk.Frame(frame_top)
                qa_frame.pack(side=tk.TOP, anchor=tk.W)  # Anchor to the left

                # Create and pack the question sub-frame to the left
                question_frame = ttk.Frame(qa_frame)
                question_frame.pack(side=tk.LEFT)

                question_label = tk.Label(question_frame, text=question)
                question_label.pack(side=tk.TOP)

                # Create and pack the answer sub-frame to the right
                answer_frame = ttk.Frame(qa_frame)
                answer_frame.pack(side=tk.LEFT)

                answer_label = tk.Label(answer_frame, text="Answer: ")
                answer_label.pack(side=tk.TOP)

                def button_click(answer):
                    for j in range(len(possible_ans)):
                        button_list[j].destroy()

                    Label(answer_frame, text=answer).pack(side=tk.LEFT)
                    memory_table[str(df.iloc[row_index]['Variable'])] = answer
                    root.user_clicked.set(answer)

                for i in range(len(possible_ans)):
                    choice_button = Button(answer_frame, text=possible_ans[i],
                                           command=lambda ans=possible_ans[i]: button_click(ans))
                    button_list.append(choice_button)
                    choice_button.pack(side=tk.LEFT, padx=5)

                root.wait_variable(root.user_clicked)
                ans = root.user_clicked.get().strip()
                print(ans)

                memory_table[str(df.iloc[row_index]['Variable'])] = ans
                mem_label = Label(frame_bottom_r, text=f"{str(df.iloc[row_index]['Variable'])} = {ans}", bg=frame_bottom_r.cget('fg_color'))
                memory_label_list.append(mem_label)
                mem_label.pack()
                q_label = Label(frame_bottom_l, text=f"{str(df.iloc[row_index]['Variable'])}", bg=frame_bottom_l.cget('fg_color'))
                q_label_list.append(q_label)
                q_label.pack()

                update_status()
                update_false()

                check_all_tu()

                update_status()
                update_false()

                check_all_tu()

            else:
                result_premise_table = premise_table.loc[premise_table['Result'].apply(lambda x: rule in x)]
                result_premise_table = result_premise_table[~result_premise_table['Rule Status'].apply(lambda x: 'd' in x)]
                if result_premise_table.empty:
                    no_solution_flag = True
                    return
                most_frequent_rule_number = result_premise_table['Rule Number'].value_counts().idxmax()
                filtered_rows = premise_table[(premise_table['Rule Number'] == most_frequent_rule_number)]
                for index, row in filtered_rows.iterrows():
                    ask(row['Premise Clause Number'][0], row['Rule Number'])
                    if no_solution_flag:
                        return
                    if SOLUTION_VAR in memory_table:
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
        if res == SOLUTION_VAR:
            reason_variable[res] = rule_num
            memory_table[SOLUTION_VAR] = ans

        else:
            reason_variable[res] = rule_num
            memory_table[res] = ans




    def check_all_tu():
        rule_numbers = premise_table['Rule Number'].unique()

        for rule_number in rule_numbers:

            all_tu = True
            rows_with_rule_number = premise_table[premise_table['Rule Number'] == rule_number]
            if not (rows_with_rule_number['status'] == 'TU').all():
                all_tu = False
            else:
                print(rule_number)
                check_solution(rule_number)


    def update_memory_and_q_ui():
        for i in memory_label_list:
            i.destroy()

        for i in q_label_list:
            i.destroy()

        for var in memory_table:
            mem_label = Label(frame_bottom_r, text=f"{var} = {memory_table[var]}",
                              bg=frame_bottom_r.cget('fg_color'))
            memory_label_list.append(mem_label)
            mem_label.pack()
            q_label = Label(frame_bottom_l, text=f"{var}",
                            bg=frame_bottom_l.cget('fg_color'))
            q_label.pack()
            q_label_list.append(q_label)


    def main():
        global premise_table
        premise_table = pd.read_excel(FILE_PATH, sheet_name='Sheet1')
        # ubah rule status dan premise clause number jadi list
        premise_table["Rule Status"] = premise_table["Rule Status"].apply(convert_au_to_list)
        premise_table["Premise Clause Number"] = premise_table["Premise Clause Number"].apply(convert_clause_number)
        # print(premise_table)
        while SOLUTION_VAR not in memory_table and 'free' in premise_table['status'].values:
            for index, row in premise_table.iterrows():
                # ambil row sekarang
                current_row = premise_table.iloc[index]

                if current_row['status'] == 'free' and all(premise_table[
                                                               (premise_table['Rule Number'] == current_row['Rule Number']) & (
                                                                       premise_table.index < index)]['status'] == 'TU'):

                    print(index)
                    ask(current_row['Premise Clause Number'][0], current_row['Rule Number'])
                    if no_solution_flag:
                        memory_table[SOLUTION_VAR] = "."
                        break
                    else:
                        update_memory_and_q_ui()
                    # print(memory_table)
                    # print(premise_table)
                    break
        if SOLUTION_VAR not in memory_table:
            memory_table[SOLUTION_VAR] = "."




    def get_file_name():
        global FILE_PATH
        file = filedialog.askopenfilename(
            initialdir="D:\\projects\\pythonProjects",
            title="Select A File",
            filetypes=(("xlsx files", "*.xlsx"), ("all files", "*.*"))
        )

        if file:
            FILE_PATH = file
            # print(FILE_PATH)
            # extension = get_file_extension(FILE_PATH)
            # if extension == "KBS" or extension == "kbs":
            #     KBS_TO_XLSX(FILE_PATH)
            # FILE_PATH = "/ASP/output.xlsx"
            file_label.config(text=f"file path: {FILE_PATH}")

    def center_window(tk, w_input, h_input):
        # get screen width and height
        ws = tk.winfo_screenwidth()  # width of the screen
        hs = tk.winfo_screenheight()  # height of the screen

        # calculate x and y coordinates for the Tk root window
        x_input = (ws / 2) - (w_input / 2)
        y_input = (hs / 2) - (h_input / 2) - 50

        # set the dimensions of the screen
        # and where it is placed
        return w_input, h_input, x_input, y_input

    def start_process():

        if FILE_PATH is not None:
            start_btn.configure(state='disable')
            main()
            Label(frame_top, text=f"final answer: {memory_table[SOLUTION_VAR]}").pack(side=tk.LEFT)
        else:
            print("Please select a file first.")

    def make_font(size):
        return tuple(['Times New Roman', size])

    if __name__ == "__main__":
        root = Tk()

        root.user_clicked = tk.StringVar()

        root.another_var = tk.StringVar()

        # frame_top = Frame(root, bg="lightblue")

        label_file_path = Label(root, text="Insert excel file:", font=FONT)
        label_file_path.pack()

        w, h, x, y = center_window(root, 700, 800)
        root.geometry('%dx%d+%d+%d' % (w, h, x, y))

        Button(root, text="Select Files", command=get_file_name, width=20, borderwidth=3).pack()

        file_label = Label(root, text="file path:", font=make_font(12))
        file_label.pack(pady=5)
        start_btn = Button(root, text="Start Processing", command=start_process)
        start_btn.pack()

        Button(root, text="How", command=how).pack()
        Button(root, text="Why", command=why).pack()

        frame_top = customtkinter.CTkScrollableFrame(root, fg_color='lightblue', height=400)
        frame_bottom = Frame(root, width=700, height=200, bg='lightgreen')

        frame_top.pack(fill="both", expand=True)
        frame_bottom.pack(fill="both", expand=True)

        title_frame_l = Frame(frame_bottom, width=350, height=40, bg='lightgreen')
        title_frame_r = Frame(frame_bottom, width=350, height=40, bg='lightyellow')
        title_frame_l.pack(side=tk.LEFT, padx=0, pady=0, fill='both')
        title_frame_r.pack(side=tk.RIGHT, padx=0, pady=0, fill='both')

        Label(title_frame_l, text='attribute queue table', bg=title_frame_l.cget('bg')).pack(side='top')
        Label(title_frame_r, text='memory table', bg=title_frame_r.cget('bg')).pack(side='top')

        frame_bottom_l = customtkinter.CTkScrollableFrame(title_frame_l, fg_color=title_frame_l.cget('bg'), width=350, height=300, corner_radius=0)
        frame_bottom_r = customtkinter.CTkScrollableFrame(title_frame_r, fg_color=title_frame_r.cget('bg'), width=350, height=300, corner_radius=0)
        frame_bottom_l.pack(padx=0, pady=0, fill='both', expand=True)
        frame_bottom_r.pack(padx=0, pady=0, fill='both', expand=True)

        root.mainloop()

