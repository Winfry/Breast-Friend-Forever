# Web/utils/api_client.py
import requests

class ApiClient:
    def __init__(self, backend_url="http://127.0.0.1:8000"):
        self.backend_url = backend_url

    def health_check(self):
        try:
            response = requests.get(f"{self.backend_url}/health")
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def get_chat_greeting(self):
        response = requests.get(f"{self.backend_url}/api/v1/chat/greeting")
        return response.json()

    def post_chat_message(self, message, conversation_id="anonymous"):
        response = requests.post(
            f"{self.backend_url}/api/v1/chat/message",
            json={"message": message, "conversation_id": conversation_id}
        )
        return response.json()

    def get_self_exam_steps(self):
        response = requests.get(f"{self.backend_url}/api/v1/self_exam/steps")
        return response.json()

    def get_hospitals(self, city=None, state=None):
        params = {}
        if city:
            params["city"] = city
        if state:
            params["state"] = state
        response = requests.get(f"{self.backend_url}/api/v1/hospitals/", params=params)
        return response.json()

    def get_resources(self):
        response = requests.get(f"{self.backend_url}/api/v1/resources/")
        return response.json()

    def get_encouragements(self):
        response = requests.get(f"{self.backend_url}/api/v1/encouragement/")
        return response.json()

    def post_encouragement(self, message, type="💖 General Support"):
        response = requests.post(
            f"{self.backend_url}/api/v1/encouragement/",
            json={"message": message, "type": type}
        )
        return response.json()

api_client = ApiClient()
