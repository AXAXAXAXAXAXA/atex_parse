import time

from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By

import aiohttp, aiofiles, asyncio


from aiogram import Bot, Dispatcher
from aiogram import types, utils, filters
from aiogram.utils import executor


#region
api_hash =  "9654cd7cc12cb638d8ac16c42c22a5df"
api_id = 1324314
bot_token = "5542870136:AAF4Z4gaguJYT_azy-CAvRWHVOVRdovzTj8"
#endregion
bot = Bot(token=bot_token)
dp = Dispatcher(bot)

list_of_text_in_link = []

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
            time.sleep(0.2)
            list_of_text_in_link.append(driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div').text)
            time.sleep(0.2)


    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()
    return list_of_text_in_link

@dp.message_handler(commands=['get_data'])
async def send_list(message: types.Message):
    list_of_text_in_link = await get_main_page()
    for x in list_of_text_in_link:
        if 'Скоморохова Гора' in x:
            await message.answer(x)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

