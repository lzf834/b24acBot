import wolframalpha
import os

import dotenv
from dotenv import load_dotenv

# Add wolfram alpha's APPID in your .env file
load_dotenv()
APPID = os.getenv('APPID')

# input = input("Question: ")
# client = wolframalpha.Client(APPID)
# res = client.query(input)
# answer = next(res.results).text
# print(answer)

def waquery(question):
    client = wolframalpha.Client(APPID)
    res = client.query(question)
    answer = next(res.results).text
    return answer