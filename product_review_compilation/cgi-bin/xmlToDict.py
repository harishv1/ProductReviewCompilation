from lxml import etree

def readXML(file):
    root = etree.parse("xml/"+file+".xml");
    conf = []
    site ={}
    searchParameters = []
    searchTags =[]
    allReviewTags =[]
    reviewHeading =[]
    reviewText =[]
    reviewUpvote =[]
    reviewNextPage =[]
    reviewStarRating = []
    tempDict = {}
    attr = {}
    prevTag =''
    for element in root.getiterator():
        #print element.tag, element.items(), element.text
        if(element.tag == "site") :
            if(site) :
                site['searchTags'] = searchTags
                site['allReviewTags'] = allReviewTags
                site['reviewHeading'] = reviewHeading
                site['reviewText'] = reviewText
                site['reviewUpvote'] = reviewUpvote
                site['reviewNextPage'] = reviewNextPage
                site['reviewStarRating'] = reviewStarRating
                searchTags =[]
                allReviewTags =[]
                reviewHeading =[]
                reviewText =[]
                reviewUpvote =[]
                reviewNextPage =[]
                reviewStarRating = []
                tempDict = {}
                attr = {}
                conf.append(site)
                site = {}
        elif(element.tag == "name"):
            site['name'] = element.text.strip()
        elif(element.tag == "prefix"):
            site['prefix'] = ''
            if element.text:
                site['prefix'] = element.text.strip()
        elif(element.tag == "searchURL"):
            site['searchURL'] = element.text.strip()
        elif(element.tag == "searchParameters"):
            site['searchParameters'] = searchParameters #CHANGE HERE
        elif(element.tag == "searchTags"):
            prevTag = "searchTags"
        elif(element.tag == "reviewStarRating"):
            prevTag = "reviewStarRating"    
        elif(element.tag == "allReviewTags"):
            prevTag = "allReviewTags" 
        elif(element.tag == "reviewHeading"):
            prevTag = "reviewHeading" 
        elif(element.tag == "reviewText"):
            prevTag = "reviewText" 
        elif(element.tag == "reviewUpvote"):
            prevTag = "reviewUpvote" 
        elif(element.tag == "reviewNextPage"):
            prevTag = "reviewNextPage"             
        elif(element.tag == "filter"):
            tempDict = {}
        elif(element.tag == "attributes"):
            if(element.text):
                tempStr = element.text.strip().split('\'')
                attr[tempStr[1]] = tempStr[3] 
                tempDict['attributes'] = attr
                attr ={}
            else :
                tempDict['attributes'] = {}
        elif(element.tag == "recursive"):
            if(element.text):
                if element.text == 'True':
                    tempDict['recursive'] = True
                else:
                    tempDict['recursive'] = False
            else :
                tempDict['recursive'] = True
        elif(element.tag == "tag"):
            if(element.text):
                tempDict['tag'] = element.text.strip()
            else :
                tempDict['tag'] = ''
            if(prevTag == "searchTags") :
                    searchTags.append(tempDict)
            elif(prevTag == "allReviewTags") :
                    allReviewTags.append(tempDict)
            elif(prevTag == "reviewHeading") :
                    reviewHeading.append(tempDict)
            elif(prevTag == "reviewText") :
                    reviewText.append(tempDict)
            elif(prevTag == "reviewUpvote") :
                    reviewUpvote.append(tempDict)
            elif(prevTag == "reviewNextPage") :
                    reviewNextPage.append(tempDict)
            elif(prevTag == "reviewStarRating") :
                    reviewStarRating.append(tempDict)     
                
                
    site['searchTags'] = searchTags
    site['allReviewTags'] = allReviewTags
    site['reviewHeading'] = reviewHeading
    site['reviewText'] = reviewText
    site['reviewUpvote'] = reviewUpvote
    site['reviewNextPage'] = reviewNextPage
    site['reviewStarRating'] = reviewStarRating
    conf.append(site)
    return conf


        
    
