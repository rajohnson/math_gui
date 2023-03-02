from typing import List
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import random
import numpy

"""
This module implements a Leitner box based spaced repetition system
for memorizing simple arithmetic facts. Several boxes exist that 
roughly correspond to the difficulty of the problem. Each time that
the problem is seen it is moved to a new box, the next higher if it
was correctly answered or the next lower box if it was incorrect.

Each time that a new set of problems is selected the oldest problem 
from each box is selected first. Which box to use if selected using
a gaussian that is trimmed to fit the desired number of bins and 
then truncated into integers. 

https://en.wikipedia.org/wiki/Leitner_system
"""

DB_PATH = "db/"
DB_NAME = "problems.sqlite"

DEFAULT_BIN = 0  # 0 is new/bad
MAX_BIN = 25
MIN_BIN = 0
distribution_mean = MIN_BIN + (MAX_BIN - MIN_BIN) // 2
distribution_st_dev = MIN_BIN + (MAX_BIN - MIN_BIN) / 3.75


def random_bin():
    result = numpy.random.normal(distribution_mean, distribution_st_dev)
    while not (MIN_BIN <= result <= MAX_BIN):
        result = numpy.random.normal(distribution_mean, distribution_st_dev)
    return int(result)


create_problem_db = False

if not os.path.isfile(f"{DB_PATH}/{DB_NAME}"):
    os.makedirs(DB_PATH, exist_ok=True)
    create_problem_db = True
engine = create_engine(f"sqlite:///{DB_PATH}/{DB_NAME}", echo=True)
base = declarative_base()


class Problem(base):
    __tablename__ = "problems"

    key = Column(Integer, primary_key=True)
    problem = Column(String)
    answer = Column(String)
    operator = Column(String)
    bin = Column(Integer)
    last_seen = Column(DateTime)
    times_seen = Column(Integer)
    times_correct = Column(Integer)

    def __repr__(self):
        return f"<Problem(key={self.key}, problem={self.problem}, answer={self.answer}, operator={self.operator}, bin={self.bin}, last_seen={self.last_seen}, times_seen={self.times_seen}, times_correct={self.times_correct}>"


base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


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


def create_problems():
    session = Session()
    session.add_all(
        [
            Problem(
                problem=_get_problem_text(x, y, operator),
                answer=_get_answer(x, y, operator),
                operator=operator,
                bin=DEFAULT_BIN,
                times_seen=0,
                times_correct=0,
                last_seen=datetime.now(),
            )
            for operator in "+-*/"
            for x in range(0, 13)
            for y in range(0, 13)
            if _use_problem(x, y, operator)
        ]
    )
    session.commit()


if create_problem_db:
    print("iniitializing DB")
    create_problems()


def select_problems(
    num_problems: int, allowed_operators: str, repeat_n_times: int = 1
) -> List[int]:
    session = Session()
    selected = []
    bins = [
        [
            problem.key
            for problem in session.query(Problem)
            .filter(Problem.operator.in_([op for op in allowed_operators]))
            .filter(Problem.bin == bin_num)
            .order_by(Problem.last_seen.desc())
            .limit(num_problems)
            .all()
        ]
        for bin_num in range(MIN_BIN, MAX_BIN + 1)
    ]

    while len(selected) < num_problems:
        bin_index = random_bin()
        if len(bins[bin_index]) > 0:
            selected.append(bins[bin_index].pop(0))

    selected *= repeat_n_times
    random.shuffle(selected)

    return selected


def update_problem(key: int, correct: bool) -> None:
    session = Session()
    problem = session.query(Problem).filter(Problem.key == key).one()
    problem.times_seen += 1
    problem.last_seen = datetime.now()
    if correct:
        problem.bin = min(problem.bin + 1, MAX_BIN)
        problem.times_correct += 1
    else:
        problem.bin = max(problem.bin - 1, MIN_BIN)
    session.commit()


def check_answer(key: int, attempt: str) -> bool:
    session = Session()
    problem = session.query(Problem).filter(Problem.key == key).one()
    return problem.answer == attempt


def problem_text(key: int) -> str:
    session = Session()
    problem = session.query(Problem).filter(Problem.key == key).one()
    return problem.problem


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    nums = [random_bin() for _ in range(100000)]
    plt.hist(nums, bins=MAX_BIN - MIN_BIN)
    plt.show()
