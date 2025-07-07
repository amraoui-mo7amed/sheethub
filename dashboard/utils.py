from decouple import config
from django.contrib.auth import get_user_model
from . import models
from mistralai import Mistral 
import json
import smtplib
from socket import gaierror
import socket
from django.utils.translation import gettext_lazy as _

userModel = get_user_model()


def create_user_notification(user, title: str, message: str ):
    """
    Create a notification for a single user
    
    Args:
        user: User instance or user ID
        message: Notification message content
        notification_type: One of Notification.NOTIFICATION_TYPES
        event: Optional related Event instance
    
    Returns:
        Notification object
    """
    
    return models.Notification.objects.create(
        user=user,
        title=title,
        message=message,
    )

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

