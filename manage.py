import os
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from sqlalchemy.exc import IntegrityError
from app_init import create_app, db
from app.model import *

app = create_app(os.getenv('ENV') or 'dev')

with app.app_context():
    from app.routes import *

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)


# manager.add_command('db', MigrateCommand)


# @manager.command
def run():
    app.run()


# @manager.command
def add_dicts():
    try:
        for i, s in enumerate(["открыт", "отвечен", "закрыт", "ожидает ответа"]):
            status = ticket_status.TicketStatus(id=i + 1, name=s)
            db.session.add(status)
            db.session.commit()
    except Exception as e:
        pass


if __name__ == '__main__':
    db.create_all()
    add_dicts()
    app.run()
