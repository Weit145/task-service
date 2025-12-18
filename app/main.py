import asyncio

from app.kafka.repositories.kafka_repositories import KafkaRepository


async def main():
    kf = KafkaRepository()
    await kf.wait_kafka("auth", "email_service")
    await kf.get_message("auth", "email_service")
    pass


if __name__ == "__main__":
    asyncio.run(main())
