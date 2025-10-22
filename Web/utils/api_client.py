# Web/utils/api_client.py
import requests
import time

class ApiClient:
    def __init__(self, backend_url="http://127.0.0.1:8000"):
        self.backend_url = backend_url
        self.timeout = 10  # seconds

    def health_check(self):
        try:
            response = requests.get(f"{self.backend_url}/health", timeout=5)
            print(f"🔍 Backend health check: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Backend healthy: {data}")
                return True
            return False
        except Exception as e:
            print(f"❌ Backend health check failed: {e}")
            return False

    # 🚨 ADD THIS MISSING METHOD!
    def send_message(self, message):
        """Alias for post_chat_message to match the hybrid code"""
        return self.post_chat_message(message)

    def get_chat_greeting(self):
        response = requests.get(f"{self.backend_url}/api/v1/chat/greeting")
        return response.json()

    def post_chat_message(self, message):
        try:
            print(f"📤 Sending message to backend: {message}")
            start_time = time.time()
            response = requests.post(
                f"{self.backend_url}/api/v1/chat/message",
                json={"message": message},
                timeout=self.timeout
            )
            response_time = time.time() - start_time
            print(f"📥 Backend response: {response.status_code} in {response_time:.2f}s")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Backend success: {data.get('source', 'No source')}")
                return data
            else:
                print(f"❌ Backend error status: {response.status_code}")
                return {
                    "response": "I'm here to help with breast health information. Please try your question again.",
                    "source": "System Error",
                    "confidence": "low"
                }
                
        except requests.exceptions.Timeout:
            print("❌ Backend timeout")
            return {
                "response": "I'm taking a bit longer to respond. Please wait or try again.",
                "source": "System Timeout",
                "confidence": "low"
            }
        except Exception as e:
            print(f"❌ Backend connection failed: {e}")
            return {
                "response": "I'm here to help with breast health information. What would you like to know about self-examination, symptoms, or prevention?",
                "source": "Connection Failed",
                "confidence": "low"
            }

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