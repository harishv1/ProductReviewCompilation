from bs4 import BeautifulSoup
import urllib2
import xmlToDict

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
    return page.find('a')['href']

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
        
        number = int(temp_tags[1][0 : -1])
        temp_results = page.find_all(name = temp_tags[0], attrs = tags[level]['attributes'], limit = number, recursive = False)
        print page
        temp_results = [temp_results.pop()]
    else:
        temp_results = page.find_all(name = tags[level]['tag'], attrs = tags[level]['attributes'], recursive = tags[level]['recursive'])
    for result in temp_results:
        res = readTagFromHTML(tags, level + 1, result, resultList, endFunc)
        if level == len(tags) - 1:
            resultList.append(res)

def readHTML(url):
    page = urllib2.urlopen(url)
    return BeautifulSoup(page.read(), "html.parser")

def mainFunction(product):

    sites = xmlToDict.readXML('flipkart')
    for site in sites:
        #product = 'Dell Inspiron 15 3521 Laptop (3rd Gen Ci3/ 4GB/ 500GB/ Win8)'

        searchPage = readHTML(site['searchURL'] + (product))
        productLinks = getLinkFromHTML(site['searchTags'], searchPage)
        productPage = readHTML(site['prefix'] + productLinks[0])
        if site['allReviewTags']:
            reviewsLink = getLinkFromHTML(site['allReviewTags'], productPage)
        else:
            reviewsLink = productLinks
        
        reviewPage = readHTML(site['prefix'] + reviewsLink[0])
        reviewsHeading = getTagFromHTML(site['reviewHeading'], reviewPage)
        reviewsText = getTagFromHTML(site['reviewText'], reviewPage)
        reviewsUpvotes = getTagFromHTML(site['reviewUpvote'], reviewPage)
        reviewStars = getTitleFromHTML(site['reviewStarRating'], reviewPage)

        nextPage = getLinkFromHTML(site['reviewNextPage'], reviewPage)
        if len(nextPage) > 0:
            reviewPage = readHTML(site['prefix'] + nextPage[0])
            reviewsHeading += getTagFromHTML(site['reviewHeading'], reviewPage)
            reviewsText += getTagFromHTML(site['reviewText'], reviewPage)
            reviewsUpvotes += getTagFromHTML(site['reviewUpvote'], reviewPage)
            reviewStars += getTitleFromHTML(site['reviewStarRating'], reviewPage)
        
        reviews = []
        for i in range(len(reviewsHeading)):
            review = {}

            review['heading'] = reviewsHeading[i]
            a = reviewsUpvotes[ 2 * i]
            if reviewsUpvotes[ 2 * i].find('%') >= 0:
                a = reviewsUpvotes[2 * i][0:reviewsUpvotes[ 2 * i].find('%')]
                a = int(a)
                b = int(reviewsUpvotes[2 * i + 1])
                a = a * b / 100
            review['upvotes'] = [ str(a), reviewsUpvotes[2 * i + 1]]
            review['stars'] = reviewStars[i].split(' ')[0]

            reviewTextSplit = reviewsText[i].split('.')
            finalText = ''
            for jj in reviewTextSplit:
                if(jj.find('Flipkart') == -1 and jj.find('flipkart') == -1 and jj.find('delivered') == -1  and jj.find('delivery') == -1):
                    finalText += jj
                    finalText += '. '
            review['text'] = finalText
            
            reviews.append(review)
    return reviews
