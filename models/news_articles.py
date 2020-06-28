# -*- coding: utf-8 -*-
from eventregistry import *
er = EventRegistry(apiKey = '')

def load_news_data(keywords,lang):

    q = QueryArticlesIter(

    keywords = keywords,
    keywordsLoc = "body",

    locationUri = er.getLocationUri(keywords),

    lang = lang,
    dataType = "news")

    news_list = []

    for article in q.execQuery(er, sortBy = "rel", maxItems = 10):
        
        news = {}
        news['title'] = article['title']
        news['date'] = article['date']
        news['source'] = article['source']['uri']
        news['url'] = article['url']
        news['body'] = article['body']

        news_list.append(news)

    return news_list


# sample news_list == an array of news articles
#
# load_news_data("Hannover","eng")
#
# [
#     {
#         'title': 'Hannover Marketing: Travelling Without moving - Virtual Hannover Vacation'

#         'date': '2020-03-30'

#         'source': 'finanznachrichten.de'

#         'url': 'https://www.finanznachrichten.de/nachrichten-2020-03/49240532-hannover-marketing-travelling-without-moving-virtual-hannover-vacation-008.htm'

#         'body': 'HANNOVER, Germany, March 30, 2020 /PRNewswire/ -- Hannover Marketing und Tourism has launched a new initiative "Traveling without moving," the digital 360° tours from Hannover. As the name suggests, it aims to make seeing the city possible without having to leave home. Hannover can be visited virtually and, depending on the users interests, they can embark on a tour of the Herrenhausen Gardens, the New Town Hall, Marienburg Castle or discover the Maschsee. The VR excursions to sights like the Hannover Adventure Zoo, also provides inspiration for future trips, whether through the Deister hills, around the Steinhuder Meer or through the Hannover old town. Hans Christian Nolte, Managing Director of Hanover Marketing and Tourism GmbH (HMTG), comments: "Now that people have to spend most of their time at home, we just want to bring the vacation into your living room. Hannover fans can take a digital tour with their mobile phone, tablet or PC and go out and make plans for when the current measures to contain the corona pandemic have passed. We look forward to welcoming guests in person again soon." The perspectives of the VR tours should give the sights a special poignancy and make visiting both well-known and unknown locations a new experience through the personalized camera work. The HMTG is also participating in the current closedbutopen campaign, in which many places that are currently closed can still be visited virtually. All tours can be found at: http://www.visit-hannover.com/en/360. Hannover Marketing und Tourism GmbH has "Hannover Tourism" available via its Facebook channels while "Visit Hannover" has reached around 350,000 people online, receiving approximately 30,000 interactions. International visitors and Hanover fans will also see the campaign in the Netherlands, Belgium and Denmark as well as Switzerland, Austria, England and Spain. Marketing activities are continuing to expand into different travel markets.'
#     }
# ]