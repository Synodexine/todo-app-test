from forms.main import MainForm
from database import db
from config import PROVIDER, DB_FILE_NAME


if __name__ == '__main__':
    db.bind(provider=PROVIDER, filename=DB_FILE_NAME, create_db=True)
    db.generate_mapping(create_tables=True)
    app = MainForm()
    app.mainloop()
