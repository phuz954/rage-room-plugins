import os
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent')

ADMIN_KEY = os.environ['ADMIN_KEY']

@app.route('/')
def index():
    return render_template('chat.html')

@socketio.on('chat_message')
def handle_chat(data):
    emit('chat_message', data, broadcast=True)

@socketio.on('delete_message')
def handle_delete(data):
    if data.get('admin_key') == ADMIN_KEY:
        emit('delete_message', data, broadcast=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port)
