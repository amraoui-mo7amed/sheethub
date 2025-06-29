from django.core.mail.backends.smtp import EmailBackend as SMTPBackend
from .models import SMTPConfig

class DynamicSMTPBackend(SMTPBackend):
    """Custom email backend that uses SMTP settings from the database"""
    def __init__(self, *args, **kwargs):
        try:
            config = SMTPConfig.get_config()
            if config.is_active:
                kwargs.update({
                    'host': config.host,
                    'port': config.port,
                    'username': config.username,
                    'password': config.password,
                    'use_tls': config.use_tls,
                    'from_email': config.from_email,
                })
        except Exception:
            # Use default settings if there's any error
            pass
            
        super().__init__(*args, **kwargs)