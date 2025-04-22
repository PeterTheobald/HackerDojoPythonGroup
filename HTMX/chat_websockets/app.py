from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
import faker
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow all origins

# In-memory storage for messages and users
messages = []
users = {}


def generate_random_name():
    return faker.Faker().name()


@app.route('/')
def index():
    user_id = request.cookies.get('user_id')
    if not user_id or user_id not in users:
        user_id = generate_random_name()
        users[user_id] = {'name': user_id}
    return render_template('index.html',
                           user_id=user_id,
                           user_name=users[user_id]['name'],
                           users=users)


@socketio.on('connect')
def handle_connect():
    user_id = request.cookies.get('user_id')
    if user_id and user_id not in users:
        users[user_id] = {'name': user_id}
    emit('update_user_list', list(users.values()), broadcast=True)


@socketio.on('disconnect')
def handle_disconnect():
    user_id = request.cookies.get('user_id')
    if user_id in users:
        del users[user_id]
        emit('update_user_list', list(users.values()), broadcast=True)


@socketio.on('send_message')
def handle_send_message(data):
    user_id = data['user_id']
    message = data['message']
    user_name = users[user_id]['name']
    messages.append({'user': user_name, 'message': message})
    emit('receive_message', {
        'user': user_name,
        'message': message
    },
         broadcast=True)


@socketio.on('change_name')
def handle_change_name(data):
    user_id = data['user_id']
    new_name = data['new_name']
    users[user_id]['name'] = new_name
    emit('name_changed', {
        'user_id': user_id,
        'new_name': new_name
    },
         broadcast=True)
    emit('update_user_list', list(users.values()),
         broadcast=True)  # Update the user list


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)
