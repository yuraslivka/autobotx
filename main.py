import requests
import telebot
import json
import os
import datetime
import asyncio
from telebot import types
import time, random
from bs4 import BeautifulSoup
import auth_data
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import filters, FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor


bot = Bot(token=auth_data.TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

class Form(StatesGroup):
    name = State()

f_date = open('text.txt', 'r', encoding='utf8')
f = f_date.read()
f_date.close()
print(f)

@dp.message_handler(commands='start')
async def start(message: types.Message):
    f_date = open('text.txt', 'r', encoding='utf8')
    f = f_date.read()
    f_date.close()
    print(f, " *")

    start_buttons = ['/start', 'SEARCH', 'OTHER','MENU']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer('Begin search', reply_markup=keyboard)


@dp.message_handler(Text(equals="SEARCH"))
async def start(message: types.Message):
    f_date = open('text.txt', 'r', encoding='utf8')
    f = f_date.read()
    f_date.close()
    print(f, " **")
    
    auto_list = {}
    now = datetime.datetime.now()
    dnow = now.strftime("%d_%m_%Y")
    await message.answer(dnow)
    await message.answer('\U0001F697\n')

    url = ("https://www.olx.pl/d/motoryzacja/samochody/"+f.lower()+"/piotrkow-trybunalski/?search%5Border%5D=created_at:desc")
    
    #url = ("https://www.olx.pl/d/motoryzacja/samochody/"+f.lower()+"/piotrkow-trybunalski/?search%5Bdist%5D=100&search%5Border%5D=created_at:desc&search%5Bfilter_enum_model%5D%5B0%5D=focus&search%5Bfilter_enum_condition%5D%5B0%5D=notdamaged")
    print(url) 


    year_min = 2008
    price_min = 10000
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
        f2 = list(f.lower().split(" "))
        auto_name = f2
        print(auto_name)
        
        #print(f2)
        #print(item_href)
        for item_a in auto_name:
            
            if item_a in item_href:
                #print(item_a)
                if "/d" in item_href:
                    item_href = item_href.replace("/d", "https://www.olx.pl/d")
                    print(item_href)
                #------------------------рік та пробіг
                item_ym = item.find(class_="css-efx9z5")
                item_year = item_ym.text.split(" ")[0]
                item_mileage = item_ym.text.split(" ")[3]+item_ym.text.split(" ")[4]
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
                        auto_list[item_href] = {
                                "year" : item_year,
                                "mileage" : item_mileage,
                                "price" : price
                            }

                        await message.answer(item_href)                            
                        print("push to telegram")

@dp.message_handler(Text(equals='MENU'))
async def start(message: types.Message):
    menu_buttons = ['/CHANGE','BACK']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*menu_buttons)
    await message.answer('MENU', reply_markup=keyboard)

@dp.message_handler(Text(equals='OTHER'))
async def oth_btn(message: types.Message):
    await message.answer(f)

@dp.message_handler(commands=['CHANGE'])
async def cmd_start(message: types.Message):
    await Form.name.set()
    await message.reply("Enter car name:")

# Сюда приходит ответ с именем
@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
        date_to_w = data['name']
        
        

        start_buttons = ['/start', 'SEARCH', 'OTHER', 'MENU']
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*start_buttons)


        ch = open('text.txt', 'w', encoding="utf8")
        ch.write(date_to_w.upper())
        ch.close()
        await bot.send_message(
            message.chat.id,
            md.text(
                md.text('Car name for search: ', data['name']),
                
                sep='\n',
            ), 
            reply_markup=keyboard
        )

    await state.finish()


@dp.message_handler(Text(equals='BACK'))
async def start(message: types.Message):
    
    start_buttons = ['/start', 'SEARCH','OTHER','MENU']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer('Begin search', reply_markup=keyboard)

def main():
    executor.start_polling(dp, skip_updates=True)

if __name__ == '__main__':
    main()