# coding=utf-8
import csv
import json
import requests
import sys
import re

mykey = "[insert your key here]"


def journal_search(query_word):
    journal_search = "https://api.elsevier.com/content/search/scidir?start=0&count=50&query=" + query_word + \
        "+and+content-type%28JL%29&apiKey=" + mykey + "&facets=contenttype(sort=fd);srctitle(sort=fd,count=100)"
    result = requests.get(journal_search)
    j = result.json()['search-results']['facet']
    for item in j[1]['category']:
        print(item['label'] + "--" + item['id'])


def saveto_file(issn, aid, date, name, num, pages):
    filename = issn + ".csv"
    article = [date, aid, name, str(num), pages]
    writer = csv.writer(
        open(
            filename,
            "a"),
        delimiter=' ',
        quotechar='|',
        quoting=csv.QUOTE_MINIMAL)
    writer.writerow(article)


def article_ref_count(aid, entitledToken, sd_session_id):
    ref_search = "http://www.sciencedirect.com/sdfe/arp/pii/" + \
        aid + "/references?entitledToken=" + entitledToken
    result = requests.get(ref_search, cookies={'sd_session_id': sd_session_id})
    try:
        content = result.json()['content'][0]['$$'][1]['$$']
        total_ref = 0
        for ref in content:
            total_ref = total_ref + 1
        return total_ref
    except BaseException:
        return -1


def journal_result(issn):
    issn_search = "http://api.elsevier.com/content/search/scidir?apikey=" + \
        mykey + "&query=issn%28" + issn + "%29&count=100"
    result = requests.get(issn_search)
    j = result.json()['search-results']
    result = requests.get(issn_search)
    print(j['opensearch:totalResults'])
    for item in j['entry']:
        item_page = "http://www.sciencedirect.com/science/article/pii/" + \
            item['prism:url'].split('/')[6]
        # Get cookie and entitledToken
        session = requests.Session()
        response = session.get(item_page)
        sd_session_id = session.cookies.get_dict()['sd_session_id']
        get_entitledToken = re.search(
            r'entitledToken\":\"(.+?)\"', response.text)
        entitledToken = get_entitledToken.group(0).split('\"')[2]
        # Get article Ref number
        ref_num = article_ref_count(
            item['prism:url'].split('/')[6],
            entitledToken,
            sd_session_id)
        if ref_num == -1:
            continue
        else:
            print(
                item['prism:coverDate'][0]['$'] +
                " -- " +
                item['dc:title'] +
                " -- " +
                str(ref_num) +
                " -- " +
                str(int(item['prism:endingPage'])-int(item['prism:startingPage'])+1))
            saveto_file(
                issn,
                item['prism:url'].split('/')[6],
                item['prism:coverDate'][0]['$'],
                item['dc:title'],
                str(ref_num),
                str(int(item['prism:endingPage'])-int(item['prism:startingPage'])+1))


def main():
    journal_finder = input("Please enter search keywords separated by space: ")
    journal_search(journal_finder)
    issn = input("Please fill in journal's ISSN: ")
    journal_result(issn)


if __name__ == '__main__':
    main()
