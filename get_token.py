import requests
import json

url = "https://ru.yougile.com/api-v2/auth/keys"
payload = {
    "login": "atimopheya@gmail.com",
    "password": "nbvjatqrf2006",
    "companyId": "6f49e495-e0c7-4e73-a8ec-02944f70af75"
}
headers = {'Content-Type': 'application/json'}

response = requests.post(url, json=payload, headers=headers)

if response.status_code == 201:
    token_data = response.json()
    print("Ваш API токен:", token_data.get('key'))
    print("Полный ответ:", json.dumps(token_data, indent=2))
else:
    print("Ошибка:", response.status_code)
    print("Ответ:", response.text)