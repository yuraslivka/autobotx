import requests
import telebot
import os
import datetime
from telebot import types
import time, random
from bs4 import BeautifulSoup
from auth_data import token



def telegram_bot(token):
    bot = telebot.TeleBot(token)

    def search():
        now = datetime.datetime.now()
        dnow = now.strftime("%d_%m_%Y")
        
        url = ("https://www.olx.pl/d/motoryzacja/samochody/piotrkow-trybunalski/?search%5Border%5D=created_at:desc")
                
        year_min = 2007
        price_min = 5000
        price_max = 28000

        headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "UserAgent" : "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36"
                }

        reg = requests.get(url, headers=headers)
        src=reg.text

        soup = BeautifulSoup(src, "lxml")
        all_auto = soup.find_all(class_="css-1bbgabe")

        for item in all_auto:
            item_href = item.get("href")
            auto_name = ["ford", "renault"]
            for item_a in auto_name:
                if item_a in item_href:
                    print(item_a)
                    if "/d" in item_href:
                        item_href = item_href.replace("/d", "https://www.olx.pl/d")

                            #------------------------рік та пробіг
                    item_ym = item.find(class_="css-niqab2")
                    item_year = item_ym.text.split(" ")[0]
                            #bot.send_message(message.chat.id, item_year)
                            #-----знаходимо ціну

                    item_price = item.find(class_="css-wpfvmn-Text eu5v0x0")
                    word_list = item_price.text
                    num_list =[]
                    for word in word_list:
                        if word.isnumeric():
                            num_list.append(int(word))
                                
                    s = [str(integer) for integer in num_list]
                    a_string = "".join(s)
                    price = int(a_string)

                    if price<=price_max and price>=price_min:
                        if int(item_year)>=year_min: 
                            print("ok")
                            print(item_href)

    @bot.message_handler(commands=["st"])
    def start_message(message):
        bot.send_message(message.chat.id, "Autobot")

        
    @bot.message_handler(commands=['start'])
    def start(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("FORD")
        btn2 = types.KeyboardButton("ALL")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, text="Привет, {0.first_name}!".format(message.from_user), reply_markup=markup)
    @bot.message_handler(content_types=['text'])
    def func(message):
        if(message.text == "FORD"):
            now = datetime.datetime.now()
            dnow = now.strftime("%d_%m_%Y")
            bot.send_message(message.chat.id, dnow)

            url = ("https://www.olx.pl/d/motoryzacja/samochody/piotrkow-trybunalski/?search%5Border%5D=created_at:desc")
            
            year_min = 2007
            price_min = 5000
            price_max = 25000

            headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "UserAgent" : "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36"
            }

            reg = requests.get(url, headers=headers)
            src=reg.text

            soup = BeautifulSoup(src, "lxml")
            all_auto = soup.find_all(class_="css-1bbgabe")

            for item in all_auto:
                item_href = item.get("href")
                auto_name = ["ford"]
                for item_a in auto_name:
                    if item_a in item_href:
                        print(item_a)
                        if "/d" in item_href:
                            item_href = item_href.replace("/d", "https://www.olx.pl/d")

                        #------------------------рік та пробіг
                        item_ym = item.find(class_="css-niqab2")
                        item_year = item_ym.text.split(" ")[0]
                        #bot.send_message(message.chat.id, item_year)
                        #-----знаходимо ціну

                        item_price = item.find(class_="css-wpfvmn-Text eu5v0x0")
                        word_list = item_price.text
                        num_list =[]
                        for word in word_list:
                            if word.isnumeric():
                                num_list.append(int(word))
                            
                        s = [str(integer) for integer in num_list]
                        a_string = "".join(s)
                        price = int(a_string)

                        if price<=price_max and price>=price_min:
                            if int(item_year)>=year_min: 

                                bot.send_message(message.chat.id, item_href)
                                print("ok")
        elif(message.text == "ALL"):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("ALL CARS")
            btn2 = types.KeyboardButton("Test func")
            back = types.KeyboardButton("Вернуться в главное меню")
            markup.add(btn1, btn2, back)
            bot.send_message(message.chat.id, text="Задай мне вопрос", reply_markup=markup)
        
        elif(message.text == "ALL CARS"):
            now = datetime.datetime.now()
            dnow = now.strftime("%d_%m_%Y")
            bot.send_message(message.chat.id, dnow)

            url = ("https://www.olx.pl/d/motoryzacja/samochody/piotrkow-trybunalski/?search%5Border%5D=created_at:desc")
            
            year_min = 2000
            price_min = 5000
            price_max = 30000

            headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "UserAgent" : "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36"
            }

            reg = requests.get(url, headers=headers)
            src=reg.text

            soup = BeautifulSoup(src, "lxml")
            all_auto = soup.find_all(class_="css-1bbgabe")

            for item in all_auto:
                item_href = item.get("href")
                auto_name = ["ford", "x3", "audi", "toyota", "116"]
                for item_a in auto_name:
                    if item_a in item_href:
                        print(item_a)
                        if "/d" in item_href:
                            item_href = item_href.replace("/d", "https://www.olx.pl/d")

                        #------------------------рік та пробіг
                        item_ym = item.find(class_="css-niqab2")
                        item_year = item_ym.text.split(" ")[0]
                        #bot.send_message(message.chat.id, item_year)
                        #-----знаходимо ціну

                        item_price = item.find(class_="css-wpfvmn-Text eu5v0x0")
                        word_list = item_price.text
                        num_list =[]
                        for word in word_list:
                            if word.isnumeric():
                                num_list.append(int(word))
                            
                        s = [str(integer) for integer in num_list]
                        a_string = "".join(s)
                        price = int(a_string)

                        if price<=price_max and price>=price_min:
                            if int(item_year)>=year_min: 

                                bot.send_message(message.chat.id, item_href)
                                print("ok")
        
        elif message.text == "Test func":
            bot.send_message(message.chat.id, "x")
            search()
            
            
            
        
        elif (message.text == "Вернуться в главное меню"):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton("FORD")
            button2 = types.KeyboardButton("ALL")
            markup.add(button1, button2)
            bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, text="На такую комманду я не запрограммировал..")

               
        
        

    bot.polling()

if __name__ == '__main__':
    telegram_bot(token)