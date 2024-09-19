from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)

socketio = SocketIO(app)

users = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('set_username')
def set_username(username):
    users[request.sid] = username
    emit('user_list', list(users.values()), broadcast=True)

@socketio.on('message')
def handle_message(msg):
    username = users.get(request.sid, 'Anonymous')
    full_message = f'{username}: {msg}'
    emit('message', full_message, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in users:
        del users[request.sid]
        emit('user_list', list(users.values()), broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)