from django.shortcuts import render
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Joke
from .serializers import JokeSerializer
from .utils import joke_urls

JOKE_API_URL = joke_urls

@api_view(['GET'])
def fetch_jokes(request):
    response = requests.get(JOKE_API_URL)
    
    if response.status_code != 200:
        return Response({"error": "Failed to fetch jokes"}, status=500)

    jokes_data = response.json().get('jokes', [])

    joke_objects = []

    for joke in jokes_data:
        joke_obj = Joke(
            category=joke["category"],
            joke_type=joke["type"],
            joke=joke.get("joke", None),
            setup=joke.get("setup", None),
            delivery=joke.get("delivery", None),
            nsfw=joke["flags"]["nsfw"],
            political=joke["flags"]["political"],
            sexist=joke["flags"]["sexist"],
            safe=joke["safe"],
            lang=joke["lang"],
        )
        joke_objects.append(joke_obj)

    print(f"*************{joke_objects}")

    Joke.objects.bulk_create(joke_objects)

    return Response({"message": f"{len(joke_objects)} jokes stored successfully!"})

@api_view(['GET'])
def list_jokes(request):
    """Retrieve all stored jokes"""
    jokes = Joke.objects.all()
    serializer = JokeSerializer(jokes, many=True)
    return Response(serializer.data)

