import redis
from mongoengine import connect
from models import Author, Quote


redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


connect(host="mongodb+srv://bogdanbanan:<password>@cluster0.th9cmj6.mongodb.net/?retryWrites=true&w=majority")

def search_quotes(query):

    if redis_client.exists(query):
        return redis_client.get(query)

    command, value = query.split(':')
    

    if command == 'name':
        author = Author.objects(fullname__icontains=value).first()
        if author:
            quotes = Quote.objects(author=author)
            result = quotes.to_json()
            
            redis_client.setex(query, 60, result)
            return result

    
    elif command == 'tag' or command == 'tags':
        tags = value.split(',')
        quotes = Quote.objects(tags__in=tags)
        result = quotes.to_json()
        
        redis_client.setex(query, 60, result)
        return result

    return 'No quotes found.'


while True:
    query = input('Enter search command (name:author_name, tag:tag_name, tags:tag1,tag2): ')
    if query.lower() == 'exit':
        break
    result = search_quotes(query)
    print(result)
