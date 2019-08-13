from flask import current_app as app
import json
from flask import request, abort
from sqlalchemy import exc
import traceback

from app.model.ticket import Ticket, db
from app.model.comment import Comment


@app.route('/comments', methods=['POST'])
def create_comment():
    """
    статус “закрыт” финальный (нельзя) изменить статус или добавить комментарий)
    :return:
    """
    data = json.loads(request.data)
    ticket_id = data.get('ticket_id')
    text = data.get('text')
    email = data.get('email')
    if not data or ticket_id is None or email is None or text is None:
        abort(400)
    try:
        ticket = Ticket.query.filter_by(id=ticket_id).first()
        if ticket is None:
            abort(400)
        if ticket.status.name == 'closed':
            abort(403)
        comment = Comment(text=text, email=email, ticket_id=ticket_id)
        db.session.add(comment)
        db.session.commit()
        return app.response_class(response=comment.json(),
                                  status=200,
                                  mimetype='application/json')
        
    except exc.SQLAlchemyError:
        print(f'''Error: \n {traceback.format_exc()}''')
        db.session.rollback()
        abort(501)
    finally:
        db.session.close()
