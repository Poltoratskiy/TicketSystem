# -*- coding: utf-8 -*-

from app_init import db
import enum


class TicketStatusEnum(enum.Enum):
    opened = enum.auto()
    answered = enum.auto()
    closed = enum.auto()
    waiting = enum.auto()

    def __str__(self):
        return self.string


class TicketStatus(db.Model):
    __tablename__ = "ticket_status"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Enum(TicketStatusEnum))
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
            "name": TicketStatusEnum(self.id).name
        }

