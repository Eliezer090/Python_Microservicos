# amqps://tdgsviob:K8mIDKp1mJbc_AZzZ9AeJh6iDNyQq4cA@shark.rmq.cloudamqp.com/tdgsviob
import pika, json

params = pika.URLParameters(
    'amqps://tdgsviob:K8mIDKp1mJbc_AZzZ9AeJh6iDNyQq4cA@shark.rmq.cloudamqp.com/tdgsviob')

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(
        exchange='', routing_key='admin', body=json.dumps(body), properties=properties)
