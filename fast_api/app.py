from fastapi import FastAPI
from fastapi.responses import JSONResponse
import socket

app = FastAPI()


@app.get("/")
def get_ip():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return JSONResponse({
        "hostname": hostname,
        "ip_address": ip
    })


@app.get("/greet")
def greet():
    return JSONResponse({
        "message": "Hello, welcome to the FastAPI app!"
    })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
