import random
import collections
from typing import List

Problem = collections.namedtuple("Problem", "problem answer operator")


def _get_problem_text(x, y, operator):
    if operator == "+":
        return f"{x} + {y}"
    elif operator == "-":
        return f"{x} - {y}"
    elif operator == "*":
        return f"{x} × {y}"
    elif operator == "/":  # problem is x*y / x
        return f"{x*y} ÷ {x}"
    else:
        raise ValueError


def _get_answer(x, y, operator):
    if operator == "+":
        return f"{x+y}"
    elif operator == "-":
        return f"{x-y}"
    elif operator == "*":
        return f"{x*y}"
    elif operator == "/":  # problem is x*y / x
        return f"{y}"
    else:
        raise ValueError


def _use_problem(x, y, operator) -> bool:
    if operator == "+":
        return True
    elif operator == "-":  # problem is x - y, don't want negative answers
        return x >= y
    elif operator == "*":
        return True
    elif operator == "/":  # problem is x*y / x
        return x != 0
    else:
        raise ValueError


problems = [
    Problem(_get_problem_text(x, y, operator), _get_answer(x, y, operator), operator)
    for operator in "+-*/"
    for x in range(0, 13)
    for y in range(0, 13)
    if _use_problem(x, y, operator)
]


def select_problems(num_problems: int, allowed_operators: str) -> List[int]:

    allowed_problem_keys = [
        key
        for key, problem in enumerate(problems)
        if problem.operator in allowed_operators
    ]
    return random.sample(allowed_problem_keys, num_problems)


def update_problem(key: int, correct: bool) -> None:
    ...  # todo - will assign to the appropriate bin and update the last seen timestamp


def check_answer(key: int, attempt: str) -> bool:
    return problems[key].answer == attempt


def problem_text(key: int) -> str:
    return problems[key].problem
