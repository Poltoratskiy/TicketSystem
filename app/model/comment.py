import json

from app_init import db
import datetime
from app.model.ticket import Ticket


class Comment(db.Model):
    __tablename__ = "comment"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    registered_on = db.Column(db.TIMESTAMP, nullable=False, default=datetime.datetime.utcnow)
    text = db.Column(db.String(200))
    email = db.Column(db.String(255), nullable=False)
    ticket_id = db.Column(db.Integer, db.ForeignKey(Ticket.id))
    ticket = db.relationship('Ticket', foreign_keys='Comment.ticket_id')

    def json(self):
        """
        JSONify object
        :return:
        """
        return json.dumps({
            "id": self.id,
            "registered_on": str(self.registered_on),
            "text": self.text,
            "email": self.email
        })
