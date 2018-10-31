import telepot
from time import sleep
from telepot.loop import MessageLoop
import dice
import sqlite3


perm = [29809662]
gm = [29809662]


def handle(msg):
    chat_id = msg['chat']['id']
    chat_username = msg['chat']['username']
    command = msg['text']
    
    # Start Bot
    if command == '/start':
        bot.sendMessage(chat_id, "HELLO MY FRIEND! <3")
    
    # Roll Dice
    elif command.startswith("/roll"):
        roll = command.split(" ")[1]
        bot.sendMessage(chat_id, "%s rolls %s result: %i " % (chat_username, roll, dice.roll(roll)))

    # Show All Characters (GM Only)
    elif command == '/s':
        if chat_id in gm:
            sheet = []
            conn = sqlite3.connect('test.db')
            cursor = conn.cursor()
            cursor.execute("""
            SELECT * FROM character;
            """)
            for l in cursor.fetchall():
                sheet.append(l)
            for x in range(len(sheet)):
                bot.sendMessage(chat_id,
                                "Player: %s \nName: %s \nST: %s \nIQ: %s \nDX: %s \nHT: %s" % (
                                    sheet[x][7], sheet[x][1], sheet[x][2], sheet[x][3], sheet[x][4], sheet[x][5],))
            conn.close()
        else:
            bot.sendMessage(chat_id, "You shall not pass!")

    # Show My Character
    elif command == '/my':
        sheet = []
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM character WHERE user_id=?;
        """, (chat_id,))
        for l in cursor.fetchall():
            sheet.append(l)
        bot.sendMessage(chat_id,
                        "Name: %s \nST: %s \nIQ: %s \nDX: %s \nHT: %s" % (
                            sheet[0][1], sheet[0][2], sheet[0][3], sheet[0][4], sheet[0][5]))
        conn.close()

    # Create Character
    elif command == '/c':
        bot.sendMessage(chat_id, "Enter Character Name")
        MessageLoop(bot, handle).run_as_thread()

    # Delete Character
    elif command == '/d':
        bot.sendMessage(chat_id, "Delete Character")

    # Show Help
    else:
        bot.sendMessage(chat_id, "Send command '/help'")


bot = telepot.Bot("[TOKEN")
MessageLoop(bot, handle).run_as_thread()
while 1:
    sleep(10)
