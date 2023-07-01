import json
from django.shortcuts import render
from django.views import View

class MovieView(View):
    def get(self, request):
        with open("movies/index.json") as f:
            movies = json.load(f)

        all_genres = list(set(genre for movie in movies for genre in movie["genres"]))

        # Filter movies by genre
        genre_filter = request.GET.getlist("genre")
        if genre_filter:
            filtered_movies = [movie for movie in movies if any(genre in movie["genres"] for genre in genre_filter)]
        else:
            filtered_movies = movies

        # Search movies by title
        search_query = request.GET.get("search")
        if search_query:
            filtered_movies = [movie for movie in filtered_movies if search_query.lower() in movie["title"].lower()]

        context = {
            "movies": filtered_movies,
            "genres": all_genres,
            "genre_filter": genre_filter,
            "search_query": search_query,
        }

        return render(request, "movies/index.html", context)
