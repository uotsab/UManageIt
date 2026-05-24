import datetime

emptydate = datetime.datetime(
    day=1,
    month=1,
    year=1
)

class struct_task:
    done: bool = False
    title: str = "task"
    assigndate: datetime = emptydate
    donedate: datetime = emptydate