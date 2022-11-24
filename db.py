from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker

# Problem = collections.namedtuple("Problem", "problem answer operator")

DB_PATH = "db/"
DB_NAME = "problems.sqlite3"

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

    def __repr__(self):
        return f"<Problem(key={self.key}, problem={self.problem}, answer={self.answer}, operator={self.operator}, bin={self.bin}, last_seen={self.last_seen})>"


base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
# session = Session()

# session.add(
#     Problem(operator="+", bin=0, last_seen=datetime.now(), problem="2 + 2", answer="4")
# )
# session.add(
#     Problem(operator="-", bin=0, last_seen=datetime.now(), problem="2 - 2", answer="4")
# )
