import os
import smtplib
from email.mime.text import MIMEText

from dotenv import load_dotenv
from langchain_core.tools import tool


# メール送信関数
@tool
def send_email(recipient, subject, body):
    """
    作成したメールを送信する
    """
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = os.getenv('EMAIL_ADDRESS')
    msg['To'] = recipient

    with smtplib.SMTP(os.getenv('SMTP_SERVER'), int(os.getenv('SMTP_PORT'))) as server:
        server.starttls()
        server.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASSWORD'))
        server.sendmail(os.getenv('EMAIL_ADDRESS'), recipient, msg.as_string())

# テスト
if __name__ == "__main__":
    load_dotenv()
    recipient_email = "shi-zc@rgsis.com"
    email_subject = "会議のご案内"
    email_body = "来週火曜日に会議が設定されました。ご確認ください。"
    send_email(recipient_email, email_subject, email_body)
    print(f"{recipient_email} にメールを送信しました。")