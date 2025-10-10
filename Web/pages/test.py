import requests

url = "https://lottie.host/4d635b14-79dc-43b3-8b8b-2226b83d48e1/YjGlLLHgaK.json"
r = requests.get(url)
print(r.status_code)
print(r.headers["Content-Type"])

