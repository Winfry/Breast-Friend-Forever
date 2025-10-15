# Web/utils/api_client.py
import requests

# Update this to your backend URL (localhost for development, or a deployed URL)
BACKEND_URL = "http://127.0.0.1:8000"

def get_health():
    response = requests.get(f"{BACKEND_URL}/health")
    return response.json()

def get_chat_greeting():
    response = requests.get(f"{BACKEND_URL}/api/v1/chat/greeting")
    return response.json()

def post_chat_message(message, conversation_id="anonymous"):
    response = requests.post(
        f"{BACKEND_URL}/api/v1/chat/message",
        json={"message": message, "conversation_id": conversation_id}
    )
    return response.json()

def get_self_exam_steps():
    response = requests.get(f"{BACKEND_URL}/api/v1/self_exam/steps")
    return response.json()

def get_hospitals(city=None, state=None):
    params = {}
    if city:
        params["city"] = city
    if state:
        params["state"] = state
    response = requests.get(f"{BACKEND_URL}/api/v1/hospitals/", params=params)
    return response.json()

def get_resources():
    response = requests.get(f"{BACKEND_URL}/api/v1/resources/")
    return response.json()

def get_encouragements():
    response = requests.get(f"{BACKEND_URL}/api/v1/encouragement/")
    return response.json()

def post_encouragement(message, type="💖 General Support"):
    response = requests.post(
        f"{BACKEND_URL}/api/v1/encouragement/",
        json={"message": message, "type": type}
    )
    return response.json()