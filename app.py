from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

from sqlalchemy.orm import selectin_polymorphic

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Session(db.Model):
    __tablename__ = 'Session'

    id = db.Column(db.String, primary_key=True, nullable=False)

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return f"<Session {self.id}>"


class Reminder(db.Model):
    __tablename__ = 'Reminder'

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String, nullable=False)
    name = db.Column(db.String)
    details = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    occurrences = db.relationship('Occurrence', backref='Reminder', lazy=True)

    def __init__(self, name, details, session_id):
        self.name = name
        self.details = details
        self.session_id = session_id

    def __repr__(self):
        return f"<Reminder {self.name}>"


class Occurrence(db.Model):
    __tablename__ = 'Occurrence'

    id = db.Column(db.Integer, primary_key=True)
    reminder_id = db.Column(db.Integer, db.ForeignKey('Reminder.id'), nullable=False)
    datetime = db.Column(db.DateTime)

    def __init__(self, reminder_id, datetime):
        self.reminder_id = reminder_id
        self.datetime = datetime

    def __repr__(self):
        return f"<Reminder {self.name}>"


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/session', methods=['POST', 'GET'])
def create_new_session():
    session_id = uuid.uuid4().hex
    new_session = Session(session_id)
    
    db.session.add(new_session)
    db.session.commit()
    
    return redirect(f'/{session_id}')


@app.route('/<session_id>', methods=['POST', 'GET'])
def reminders(session_id):
    if request.method == 'POST':
        # request must be sent do OCR API
        # algorithm to decide occurrence datetimes
        reminder_name = request.form['name']
        reminder_details = request.form['details']
        new_reminder = Reminder(reminder_name, reminder_details, session_id)

        db.session.add(new_reminder)
        db.session.commit()
        return redirect(f'/{session_id}')

    else:
        reminders = Reminder.query.filter(Reminder.session_id == session_id).order_by(Reminder.date_created).all()
        return render_template('reminder.html', reminders=reminders, session_id=session_id)


@app.route('/<session_id>/delete/<id>')
def delete(session_id, id):
    reminder_to_delete = Reminder.query.get_or_404(id)

    db.session.delete(reminder_to_delete)
    db.session.commit()

    return redirect(f'/{session_id}')


@app.route('/<session_id>/edit/<id>', methods=['POST', 'GET'])
def edit(session_id, id):
    reminder = Reminder.query.get_or_404(id)
    if request.method == 'POST':
        reminder.name = request.form['name']

        db.session.commit()
        return redirect(f'/{session_id}')
        
    else:
        return render_template('edit.html', reminder=reminder, session_id=session_id)


if __name__ == "__main__":
    app.run(debug=True)
