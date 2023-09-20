from database.enitities import Task
from pony.orm import db_session, desc


@db_session
def get_tasks():
    return [task.text for task in Task.select().order_by(desc(Task.creation_date))]


@db_session
def create_task(text: str):
    if not Task.exists(text=text):
        new_task = Task(text=text)
        return new_task
    return False


@db_session
def remove_task(text: str):
    task = Task.get(text=text)
    if task:
        task.delete()
        return True
    return False


@db_session
def edit_task(text: str, new_text: str):
    task = Task.get(text=text)
    if task:
        task.text = new_text
        return True
    return False
