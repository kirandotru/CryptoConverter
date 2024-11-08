# Дорогой преподаватель!
# Приложение позволяет проверять как курс популярных валют, включенных в локальные словари,
# так и непопулярных, название которых можно вводить вручную в представленном поле

from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import requests

def update_crypto_label(event):
    crypto_id = crypto_combobox.get() # Получить и сохранить выбранную криптовалюту
    crypto_name = cryptocurrencies[crypto_id]
    crypto_label.config(text=crypto_name)

# Установить полное название целевой валюты на метке
def update_t_label(event):
    code = t_combobox.get()
    name = currencies[code]
    t_label.config(text=name)

# Вывод сообщения
def message_output(type_message, message):
        if type_message == 'warning':
            mb.showwarning("Предупреждение", f"Выберите {message}")
        elif type_message == 'error':
            mb.showerror('Ошибка', message)
        else:
            mb.showinfo('Справка', message)

def crypto_exchange():
    crypto_code = crypto_combobox.get().lower() # Сохранить криптовалюту в нижнем регистре
    target_code = t_combobox.get() # Сохранить целевую валюту
    # Проверить ввод пользователя
    if not crypto_code:
        message_output('warning', 'криптовалюту')
    elif not target_code:
        message_output('warning', 'целевую валюту')
    else:
        try:
            # Запрос курса конкретной криптовалюты в выбранной валюте
            url = 'https://api.coingecko.com/api/v3/simple/price'
            crypto_response = requests.get(url, params=get_params(crypto_code, target_code))
            crypto_response.raise_for_status() # Проверить понимания запроса
            data = crypto_response.json()

            if crypto_response.json() == {}:
                mb.showinfo('Предупреждение', 'Криптовалюта введена некорректно!')
            elif crypto_response.json()[crypto_code] == {}:
                mb.showinfo('Предупреждение', 'Целевая валюта введена некорректно!')
            else:
                exchange_rate = data[crypto_code][target_code.lower()]
                # Сформировать сообщение с результатом
                info = f'1 {crypto_code} торгуется на уровне {exchange_rate} {target_code}'
                result_label.config(text=f'Курс обмена:\n{info}')
                mb.showinfo('Курс обмена', info)
        except Exception as er:
            message_output('error', er)


# Получение параметров для запроса
def get_params(ids, vs_currencies):
    params = {
        'ids': ids,
        'vs_currencies': vs_currencies
    }
    return params

# Словарь популярных криптовалют и их кириллических названий
cryptocurrencies = {
    'bitcoin': 'Биткойн (BTC)',
    'ethereum': 'Эфириум (ETH)',
    'dogecoin': 'Догикоин (DOGE)',
    'algorand': 'Алгоранд (ALGO)',
    'tron': 'Трон (TRX)',
    'aave': 'Ааве (AAVE)',
    'ripple': 'Рипл (XRP)',
    'litecoin': 'Лайткойн (LTC)',
    'cardano': 'Кардано (ADA)',
    'tether': 'Тезер (USDT)',
    'solana': 'Солана (SOL)',
    'stacks': 'Стакс (STX)'
}

# Словарь популярных государственных валют и их полных названий
currencies = {
    "USD": "Американский доллар",
    "EUR": "Евро",
    "JPY": "Японская йена",
    "GBP": "Британский фунт стерлингов",
    "AUD": "Австралийский доллар",
    "CAD": "Канадский доллар",
    "CHF": "Швейцарский франк",
    "CNY": "Китайский юань",
    "RUB": "Российский рубль",
    "KZT": "Казахстанский тенге",
    "UZS": "Узбекский сум"
}

# Создание графического интерфейса
window = Tk()
window.title("CryptoConverter | Version 1.0")
window.geometry("400x400")

# Блок выбора криптовалюты
Label(text="Введите название криптовалюты\nили выберите из базового списка:", font="Arial 10 bold").pack(padx=10, pady=15)
crypto_combobox = ttk.Combobox(values=list(cryptocurrencies.keys()))
crypto_combobox.pack(padx=10, pady=5)
crypto_combobox.bind("<<ComboboxSelected>>", update_crypto_label)

# Блок описания криптовалюты
crypto_label = ttk.Label()
crypto_label.pack(padx=10, pady=5)

# Блок для целевой валюты
Label(text="Целевая валюта:").pack(padx=10, pady=5)
t_combobox = ttk.Combobox(values=list(currencies.keys()))
t_combobox.pack(padx=10, pady=5)
t_combobox.bind("<<ComboboxSelected>>", update_t_label)

t_label = ttk.Label()
t_label.pack(padx=10, pady=10)

Button(text="Курс обмена", command=crypto_exchange).pack(padx=10,pady=15)

# Блок результатов конвертации
result_label = Label(width=100, height=50, background='#ffffff',
                     borderwidth=2, relief='groove', font="Arial 10")
result_label.pack(padx=10, pady=5)

window.mainloop()