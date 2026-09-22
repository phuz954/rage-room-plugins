import os
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'rage-room-secret'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

ADMIN_KEY = os.environ.get("ADMIN_KEY", "YOUR_SECRET_KEY_123")

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
    port = int(os.environ.get("PORT", 8080))
    socketio.run(app, host='0.0.0.0', port=port)
