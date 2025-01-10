from django.shortcuts import render
from elasticsearch import Elasticsearch
from .nltk_utils import get_wordnet_info
from .models import City
from django.db import DatabaseError

# Connect to Elasticsearch
es = Elasticsearch("http://localhost:9200")


def search_page(request):
    return render(request, "search/search_page.html")


def query_results(request):
    query = request.GET.get("q", "")

    # Validate the query
    if not query:
        return render(
            request,
            "search/query_results.html",
            {"query": query, "results": [], "nltk_info": None, "random_cities": []},
        )

    results = []

    # Perform search in Elasticsearch
    try:
        response = es.search(
            index="city_data",
            body={"query": {"match": {"content": query}}},
        )
    except Exception as e:
        return render(
            request,
            "search/query_results.html",
            {
                "query": query,
                "results": [{"title": "Error", "content": str(e)}],
                "nltk_info": None,
                "random_cities": [],
            },
        )

    if response["hits"]["total"]["value"] > 0:
        for hit in response["hits"]["hits"]:
            results.append(
                {
                    "title": hit["_source"]["city"],
                    "content": hit["_source"]["content"],
                }
            )
    else:
        results.append({"title": "No results found", "content": ""})

    # Fetch NLTK information (synonyms, definitions, related terms)
    try:
        nltk_info = get_wordnet_info(query)
    except Exception as e:
        nltk_info = None
        # Optionally log the error for debugging
        print(f"Error fetching NLTK information: {e}")

    # Fetch 3 random city names from the database
    try:
        random_cities = City.objects.order_by("?")[:3]
    except DatabaseError as e:
        random_cities = []
        # Optionally log the error for debugging
        print(f"Error fetching cities from database: {e}")

    return render(
        request,
        "search/query_results.html",
        {
            "query": query,
            "results": results,
            "nltk_info": nltk_info,
            "random_cities": random_cities,  # Pass the random cities to the template
        },
    )
