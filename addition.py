import random
import tkinter

problems = [(x, y) for x in range(1, 11) for y in range(1,11)]
selected_problems = random.sample(problems, 50)
incorrect = []


