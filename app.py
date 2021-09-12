from flask import Flask, render_template, request, redirect, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid
from image_analysis import ocr_space_file, resize_image
from werkzeug.utils import secure_filename
import os
import json
from get_timenfreq import get_medinfo
from create_calendar import create_calendar

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


UPLOAD_FOLDER = 'static/uploads/'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
    calendar = db.Column(db.String)

    def __init__(self, name, details, calendar, session_id):
        self.name = name
        self.details = details
        self.calendar = calendar
        self.session_id = session_id

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

    query = Reminder.query.filter(Reminder.session_id == session_id).order_by(Reminder.date_created).all()
    calendars = [q.calendar for q in query]
    names = [q.name for q in query]
    details = [q.details for q in query]

    create_calendar(calendars, names, details)
    
    return redirect(f'/{session_id}')


@app.route('/<session_id>', methods=['POST', 'GET'])
def reminders(session_id):
    if request.method == 'POST':

        if 'file' not in request.files:
            flash('No file part')
            return redirect(f"/{session_id}")


        file = request.files['file']
        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(f"/{session_id}")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            resize_image(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            ocr = json.loads(ocr_space_file(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
            
            try:
                original = ocr['ParsedResults'][0]['ParsedText']
                text = original.split('\r\n')
                reminder_details = []
                for i in text:
                    i = i.split(' ')
                    for word in i:
                        reminder_details.append(word)

                nlp = get_medinfo(reminder_details)

                name = nlp.pop('Name')

                calendar = str(nlp)

                details = original

                reminder_name = name
                reminder_details = details
                new_reminder = Reminder(reminder_name, reminder_details, calendar, session_id)

                db.session.add(new_reminder)
                db.session.commit()

                query = Reminder.query.filter(Reminder.session_id == session_id).order_by(Reminder.date_created).all()
                calendars = [q.calendar for q in query]
                names = [q.name for q in query]
                details = [q.details for q in query]

                create_calendar(calendars, names, details)

                return redirect(f"/{session_id}")

            except:
                return redirect(f"/{session_id}/tryagain")

        else:
            flash('Allowed image types are -> png, jpg, jpeg, gif')
            return redirect(f"/{session_id}")


    else:
        reminders = Reminder.query.filter(Reminder.session_id == session_id).order_by(Reminder.date_created).all()
        return render_template('reminder.html', reminders=reminders, session_id=session_id)


@app.route('/<session_id>/add', methods=['POST', 'GET'])
def add(session_id):
    if request.method == 'POST':
        reminder_name = request.form['name']
        reminder_details = request.form['details']
        nlp = get_medinfo(reminder_details.split(' '))
        nlp.pop('Name')
        calendar = str(nlp)
        new_reminder = Reminder(reminder_name, reminder_details, calendar, session_id)

        db.session.add(new_reminder)
        db.session.commit()

        query = Reminder.query.filter(Reminder.session_id == session_id).order_by(Reminder.date_created).all()
        calendars = [q.calendar for q in query]
        names = [q.name for q in query]
        details = [q.details for q in query]

        create_calendar(calendars, names, details)

        return redirect(f"/{session_id}")
    
    else:
        return render_template('new.html', session_id=session_id)


@app.route('/<session_id>/delete/<id>')
def delete(session_id, id):
    reminder_to_delete = Reminder.query.get_or_404(id)

    # TODO delete instances of calendars

    db.session.delete(reminder_to_delete)
    db.session.commit()

    return redirect(f'/{session_id}')


@app.route('/<session_id>/edit/<id>', methods=['POST', 'GET'])
def edit(session_id, id):
    reminder = Reminder.query.get_or_404(id)
    if request.method == 'POST':
        reminder.name = request.form['name']
        reminder.details = request.form['details']
        nlp = get_medinfo(reminder.details.split(' '))
        nlp.pop('Name')
        reminder.calendar = str(nlp)

        db.session.commit()

        query = Reminder.query.filter(Reminder.session_id == session_id).order_by(Reminder.date_created).all()
        calendars = [q.calendar for q in query]
        names = [q.name for q in query]
        details = [q.details for q in query]

        create_calendar(calendars, names, details)

        return redirect(f'/{session_id}')
        
    else:
        return render_template('edit.html', reminder=reminder, session_id=session_id)


@app.route('/<session_id>/tryagain')
def tryagain(session_id):
    if request.method == 'POST':
        reminder_name = request.form['name']
        reminder_details = request.form['details']

        nlp = get_medinfo(reminder_details.split(' '))
        nlp.pop('Name')
        calendar = str(nlp)

        new_reminder = Reminder(reminder_name, reminder_details, calendar, session_id)

        reminder_details = reminder_details.split(' ')
        calendar = get_medinfo(reminder_details)

        db.session.add(new_reminder)
        db.session.commit()

        query = Reminder.query.filter(Reminder.session_id == session_id).order_by(Reminder.date_created).all()
        calendars = [q.calendar for q in query]
        names = [q.name for q in query]
        details = [q.details for q in query]

        create_calendar(calendars, names, details)

        return redirect(f"/{session_id}")
    
    else:
        return render_template('tryagain.html', session_id=session_id)


@app.route('/<session_id>/download')
def download(session_id):
    filename = str(os.path.join(app.config['UPLOAD_FOLDER']))+"example.ics"
    return send_file(filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
