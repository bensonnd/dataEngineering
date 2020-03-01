import requests
import json

def  getMovieTitles(substr):
    endpoint = "https://jsonmock.hackerrank.com/api/movies/search/"
    #https: // jsonmock.hackerrank.com / api / movies / search /?Title = substr & page = pageNumber
    PARAMS = {'Title': substr}
    headers = {'Content-Type': 'application/json'}
    resp = requests.get(endpoint, params = PARAMS, headers=headers)
    respdict = dict(resp.json())
    total_pages = respdict.get('total_pages')
    titles = []
    for i in range(total_pages):
        pagenum = i + 1
        PARAMS = {'Title': substr, 'page': pagenum}
        resp = requests.get(endpoint, params=PARAMS, headers=headers)
        respdict = dict(resp.json())
        items = respdict.get('data')
        for item in items:
            titles.append(item.get('Title', {}))
    return sorted(titles)

_substr = 'spiderman'
res = getMovieTitles(_substr)
for res_cur in res:
    print( str(res_cur) + "\n" )