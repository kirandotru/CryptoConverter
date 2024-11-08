#from crypt import crypt
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import requests

def update_crypto_label(event):
    crypto_id = crypto_combobox.get() # Получить и сохранить выбранную криптовалюту
    crypto_name = cryptocurrencies[crypto_id]
    crypto_label.config(text=crypto_name)

def update_b_label(event):
    print(event)
    # Получаем полное название 1-й базовой валюты из словаря и обновляем метку
    code = b_combobox.get()
    name = currencies[code]
    b_label.config(text=name)

def update_t_label(event):
    # Получаем полное название целевой валюты из словаря и обновляем метку
    code = t_combobox.get()
    name = currencies[code]
    t_label.config(text=name)

def crypto_exchange():
    crypto_code = crypto_combobox.get() # Сохранить криптовалюту
    target_code = t_combobox.get() # Сохранить целевую валюту
    print("Привет, как дела?")
    print(crypto_code, target_code)
    if crypto_code and target_code:
        try:
            # Работа с криптовалютами
            url = 'https://api.coingecko.com/api/v3/simple/price'
            crypto_response = requests.get(url, params=get_params(crypto_code, target_code))
            crypto_response.raise_for_status() # Обработка ошибок
            data = crypto_response.json()
            print(data)
            # Сформировать сообщение с результатом
            info = f"1 {crypto_code} торгуется на уровне {data[crypto_code][target_code.lower()]} {target_code}"
            mb.showinfo("Курс обмена", info)

        except Exception as er:
            mb.showerror("Предупреждение", f"{er}")
    elif not crypto_code:
        mb.showwarning("Предупреждение", "Внимание! Выберите криптовалюту")
    elif not target_code:
        mb.showwarning("Предупреждение", "Внимание! Выберите целевую валюту")

def exchange():
    target_code = t_combobox.get()
    base_code = b_combobox.get()
    if target_code and base_code:
        try:
            if base_code:
                response = requests.get(f'https://open.er-api.com/v6/latest/{base_code}')
                response.raise_for_status()
                data = response.json()

            if target_code in data['rates']:
                exchange_rate = data['rates'][target_code]
                base = currencies[base_code]
                target = currencies[target_code]
                info = f"Курс {exchange_rate:.2f} {target} за 1 {base}"
                info = f"{info}"
                mb.showinfo("Курс обмена", info)

            else:
                mb.showerror("Ошибка", f"Валюта {target_code} не найдена")
        except Exception as e:
            mb.showerror("Ошибка", f"Ошибка: {e}")
    else:
        mb.showwarning('Внимание', 'Выберите коды валют для каждого поля!')

# Получение параметров для запроса
def get_params(ids, vs_currencies):
    params = {
        'ids': ids,
        'vs_currencies': vs_currencies
    }
    return params

# Словарь криптовалют и их полных названий
cryptocurrencies = {
    'bitcoin': 'Биткойн',
    'ethereum': 'Эфириум',
    'ripple': 'Райпл',
    'litecoin': 'Лайткойн',
    'cardano': 'Кардано'
}

print(cryptocurrencies['bitcoin'])

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
window.geometry("360x400")

# Блок выбора криптовалюты
Label(text="Выберите криптовалюту").pack(padx=10, pady=5)
crypto_combobox = ttk.Combobox(values=list(cryptocurrencies.keys()))
crypto_combobox.pack(padx=10, pady=5)
crypto_combobox.bind("<<ComboboxSelected>>", update_crypto_label)

# Блок описания криптовалюты
crypto_label = ttk.Label()
crypto_label.pack(padx=10, pady=5)

# Блок первой базовой валюты
Label(text="Базовая валюта №1:").pack(padx=10, pady=5)
b_combobox = ttk.Combobox(values=list(currencies.keys()))
b_combobox.pack(padx=10, pady=5)
b_combobox.bind("<<ComboboxSelected>>", update_b_label)

b_label = ttk.Label()
b_label.pack(padx=10, pady=10)

Label(text="Целевая валюта:").pack(padx=10, pady=5)
t_combobox = ttk.Combobox(values=list(currencies.keys()))
t_combobox.pack(padx=10, pady=5)
t_combobox.bind("<<ComboboxSelected>>", update_t_label)

t_label = ttk.Label()
t_label.pack(padx=10, pady=10)

Button(text="Получить курс обмена", command=exchange).pack(padx=10, pady=10)
Button(text="Курс криптовалюты", command=crypto_exchange).pack(padx=10,pady=5)

window.mainloop()