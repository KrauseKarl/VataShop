import uuid
import smtplib
from email.message import EmailMessage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import jinja2
import pdfkit

import datetime
from celery import Celery
from config import SMTP_USER, SMTP_PASSWORD

# celery -A tasks worker -l INFO --pool=solo

celery = Celery(
    'orders',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1'
)
celery.conf.broker_url = "redis://localhost:6379/0"
celery.autodiscover_tasks()

SMTP_USER = SMTP_USER
SMTP_PASSWORD = SMTP_PASSWORD
SMTP_HOST = "smtp.mail.ru"
SMTP_PORT = 465


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
    return output_text


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


def create_mail(data):
    envelope = MIMEMultipart()
    envelope['Subject'] = 'VATASHOP | Новый заказ от ' + datetime.datetime.now().strftime("от %d-%B-%Y %H:%M")
    envelope['From'] = SMTP_USER
    envelope['To'] = SMTP_USER
    attached_content = create_pdf(data)
    envelope.attach(MIMEText(attached_content, 'html'))
    filename = data.get("phone")
    pdf_path = f'./orders/pdf/order_{filename}.pdf'

    with open(pdf_path, "rb") as f:
        attach = MIMEApplication(f.read(), _subtype="pdf")
    attach.add_header('Content-Disposition', 'attachment', filename=str(pdf_path))
    envelope.attach(attach)
    return envelope


@celery.task
def send_order_email(**data):
    email = create_mail(**data)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)
    return {"status": "ok"}