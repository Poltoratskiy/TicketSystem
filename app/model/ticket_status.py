# -*- coding: utf-8 -*-

from app_init import db
import datetime
import json
from sqlalchemy import Enum

statuses = ('открыт', 'отвечен', 'закрыт', 'ожидает ответа')

status_enum = Enum(*statuses, name="status")


class TicketStatus(db.Model):
    __tablename__ = "ticket_status"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(status_enum)
    ticket = db.relationship('Ticket')

    def __repr__(self):
        return str({"id": str(self.id), "name": self.name})

    def json(self):
        """
        JSONify object
        :return:
        """
        return {
            "id": self.id,
            "name": self.name
        }
