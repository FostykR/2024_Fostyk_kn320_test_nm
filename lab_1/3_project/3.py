import requests
import os

print(os.environ)["COLORTERM"]

payload = {'name': os.environ.get("ENV_NAME"), 'cpu': os.environ.get("CPU")}
r = requests.get('https://httpbin.org/get', params=payload)
print(f"Звертаємо до URL: {r.url} та отримуємо відповідь: {r.status_code}")