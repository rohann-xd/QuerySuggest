from django.shortcuts import render
import random


def search_page(request):
    return render(request, "search/search_page.html")


def query_results(request):
    query = request.GET.get("q", "")

    # Mimic dynamic data: Generate a random number of results
    possible_results = [
        {"title": "Django Documentation", "url": "https://docs.djangoproject.com/"},
        {"title": "Python Official Website", "url": "https://www.python.org/"},
        {"title": "Learn Django", "url": "https://www.djangoproject.com/start/"},
        {"title": "GitHub", "url": "https://github.com/"},
        {"title": "Stack Overflow", "url": "https://stackoverflow.com/"},
    ]
    results = random.sample(possible_results, random.randint(0, len(possible_results)))

    return render(
        request, "search/query_results.html", {"query": query, "results": results}
    )
