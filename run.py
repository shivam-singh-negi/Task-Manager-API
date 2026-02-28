import os
import socket
from dotenv import load_dotenv
from app import create_app

# Load environment variables from .env file
load_dotenv()

# Create the Flask application
app = create_app()

def _print_dev_urls(port: int = 5000) -> None:
    local = '127.0.0.1'
    try:
        lan_ip = socket.gethostbyname(socket.gethostname())
    except Exception:
        lan_ip = local

    swagger_ui = f"http://{local}:{port}/apidocs/"
    swagger_json = f"http://{local}:{port}/apispec_1.json"
    health = f"http://{local}:{port}/api/health"
    base = f"http://{local}:{port}/api"

    print(f"\nSwagger UI: {swagger_ui}")
    print(f"Swagger JSON: {swagger_json}")
    print(f"Health check: {health}")
    print(f"Base API: {base}")

    if lan_ip and lan_ip != local:
        print(f"\nLAN Swagger UI: http://{lan_ip}:{port}/apidocs/")
        print(f"LAN Swagger JSON: http://{lan_ip}:{port}/apispec_1.json")


if __name__ == '__main__':
    _print_dev_urls(port=5000)
    app.run(debug=True, host='0.0.0.0', port=5000)
