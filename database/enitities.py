from datetime import datetime

from pony.orm import Required

from database import db


class Task(db.Entity):
    text = Required(str, unique=True)
    creation_date = Required(datetime, default=datetime.utcnow)
