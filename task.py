import smtplib
import telebot
import requests
import jinja2
import pdfkit
import datetime
from email.message import EmailMessage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from celery import Celery
from config import TOKEN_TG, CHAT_ID, SMTP_USER, SMTP_PASSWORD

# celery -A task:celery worker -l INFO --pool=solo
# celery -A task:celery flower


# SMTP_USER = SMTP_USER
# SMTP_PASSWORD = SMTP_PASSWORD
# SMTP_HOST = "smtp.mail.ru"
# SMTP_PORT = 465

celery = Celery(
    'orders',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1'
)
celery.conf.broker_url = "redis://localhost:6379/0"
celery.autodiscover_tasks()


def create_pdf(data):
    filename = data.get("phone")
    context = {
        "date": datetime.datetime.now().strftime("%H:%M от %B-%d-%Y"),
        "name": data.get("name"),
        "email": data.get("email"),
        "phone": data.get("phone"),
        "msg": data.get("msg"),
        'cart': data.get("cart")
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
    html_path = f'./orders/html/order.html'
    with open(html_path, 'w', encoding='utf-8') as file:
        file.write(output_text)
    pdf_path = f'./orders/pdf/order_{filename}.pdf'
    html2pdf(html_path, pdf_path)
    finale_message = "Новый заказ\n\nот:{name}\n{email}\n{phone}\n\n{items}\nкомментарий:\n{msg}".format(
        name=context.get('name', 'anon'),
        email=context.get('email', 'anon'),
        phone=context.get('phone', 'anon'),
        items="".join(order_items),
        msg=context.get('msg', 'anon')
    )
    return finale_message
    # return output_text


def html2pdf(html_path, pdf_path):
    options = {
        'page-size': 'Letter',
        'margin-top': '0.35in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None,
        'enable-local-file-access': '',

    }
    config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
    # pdfkit.from_string(output_text, 'pdf_generated.pdf', configuration=config, css='style.css')
    with open(html_path) as f:
        pdfkit.from_file(f, pdf_path, configuration=config, options=options)


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
#     return {"status": "ok"}

def bot_init(token: str):
    bot = telebot.TeleBot(token)
    return bot


def send_order_to_tg_chat(bot, chat_id, message, file=None):
    bot.send_message(chat_id, message)


def send_pdf_to_tg_chat(bot, chat_id, filename):
    pdf_file = open(filename, "rb")
    bot.send_document(chat_id, pdf_file)


def get_filename(**data):
    filename = data.get("data").get("phone")
    data.get("phone")
    pdf_path = f'./orders/pdf/order_{filename}.pdf'
    return pdf_path


@celery.task
def send_order_email(**data):
    try:
        bot = bot_init(token=TOKEN_TG)
        chat_id = CHAT_ID

        filename = get_filename(**data)
        message = create_pdf(**data)
        try:
            send_order_to_tg_chat(bot, chat_id, message)
        except Exception:
            message = "ОШИБКА! не смог отправить данные по заказу."
            send_order_to_tg_chat(bot, chat_id, message)
        try:
            send_pdf_to_tg_chat(bot, chat_id, filename)
        except Exception:
            message = "ОШИБКА! не смог отправить PDF-файл."
            send_order_to_tg_chat(bot, chat_id, message)
        return {"msg": "SUCCESS! bot just has sent a pdf."}
    except Exception:
        return {"msg": "ERROR! bot  has not sent a pdf."}


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
