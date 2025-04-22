from flask import Flask, render_template, request, Response, redirect, url_for, make_response
from faker import Faker
import uuid
import time
import logging

app = Flask(__name__)
faker = Faker()
logging.basicConfig(level=logging.DEBUG)

# In-memory storage for simplicity
clients = {}
messages = []


@app.route('/')
def index():
    client_id = request.cookies.get('client_id')
    if not client_id or client_id not in clients:
        # Assign new client_id and screen_name
        client_id = str(uuid.uuid4())
        screen_name = faker.first_name()
        clients[client_id] = {'screen_name': screen_name}
        current_users = [client['screen_name'] for client in clients.values()]
        recent_messages = messages[-10:]
        # Create response and set cookie
        response = make_response(
            render_template('index.html',
                            screen_name=screen_name,
                            current_users=current_users,
                            recent_messages=recent_messages))
        response.set_cookie('client_id', client_id)  # Set the client_id cookie
        return response
    else:
        screen_name = clients[client_id]['screen_name']
        current_users = [client['screen_name'] for client in clients.values()]
        recent_messages = messages[-10:]
        return render_template('index.html',
                               screen_name=screen_name,
                               current_users=current_users,
                               recent_messages=recent_messages)


@app.route('/send_message', methods=['POST'])
def send_message():
    client_id = request.cookies.get('client_id')
    if not client_id:
        return '', 403
    screen_name = clients[client_id]['screen_name']
    message = request.form['message']
    messages.append(f"{screen_name}: {message}")
    app.logger.debug(f"/send_message: {screen_name}:{message}")
    return '', 204


@app.route('/messages')
def events():

    def event_stream():
        last_index = len(messages)
        interval = 0.1  # Start with a short interval (100ms)
        max_interval = 5  # Maximum interval (5 seconds)
        while True:
            if len(messages) > last_index:
                yield f"data: {messages[last_index]}\n\n"
                last_index += 1
                interval = 0.1  # Reset to the shortest interval when new messages arrive
            else:
                time.sleep(interval)  # delay to reduce CPU load
                if interval < max_interval:
                    interval = min(
                        interval * 2,
                        max_interval)  # Increase the interval gradually

    return Response(event_stream(), mimetype='text/event-stream')


@app.route('/user_events')
def user_events():

    def user_event_stream():
        known_clients = set(clients.keys())
        known_screen_names = [clients[c]['screen_name'] for c in clients]
        while True:
            current_clients = set(clients.keys())
            current_screen_names = [clients[c]['screen_name'] for c in clients]
            if current_clients != known_clients or current_screen_names != known_screen_names:
                # If there is any change in clients or screen names, update the list
                yield f"data: {','.join(current_screen_names)}\n\n"
                known_clients = current_clients
                known_screen_names = current_screen_names
            time.sleep(5)  # Check for updates every 5 seconds

    return Response(user_event_stream(), mimetype='text/event-stream')


@app.route('/change_screen_name', methods=['POST'])
def change_screen_name():
    client_id = request.cookies.get('client_id')
    if not client_id:
        return '', 403
    old_name = clients[client_id]['screen_name']
    new_name = request.form['screen_name'].strip()

    if new_name:
        clients[client_id]['screen_name'] = new_name
        app.logger.debug(f"Screen name changed from {old_name} to {new_name}")

        # Send a message notifying users of the screen name change
        change_message = f"User '{old_name}' changed their name to '{new_name}'"
        messages.append(change_message)

    return '', 204


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
