import problem_set
import tkinter

NUM_PROBLEMS = 50  # todo - make menu to choose number of problems
OPERATORS = (
    "+"  # todo - add menu option to select operator types - allowable symbols: '+*-/'
)

selected_problems = problem_set.select_problems(NUM_PROBLEMS, OPERATORS)
incorrect = []
correct = []


def handle_submit():
    attempt = entry_window.get()
    if attempt == "":
        return
    entry_window.delete(0, tkinter.END)
    problem = selected_problems.pop()
    if problem_set.check_answer(problem, attempt):
        result["text"] = "Correct!"
        correct.append(problem)
        problem_set.update_problem(problem, True)
    else:
        result["text"] = "Wrong!"
        incorrect.append(problem)
        problem_set.update_problem(problem, False)
    remaining["text"] = f"{len(selected_problems)} problems left"
    correct_count["text"] = f"Correct: {len(correct)}"
    incorrect_count["text"] = f"Incorrect: {len(incorrect)}"
    if len(selected_problems) > 0:
        problem_label["text"] = problem_set.problem_text(selected_problems[-1])
    else:
        problem_label["text"] = f"All done"
        print("\n".join([problem_set.problem_text(id) for id in incorrect]))
        root.quit()


root = tkinter.Tk()
root.geometry("200x180")
root.title("Math")

remaining = tkinter.Label(root, text=f"{len(selected_problems)} problems left")
remaining.pack(pady=(10, 0))

correct_count = tkinter.Label(root, text=f"Correct: {len(correct)}")
correct_count.pack()

incorrect_count = tkinter.Label(root, text=f"Incorrect: {len(incorrect)}")
incorrect_count.pack()

result = tkinter.Label(root, text=" ")
result.pack()

problem_label = tkinter.Label(
    root, text=problem_set.problem_text(selected_problems[-1])
)
problem_label.pack()

entry_window = tkinter.Entry(root)
entry_window.bind("<Return>", (lambda _: handle_submit()))
entry_window.pack(padx=10)

submit_button = tkinter.Button(root, text="Submit", command=handle_submit)
submit_button.pack(pady=10)

tkinter.mainloop()
