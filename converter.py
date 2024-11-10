# CryptoConverter | Version 1.1
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from datetime import datetime
import requests
import webbrowser

#========================================================================
# CONTROLLER / КОНТРОЛЛЕР — ПОЛУЧАТАЕТ И ПРЕОБРАЗУЕТ ЗАПРОСЫ ПОЛЬЗОВАТЕЛЯ

def update_crypto_label(event):
    """
    Заполняет/обновляет метку для размещения названия криптовалюты.
    :param event: Объект события
    :return: None
    """
    crypto_id = crypto_combobox.get() # Получить и сохранить выбранную криптовалюту
    crypto_name = cryptocurrencies[crypto_id]
    crypto_label.config(text=crypto_name)

def update_t_label(event):
    """
    Заполняет/обновляет метку для размещения названия целевой валюты.
    :param event: Объект события
    :return: None
    """
    code = t_combobox.get()
    name = currencies[code]
    t_label.config(text=name)

def message_output(type_message, message):
    """
    Выводит на экран сообщение messagebox, исходя из переданных параметров.
    :param type_message: Тип сообщения
    :param message: Содержание сообщения
    :return: None
    """
    if type_message == 'warning':
        mb.showwarning("Предупреждение", f"Выберите {message}")
    elif type_message == 'error':
        mb.showerror('Ошибка', message)
    else:
        mb.showinfo('Справка', message)

def create_help(coin):
    """
    Создаёт/удаляет кнопки для получения справки из стороннего ресурса.
    :param coin: Наименование выбранной криптовалюты
    :return: None
    """
    for widget in help_frame.winfo_children():
        widget.destroy()
    help_button = Button(help_frame, text=f"Подробнее о монете '{coin.capitalize()}'", command=lambda: open_help(coin))
    help_button.pack()

def open_help(cryptocurrency):
    """
    Реализует открытие справки из указанного ресурса в браузере по умолчанию.
    :param cryptocurrency: Наименование выбранной криптовалюты
    :return: None
    """
    link = f"https://ru.wikipedia.org/wiki/{cryptocurrency}"
    webbrowser.open(link)

def crypto_exchange():
    """
    Реализует обмен криптовалют, ввёденных/выбранных пользователем.
    Позволяет получать курс даже на те валюты, которые не указаны в локальном словаре.
    :return: None
    """
    crypto_code = crypto_combobox.get().lower() # Сохранить криптовалюту в нижнем регистре.
    target_code = t_combobox.get() # Сохранить целевую валюту.
    # Проверить ввод пользователя.
    if not crypto_code:
        message_output('warning', 'криптовалюту')
    elif not target_code:
        message_output('warning', 'целевую валюту')
    else:
        try:
            # Запрос курса конкретной криптовалюты в выбранной валюте.
            url = 'https://api.coingecko.com/api/v3/simple/price'
            crypto_response = requests.get(url, params=get_params(crypto_code, target_code))
            crypto_response.raise_for_status() # Проверить понимания запроса.
            data = crypto_response.json()

            if crypto_response.json() == {}:
                mb.showinfo('Предупреждение', 'Криптовалюта введена некорректно!')
            elif crypto_response.json()[crypto_code] == {}:
                mb.showinfo('Предупреждение', 'Целевая валюта введена некорректно!')
            else:
                exchange_rate = data[crypto_code][target_code.lower()]
                # Сформировать сообщение с результатом.
                info = f'1 {crypto_code} торгуется на уровне {exchange_rate} {target_code.upper()}'
                result_label.config(text=f'Курс обмена:\n{info}')
                save_history(info)
                # Создать кнопку помощи для выбранной криптовалюты.
                create_help(crypto_code)

        except Exception as er:
            message_output('error', er)

def save_history(user_request):
    """
    Создаёт файл history.txt, если его не существует, сохраняет историю всех запросов.
    :param user_request: Сообщение, включающее курс выбранной криптовалюты
    :return: None
    """
    try:
        with open('history.txt', 'a+', encoding="utf-8") as f:
            f.write(f'{user_request} | Время торговли: {datetime.now()}\n')
            # text.insert(1.0, s) # От 1 строки 0 элемента до конца / добавляем то, что в переменной s
    except Exception as er:
        message_output('error', f'История запросов не может быть сохранена.\n{er}')

def developer():
    """
    Отображает информацию о приложении
    :return: None
    """
    message_output('info', f'© {datetime.now().year} {application}\nCreated by KIRILL')

def get_params(ids, vs_currencies):
    """
    Формирует словарь параметров, необходимый для осуществления запроса к API.
    :param ids: Название криптовалюты
    :param vs_currencies: Название целевой валюты
    :return: Параметры для запроса к API
    """
    params = {
        'ids': ids,
        'vs_currencies': vs_currencies
    }
    return params

#=============================================
# MODEL / МОДЕЛЬ — ОТВЕЧАЕТ ЗА ХРАНЕНИЕ ДАННЫХ

# Словарь популярных криптовалют и их кириллических названий.
cryptocurrencies = {
    'bitcoin': 'Биткойн (BTC)',
    'ethereum': 'Эфириум (ETH)',
    'dogecoin': 'Догикоин (DOGE)',
    'tron': 'Трон (TRX)',
    'ripple': 'Рипл (XRP)',
    'litecoin': 'Лайткойн (LTC)',
    'cardano': 'Кардано (ADA)',
    'tether': 'Тезер (USDT)',
}

# Словарь популярных государственных валют и их полных названий.
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

# Название приложения и версия
application = 'CryptoConverter | Version 1.1'

#==============================================
# GUI -- ГРАФИЧЕСКИЙ ПОЛЬЗОВАТЕЛЬСКИЙ ИНТЕРФЕЙС
window = Tk()
window.title(application)
window.geometry('400x425')
try:
    window.iconbitmap('images/btc.ico')
except TclError:
    message_output('info', 'Приложение будет запущено без фирменной иконки:(')
except Exception as er:
    message_output('error', er)

# Главное меню
main_menu = Menu(window)
window.config(menu=main_menu)

# Всплывающее меню
file_menu = Menu(main_menu, tearoff=0)
file_menu.add_command(label='О программе', command=developer)
main_menu.add_cascade(label='Меню', menu=file_menu)

# Блок выбора криптовалюты
Label(text="Введите название криптовалюты\nили выберите из базового списка:", font="Arial 10 bold").pack(padx=10, pady=15)
crypto_combobox = ttk.Combobox(values=list(cryptocurrencies.keys()))
crypto_combobox.pack(padx=10, pady=5)
crypto_combobox.bind("<<ComboboxSelected>>", update_crypto_label)

# Блок комментария к выбранной криптовалюте.
crypto_label = ttk.Label()
crypto_label.pack(padx=10, pady=5)

# Блок для целевой валюты.
Label(text="Целевая валюта:", font="Arial 10 bold").pack(padx=10, pady=5)
t_combobox = ttk.Combobox(values=list(currencies.keys()))
t_combobox.pack(padx=10, pady=5)
t_combobox.bind("<<ComboboxSelected>>", update_t_label)

# Блок комментария к выбранной целевой валюте.
t_label = ttk.Label()
t_label.pack(padx=10, pady=10)

Button(text="Получить курс обмена", command=crypto_exchange).pack(padx=10,pady=15)

# Блок результатов конвертации.
result_label = Label(width=100, height=4, background='#ffffff',
                     borderwidth=2, relief='groove', font="Arial 10")
result_label.pack(padx=10, pady=5)

# Фрейм для кнопки помощи.
help_frame = Frame(window, width=300, height=100)
help_frame.pack(pady=5)

window.mainloop()