import json
import pika
from faker import Faker
from mongoengine import connect
from models import Contact

connect(host="mongodb+srv://bogdanbanan:<password>@cluster0.th9cmj6.mongodb.net/?retryWrites=true&w=majority")


connection = pika.BlockingConnection(pika.ConnectionParameters('93.127.115.162'))
channel = connection.channel()


channel.queue_declare(queue='contacts_queue')

def generate_fake_contacts(num_contacts):
    fake = Faker()
    contacts = []
    for _ in range(num_contacts):
        fullname = fake.name()
        email = fake.email()
        contact = Contact(fullname=fullname, email=email)
        contacts.append(contact)
    return contacts


fake_contacts = generate_fake_contacts(10)
for contact in fake_contacts:
    message = json.dumps({'fullname': contact.fullname, 'email': contact.email})
    channel.basic_publish(exchange='', routing_key='contacts_queue', body=message)
    print(f'Sent message: {message}')

connection.close()
