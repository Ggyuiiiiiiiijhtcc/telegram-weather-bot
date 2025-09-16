import requests

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import F,Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from start_name import API_KEY
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

router = Router()

class Weather(StatesGroup):
    weather = State()

main = ReplyKeyboardMarkup(resize_keyboard=True,keyboard=[[KeyboardButton(text='Узнать погоду🌍')]])


@router.message(CommandStart())
async def start(message: Message):
    await message.answer('Привет, Я бот который тебе поможет узнать погоду в любом городе!',reply_markup=main)

@router.message(F.text == 'Узнать погоду🌍')
async def weather_city(message: Message, state: FSMContext):
    await message.answer('Введите город, в котором хотите узнать погоду 🌍:')
    await state.set_state(Weather.weather)

@router.message(Weather.weather)
async def weather(message: Message, state: FSMContext):
    city = message.text
    try:
        red = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ru')
        data = red.json()
        if data.get('cod') != 200:
            await message.answer("⚠️ Город не найден. Попробуйте ещё раз.")
            return
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        desc = data['weather'][0]['description']
        wind = data['wind']['speed']
        humidity = data['main']['humidity']
        await message.answer(
            f"📍 Погода в <b>{city.title()}</b>:\n"
            f"🌡 Температура: {temp}°C (ощущается как {feels_like}°C)\n"
            f"☁ {desc.capitalize()}\n"
            f"💨 Ветер: {wind} м/с\n"
            f"💧 Влажность: {humidity}%",
            parse_mode="HTML",reply_markup=main
        )
    except Exception as e:
        await message.answer("❌ Ошибка при получении погоды. Попробуйте позже.")
        print(f"Ошибка погоды: {e}")
    await state.set_state(Weather.weather)

