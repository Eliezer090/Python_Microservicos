import pika, json, os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()
from products.models import Product

params = pika.URLParameters(
    'amqps://tdgsviob:K8mIDKp1mJbc_AZzZ9AeJh6iDNyQq4cA@shark.rmq.cloudamqp.com/tdgsviob')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='admin')


def callback(ch, method, properties, body):
    print("Received admin ", body)
    id =json.loads(body)
    print(id)
    product = Product.objects.get(id=id)
    product.likes = product.likes+1
    product.save()
    print('Product '+str(id)+' likes increase')


channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

print("Start consuming")
channel.start_consuming()
channel.close()
