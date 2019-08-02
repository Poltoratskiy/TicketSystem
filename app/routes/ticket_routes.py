from flask import current_app as app
from app.model.ticket_status import TicketStatus
from app.model.ticket import Ticket, db
from validate_email import validate_email
import ast
import json
from flask import jsonify, request


@app.route('/tickets/<int:id_>', methods=['GET'])
def get_tickets(id_):
    """
    get ticket by id
    :param id_: identifier of object
    :return:
    """
    ticket = Ticket.query.filter_by(id=id_).first()
    if ticket is None:
        response = app.response_class(status=404,
                                      mimetype='application/json')
        return response
    response = app.response_class(response=ticket.json(),
                                  status=200,
                                  mimetype='application/json')
    return response


@app.route('/tickets', methods=['POST'])
def create_ticket():
    """
    Create new ticket in database
    :return:
    """
    data = json.loads(request.data)
    theme = str(data.get('theme'))
    text = str(data.get('text'))
    email = str(data.get('email'))
    if not data or theme is None or email is None or not validate_email(email):
        response = app.response_class(status=400,
                                      mimetype='application/json')
        return response
    try:
        ticket = Ticket(theme=theme, text=text, email=email)
        db.session.add(ticket)
        db.session.commit()
        response = app.response_class(response=ticket.json(),
                                      status=200,
                                      mimetype='application/json')
        return response
    except Exception as e:
        db.session.rollback()
        response = app.response_class(status=501,
                                      mimetype='application/json')
        return response
    finally:
        db.session.close()


@app.route('/tickets', methods=['PATCH'])
def update_ticket():
    """
    Update status of ticket
        Тикет создается в статусе “открыт”, может перейти в “отвечен” или “закрыт”, из отвечен в “ожидает ответа” или
        TODO(? - как из "отвечен" в "ожидает ответа"). На что может поменяться “ожидает ответа”
        “закрыт”, статус “закрыт” финальный (нельзя изменить статус или добавить комментарий)

    :return:
    """
    data = json.loads(request.data)
    ticket_id = str(data.get('id'))
    status = data.get('status')
    status_id = status.get('id')
    if not data or ticket_id is None or status is None or status_id is None:
        response = app.response_class(status=400,
                                      mimetype='application/json')
        return response
    try:
        new_status = TicketStatus.query.filter_by(id=status_id).first()
        ticket = Ticket.query.filter_by(id=ticket_id).first()
        if new_status is None or ticket is None:
            response = app.response_class(status=400,
                                          mimetype='application/json')
            return response
        flag = ticket.change_status_check(new_status.id)
        if not flag:
            response = app.response_class(status=403,
                                          mimetype='application/json')
            return response
        ticket.status_id = new_status.id
        db.session.commit()
        response = app.response_class(response=ticket.json(),
                                      status=200,
                                      mimetype='application/json')
        return response
    except Exception as e:
        db.session.rollback()
        response = app.response_class(status=501,
                                      mimetype='application/json')
        return response
    finally:
        db.session.close()
