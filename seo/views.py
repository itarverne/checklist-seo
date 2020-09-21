import string

from nltk.corpus import stopwords
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect

import lxml.html
import json
from collections import Counter
import os
import re

ERROR_JSON = JsonResponse({'error': 'Request wrong formatted'})
NO_KEYWORD_JSON = JsonResponse({"response": "NO_KEYWORD"})


@csrf_protect
def check_keyword(request):
    """Checks if the Keyword is valid"""
    if request.is_ajax():
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            if data == []:
                return ERROR_JSON
            keywords = data[0].lower().split()
            results = {}
            if keywords == []:
                return NO_KEYWORD_JSON
            text = data[1]
            if not text:
                return JsonResponse({"response": "NO_TEXT"})
            table = str.maketrans(dict.fromkeys(string.punctuation))
            words = lxml.html.document_fromstring(text.translate(table)).text_content().split()
            word_counts = Counter(map(str.lower, words))
            nb_words = len(words)
            nb_keyword = 0
            if nb_words != 0:
                for keyword in keywords:
                    nb_keyword += word_counts[keyword]
                percentage = nb_keyword / nb_words * 100
            else:
                percentage = 0
            if percentage <= 3 and percentage > 2:
                results = {'response': "VALID_KEYWORD", 'percentage': percentage}
            else:
                results = {'response': "INVALID_KEYWORD", 'percentage': percentage}
            return JsonResponse(results, safe=True)
    return ERROR_JSON


@csrf_protect
def frequency(request):
    """Returns the frequency of the given word."""
    if request.is_ajax():
        if request.method == 'POST':
            text = json.loads(request.body.decode('utf-8'))
            if not text:
                return ERROR_JSON
            frequencies = []
            table = str.maketrans(dict.fromkeys(string.punctuation))
            word_counts = Counter(map(str.lower, lxml.html.document_fromstring(text.translate(table)).text_content().split()))
            keyword_clean = set(stopwords.words('french'))
            word_counts = word_counts.most_common()
            for word in word_counts:
                if word[0] not in keyword_clean and word != "":
                    frequencies.append(word)
            return JsonResponse(frequencies, safe=False)
    return ERROR_JSON


@csrf_protect
def article_length(request):
    """Returns a code telling if the article is of appropriate length regarding seo rules."""
    if request.is_ajax():
        if request.method == 'POST':
            text = json.loads(request.body.decode('utf-8'))
            if not text:
                return ERROR_JSON
            table = str.maketrans(dict.fromkeys(string.punctuation))
            article_length = len(lxml.html.document_fromstring(text.translate(table)).text_content().split())
            # the code is to use as follow
            # 0 for red (bad seo)
            # 1 for orange (average seo)
            # 2 for green (good seo)
            if (article_length < 900):
                response_code = 0
            elif (article_length >= 900 and article_length < 1400):
                response_code = 1
            elif (article_length >= 1400 and article_length <= 1600):
                response_code = 2
            else:
                response_code = 1
            return JsonResponse({"code": response_code, "length": article_length})
    return ERROR_JSON


@csrf_protect
def check_title(request):
    """Check if the title is valid"""
    if request.is_ajax():
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            if data == []:
                return ERROR_JSON
            title = data[1]
            if not title:
                return JsonResponse({"response": "NO_TITLE"})
            table = str.maketrans(dict.fromkeys(string.punctuation))
            title_words = lxml.html.document_fromstring(title.translate(table)).text_content().split()
            title_word_count = len(lxml.html.document_fromstring(title.translate(table)).text_content().split())
            title_character_count = len(lxml.html.document_fromstring(title.translate(table)).text_content().replace(" ", ""))
            keywords = data[0].lower().split()
            if keywords == []:
                return JsonResponse({"response": "NO_KEYWORD", "character_count": title_character_count, "word_count": title_word_count})
            is_keyword_present = all(elem in title_words for elem in keywords)
            if title_character_count > 70 or (title_word_count < 6 or title_word_count > 13) or not is_keyword_present:
                return JsonResponse({"response": "INVALID_TITLE", "keyword_present": is_keyword_present, "character_count": title_character_count, "word_count": title_word_count})
            return JsonResponse({"response": "VALID_TITLE", "keyword_present": is_keyword_present, "character_count": title_character_count, "word_count": title_word_count})
    return ERROR_JSON


@csrf_protect
def check_slug(request):
    """Check if the slug is valid"""
    if request.is_ajax():
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            if data == []:
                return ERROR_JSON
            keywords = data[0].lower().split()
            if keywords == []:
                return NO_KEYWORD_JSON
            slug = data[1]
            if not slug:
                return JsonResponse({"response": "NO_SLUG"})
            table = str.maketrans(dict.fromkeys(string.punctuation))
            slug_words = lxml.html.document_fromstring(slug.translate(table)).text_content().replace("-", "")
            if not all(elem in slug_words for elem in keywords):
                return JsonResponse({"response": "INVALID_SLUG"})
            return JsonResponse({"response": "VALID_SLUG"})
    return ERROR_JSON


@csrf_protect
def check_internal_links(request):
    """Returns a code telling if the article has enough internal links."""
    if request.is_ajax():
        if request.method == 'POST':
            text = json.loads(request.body.decode('utf-8'))
            if not text:
                return ERROR_JSON
            internal_links_count = len(re.findall("""href=["|']/[^/]{1}""", text)) + len(re.findall(f"""href=["|']http(s)?://{os.environ.get('BASE_URL')}""", text)) + len(
                re.findall("""href=["|']\./""", text)) + len(re.findall("""href=["|']\.\./""", text)) + len(re.findall(f"""href=["|']//{os.environ.get('BASE_URL')}""", text))
            if (internal_links_count == 0):
                response_code = 0
            elif (internal_links_count <= 4):
                response_code = 1
            elif (internal_links_count == 5):
                response_code = 2
            else:
                response_code = 1
            return JsonResponse({"code": response_code, "internal_links": internal_links_count})
    return ERROR_JSON


@csrf_protect
def check_title_in_article(request):
    """Check there are no h1 in the content of the article"""
    if request.is_ajax():
        if request.method == 'POST':
            text = json.loads(request.body.decode('utf-8'))
            if not text:
                return ERROR_JSON
            if (text.find('<h1') != -1):
                return JsonResponse({"response": "H1_PRESENT"})
            return JsonResponse({"response": "NO_H1_PRESENT"})
    return ERROR_JSON
