from selenium import webdriver
import time
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import pandas as pd

data = {
    'book_title': [],
    'author': [],
    'book_url': [],
    'cover_img_url': []
}

df = pd.DataFrame(data)

"""Scrolls the driver to the bottom of the page."""
def scroll_to_bottom(driver):
  
  

  scroll_from = 0
  scroll_range = 1000
  scroll_to = scroll_range
  for i in range(141):
        time.sleep(5)
        scroll_js = "window.scrollTo(%i, %i)" % (scroll_from, scroll_to)
        scroll_from += scroll_range
        scroll_to += scroll_range
        driver.execute_script(scroll_js) 

        time.sleep(6)
        print(i)


options = Options()
driver = webdriver.Firefox(options=options) 
free_book_url = "https://taaghche.com/filter?filter-custom=2&filter-bookType=0&filter-target=0&order=7"
driver.get(free_book_url)

# Scroll to the bottom of the page.
scroll_to_bottom(driver)

# Get all of the HTML from the page.
html = driver.page_source

soup = BeautifulSoup(html, "html.parser")
book_card_elements = soup.select("div[class^='bookCard_book_']")

for book_card_element in book_card_elements:

   soup = BeautifulSoup(str(book_card_element), "html.parser")
   results = soup.findAll("a", {"rel" : "nofollow"})
   # print(results[0]['href'].rsplit('/', 1)[0])

   book_url = results[0]['href'].rsplit('/', 1)[0]
   results = soup.select("img[class^=bookCard_bookCover__]")
   # print(results[0]['src'].rsplit('?', 1)[0])

   img_url = results[0]['src'].rsplit('?', 1)[0]
   results = soup.select("div[class^=bookCard_bookTitle__]")
   book_title = results[0].text

   results = soup.select("div[class^=bookCard_bookAuthor__]")
   if(len(results) < 1):
      continue
   book_author = results[0].text

   new_row = [book_title, book_author, book_url, img_url]

   df.loc[len(df)] = new_row

   df.to_csv("taaghche_free_books.csv", index=True, encoding="utf-8-sig")


# print(df.head(50))
driver.close()


    