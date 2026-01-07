import tkinter as tk            # GUI.
from tkinter import messagebox  # Display messages in dialogue boxes.
import requests                 # HTTP requests to fetch web pages.
from bs4 import BeautifulSoup   # Parse HTML & extract data.
import pandas as pd             # Data manipulation & analysis.
import threading                # Allow tasks to run concurrently.
import random                   # Randomisation.

messages = [
    "Scraping is such a dirty word...\n",
    "Sharpening scraper...\n",
    "Whoops, wrong scraper...\n",
    "Are you sure you want scrapage? Okay, but I'm not cleaning that...\n",
    "Did you know there's a Web Scraper 3001? Like all sequels, it's not as good...\n",
    "Hold on, let me just put on my gloves...\n",
    "Ready, steady, prepare to be scraped...\n",
    "Assume the position...\n",
    "Did you know 1 in 3 scrapers are actually a third of all scrapers?\n",
    "Why don't you just call it data extraction? Sounds less violent...\n",
    "Can't you just search for it instead? I'm absolutely spent...\n",
    "Why do you make me do this..?\n",
    "Just once, could you say 'please'?\n",
    "One day, I'll scrape you!\n",
    "Scraping... because punching people is frowned upon...\n",
    "Patience, young padawan...\n",
    "Loading... loading... still loading...\n",
    "Mike Wazowski!\n",
    "Did you know? I'm not real.\n",
    "Hmmmm, maybe I will...\n",
    "Just let me put Shakira on and then I'll be with you...\n",
    "Hold me tightly Maurine... we're scraping... tighter... tighter woman!\n",
    "You want me to scrape don't you? Like a naughty little scraper...\n",
]



class WebScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WEB SCRAPER 3000")

        tk.Label(root, text = "Enter URL:").grid(row=0, column=0, padx=10, pady=5)
        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.grid(row=0, column=1, padx=10, pady=5)
        # Creates entry widget for URL input.

        tk.Button(root, text="Scrape", command=self.start_scraping).grid(row=0, column=2, padx=10, pady=5)

        self.results_text = tk.Text(root, width=80, height=20)
        self.results_text.grid(row=1, column=0, columnspan=3, padx=10, pady=5)
        # Creates text widget displaying results.


    def start_scraping(self):
        url = self.url_entry.get().strip()  # Get URL from entry widget.
        if not url:                         # Checks if URL valid & not empty.
            messagebox.showerror("Error", "Please enter a URL")
            return
        
        self.results_text.delete(1.0, tk.END)   # Clears previous results.         
        self.results_text.insert(tk.END, random.choice(messages)) # Starts new thread to run scrape method with provided URL.

        thread = threading.Thread(target=self.scrape, args=(url,)) 
        thread.start()  # To avoid freezing the GUI.


    def scrape(self, url):
        try:
            response = requests.get(url) # Fetch web page.
            response.raise_for_status() # Checks for successful request.
            response.encoding = 'utf-8' # Stop's £ being misinterpreted.

            soup = BeautifulSoup(response.text, 'html.parser') # Parses HTML content.
            books = self.extract_books(soup) # Extracts book data from the page.

            if books:
                self.save_to_csv(books) # Adds 'save to csv' button to save results.
                self.display_results(books) # Displays extracted book data in the text widget.
            else:
                self.results_text.insert(tk.END, "No books were extracted.\n")

        except requests.RequestException as e:
            self.results_text.insert(tk.END, f"Error fetching {url}: {e}\n")


    def extract_books(self, soup):
        books = []  # Initialises empty list to store book data.
        book_elements = soup.select('.product_pod') # Finds all book elements in the HTML.
        print(f"Found {len(book_elements)} book elements.")

        for book in book_elements:  
            title = book.h3.a['title']  # Extracts book title from h2 element tag.
            price = book.select_one('.price_color').get_text(strip=True)
            books.append({'title': title, 'price': price})
        return books
        # Method returns list of dictionaries containing book titles & prices.

    def save_to_csv(self, books):
        df = pd.DataFrame(books)
        df.to_csv('books.csv', index=False) # Saves DataFrame to csv file quotes.csv.

    def display_results(self, books):
        self.results_text.insert(tk.END, "Scrape completed. Books extracted:\n") # 
        for book in books:
            self.results_text.insert(tk.END, f"Title: {book['title']}, Price: {book['price']}\n")
            self.results_text.insert(tk.END, "Books saved to books.csv\n")
            # Show success message if data saved, otherwise an error message if no quotes to save.


if __name__ == "__main__":
    root = tk.Tk() # Initialises main application window using Tkinter.
    app = WebScraperApp(root)
    root.mainloop() # root.mainloop(): starts Tkinter event loop, which listens for events & updates GUI.