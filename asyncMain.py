import time

import datetime
from dateutil.relativedelta import *

from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By

from aiogram import Bot, Dispatcher
from aiogram import types, utils, filters
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

# region
api_hash = "9654cd7cc12cb638d8ac16c42c22a5df"
api_id = 1324314
bot_token = "5542870136:AAF4Z4gaguJYT_azy-CAvRWHVOVRdovzTj8"
# endregion
storage = MemoryStorage()
bot = Bot(token=bot_token)
dp = Dispatcher(bot, storage=storage)


async def get_main_page():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
    }

    options = webdriver.ChromeOptions()
    options.add_argument(
        f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36')
    options.add_argument("--disable-blink-features=AutomationControlled")

    url = 'https://atexplus.net/news/news_category/tehnicheskie-raboty/'

    service = Service('E:\\eldoradoPARSE\\chromedriver\\chromedriver.exe')
    driver = webdriver.Chrome(
        service=service,
        options=options
    )

    list_of_hrefs = []
    list_of_text_in_link = []

    try:
        driver.get(url)
        a_elems = driver.find_elements(By.CLASS_NAME, 'nb_more')  # получение тегов а с class=nb_more
        for elem in a_elems:
            list_of_hrefs.append(elem.get_attribute('href'))  # получение всех ссылок из href

        for x in list_of_hrefs:
            driver.get(x)
            time.sleep(0.05)
            list_of_text_in_link.append(driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div').text)
            time.sleep(0.05)


    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()
    return list_of_text_in_link


class From:
    dt_not_now = None


@dp.message_handler(commands=['get_data'])
async def send_list(message: types.Message):
    dt = datetime.datetime.now().strftime('%d-%m-%Y %H:%M')
    if From.dt_not_now is not None and dt < From.dt_not_now.strftime('%d-%m-%Y %H:%M'):
        await message.answer(f"Следующее получение данных доступно в: {From.dt_not_now.strftime('%d-%m-%Y %H:%M')}")

        From.dt_not_now = None
    else:
        m = await message.answer("Ожидайте загрузки данных (~10-20 сек).")

        From.dt_not_now = datetime.datetime.now() + relativedelta(hours=+1)

        dt_now = datetime.datetime.now()
        next_day1 = dt_now + relativedelta(days=+1)
        next_day2 = dt_now + relativedelta(days=+2)
        list_of_text_in_link = await get_main_page()

        for x in list_of_text_in_link:
            f_date = str(next_day1.strftime("%d.%m.%Y")) in x and \
                     str(next_day2.strftime("%d.%m.%Y")) in x and \
                     str(dt_now.strftime("%d.%m.%Y")) in x

            if 'Скоморохова Гора' in x and f_date:
                await message.answer(x)
            else:
                await message.answer('Нет данных о профилактических работах на <<Скоморовой Горе>> на ближайшее 2 дня.')

        await bot.delete_message(chat_id=m.chat.id, message_id=m.message_id)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
