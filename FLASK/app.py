from flask import Flask
import socket

app = Flask(__name__)

@app.route("/")
def get_ip():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return f"Hostname: {hostname}, IP Address: {ip}"

@app.route("/greet")
def greet():
    return "Hello, welcome to the Flask app!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)