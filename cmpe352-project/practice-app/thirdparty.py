import scholarly
import feedparser

#if one wanted to search for 10 articles that contain the word electron in the title or abstract.
url= "http://export.arxiv.org/api/query?search_query=all:electron&start=0&max_results=10"
#one can also search for articles that contain electron AND proton with the API by entering.
url= "http://export.arxiv.org/api/query?search_query=all:electron+AND+all:proton"
feed = feedparser.parse(url)    

#prints dates,titles,links of all articles searched.
for post in feed.entries:
    date = "(%d/%02d/%02d)" % (post.published_parsed.tm_year,\
        post.published_parsed.tm_mon, \
        post.published_parsed.tm_mday)
    print("post date: " + date)
    print("post title: " + post.title)
    print("post link: " + post.link)
    
#Search for an author by name and return a generator of Author objects.
search_query = scholarly.search_author('Marty Banks, Berkeley')
print(next(search_query))

#Search by keyword and return a generator of Author objects.
search_query = scholarly.search_keyword('Haptics')
print(next(search_query))

# Search for articles/publications and return generator of Publication objects.
search_query = scholarly.search_pubs_query('Perception of physical stability and center of mass of 3D objects')
print(next(search_query))

# Retrieve the author's data, fill-in, and print
search_query = scholarly.search_author('Steven A Cholewiak')
author = next(search_query).fill()
print(author)

# Print the titles of the author's publications
print([pub.bib['title'] for pub in author.publications])

# Take a closer look at the first publication
pub = author.publications[0].fill()
print(pub)

# Which papers cited that publication?
print([citation.bib['title'] for citation in pub.get_citedby()])
