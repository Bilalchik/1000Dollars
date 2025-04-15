from django.core.mail.backends.smtp import EmailBackend
import ssl

class QuickEmailBackend(EmailBackend):
    def open(self):
        if self.connection:
            return False

        connection = None
        try:
            # Открываем SMTP-соединение
            connection = self.connection_class(self.host, self.port, timeout=self.timeout)
            connection.ehlo()
            if self.use_tls:
                # Используем небезопасный SSL-контекст, который не проверяет сертификаты
                context = ssl._create_unverified_context()
                connection.starttls(context=context)
                connection.ehlo()
            if self.username and self.password:
                connection.login(self.username, self.password)
            self.connection = connection
            return True
        except Exception:
            if connection:
                connection.close()
            raise
