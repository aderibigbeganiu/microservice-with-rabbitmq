import json
import pika
import django
from sys import path
from os import environ


# Your path to settings.py file
path.append(
    "/Users/adeleke/Documents/webprojects/microservice-tut/Quotes/Quotes/settings.py"
)
environ.setdefault("DJANGO_SETTINGS_MODULE", "Quotes.settings")
environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()
from quote.models import Quote

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        "localhost", heartbeat=600, blocked_connection_timeout=300
    )
)
channel = connection.channel()
channel.queue_declare(queue="quotes", durable=True)


def callback(ch, method, properties, body):
    print(body)
    data = json.loads(body)
    print(data)

    if properties.content_type == "quote_liked":
        quote = Quote.objects.get(id=data)
        quote.likes += 1
        quote.save()
        print("Quote like increased.")


channel.basic_consume(queue="quotes", on_message_callback=callback)
print("Start consuming")
channel.start_consuming()
channel.close()
