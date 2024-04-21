import json
import pika
from time import sleep


connection = pika.BlockingConnection(pika.ConnectionParameters('93.127.115.162'))
channel = connection.channel()


channel.queue_declare(queue='contacts_queue')

def send_email(contact_data):
    
    print(f'Sending email to {contact_data["email"]}: Hello, {contact_data["fullname"]}!')

def callback(ch, method, properties, body):
    contact_data = json.loads(body)
    send_email(contact_data)
    sleep(1)  
    print(f'Received message: {body}')

channel.basic_consume(queue='contacts_queue', on_message_callback=callback, auto_ack=True)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
