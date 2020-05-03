#http://quotes.toscrape.com/

import requests
from bs4 import BeautifulSoup
import csv
from random import randrange

#variables
url_heading = "http://quotes.toscrape.com"
all_quotes, texts, authors, bios = [],[],[],[]
next_page = 2 
num_chances = 4

def scrape_site(soup,has_next, next_page):
    while(has_next):
        has_next = soup.select(".next")
        page_quotes = soup.select(".quote")
        all_quotes.extend(page_quotes)
        new_url = f"{url_heading}/page/{next_page}"
        response = requests.get(new_url)
        soup = BeautifulSoup(response.text, "html.parser")
        next_page += 1

    for quote in all_quotes:
        texts.append(quote.find("span").get_text())
        authors.append(quote.find("small").get_text())
        bios.append(quote.find("a")["href"])

def play_game(num_chances):
    continue_playing = True
    print("*****Welcome to the quote guessing game!*****")
    print(f"*****I'll give you a quote and you'll have {num_chances} chances to guess the author!*****")
    print("*****Here's your first quote!*****")
    while(continue_playing):
        random_index = randrange(len(all_quotes))
        answer = authors[random_index]
        bio_link = f"{url_heading}{bios[random_index]}"
        invalid_response = True
        num_chances = 4
        print(texts[random_index])
        while num_chances > 0:
            print(f"{num_chances} guesses remaining.")    
            guess = input("Please Guess An Author (Full Name): ")
            num_chances -= 1
            if guess.upper() == answer.upper():
                print("*****YOU WIN!*****")
                break
            else:
                if(num_chances == 0):
                    print(f"Sorry you've run out of guesses. The answer was: {answer}")
                else:
                    print(give_hint(num_chances, bio_link, answer))
        while(invalid_response):
            response = input("Would you like to play again? (Y/N)")
            if response == 'N' or response == 'n':
                continue_playing = False
                invalid_response = False
                print("Thank you for playing! Goodbye :)")
            elif response == 'Y' or response == 'y':
                print("Next round!")
                invalid_response = False
            else:
                print("Please respond with a (Y/N)")
        invalid_response = True

def give_hint(chances, url, author):
    if chances == 3:
        return scrape_bio(url)
    elif chances == 2:
        return f"The author's first name starts with: {author[0]}"
    elif chances == 1:
        return f"The author's last name starts with: {author.split(' ')[1][0]}"

def scrape_bio(url):
    response_bio = requests.get(url)
    soup_bio = BeautifulSoup(response_bio.text,"html.parser")
    author_birthday = soup_bio.find(class_="author-born-date").get_text() 
    author_birthplace = soup_bio.find(class_="author-born-location").get_text() 
    return f"The author was born in {author_birthplace} on {author_birthday}."


#Request Logic 
response = requests.get(url_heading)
soup = BeautifulSoup(response.text, "html.parser")
has_next = soup.select(".next")
scrape_site(soup, has_next, next_page)
play_game(num_chances)

