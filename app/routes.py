from flask import render_template, flash, redirect, url_for, request, session, copy_current_request_context
from app import app, db
from app.forms import LoginForm, RegistrationForm, PostForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post
from app.chatbot import get_stock
from werkzeug.urls import url_parse
from flask_socketio import SocketIO, emit, disconnect

async_mode = None
socketio = SocketIO(app, async_mode=async_mode)


@app.route('/')
def main():
    return redirect(url_for('index'))


@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    posts = Post.query.order_by(Post.timestamp.asc()).all()
    last_fifty_posts = posts[-50:]
    if request.method == 'POST':
        post = Post(body=request.form['broadcast_data'], author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        form = PostForm()
        if form.validate_on_submit():
            post = Post(body=form.post.data, author=current_user)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template("index.html", title='Home Page', form=form,
                           posts=last_fifty_posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, your registration was successful!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@socketio.event
def my_event(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})

@socketio.event
def my_broadcast_event(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'user': message['user'], 'count': session['receive_count']},
         broadcast=True)
    data = message['data']
    if data:
        print(data)
        if data.startswith('/stock='):
            msg = get_stock(data)
            emit('my_response',
                 {'data': msg, 'user': 'bot', 'count': session['receive_count']},
                 broadcast=True)
        else:
            post = Post(body=message['data'], author=current_user)
            db.session.add(post)
            db.session.commit()

@socketio.event
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()

    session['receive_count'] = session.get('receive_count', 0) + 1
    # for this emit we use a callback function
    # when the callback function is invoked we know that the message has been
    # received and it is safe to disconnect
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']},
         callback=can_disconnect)



@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected', request.sid)
    logout()
