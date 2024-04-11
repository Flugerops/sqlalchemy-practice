from datetime import datetime
from sqlalchemy import create_engine, String, select, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, sessionmaker


engine = create_engine("sqlite:///my.sql", echo=True)


class Base(DeclarativeBase):
    pass


#OUR MODELS
class Event(Base):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    start_time: Mapped[datetime]
    end_time: Mapped[datetime]
    status: Mapped[bool]
    def __repr__(self) -> str:
        return f"<Event(id: {self.id}, name: '{self.name}', start_date: {self.start_date}, end_date: {self.end_date}, status: {self.status})>"

# ~ OUR MODELS
Base.metadata.create_all(engine)

Session = sessionmaker(engine)

# id = int(input("Id>> "))
# name = str(input("Name>> "))
# start_time = datetime.strptime(input("Enter start time>> "), "%Y-%m-%d %H:%M:%S")
# end_time = datetime.strptime(input("Enter end  time>> "), "%Y-%m-%d %H:%M:%S")
# status = input("Enter status ready or not>> ")
# if status == "ready":
#     status = True
# else:
#     status = False

filter_start = datetime.strptime(input("Enter filter start time>> "), "%Y-%m-%d %H:%M:%S")
filter_end = datetime.strptime(input("Enter filter end time>> "), "%Y-%m-%d %H:%M:%S")


with Session.begin() as session:
    # event = Event(id=id, name=name, start_time=start_time, end_time=end_time, status=status)
    # session.add(event)
    events = session.scalars(select(Event).where(Event.start_time >= filter_start).where(Event.end_time <= filter_end)).all()
    finished = 0
    total_events = len(events)
    for i in events:
        if i.status == True:
            finished += 1
    winrate = (finished / total_events) * 100 if total_events > 0 else 0
    print(f"Total events: {total_events}, Finished: {finished}, Winrate: {winrate}")
        
    