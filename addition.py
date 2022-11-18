import random
import tkinter

NUM_PROBLEMS = 50

problems = [(x, y) for x in range(1, 11) for y in range(1, 11)]
selected_problems = random.sample(problems, NUM_PROBLEMS)
incorrect = []
correct = []


root = tkinter.Tk()

remaining = tkinter.Label(root, text=f"{len(selected_problems)} problems left")
remaining.pack()

correct_count = tkinter.Label(root, text=f"Correct: {len(correct)}")
correct_count.pack()

incorrect_count = tkinter.Label(root, text=f"Incorrect: {len(incorrect)}")
incorrect_count.pack()

result = tkinter.Label(root, text=" ")
result.pack()

problem = tkinter.Label(
    root, text=f"{selected_problems[0][0]} + {selected_problems[0][1]}"
)
problem.pack()

entry_window = tkinter.Entry(root)
entry_window.pack()

submit_button = tkinter.Button(root, text="Submit")
submit_button.pack()

tkinter.mainloop()
