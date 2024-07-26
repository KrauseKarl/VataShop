import json
import os
import locale
import smtplib
import telebot
from telebot.async_telebot import AsyncTeleBot
import requests
import jinja2
import pdfkit
import datetime
from email.message import EmailMessage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from celery import Celery
<<<<<<< HEAD
<<<<<<< HEAD
from config import TOKEN_TG, CHAT_ID, SMTP_USER, SMTP_PASSWORD, CELERY_BROKER, CELERY_BACKEND
from order_db import ORDER_DB_PATH, record_to_order_db, create_order_json,update_order_json
=======
from config import TOKEN_TG, CHAT_ID
from config import SMTP_USER, SMTP_PASSWORD
from config import DEBUG, OST, WINDOWS
from config import ORDER_DB_PATH, ORDER_DB_FILE
from config import CELERY_BROKER, CELERY_BACKEND

from order_db import create_order_json
from order_db import update_order_json
from order_db import record_to_order_db
>>>>>>> 4bc9bce99031afd8465234f752b7911e6cd598db

# celery -A task:celery worker -l INFO --pool=solo
# celery -A task:celery flDower
#locale.setlocale(
#    category=locale.LC_ALL,
#    locale="ru_RU.UTF-8"
#)
ORDER_DB_FILE = os.path.join(ORDER_DB_PATH, "order_db.json") 
=======
from config import TOKEN_TG, CHAT_ID
from config import SMTP_USER, SMTP_PASSWORD
from config import DEBUG, OST, WINDOWS
from config import ORDER_DB_PATH, ORDER_DB_FILE
from config import CELERY_BROKER, CELERY_BACKEND

from order_db import create_order_json
from order_db import update_order_json
from order_db import record_to_order_db

# celery -A task:celery worker -l INFO --pool=solo
# celery -A task:celery flower

if OST == WINDOWS:
    locale.setlocale(
        category=locale.LC_ALL,
        locale="ru_RU.UTF-8"
    )
<<<<<<< HEAD
>>>>>>> 4bc9bce99031afd8465234f752b7911e6cd598db
=======
>>>>>>> 4bc9bce99031afd8465234f752b7911e6cd598db

ORDER_DB_FILE = os.path.join(ORDER_DB_PATH, ORDER_DB_FILE)

app_celery = Celery(
    'orders',
    broker=CELERY_BROKER,
    backend=CELERY_BACKEND
)
<<<<<<< HEAD
celery.conf.broker_url = CELERY_BROKER
celery.autodiscover_tasks()
=======
app_celery.conf.broker_url = CELERY_BROKER
app_celery.autodiscover_tasks()
>>>>>>> 4bc9bce99031afd8465234f752b7911e6cd598db


def create_pdf(data):
    with open(ORDER_DB_FILE, "r", encoding='utf-8') as jsonFile:
        data = json.load(jsonFile)
        # try:
        number_cart = str(list(data["orders"].keys())[-1])
        last_cart = data["orders"].get(number_cart)
        # except (KeyError, IndexError):
        #     filename = datetime.datetime.now().strftime("%B_%m_%y")

    context = {
        "date": datetime.datetime.now().strftime("%B %d %Y (%H:%M)"),
        "name": last_cart.get("name"),
        "email": last_cart.get("email"),
        "phone": last_cart.get("phone"),
        "msg": last_cart.get("msg"),
        'cart': last_cart.get("cart"),
        "order_id": last_cart.get("order_id")
    }

    cart = context.get("cart")
    products = cart.get("item")

    order_items = [
        "{name}  [{quantity}] шт ({color})\n".format(
            name=it.get("name"),
            quantity=it.get("quantity"),
            color=it.get("color_name")
        ) for item_id, it in products.items()
    ]

    template_loader = jinja2.FileSystemLoader('./templates')
    template_env = jinja2.Environment(loader=template_loader)
    template_file = "/order-list.html"
    template = template_env.get_template(template_file)
    output_text = template.render(context)
    html_path = ORDER_DB_PATH +'/html/order.html'
    with open(html_path, 'w', encoding='utf-8') as file:
        file.write(output_text)
    pdf_path = ORDER_DB_PATH + f'/pdf/order_{number_cart}.pdf'

    html2pdf(html_path, pdf_path)

    finale_message = "✅Заказ {order_id}\n👤: {name}\n✉️: {email}\n☎️: {phone}\n💰 {total}\n\n{items}".format(
        name=context.get('name', 'anon'),
        order_id=context.get('order_id', 'none'),
        date=datetime.datetime.now().strftime(" %d-%b-%y (%H:%M)"),
        email=context.get('email', 'anon'),
        phone=context.get('phone', 'anon'),
        total=context.get('cart', 'anon').get("total", 0),
        items="".join(order_items),
    )
    if context.get('msg'):
        msg = "\n🗒 комментарий:\n\n{msg}\n\n#{order_id}\n#{telephone}".format(
            msg=context.get('msg', 'anon'),
            order_id=str(context.get('order_id', 'none')),
            telephone=context.get('phone', 'anon').strip(),
        )
        finale_message = finale_message + msg

    return finale_message
    # return output_text


