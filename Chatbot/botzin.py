import os
import telebot
import pandas as pd
from pandasai import PandasAI
from pandasai.llm.starcoder import Starcoder

# Define the directory where your files are located and list them
directory_path = "files"
file_list = os.listdir(directory_path)

# Telegram API Token, from BotFather
API_TOKEN = "6172180603:AAFwSuG0b-Tu7_NhCpjy_gLwE3XEPg7fy3M"
bot = telebot.TeleBot(API_TOKEN)

# Starcoder API Token, from Hugging Face
llm = Starcoder(api_token="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")

# Create a list to store data frames
data_frames = []

# PandasAI reanding and manipulating data
for file_name in file_list:
    file_path = os.path.join(directory_path, file_name)
    if os.path.isfile(file_path):
        try:
            data = pd.read_csv(
                file_path
            )  # Adjust the read function for your file format, in this case, is CSV
            data_frames.append(data)  # Saving the CSVs in the data frames list
        except Exception as e:
            print(f"Error reading file {file_name}: {str(e)}")
            traceback.print_exc()  # Print the full stack trace

pandas_ai = PandasAI(llm, conversational=False)

# print("DATA FRAMES:", data_frames)  # DEBUGGING PURPOSE


@bot.message_handler(func=lambda message: True)
def response(message):
    try:
        # Use all available data frames to generate a response
        response_text = pandas_ai.run(data_frames, prompt=message.text)

        # print("MESSAGE: ", message)  # DEBUGGING PURPOSE
        # print("RESPONSE TEXT: ", response_text)  # DEBUGGING PURPOSE

        bot.reply_to(message, response_text)
    except Exception as e:
        print(f"Error processing message: {str(e)}")
        traceback.print_exc()  # Print the full stack trace
        bot.reply_to(
            message,
            "An error occurred while processing your request. Please try again later.",
        )


# Starting the bot
bot.polling()
