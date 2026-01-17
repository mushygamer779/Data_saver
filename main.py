import telebot
from config import token
from logic import *

bot = telebot.TeleBot(token)

message_handlers_user_set = []
message_handlers_user_get = []

@bot.message_handler(commands=['start'])
def send_welcome(message):
    start(message.from_user.id)
    bot.reply_to(message, f"hello {message.from_user.username} its my pleasure.\nthis bot designed to save infomation.\nto save info use /save\nto veiw use /veiw\nto delete info use /delete\n to quit and delete all your info use /quit")


@bot.message_handler(commands=['save'])
def save_info(message):
    global message_handlers_user_set
    message_handlers_user_set.append({"user_id" : message.from_user.id, "message_text" : None, "index": None, "state" : "awaiting_info"})
    bot.reply_to(message, f"Please enter the information you want to save:")


@bot.message_handler(commands=['veiw'])
def view_info(message):
    global message_handlers_user_get
    message_handlers_user_get.append({"user_id" : message.from_user.id, "state" : "getting_index_veiw", "index" : None})
    bot.reply_to(message, "can you give me the index of the info that you saved")


@bot.message_handler(commands=["delete"])
def delete_info(message):
    global message_handlers_user_get
    message_handlers_user_get.append({"user_id" : message.from_user.id, "state" : "getting_index_delete", "index" : None})
    bot.reply_to(message, "can you give me the index of the info that you want to delete")

@bot.message_handler(commands=["quit"])
def quit(message):
    quit_msg(message.from_user.id)
    bot.send_message(message.chat.id, "you have been deleted from the database.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    global message_handlers_user_set, message_handlers_user_get

    for handler in message_handlers_user_set:
        if handler["user_id"] == message.from_user.id:
            if handler["state"] == "awaiting_info":

                handler["message_text"] = message.text
                handler["state"] = "awaiting_index"

                bot.send_message(message.chat.id, "ok now selct the index for your info")
                return
            
            if handler["state"] == "awaiting_index":

                handler["index"] = message.text  

                save(handler)

                print(handler)

                bot.send_message(message.chat.id, "good. the info was saved")

                message_handlers_user_set.remove(handler)
                return


    for handle_g in message_handlers_user_get:
        if handle_g["user_id"] == message.from_user.id:
            if handle_g["state"] == "getting_index_veiw":
                try:
                    handle_g["index"] = message.text

                    message_r = get_info(handle_g)

                    print(message_r)

                    bot.send_message(message.chat.id, f"here is the info:\n{message_r}")

                    message_handlers_user_get.remove(handle_g)
                except Exception as e:
                    bot.send_message(message.chat.id, f"an error occurred: {e}")

            elif handle_g["state"] == "getting_index_delete":
                try:
                    handle_g["index"] = message.text

                    delete_info_msg(handle_g)

                    bot.send_message(message.chat.id, f"the message under index {handle_g["index"]} has been removed")

                    message_handlers_user_get.remove(handle_g)

                except Exception as e:
                    bot.send_message(message.chat.id, "an error occured")
    


bot.delete_my_commands(scope=None, language_code=None)

bot.set_my_commands(
    commands= [
        telebot.types.BotCommand("/start","start bot"),
        telebot.types.BotCommand("/save", "save info"),
        telebot.types.BotCommand("/veiw","view info"),
        telebot.types.BotCommand("/delete","delete info"),
        telebot.types.BotCommand("/quit","quit and delete all your info"),
            ],
        scope=None, language_code=None
)

# check command
cmd = bot.get_my_commands(scope=None, language_code=None)
print([c.to_json() for c in cmd])


bot.infinity_polling()