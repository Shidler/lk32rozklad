import telebot
from background import keep_alive
import json
import requests
import datetime

bot = telebot.TeleBot(BOT_TOKEN_HERE)
print("RUNNING")

url = "http://schedule.kpi.ua/api/schedule/lessons?groupId=e2afdbb9-45e4-4893-a423-3fa250a47d66"

response = requests.get(url)

@bot.message_handler(commands=['start'])
def start_message(message):
  bot.send_message(message.chat.id,"Привіт! Я бот для розкладу КПІ ім. І. Сікорського для групи ЛК-32!")

@bot.message_handler(commands=['today'])
def todayschedule(message):
  result = str()
  
  now = datetime.datetime.now()
  
  day = now.weekday()
  
  # Отримати поточну дату
  today = datetime.date.today()
  
  # Отримати кількість днів у році
  days_in_year = 365
  
  # Отримати рік
  year = today.year
  
  # Отримати кількість днів, які минули з початку року
  days_since_start_of_year = (today.month - 1) * 30 + today.day
  
  # Розрахувати загальну кількість днів
  total_days = days_in_year * (year - 1) + days_since_start_of_year
  
  # Вивести результат
  print(total_days)
  
  weekdiff = ((total_days - 738274) // 7) % 2 + 1
  
  print(weekdiff)
  
  if weekdiff == 1:
    week = "scheduleFirstWeek"
    weekname = "Перший"
  else:
    week = "scheduleSecondWeek"
    weekname = "Другий"
  
  print(weekname)
  
  if response.status_code == 200:
    data = response.json()
    week_day = ("День тижня: " +  data["data"][week][day]["day"])
    week_text = ("Тиждень: " + weekname)
    x = 0

    result = result + f'''╓
╠	{week_day}
╠	{week_text}
'''
    
    pairs_amount = len(data["data"][week][day]["pairs"])
    if pairs_amount > 0:
      for elements in data["data"][week][day]["pairs"]:
        while x < pairs_amount:
          pairname = str(data["data"][week][day]["pairs"][x]["time"] + ": " + data["data"][week][day]["pairs"][x]["name"] + ";")
          if data["data"][week][day]["pairs"][x]["tag"] == "lab":
            pair_type = "Лабораторна робота"
          elif data["data"][week][day]["pairs"][x]["tag"] == "lec":
            pair_type = "Лекція"
          elif data["data"][week][day]["pairs"][x]["tag"] == "prac":
            pair_type = "Практика"
          pairsub = str("Викладач: " + data["data"][week][day]["pairs"][x]["teacherName"] + "; Тип пари: " + pair_type + ".")
          x = x + 1
          result = result + f'''║
╠	{pairname}
╠	{pairsub}
'''
          print(result)
    else:
      print("немає пар")
      pairname = "Сьогодні немає пар! Відпочивайте!"
    result = result + '''╙'''
    bot.send_message(message.chat.id, result)
    # Здесь ваш код, который выводит в консоль пары


@bot.message_handler(commands=['tomorrow'])
def tomorrowschedule(message):
  result = str()
  
  now = datetime.datetime.now()
  
  day = now.weekday()
  
  # Отримати поточну дату
  today = datetime.date.today()
  
  # Отримати кількість днів у році
  days_in_year = 365
  
  # Отримати рік
  year = today.year
  
  # Отримати кількість днів, які минули з початку року
  days_since_start_of_year = (today.month - 1) * 30 + today.day + 1
  
  # Розрахувати загальну кількість днів
  total_days = days_in_year * (year - 1) + days_since_start_of_year
  
  # Вивести результат
  print(total_days)
  
  weekdiff = ((total_days - 738274) // 7) % 2 + 1
  
  print(weekdiff)
  
  if weekdiff == 1:
    week = "scheduleFirstWeek"
    weekname = "Перший"
  else:
    week = "scheduleSecondWeek"
    weekname = "Другий"
  
  print(weekname)
  
  if response.status_code == 200:
    data = response.json()
    week_day = ("День тижня: " +  data["data"][week][day + 1]["day"])
    week_text = ("Тиждень: " + weekname)
    x = 0

    result = result + f'''╓
╠	{week_day}
╠	{week_text}
'''
    
    pairs_amount = len(data["data"][week][day + 1]["pairs"])
    if pairs_amount > 0:
      for elements in data["data"][week][day + 1]["pairs"]:
        while x < pairs_amount:
          pairname = str(data["data"][week][day + 1]["pairs"][x]["time"] + ": " + data["data"][week][day + 1]["pairs"][x]["name"] + ";")
          if data["data"][week][day + 1]["pairs"][x]["tag"] == "lab":
            pair_type = "Лабораторна робота"
          elif data["data"][week][day + 1]["pairs"][x]["tag"] == "lec":
            pair_type = "Лекція"
          elif data["data"][week][day + 1]["pairs"][x]["tag"] == "prac":
            pair_type = "Практика"
          pairsub = str("Викладач: " + data["data"][week][day + 1]["pairs"][x]["teacherName"] + "; Тип пари: " + pair_type + ".")
          x = x + 1
          result = result + f'''║
╠	{pairname}
╠	{pairsub}
'''
          print(result)
    else:
      print("немає пар")
      pairname = "Завтра немає пар! Відпочивайте!"
    result = result + '''╙'''
    bot.send_message(message.chat.id, result)
    # Здесь ваш код, который выводит в консоль пары


keep_alive()
bot.polling(non_stop=True, interval=0)
