from django.shortcuts import render
from elasticsearch import Elasticsearch
from .nltk_utils import get_wordnet_info  

# Connect to Elasticsearch
es = Elasticsearch("http://localhost:9200")


def search_page(request):
    return render(request, "search/search_page.html")


def query_results(request):
    query = request.GET.get("q", "")

    # Perform search in Elasticsearch
    response = es.search(
        index="city_data",  
        body={"query": {"match": {"content": query}}},
    )

    results = []
    if response["hits"]["total"]["value"] > 0:
        for hit in response["hits"]["hits"]:
            # Extract relevant data from the search hit
            results.append(
                {
                    "title": hit["_source"][
                        "city"
                    ],  # You can change this based on your document structure
                    "content": hit["_source"]["content"],
                }
            )
    else:
        results.append({"title": "No results found", "content": ""})

    # Fetch NLTK information (synonyms, definitions, related terms)
    nltk_info = get_wordnet_info(query)
    
    return render(
        request,
        "search/query_results.html",
        {
            "query": query,
            "results": results,
            "nltk_info": nltk_info,
        },
    )
