import asyncio

from app.kafka.repositories.kafka_repositories import KafkaRepository


async def main():
    kf = KafkaRepository()
    await kf.wait_kafka("check_verified", "email_service")
    kafka_task = asyncio.create_task(kf.get_message("auth", "email_service"))
    await asyncio.gather(kafka_task)
    pass


if __name__ == "__main__":
    asyncio.run(main())
