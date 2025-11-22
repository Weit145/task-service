import json
import asyncio


from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from aiokafka.admin import NewTopic, AIOKafkaAdminClient
from app.kafka.kf_helper import kf_helper

from app.tasks.celery import app
from app.tasks.tasks import send_message_email

class KafkaRepository:

    async def create_topic(self, name_topic:str, partitions:int = 3, replication:int =1):
        admin_client = kf_helper.get_admin()
        topic_list = [NewTopic(name=name_topic,
            num_partitions=partitions,
            replication_factor=replication)]
        try:
            await admin_client.start()
            await admin_client.create_topics(new_topics=topic_list, validate_only=False)
        finally:
            await admin_client.close()


    async def send_message(self,topic:str, message:dict):
        producer = kf_helper.get_producer()
        await producer.start()
        try:
            await  producer.send_and_wait(topic,json.dumps(message).encode('utf-8'))
        finally:
            await producer.stop()

    async def get_message(self,topic:str, group_id:str):
        consumer = kf_helper.get_consumer(topic,group_id)
        await consumer.start()
        try:
            async for msg in consumer:
                data = json.loads(msg.value.decode("utf-8"))
                if data:
                    print(data,flush=True)
                    # app.send_task("send_email", args=(data.get("token"),data.get("username"),data.get("email")))
                    send_message_email.delay(token = data.get("token"),username = data.get("username"),email = data.get("email"))
                    print("Task sent via send_message_email.delay()", flush=True)
        finally:
            await consumer.stop()

    async def wait_kafka(self,topic:str, group_id:str, retries=10000, delay=20):
        for i in range(retries):
            try:
                consumer = kf_helper.get_consumer(topic,group_id)
                await consumer.start()
                await consumer.stop()
                print("Kafka is ready")
                return
            except Exception as e:
                print(f"Kafka not ready yet ({i+1}/{retries}): {e}")
                await asyncio.sleep(delay)
        raise Exception("Kafka is not available after retries")