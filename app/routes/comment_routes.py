from flask import current_app as app
from app.model.ticket import Ticket, db
from app.model.comment import Comment
import json
from flask import request


@app.route('/comments', methods=['POST'])
def create_comment():
    """
    статус “закрыт” финальный (нельзя) изменить статус или добавить комментарий)
    :return:
    """
    data = json.loads(request.data)
    ticket_id = data.get('ticket_id')
    text = str(data.get('text'))
    email = str(data.get('email'))
    if not data or ticket_id is None or email is None or text is None:
        response = app.response_class(status=400,
                                      mimetype='application/json')
        return response
    try:
        ticket = Ticket.query.filter_by(id=ticket_id).first()
        if ticket is None:
            response = app.response_class(status=400,
                                          mimetype='application/json')
            return response
        if ticket.status.name == 'закрыт':
            response = app.response_class(status=403,
                                          mimetype='application/json')
            return response
        comment = Comment(text=text, email=email, ticket_id=ticket_id)
        db.session.add(comment)
        db.session.commit()
        response = app.response_class(response=comment.json(),
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
