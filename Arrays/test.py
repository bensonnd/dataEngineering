import requests
import json

# Complete the function below.
# Base url: https://jsonmock.hackerrank.com/api/movies/search/?Title=

endpoint = "https://jsonmock.hackerrank.com/api/movies/search/json"
headers = {'Content-Type': 'application/json'}
def  getMovieTitles(substr):
    endpoint = "https://jsonmock.hackerrank.com/api/movies/search/json"
    headers = {'Content-Type': 'application/json'}
    PARAMS = {'Title': substr}
    resp = requests.get(endpoint, params = PARAMS, headers=headers)

    respdict = dict(resp.json())
    totalPages = respdict.get('total_pages')
    titles = []
    for pageNumber in range(totalPages):
        PARAMS = {'Title': substr, 'page': pageNumber + 1}
        resp = requests.get(endpoint, params = PARAMS, headers=headers)
        items = respdict.get('data')
        for item in items:
            titles.append(item.get('Title', {}))
    return sorted(titles)
try:
    _substr = 'spiderman'
except:
    _substr = None

res = getMovieTitles(_substr)
print(res)