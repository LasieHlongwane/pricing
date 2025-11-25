# utils.py
import smtplib
import string, random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

APP_NAME = "LAC Accounting Bots"
SENDER_NAME = "LAC Admin Team"
EMAIL_SUBJECT = "Your LAC Bot product is ready"

def generate_activation_key(length=10):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))

def build_email_body_plain(name, product, activation_key, product_link):
    return f"""Hi {name},

Thank you for your purchase of {product} from {APP_NAME}.

Your activation key is: {activation_key}

To use your product:
1) Open: {product_link}
2) Enter your activation key when prompted.

If you need help, reply to this email or WhatsApp +27 76 611 4909.

Regards,
{SENDER_NAME}
{APP_NAME}
"""

def build_email_body_html(name, product, activation_key, product_link):
    html = f"""
<html>
  <body style="font-family: Arial, sans-serif; color:#222;">
    <h2 style="color:#0b5ed7;">{APP_NAME} — Product Activated</h2>
    <p>Hi <strong>{name}</strong>,</p>
    <p>Thank you for purchasing <strong>{product}</strong>.</p>
    <p><strong>Your activation key:</strong><br>
       <span style="display:inline-block; padding:8px 12px; background:#f1f5ff; border:1px solid #dbeafe; border-radius:4px; font-weight:700;">
         {activation_key}
       </span>
    </p>
    <p>To activate your product:</p>
    <ol>
      <li>Go to: <a href="{product_link}">{product_link}</a></li>
      <li>Enter your activation key when prompted.</li>
    </ol>
    <p>If you need help, reply to this email or WhatsApp <strong>+27 76 611 4909</strong>.</p>
    <p>Regards,<br><strong>{SENDER_NAME}</strong><br>{APP_NAME}</p>
  </body>
</html>
"""
    return html

def send_activation_email(to_email, name, product, activation_key, product_link, smtp_user, smtp_pass):
    subject = EMAIL_SUBJECT
    plain = build_email_body_plain(name, product, activation_key, product_link)
    html = build_email_body_html(name, product, activation_key, product_link)

    msg = MIMEMultipart('alternative')
    msg['From'] = f"{SENDER_NAME} <{smtp_user}>"
    msg['To'] = to_email
    msg['Subject'] = subject

    part1 = MIMEText(plain, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)

    # send via Gmail SMTP
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(smtp_user, smtp_pass)
    server.sendmail(smtp_user, to_email, msg.as_string())
    server.quit()
