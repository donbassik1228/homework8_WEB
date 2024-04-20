import json
from mongoengine import connect
from models import Author


connect(host="mongodb+srv://bogdanbanan:<password>@cluster0.th9cmj6.mongodb.net/?retryWrites=true&w=majority")


with open('authors.json', 'r', encoding='utf-8') as file:
    authors_data = json.load(file)


for author_data in authors_data:
    author = Author(**author_data)
    author.save()
