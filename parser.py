from bs4 import BeautifulSoup
import urllib2

def getLinkFromHTML(tags, page):
    result = []
    readTagFromHTML(tags, 0, page, result, getLink)
    return result

def getHTMLFromHTML(tags, page):
    result = []
    readTagFromHTML(tags, 0, page, result, getHTML)
    return result

def getTagFromHTML(tags, page):
    result = []
    readTagFromHTML(tags, 0, page, result, getText)
    return result

def getTitleFromHTML(tags, page):
    result = []
    readTagFromHTML(tags, 0, page, result, getTitle)
    return result

def getLink(page):
    if page.has_attr('href'):
        return page['href']
    link = page.find('a')
    if link:
        return link['href']
    return None

def getTitle(page):
    return page['title']

def getHTML(page):
    return page

def getText(page):
    return page.text.strip()

def readTagFromHTML(tags, level, page, resultList, endFunc):
    if level == len(tags):
        return endFunc(page)
    
    if 'tag' not in tags[level]:
        tags[level]['tag'] = ''
    if 'attributes' not in tags[level]:
        tags[level]['attributes'] = {}
    if 'recursive' not in tags[level]:
        tags[level]['recursive'] = True

    if tags[level]['tag'].find('[') >= 0:
        
        temp_tags = tags[level]['tag'].split('[')
        #tags[level]['tag'] = temp_tags[0]
        
        number = int(temp_tags[1][0 : -1])
        print level, "page.find_all(name = "+temp_tags[0]+", attrs = "+str(tags[level]['attributes'])+", limit = "+str(number)+", recursive = False)"
        temp_results = page.find_all(name = temp_tags[0], attrs = tags[level]['attributes'], limit = number, recursive = False)
        temp_results = [temp_results.pop()]
    else:
        print level, "page.find_all(name = "+tags[level]['tag']+", attrs = "+str(tags[level]['attributes'])+", recursive = "+str(tags[level]['recursive'])+")"
        temp_results = page.find_all(name = tags[level]['tag'], attrs = tags[level]['attributes'], recursive = tags[level]['recursive'])

    for result in temp_results:
        res = readTagFromHTML(tags, level + 1, result, resultList, endFunc)
        if level == len(tags) - 1:
            resultList.append(res)

def readHTML(url):
    page = urllib2.urlopen(url)
    return BeautifulSoup(page.read(), "html.parser")


#page = readHTML('https://www.amazon.com/s/?url=field-keywords=Dell Inspiron 15 3521 Laptop (3rd Gen Ci3/ 4GB/ 500GB/ Win8) ')
#tags = [{'attributes' : {'class':'prod'} }, {'attributes' : {'class':'rvwCnt'}}]
#print getTagFromHTML(tags, page)

review_attributes = [
{'id' : 'productReviews' },
{},
{},
]


review_tags = [
{'tag':'table', 'attributes':{'id':'productReviews'}},
{'tag':'td'},
{'tag':'div', 'recursive':False},
{'tag':'div[2]', 'recursive':False},
{'tag':'span[1]', 'recursive':False}
]
review_url = 'http://www.amazon.com/product-reviews/B004JASEMS/ref=acr_dpinstantvideo_text?ie=UTF8&showViewpoints=1'

result = getTagFromHTML(review_tags, readHTML(review_url))
print (result)
