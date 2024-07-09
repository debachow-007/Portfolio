from flask import render_template, send_file, url_for, flash, redirect, request
from portfolio import app, data, mail
from flask_mail import Message  # type: ignore
from portfolio.forms import ContactForm
from portfolio.utils import calculate_age, send_email
import datetime
import os

@app.route('/')
@app.route('/home')
def home():
    home_text = data['home_text']
    roles = data['home_roles']
    return render_template('home.html', roles=roles, home_text=home_text)

@app.route('/resume')
def resume():
    pdf_path = os.path.join(app.root_path, 'static/pdf/debargha_cv.pdf')
    return send_file(pdf_path, as_attachment=True)

@app.route('/about')
def about():
    about_data = data['about_data']
    about_text = data['about_text']
    age = calculate_age()
    return render_template('about.html', title='About', about_data=about_data, about_text=about_text, age=age)

@app.route('/experience')
def experience():
    experiences = data['experiences']
    return render_template('experience.html', title='Experience', experiences=experiences)

@app.route('/education')
def education():
    educations = data['educations']
    return render_template('education.html', title='Education', educations=educations)

@app.route('/projects')
def projects():
    projects = data['projects']
    return render_template('projects.html', title='Projects', projects=projects)

@app.route('/hobbies')
def hobbies():
    hobbies = data['hobbies']
    return render_template('hobbies.html', title='Hobbies', hobbies=hobbies)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    
    if form.validate_on_submit():
        print("Form validated")
        visitor = {'name': form.name.data, 'email': form.email.data, 'message': form.message.data}
        
        try:
            send_email(visitor)
            flash('Message sent successfully!', 'success')
            return redirect(url_for('contact'))
        
        except:
            flash('Message could not be sent.', 'danger')
            return redirect(url_for('contact'))
        
    return render_template('contact.html', title='Contact', form=form)

