'''

https://documenter.getpostman.com/view/7317157/2s9YRGw8qy#f6f6568d-9ab4-42aa-8af7-5bbd8fd3eccd

2. ПРОВЕРКА БАЛАНСА
Используйте метод GET 1.1. Show

3. ПОПОЛНЕНИЕ БАЛАНСА
Используйте метод GET 1.2. Top up

4. СОЗДАНИЕ ЗАКАЗА ЭНЕРГИИ
Используйте метод GET 2.2. Create

5. ВЫВОД СПИСКА ПОТРЕБИТЕЛЕЙ ЭНЕРГИИ
(Это кошельки, на которые делегируется энергия)

Чтобы отобразить 1 адрес используйте метод GET 2.3. Show

Чтобы отобразить все адреса используйте метод GET 2.1. Index

6. ОБНОВЛЕНИЕ ДАННЫХ ПОТРЕБИТЕЛЕЙ ЭНЕРГИИ
(Вы можете изменить имя потребителя, кол-во энергии, срок аренды энергии, тип потребителя: динамический/статический, статус автопродления)

Используйте метод PATCH 2.7. Update
функция автопродления - POST 2.9. Toggle Auto Renewal

функция Boost - POST 2.6. Boost

7. АКТИВИРОВАНИЕ ЗАКАЗА ЭНЕРГИИ
Используйте метод POST 2.4. Activate

8. ДЕАКТИВИРОВАНИЕ ЗАКАЗА ЭНЕРГИИ
Используйте метод POST 2.5. Deactivate

9. УДАЛЕНИЕ ПОТРЕБИТЕЛЯ ЭНЕРГИИ
Используйте метод DELETE 2.8. Destroy
'''

import requests
import pprint
import json
import time

class Trenergy():
    def __init__(self):
        self.API_KEY = '9357|tRwbVn**************' # API KEY FROM https://tr.energy/ru/consumers/dashboard
        self.headers = {
  'Authorization': f"Bearer {self.API_KEY}"
    }
        self.wallet_address = 'TYbYJ*********' # Your tron address

    # 1.1. Show
    def account(self):
        payload = {}
        files={}
        url = "http://core.tr.energy/api/account"
        response = requests.request("GET", url, headers=self.headers, data=payload, files=files)

        pprint.pprint(json.loads(response.text))

    # 2.2. Create
    def create(self, name, amount):
        url = "https://core.tr.energy/api/consumers"

        payload = {'payment_period': '1',
        'address': 'TYbYJinNhMHDaWXpGrZH84GgYjGqLSWV8o',
        'auto_renewal': '0',
        'consumption_type': '1',
        'resource_amount': str(amount),
        'name': name}

        response = requests.request("POST", url, headers=self.headers, data=payload )

        answer = json.loads(response.text)

        pprint.pprint(answer)
        id = answer['data']['id']

        return id

    # 2.2. Create
    def activate(self, id):
        url = f"https://core.tr.energy/api/consumers/{id}/activate"

        payload = {}
        response = requests.request("POST", url, headers=self.headers, data=payload )
        pprint.pprint(json.loads(response.text))
        answer = json.loads(response.text)
        return answer['status']

    # 2.3. Show
    def show(self):
        payload = {}
        files={}
        url = f"http://core.tr.energy/api/consumers/{self.consumer_id}"
        response = requests.request("GET", url, headers=self.headers, data=payload, files=files)

        pprint.pprint(json.loads(response.text))

    def get_energy_balance(self):
        url = f"https://apilist.tronscanapi.com/api/accountv2?address={self.wallet_address}"
        response = requests.request("GET", url)

        answer = json.loads(response.text)

        # pprint.pprint(answer)

        return int(answer['bandwidth']['energyRemaining'])



def upgrade_energy_balance(name): # Name - имя заказа
    tren = Trenergy()
    # tren.account()
    balance = tren.get_energy_balance()
    if balance >= 65000:
        return True
    id = tren.create( name, max(int(65000 - balance), 30000))
    time.sleep(0.5)
    result = tren.activate(id)
    return result

upgrade_energy_balance("ZHCASH")
