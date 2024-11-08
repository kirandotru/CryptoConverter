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

def crypto_exchange():
    crypto_code = crypto_combobox.get() # Сохранить криптовалюту
    target_code = t_combobox.get() # Сохранить целевую валюту
    if crypto_code and target_code:
        try:
            # Запрос курса конкретной криптовалюты в выбранной валюте
            url = 'https://api.coingecko.com/api/v3/simple/price'
            crypto_response = requests.get(url, params=get_params(crypto_code, target_code))
            crypto_response.raise_for_status() # Проверить понимания запроса
            data = crypto_response.json()
            exchange_rate = data[crypto_code][target_code.lower()]

            # Сформировать сообщение с результатом
            info = f"1 {crypto_code} торгуется на уровне {exchange_rate} {target_code}"
            mb.showinfo("Курс обмена", info)

        except Exception as er:
            mb.showerror("Предупреждение", f"{er}")
    elif not crypto_code:
        mb.showwarning("Предупреждение", "Внимание! Выберите криптовалюту")
    elif not target_code:
        mb.showwarning("Предупреждение", "Внимание! Выберите целевую валюту")

# Получение параметров для запроса
def get_params(ids, vs_currencies):
    params = {
        'ids': ids,
        'vs_currencies': vs_currencies
    }
    return params

# Словарь популярных криптовалют и их кириллических названий
cryptocurrencies = {
    'bitcoin': 'Биткойн',
    'ethereum': 'Эфириум',
    'ripple': 'Рипл (пульсация)',
    'litecoin': 'Лайткойн (лёгкая монета)',
    'cardano': 'Кардано'
}

# Словарь кодов валют и их полных названий
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
window.title("Курс обмена валюты")
window.geometry("400x400")

# Блок выбора криптовалюты
Label(text="Выберите криптовалюту").pack(padx=10, pady=5)
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

Button(text="Курс обмена", command=crypto_exchange).pack(padx=10,pady=5)

window.mainloop()