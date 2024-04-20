from mongoengine import connect
from models import Author, Quote


connect(host='mongodb+srv://username:password@your-cluster-url/database-name')

def search_quotes(query):
    
    command, value = query.split(':')
    
    
    if command == 'name':
        author = Author.objects(fullname__icontains=value).first()
        if author:
            quotes = Quote.objects(author=author)
            return quotes.to_json()

    # Пошук за тегом або набором тегів
    elif command == 'tag' or command == 'tags':
        tags = value.split(',')
        quotes = Quote.objects(tags__in=tags)
        return quotes.to_json()

    return 'No quotes found.'


while True:
    query = input('Enter search command (name:author_name, tag:tag_name, tags:tag1,tag2): ')
    if query.lower() == 'exit':
        break
    result = search_quotes(query)
    print(result)
