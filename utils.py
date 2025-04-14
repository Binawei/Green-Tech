import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from flask import current_app


def check_temperature(temperature):
    return 10 <= temperature <= 35

def check_humidity(humidity):
    return 30 <= humidity <= 90

def check_co2(co2):
    return 200 <= co2 <= 1500

def check_light_intensity(light_intensity):
    return 25 <= light_intensity <= 30

def check_soil_ph(soil_ph):
    return 5.5 <= soil_ph <= 7

def check_soil_moisture(soil_moisture):
    return 80 <= soil_moisture <= 100

def send_email_notification(subject, recipients, body):
    """Sends an email notification using app configuration."""
    # Check if emails are globally disabled
    if not current_app.config.get('MAIL_ENABLED', False):
        current_app.logger.info("Email notifications are disabled in config.")
        return False

    sender_name, sender_email = current_app.config['MAIL_DEFAULT_SENDER']
    password = current_app.config['MAIL_PASSWORD']
    smtp_server = current_app.config['MAIL_SERVER']
    smtp_port = current_app.config['MAIL_PORT']
    use_tls = current_app.config.get('MAIL_USE_TLS', True)

    if not sender_email or not password or not smtp_server:
        current_app.logger.error("Mail server configuration incomplete. Cannot send email.")
        return False

    if not recipients:
        current_app.logger.info("No recipients provided for email notification.")
        return False

    if isinstance(recipients, str):
        recipients = [recipients]

    try:
        msg = MIMEMultipart()
        msg['From'] = f"{sender_name} <{sender_email}>"
        msg['To'] = ", ".join(recipients)
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(smtp_server, smtp_port)
        if use_tls:
            server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, recipients, text)
        server.quit()
        current_app.logger.info(f"Email sent successfully to: {', '.join(recipients)}")
        return True
    except smtplib.SMTPAuthenticationError:
        current_app.logger.error(f"SMTP Authentication Error for user {sender_email}. Check username/password.")
        return False
    except Exception as e:
        current_app.logger.error(f"Failed to send email: {e}", exc_info=True)
        return False