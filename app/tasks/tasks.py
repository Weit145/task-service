import asyncio
from pathlib import Path

from jinja2 import Template

from app.tasks.celery import app
from app.tasks.email.email import send_email


@app.task(name="send_email")
def send_message_email(token: str, username: str, email: str):
    html_path = Path("app/templates/pod_reg.html")
    html_content = html_path.read_text(encoding="utf-8")

    template = Template(html_content)
    rendered_html = template.render(
        confirm_url=f"https://kload.ru/confirm/?token_pod={token}",
        username=username,
        site_url="https://kload.ru/",
        support_email="kloader145@gmail.com",
        unsubscribe_url="https://kload.ru/",
        year=2025,
    )
    asyncio.run(
        send_email(
            recipient=email,
            subject="Подтверждение регистрации на Kload",
            plain_content="Здравствуйте! Подтвердите свою регистрацию, перейдя по ссылке в письме.",
            html_content=rendered_html,
        )
    )
    return


@app.task(name="check_verified")
def send_check_verified(id: int):
    payload = {"id": id}
    from app.kafka.repositories.kafka_repositories import KafkaRepository

    asyncio.run(KafkaRepository().send_message("check_verified", payload))
