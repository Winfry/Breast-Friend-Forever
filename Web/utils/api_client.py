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
            print(f"[HEALTH] Backend health check: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"[OK] Backend healthy: {data}")
                return True
            return False
        except Exception as e:
            print(f"[ERROR] Backend health check failed: {e}")
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
            print(f"[SEND] Sending message to backend: {message}")
            start_time = time.time()
            response = requests.post(
                f"{self.backend_url}/api/v1/chat/message",
                json={"message": message},
                timeout=self.timeout
            )
            response_time = time.time() - start_time
            print(f"[RECV] Backend response: {response.status_code} in {response_time:.2f}s")

            if response.status_code == 200:
                data = response.json()
                print(f"[OK] Backend success: {data.get('source', 'No source')}")
                return data
            else:
                print(f"[ERROR] Backend error status: {response.status_code}")
                return {
                    "response": "I'm here to help with breast health information. Please try your question again.",
                    "source": "System Error",
                    "confidence": "low"
                }

        except requests.exceptions.Timeout:
            print("[ERROR] Backend timeout")
            return {
                "response": "I'm taking a bit longer to respond. Please wait or try again.",
                "source": "System Timeout",
                "confidence": "low"
            }
        except Exception as e:
            print(f"[ERROR] Backend connection failed: {e}")
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

    # --- New Features ---

    def analyze_symptoms(self, symptoms, pain_level, duration, cycle_day, age):
        """Call the Expert System API"""
        payload = {
            "symptoms": symptoms,
            "pain_level": pain_level,
            "duration_days": duration,
            "cycle_day": cycle_day,
            "age": age
        }
        try:
            response = requests.post(f"{self.backend_url}/api/v1/symptom-check/analyze", json=payload)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Error: {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}

    def calculate_reminders(self, last_period_date, cycle_length):
        """Call the Reminders API"""
        payload = {
            "last_period_date": str(last_period_date),
            "cycle_length_days": cycle_length
        }
        try:
            response = requests.post(f"{self.backend_url}/api/v1/reminders/calculate", json=payload)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Error: {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}

    def get_journal_entries(self):
        """Get all journal entries"""
        try:
            response = requests.get(f"{self.backend_url}/api/v1/journal/")
            return response.json()
        except Exception:
            return []

    def add_journal_entry(self, date, symptoms, notes, mood):
        """Add a new journal entry"""
        payload = {
            "date": str(date),
            "symptoms": symptoms,
            "notes": notes,
            "mood": mood
        }
        try:
            response = requests.post(f"{self.backend_url}/api/v1/journal/", json=payload)
            return response.json()
        except Exception as e:
            return {"error": str(e)}

api_client = ApiClient()