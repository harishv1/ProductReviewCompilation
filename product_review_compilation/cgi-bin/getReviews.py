import cgi
import flipkart
import amazon
import json
import sentiment_analysis

form = cgi.FieldStorage()

search = form['search'].value

flipkartReviews = flipkart.mainFunction(search)
amazonReviews = amazon.mainFunction(search)
res = sentiment_analysis.mainFunction(flipkartReviews + amazonReviews)
print 'Content-type:text/html\n\n'
outerJSON = [
    res, 
flipkartReviews,
amazonReviews
]

print json.dumps(outerJSON, indent=4)
