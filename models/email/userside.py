from models.emails import mail
from flask_mail import Message
import os


def sendActivationEmail(email, link):
    url = str(os.environ.get('URL')) + '/activate?token=' + str(link)

    body = ''' 
        <!DOCTYPE html>
        <html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width,initial-scale=1">
            <meta name="x-apple-disable-message-reformatting">
        </head>
        <body style="margin:0;padding:0;">
            <div style="width: 100%; height: 100%; background-color: gray; text-align: center;">
                <h2>Confirmation link</h2>
                <a href="''' +  url + '''">Activate your account</a>
            </div>
        </body>
        </html>
    '''

    msg = Message("New confirmation link", sender='adulaty@pepisandbox.com', recipients=[email])
    msg.html = body
    
    mail.send(msg)

def sendResetPasswEmail(email, user, token):
    url = str(os.environ.get('URL')) + '/resetpassw?user=' + str(user) + '&token=' + str(token)

    body = ''' 
        <!DOCTYPE html>
        <html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width,initial-scale=1">
            <meta name="x-apple-disable-message-reformatting">
        </head>
        <body style="margin:0;padding:0;">
            <div style="width: 100%; height: 100%; background-color: gray; text-align: center;">
                <h2>Confirmation link</h2>
                <a href="''' +  url + '''">Activate your account</a>
            </div>
        </body>
        </html>
    '''

    msg = Message("Reset password", sender='adulaty@pepisandbox.com', recipients=[email])
    msg.html = body
    
    mail.send(msg)