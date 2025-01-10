import nltk
from nltk.corpus import wordnet

# Download NLTK data if not already done
nltk.download('wordnet')
nltk.download('omw-1.4')

# Function to get WordNet information (synonyms, definitions, related words)
def get_wordnet_info(word):
    synonyms = set()
    definitions = set()  # Using a set to prevent duplicate definitions
    related_words = set()

    # Check if the word has any synsets in WordNet
    synsets = wordnet.synsets(word)
    if not synsets:
        return {"synonyms": [], "definitions": [], "related_words": [], "message": "No data found for this word in WordNet"}

    # Collect synonyms, antonyms, and related words from synsets
    for syn in synsets:
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())  # Add synonym word form
            if lemma.antonyms():
                synonyms.add(lemma.antonyms()[0].name())  # Add antonym if present

        # Collect definitions
        definitions.add(syn.definition())

        # Collect related words (hypernyms, hyponyms) and their lemma names
        for hypernym in syn.hypernyms():
            for lemma in hypernym.lemmas():
                related_words.add(lemma.name())
        for hyponym in syn.hyponyms():
            for lemma in hyponym.lemmas():
                related_words.add(lemma.name())

    # Return the data in a structured form
    return {
        "synonyms": list(synonyms),
        "definitions": list(definitions),
        "related_words": list(related_words),
        "message": "Data retrieved successfully",
    }