def html2pdf(html_path, pdf_path):
    options = {
        'page-size': 'A4',
        'margin-top': '0.35in',
        'margin-right': '0.15in',
<<<<<<< HEAD
<<<<<<< HEAD
        'margin-bottom': '0.25in',
=======
        'margin-bottom': '0.15in',
>>>>>>> 4bc9bce99031afd8465234f752b7911e6cd598db
=======
        'margin-bottom': '0.15in',
>>>>>>> 4bc9bce99031afd8465234f752b7911e6cd598db
        'margin-left': '0.15in',
        'encoding': "UTF-8",
        'no-outline': None,
        'enable-local-file-access': '',

    }
    #config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
    #pdfkit.from_string(output_text, 'pdf_generated.pdf', configuration=config, css='style.css')
    with open(html_path) as f:
<<<<<<< HEAD
<<<<<<< HEAD
        pdfkit.from_file(f, pdf_path, options=options)


# def create_mail(data):
#     envelope = MIMEMultipart()
#     envelope['Subject'] = 'VATASHOP | Новый заказ от ' + datetime.datetime.now().strftime("от %d-%B-%Y %H:%M")
#     envelope['From'] = SMTP_USER
#     envelope['To'] = SMTP_USER
#     attached_content = create_pdf(data)
#     envelope.attach(MIMEText(attached_content, 'html'))
#     filename = data.get("phone")
#     pdf_path = f'./orders/pdf/order_{filename}.pdf'
#
#     with open(pdf_path, "rb") as f:
#         attach = MIMEApplication(f.read(), _subtype="pdf")
#     attach.add_header('Content-Disposition', 'attachment', filename=str(pdf_path))
#     envelope.attach(attach)
#     return envelope
=======
=======
>>>>>>> 4bc9bce99031afd8465234f752b7911e6cd598db
        if DEBUG:
            pdfkit.from_file(f, pdf_path, options=options, configuration=config)
        else:
            pdfkit.from_file(f, pdf_path, options=options)
<<<<<<< HEAD
>>>>>>> 4bc9bce99031afd8465234f752b7911e6cd598db
=======
>>>>>>> 4bc9bce99031afd8465234f752b7911e6cd598db


def bot_init(token: str):
    bot = telebot.TeleBot(token)
    #bot = AsyncTeleBot(token)
    return bot


def send_order_to_tg_chat(bot, chat_id, message, file=None):
    bot.send_message(chat_id, message)


def send_pdf_to_tg_chat(bot, chat_id, filename):
    pdf_file = open(filename, "rb")
    bot.send_document(chat_id, pdf_file)


def get_filename(**data):
    filename = data.get("data").get("order_id")
    pdf_path = f'./orders/pdf/order_{filename}.pdf'
    return pdf_path


@app_celery.task
def send_order_email(**data):
    # try:
    bot = bot_init(token=TOKEN_TG)
    chat_id = CHAT_ID

    filename = get_filename(**data)
    message = create_pdf(**data)
    try:
        send_order_to_tg_chat(bot, chat_id, message)
    except Exception as error:

        message = "ОШИБКА! не смог отправить данные по заказу."
        send_order_to_tg_chat(bot, chat_id, message)
    try:
        send_pdf_to_tg_chat(bot, chat_id, filename)
    except Exception as error:

        message = "ОШИБКА! не смог отправить PDF-файл."
        send_order_to_tg_chat(bot, chat_id, message)
    return {"msg": "SUCCESS! bot just has sent a pdf."}
    # except Exception as error:
    #     return {"msg": "ERROR! bot  has not sent a pdf."}


    # @bot.message_handler(commands=['marksSYAP'])
    # def send_welcome(message):
    #     # pdf_file = get_order_pdf(data)

    # f = open("D:\\MarksSYAP.xlsx", "rb")
    # bot.send_document(message.chat.id, f)
    #
    # import requests
    #
    # with open("MarksSYAP.xlsx", "rb") as filexlsx:
    #     files = {"document": filexlsx}
    #     title = "MarksSYAP.xlsx"
    #     chat_id = "1234567890"
    #     r = requests.post(method, data={"chat_id": chat_id, "caption": title}, files=files)
    #     if r.status_code != 200:
    #         raise Exception("send error")


# def create_mail(data):
#     envelope = MIMEMultipart()
#     envelope['Subject'] = 'VATASHOP | Новый заказ от ' + datetime.datetime.now().strftime("от %d-%B-%Y %H:%M")
#     envelope['From'] = SMTP_USER
#     envelope['To'] = SMTP_USER
#     attached_content = create_pdf(data)
#     envelope.attach(MIMEText(attached_content, 'html'))
#     filename = data.get("phone")
#     pdf_path = f'./orders/pdf/order_{filename}.pdf'
#
#     with open(pdf_path, "rb") as f:
#         attach = MIMEApplication(f.read(), _subtype="pdf")
#     attach.add_header('Content-Disposition', 'attachment', filename=str(pdf_path))
#     envelope.attach(attach)
#     return envelope


# @celery.task
# def send_order_email(**data):
#     email = create_mail(**data)
#     with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
#         server.login(SMTP_USER, SMTP_PASSWORD)
#         server.send_message(email)
<<<<<<< HEAD
#     return {"status": "ok"}
=======
#     return {"status": "ok"}
>>>>>>> 4bc9bce99031afd8465234f752b7911e6cd598db
