from app_init import db
import datetime
from app.model.ticket_status import TicketStatus
import json


class Ticket(db.Model):
    __tablename__ = "ticket"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    registered_on = db.Column(db.TIMESTAMP, nullable=False, default=datetime.datetime.utcnow)
    changed_on = db.Column(db.TIMESTAMP, nullable=False, default=datetime.datetime.utcnow)
    text = db.Column(db.String(200))
    theme = db.Column(db.String(50))
    email = db.Column(db.String(255), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey(TicketStatus.id))
    status = db.relationship('TicketStatus', foreign_keys='Ticket.status_id')
    comments = db.relationship('Comment', back_populates="ticket", lazy=True)

    def __init__(self, theme, email, text=''):
        self.email = email
        self.text = text
        self.theme = theme
        self.status_id = 1

    def __repr__(self):
        return str({"id": str(self.id), "text": self.text, "theme": self.theme})

    def json(self):
        """
        JSONify object
        :return:
        """
        return json.dumps(
            {
                "id": self.id,
                "registered_on": str(self.registered_on),
                "changed_on": str(self.changed_on),
                "text": self.text,
                "theme": self.theme,
                "email": self.email,
                "status": TicketStatus.query.filter_by(id=self.status_id).first().json(),
                "comments": [json.loads(c.json()) for c in self.comments]
            })

    def change_status_check(self, new_status_id):
        """
        Тикет создается в статусе “открыт”, может перейти в “отвечен” или “закрыт”, из отвечен в “ожидает ответа” или
        TODO(? - как из "отвечен" в "ожидает ответа"). На что может поменяться “ожидает ответа”
        “закрыт”, статус “закрыт” финальный (нельзя изменить статус или добавить комментарий)

        :param new_status_id:
        :return:
        """
        new_status = TicketStatus.query.filter_by(id=new_status_id).first()
        if self.status.name == "открыт" and new_status.name in ["отвечен", "закрыт"]:
            return True
        elif self.status.name == "отвечен" and new_status.name in ["ожидает ответа", "закрыт"]:
            return True
        return False
