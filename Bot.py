import telebot
from datetime import datetime
from datetime import timedelta
import datetime
import pytz
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()
api = os.getenv("API")
bot = telebot.TeleBot(api)

# Setting up sqlite3 
con = sqlite3.connect("database.db", check_same_thread=False)
cur = con.cursor()

# Make the time follow my timezone
here = pytz.timezone("Asia/Kuala_Lumpur")
now = datetime.datetime.now(here)
dater = now.strftime("%d-%m")
hour = now.strftime("%H:%M:%S")
today = datetime.datetime.today().strftime("%d-%m")
tmr = (datetime.datetime.today() + timedelta(days=1)).strftime("%d-%m")

print(today)

# Creating a table
con.execute('''CREATE TABLE IF NOT EXISTS birthday (name TEXT PRIMARY KEY, date TEXT);''')

# Start command
@bot.message_handler(commands=["start"])
def start(message):
  username = message.chat.username
  id = message.chat.id
  if id != 1160508602:
    bot.send_message(id, "Sorry, this bot is only for the admin.")
    return
  else:
    bot.send_message(id, "Hello, I am the birthday bot. I will help you to keep track of your birthday.")
    bot.send_message(id, "To add a birthday, type /add <name> <date>.")
    bot.send_message(id, "To delete a birthday, type /delete <name>.")
    bot.send_message(id, "To view all birthdays, type /view.")
    bot.send_message(id, "To view a specific birthday, type /view <name>.")

@bot.message_handler(commands=["add"])
def add(message):
  username = message.chat.username
  id = message.chat.id
  if id != 1160508602:
    bot.send_message(id, "Sorry, this bot is only for the admin.")
    return
  else:
    if len(message.text.split()) != 3:
      bot.send_message(id, "Please enter the name and date in the format <name> <date>.")
      bot.send_message(id, "Example: /add John 10-10")
    elif len(message.text.split()) == 3:
      bday = message.text.split()
      name = bday[1]
      date = bday[2]
      cur.execute("INSERT INTO birthday (name, date) VALUES (?, ?)", (name, date))
      bot.send_message(id, "Birthday added successfully.")

@bot.message_handler(commands=["view"])
def view(message):
  username = message.chat.username
  id = message.chat.id
  if id != 1160508602:
    bot.send_message(id, "Sorry, this bot is only for the admin.")
    return
  else:
    cur.execute("SELECT * FROM birthday")
    rows = cur.fetchall()
    if len(rows) == 0:
      bot.send_message(id, "No birthdays found.")
    else:
      for row in rows:
        name = row[0]
        date = row[1]
        bot.send_message(id, f"{name}: {date}")

@bot.message_handler(commands=["delete"])
def delete(message):
  username = message.chat.username
  id = message.chat.id
  if id != 1160508602:
    bot.send_message(id, "Sorry, this bot is only for the admin.")
    return
  else:
    if len(message.text.split()) != 2:
      bot.send_message(id, "Please enter the name in the format <name>.")
      bot.send_message(id, "Example: /delete John")
    elif len(message.text.split()) == 2:
      bday = message.text.split()
      name = bday[1]
      cur.execute("DELETE FROM birthday WHERE name=?", (name,))
      bot.send_message(id, "Birthday deleted successfully.")

id = 1160508602

if name == "main":
  def refresh(message):
    id = message.chat.id
    if id != 1160508602:
      pass
    else:
      if today == today:
      #bot.send_message(id, "")
        cur.execute("SELECT * FROM birthday")
        rows = cur.fetchall()
        for row in rows:
          name = row[0]
          date = row[1]
          if dater == date:
            bot.send_message(id, f"Happy birthday, {name}!")
          else:
            bot.send_message(id, "No birthdays today.")


      
# Bot is always listening
bot.infinity_polling()
