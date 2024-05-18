from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from . import db, login_manager, create_app
from .models import User, Student, Attendance
from .forms import LoginForm, RegisterForm
from .face_recognition import capture_face, recognize_faces
from .camera import capture_image, save_image
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
import pandas as pd

app = create_app()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            image = capture_image()
            face_encoding = capture_face(image)
            if face_encoding is not None:
                new_student = Student(name=form.name.data, roll_no=form.roll_no.data, branch=form.branch.data, face_encoding=face_encoding)
                db.session.add(new_student)
                db.session.commit()

                image_filename = f"app/static/images/{form.roll_no.data}.jpg"
                save_image(image, image_filename)

                flash('Student Registered Successfully!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('No face detected. Please try again.', 'danger')
        except Exception as e:
            flash(str(e), 'danger')
    return render_template('register.html', form=form)

@app.route('/take_attendance', methods=['GET', 'POST'])
@login_required
def take_attendance():
    if request.method == 'POST':
        try:
            image = capture_image()
            recognized_students = recognize_faces(image)
            for student in recognized_students:
                new_attendance = Attendance(student_id=student.id, date=date.today(), present=True)
                db.session.add(new_attendance)
            db.session.commit()
            flash('Attendance Taken Successfully!', 'success')
        except Exception as e:
            flash(str(e), 'danger')
        return redirect(url_for('dashboard'))
    return render_template('take_attendance.html')

@app.route('/display_attendance')
@login_required
def display_attendance():
    students = Student.query.all()
    attendance_data = []
    for student in students:
        total_days = Attendance.query.filter_by(student_id=student.id).count()
        present_days = Attendance.query.filter_by(student_id=student.id, present=True).count()
        attendance_data.append({
            'name': student.name,
            'roll_no': student.roll_no,
            'branch': student.branch,
            'total_days': total_days,
            'present_days': present_days,
            'attendance_percentage': (present_days / total_days) * 100 if total_days else 0
        })
    return render_template('display_attendance.html', attendance_data=attendance_data)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')
