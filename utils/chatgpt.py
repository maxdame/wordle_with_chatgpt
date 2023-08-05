import openai
from dotenv import dotenv_values
from utils.display import Colors

config = dotenv_values("utils/.env")

openai.api_key = config["OPENAI_API_KEY"]


def provide_real_word():
    context = [
        {"role": "system", "content": "You are a helpful word generator. Your task is to provide ONLY a 5 letter English word."},
        {"role": "user", "content": f"Provide a real 5 letter English word that exists in the English Dictionary. Do not start with 'apple' and select difficult words. Respond only with the 5 letter word without any punctuation or other content"}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=context
    )

    return response['choices'][0]['message']['content'][0:5].strip().lower()


def gpt_validation(guess):
    if real_word_validation(guess):
        return True


def real_word_validation(guess):
    context = [
        {"role": "system", "content": "You are a helpful word validator. Your task is to check if a word exists in the English language."},
        {"role": "user", "content": f"Is {guess} a valid English word? Be VERY strict on spelling but allow for plurals. Respond only with 'True' or 'False' without any punctuation or other content."}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=context
    )

    validation = response['choices'][0]['message']['content'][0:5].strip()
    print(f"{Colors.CYAN}GPT VALIDATION:{Colors.BASE} {validation}")

    if validation in ("True", "True."):
        return True


def gpt_riddle(guess):
    context = [
        {"role": "system", "content": "The user will provide a word and your task is to generate a riddle where the provided word is the answer. The riddle should be creative, engaging, and difficult to solve."},
        {"role": "user", "content": f"Write a 2 line riddle where {guess} is the answer."}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=context
    )

    return response['choices'][0]['message']['content'].strip()
