import os, random

import cherrypy


class WordOven(object):
    @cherrypy.expose
    def healthcheck(self):
        return 'aok!'

    @cherrypy.expose
    @cherrypy.popargs('word')
    def bake(self, word):
        image = word_to_image(word)
        return image_to_html_ascii(image)


def word_to_image(word):
    from asciiart.shortcuts import image_from_url
    import requests

    FAIL_URL = 'http://www.clipartbest.com/cliparts/pi5/obz/pi5obzriB.jpeg'

    r = requests.get('http://pixabay.com/api/', params={
        'username': os.environ['PIXABAY_USERNAME'],
        'key': os.environ['PIXABAY_KEY'],
        'q': word
    })
    urls = [hit['webformatURL'] for hit in r.json()['hits']]
    return image_from_url(random.choice(urls) if urls else FAIL_URL)


def image_to_html_ascii(image):
    from asciiart.parsers import HtmlColorParser

    return HtmlColorParser(image).parse(180, 60)


if __name__ == '__main__':
    cherrypy.config.update({
        'environment': 'production',
        'server.socket_host': '0.0.0.0',
        'log.screen': True
    })
    cherrypy.quickstart(WordOven())
