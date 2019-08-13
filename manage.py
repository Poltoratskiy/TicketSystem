import os
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy import exc
from flask_script import Manager
from psycopg2 import errors
from app_init import create_app, db
from app.model import *

app = create_app(os.getenv('ENV') or 'dev')

with app.app_context():
    from app.routes import *

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def run():
    app.run()


@manager.command
def add_dicts():
    status = []
    try:
        for i, s in enumerate(['opened', 'answered', 'closed', 'waiting']):
            status.append(ticket_status.TicketStatus(id=i + 1, name=s))
        print(status)
        db.session.add_all(status)
        db.session.commit()
    except (exc.IntegrityError, exc.SQLAlchemyError, exc.DBAPIError) as e:
        print(e)


if __name__ == '__main__':
    db.create_all()
    add_dicts()
    app.run()
