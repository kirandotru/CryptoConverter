from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import requests

def update_b_label_1(event):
    print(event)
    # Получаем полное название 1-й базовой валюты из словаря и обновляем метку
    code_1 = b_combobox_1.get()
    name_1 = currencies[code_1]
    b_label_1.config(text=name_1)

def update_t_label(event):
    # Получаем полное название целевой валюты из словаря и обновляем метку
    code = t_combobox.get()
    name = currencies[code]
    t_label.config(text=name)

def exchange():
    target_code = t_combobox.get()
    base_code_1 = b_combobox_1.get()

    if target_code and base_code_1:
        try:
            if base_code_1:
                response = requests.get(f'https://open.er-api.com/v6/latest/{base_code_1}')
                response.raise_for_status()
                data_1 = response.json()

            if target_code in data_1['rates']:
                exchange_rate_1 = data_1['rates'][target_code]
                base_1 = currencies[base_code_1]
                target = currencies[target_code]
                info_1 = f"Курс {exchange_rate_1:.2f} {target} за 1 {base_1}"
                info = f"{info_1}"
                mb.showinfo("Курс обмена", info)

            else:
                mb.showerror("Ошибка", f"Валюта {target_code} не найдена")
        except Exception as e:
            mb.showerror("Ошибка", f"Ошибка: {e}")
    else:
        mb.showwarning("Внимание", "Выберите коды валют для каждого поля!")

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

# Блок первой базовой валюты
Label(text="Базовая валюта №1:").pack(padx=10, pady=5)
b_combobox_1 = ttk.Combobox(values=list(currencies.keys()))
b_combobox_1.pack(padx=10, pady=5)
b_combobox_1.bind("<<ComboboxSelected>>", update_b_label_1)

b_label_1 = ttk.Label()
b_label_1.pack(padx=10, pady=10)

Label(text="Целевая валюта:").pack(padx=10, pady=5)
t_combobox = ttk.Combobox(values=list(currencies.keys()))
t_combobox.pack(padx=10, pady=5)
t_combobox.bind("<<ComboboxSelected>>", update_t_label)

t_label = ttk.Label()
t_label.pack(padx=10, pady=10)

Button(text="Получить курс обмена", command=exchange).pack(padx=10, pady=10)

window.mainloop()