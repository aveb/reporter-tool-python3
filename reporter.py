#!/usr/bin/env python3

#Needed to install psycopg2 again using:
#sudo apt-get install python3 python-dev python3-dev
#sudo pip3 install psycopg2
import psycopg2

# try connecting to the news database!
try:
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
except psycopg2.DatabaseError:
    print("Could not connect to News database")

#sql queries to run:
query1 = """
          select articles.title, count(log.path) from articles, log
          where articles.slug = REPLACE(log.path, '/article/', '')
          group by articles.title order by count(log.path) desc limit 3;
        """
query2 = """
          select articles_authors.name, count(log.path)
          from articles_authors, log
          where articles_authors.slug = REPLACE(log.path, '/article/', '')
          group by articles_authors.name order by count(log.path) desc;
         """
query3 = "select d, percentage from percentages where percentage > 1;"

#method to run queries, returns results
def newsQuery(q):
  c.execute(q)
  result = c.fetchall()
  return result


pop_articles = newsQuery(query1)
pop_author = newsQuery(query2)
errs = newsQuery(query3)

#close connection to database
db.close()

# Print top three articles sorted by views
print("Top 3 most popular articles by views")
for i in pop_articles:
    print ("  ", i[0], "--", i[1], " views")

# Print authors sorted by views
print("\n","Author's Popularity by views")
for auth in pop_author:
    print("  ", auth[0], "--", auth[1], " total views")

# Print date where more than 1% 404
print("\n","Dates where more than 1 percent of requests returned errors")
for var in range(len(errs)):
    print("  ", errs[var][0].strftime("%B %d, %Y"),
          "--", round(errs[var][1], 2), "percent")


