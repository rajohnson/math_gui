# import random
# import collections
from typing import List
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker

# Problem = collections.namedtuple("Problem", "problem answer operator")

DB_PATH = "db/"
DB_NAME = "problems.sqlite3"

DB_PATH = "db/"
DB_NAME = "problems.sqlite3"

DEFAULT_BIN = 0  # 0 is new/bad

# engine = sqlalchemy.create_engine(f"sqlite:///{DB_PATH}/{DB_NAME}", echo=True)
engine = create_engine("sqlite:///:memory:", echo=True)
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
            )
            for operator in "+-*/"
            for x in range(0, 13)
            for y in range(0, 13)
            if _use_problem(x, y, operator)
        ]
    )
    session.commit()


if not os.path.isfile(f"{DB_PATH}/{DB_NAME}"):
    print("iniitializing DB")
    create_problems()


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
