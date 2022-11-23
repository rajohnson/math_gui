import random
import tkinter

NUM_PROBLEMS = 50

problems = [(x, y) for x in range(1, 11) for y in range(1, 11)]
selected_problems = random.sample(problems, NUM_PROBLEMS)
incorrect = []
correct = []


def handle_submit():
    expected = str(sum(selected_problems[0]))
    provided = entry_window.get()
    entry_window.delete(0, tkinter.END)
    problem = selected_problems.pop(0)
    if expected == provided:
        result["text"] = "Correct!"
        correct.append(problem)
    else:
        result["text"] = "Wrong!"
        incorrect.append(problem)
    remaining["text"] = f"{len(selected_problems)} problems left"
    correct_count["text"] = f"Correct: {len(correct)}"
    incorrect_count["text"] = f"Incorrect: {len(incorrect)}"
    if len(selected_problems) > 0:
        problem_label["text"] = f"{selected_problems[0][0]} + {selected_problems[0][1]}"
    else:
        problem_label["text"] = f"All done"
        print("\n".join([f"{x} + {y}" for x, y in incorrect]))
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

problem_label = tkinter.Label(
    root, text=f"{selected_problems[0][0]} + {selected_problems[0][1]}"
)
problem_label.pack()

entry_window = tkinter.Entry(root)
entry_window.pack()

submit_button = tkinter.Button(root, text="Submit", command=handle_submit)
submit_button.pack()

tkinter.mainloop()
