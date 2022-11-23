import problems
import tkinter

NUM_PROBLEMS = 10

selected_problems = problems.select_problems(NUM_PROBLEMS)
incorrect = []
correct = []


def handle_submit():
    attempt = entry_window.get()
    entry_window.delete(0, tkinter.END)
    problem = selected_problems.pop()
    if problems.check_answer(problem.key, attempt):
        result["text"] = "Correct!"
        correct.append(problem)
        problems.update_problem(problem.key, True)
    else:
        result["text"] = "Wrong!"
        incorrect.append(problem)
        problems.update_problem(problem.key, False)
    remaining["text"] = f"{len(selected_problems)} problems left"
    correct_count["text"] = f"Correct: {len(correct)}"
    incorrect_count["text"] = f"Incorrect: {len(incorrect)}"
    if len(selected_problems) > 0:
        problem_label["text"] = selected_problems[-1].problem
    else:
        problem_label["text"] = f"All done"
        print("\n".join([problem.problem for problem in incorrect]))
        root.quit()


root = tkinter.Tk()

remaining = tkinter.Label(root, text=f"{len(selected_problems)} problems left")
remaining.pack()

correct_count = tkinter.Label(root, text=f"Correct: {len(correct)}")
correct_count.pack()

incorrect_count = tkinter.Label(root, text=f"Incorrect: {len(incorrect)}")
incorrect_count.pack()

result = tkinter.Label(root, text=" ")
result.pack()

problem_label = tkinter.Label(root, text=selected_problems[-1].problem)
problem_label.pack()

entry_window = tkinter.Entry(root)  # todo - bind enter to submit
entry_window.pack()

submit_button = tkinter.Button(root, text="Submit", command=handle_submit)
submit_button.pack()

tkinter.mainloop()
