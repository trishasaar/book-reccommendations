from email.mime.text import MIMEText
import smtplib

def send_email(email, book, category):
    from_email="saartrisha@gmail.com"
    from_password="bookreccommendations"
    to_email=email

    subject="Book Reccomendation"
    message="Hey there, your book reccomendation from the category <strong>%s</strong> is <strong>%s</strong>. <br> Thanks!" % (category, book)

    msg=MIMEText(message, 'html')
    msg['Subject']=subject
    msg['To']=to_email
    msg['From']=from_email

    gmail=smtplib.SMTP('smtp.gmail.com',587) # Gets SMTP server address and the TLS required port
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)
    gmail.send_message(msg)
