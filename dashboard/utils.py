from decouple import config
from django.contrib.auth import get_user_model
from . import models
from mistralai import Mistral 
import json
import smtplib
from socket import gaierror
import socket
from django.utils.translation import gettext_lazy as _
from django_eventstream import send_event
from django_eventstream import send_event
from django.contrib.auth import get_user_model
from . import models  # your Notification model

userModel = get_user_model()

def send_notification(title: str, message: str, user=None, batch_size=1000):
    """
    Send a notification either to a specific user or to all users.

    Args:
        title (str): Notification title
        message (str): Notification message content
        user (User instance or None): Target user. If None, broadcast to all users.
        batch_size (int): Number of notifications to create per bulk insert batch.

    Returns:
        List of created Notification objects
    """
    if user:
        # Single user
        notification = models.Notification.objects.create(
            user=user,
            title=title,
            message=message,
        )

        # Push event for this user only
        send_event(
            "notifications",
            "new_notification",
            {"title": title, "message": message, "user_id": user.id}
        )

        return [notification]

    else:
        # Broadcast to all users
        notifications = []
        all_users = userModel.objects.only("id")  # only fetch ids for efficiency

        batch = []
        for u in all_users.iterator():  # use iterator to avoid loading all users in memory
            batch.append(models.Notification(user=u, title=title, message=message))
            if len(batch) >= batch_size:
                notifications.extend(models.Notification.objects.bulk_create(batch))
                batch = []

        # create remaining notifications
        if batch:
            notifications.extend(models.Notification.objects.bulk_create(batch))

        # Push a single global event
        send_event(
            "notifications",
            "new_notification",
            {"title": title, "message": message}
        )

        return notifications



def translate(text: str):
    MISTRALAI_API_KEY = config('MISTRAL_API_KEY')
    model = "mistral-large-latest"

    client = Mistral(api_key=MISTRALAI_API_KEY)
    messages = [
        {
            'role': "system",
            'content': """You are a helpful assistant. who translates the text to from english to french or french to english and return it as a JSON object.
                        rules:
                            - if the text is in english translate it to french
                              ex:
                                {
                                    'text': 'hello', 
                                    'translation' : 'bonjour'
                                }
                            - if the text is in french translate it to english
                              ex:
                                {
                                    'text': 'bonjour', 
                                    'translation' : 'hello'
                                }
                      
                        """,
        },
        {
            "role": "user",
            "content": text,
        }
    ]
    chat_response = client.chat.complete(
        model = model,
        messages = messages,
        response_format = {
            "type": "json_object",
        }
    )
    translation_dict = chat_response.choices[0].message.content
    translation_dict = json.loads(translation_dict)
    print(translation_dict)
    return translation_dict['translation']


def test_smtp_connection(host, port, username, password, use_tls):
    server = None
    try:
        connection_timeout = 5
        operation_timeout = 10

        # Connect
        server = smtplib.SMTP(host=host, port=port, timeout=connection_timeout)
        server.set_debuglevel(0)

        # Start TLS if enabled
        if use_tls:
            server.starttls()
            if server.sock:
                server.sock.settimeout(operation_timeout)

        # Attempt login
        if username and password:
            server.login(username, password)

        return True, None

    except smtplib.SMTPAuthenticationError:
        return False, _('SMTP authentication failed. Please check your username and password.')
    except (gaierror, smtplib.SMTPConnectError, socket.timeout):
        return False, _('Unable to connect to the SMTP server. Please check your host and port.')
    except smtplib.SMTPException as e:
        return False, _('SMTP error: {}').format(str(e))
    except Exception as e:
        return False, _('Connection error: {}').format(str(e))
    finally:
        try:
            if server:
                server.quit()
        except Exception:
            pass

