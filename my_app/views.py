import requests
from django.shortcuts import render
from requests.compat import quote_plus
from bs4 import BeautifulSoup
from . import models

BASE_CRAIGSLIST_URL = 'https://losangeles.craigslist.org/search/?query={}'
BASE_IMAGE_URL = "https://images.craigslist.org/{}_300x300.jpg"


def home(request):
    """
    Handles request for home directory
    """

    return render(request, 'base.html')


def new_search(request):
    """
    Handles request for new searches and renders a list of results
    """

    search = request.POST.get('search')

    models.Search.objects.create(search=search)

    # quote_plus joins search query keywords with '+' delimiters (e.g "experienced+python+tutor") 
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))

    # gets the response object from the specified '@url' argument.
    response = requests.get(final_url)

    # returns the HTML source code of response
    data = response.text

    # create a soup object for the source code
    soup = BeautifulSoup(data, features='html.parser')

    # returns all list items with class="result-row"
    post_listings = soup.find_all('li', {'class': 'result-row'})

    final_postings = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_='result-price'):
            post_price = post.find(class_ = 'result-price').text
        else:
            post_price = 'N/A'

        if post.find(class_="result-image").get('data-ids'):
            post_image_id = post.find(class_="result-image").get('data-ids').split(',')[0].split(':')[1]       
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
        else:
            post_image_url = "https://craigslist.org/images/peace.jpg"
            

        final_postings.append((post_title, post_url, post_price, post_image_url))

    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings[:12],
    }

    return render(request, 'search_app/new_search.html', stuff_for_frontend)