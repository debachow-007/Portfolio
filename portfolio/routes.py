from flask import render_template, send_file, url_for, flash, redirect, request, session, jsonify # type: ignore
from portfolio import app, data
from portfolio.forms import ContactForm
from portfolio.utils import calculate_age, send_email
from portfolio.chatbot_utils import ask_gemini, get_relevant_context
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
        visitor = {'name': form.name.data, 'email': form.email.data, 'message': form.message.data}

        try:
            send_email(visitor)
            flash('Message sent successfully!', 'success')
            return redirect(url_for('contact'))

        except Exception as e:
            flash('Message could not be sent.', 'danger')
            return redirect(url_for('contact'))

    return render_template('contact.html', title='Contact', form=form)

@app.route("/start_chat", methods=["POST"])
def start_chat():
    try:
        data = request.get_json(force=True)
        print("Received data:", data)

        if not data or "name" not in data or "email" not in data:
            return {"error": "Invalid data"}, 400

        session["chat_name"] = data.get("name")
        session["chat_email"] = data.get("email")
        session["chat_history"] = []

        return {"message": "Chat session started"}, 200
    except Exception as e:
        return {"error": str(e)}, 400


@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "")
    history = session.get("chat_history", "")
    context = get_relevant_context(user_msg)
    reply = ask_gemini(user_msg, history, context)

    history += f"\nUser: {user_msg}\nBot: {reply}"
    session["chat_history"] = history
    return jsonify({"response": reply})


@app.route('/reset', methods=['POST'])
def reset_chat():
    session.pop("chat_history", None)
    return jsonify({"message": "Chat reset."})