from app.tasks.tasks import send_message_email, send_check_verified


class EmailService:
    @staticmethod
    def process_registration_message(data: dict):
        send_message_email.delay(
            token=data.get("token"),
            username=data.get("username"),
            email=data.get("email"),
        )

    @staticmethod
    def check_verified(data : dict):
        send_check_verified.apply_async(
            args=[data.get("id")],
            countdown=1*60
        )