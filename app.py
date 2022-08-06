import os
from datetime import datetime

from flask import Flask, abort, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import random
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))


@app.route("/", methods=["GET", "POST"])
def callback():

    if request.method == "GET":
        return "Hello Heroku"
    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return "OK"

def fill():  
    "避免彈跳視窗" 
    options = Options()
    options.add_argument("--disable-notifications")
    options.add_argument("--headless")
    chrome = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=options)
    chrome.get("https://zh.surveymonkey.com/r/EmployeeHealthCheck")
    chrome.find_element_by_id("66405067_542650090").click()
    company_id = str(534301)
    input_company_id = chrome.find_element_by_id("66405064")
    input_company_id.send_keys(company_id)

    chrome.find_element_by_id("66405069_542650092").click()

    temperature = float(random.randint(360,367)) / 10
    chrome.find_element_by_id("66405065").send_keys(str(temperature))

    chrome.find_element_by_id("66405075_542650132").click()

    chrome.find_element_by_id("66405078_542650167").click()

    chrome.find_element_by_id("66405074_542650161").click()

    chrome.find_element_by_id("66405076_542650156").click()

    chrome.find_element_by_id("66405066_542650082").click()
    chrome.find_element_by_css_selector(".survey-submit-actions").click()

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    get_message = event.message.text
    fill()
    # Send To Line
    reply = TextSendMessage(text=f"OK!")
    line_bot_api.reply_message(event.reply_token, reply)
