from app.tasks.tasks import send_message_email


class EmailService:
    @staticmethod
    def process_registration_message(data: dict):
        send_message_email.delay(
            token=data.get("token"),
            username=data.get("username"),
            email=data.get("email"),
        )
