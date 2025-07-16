# Web Crawler Attempt

# necessary libraries for GUI of web crawler.

import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import pandas as pd
import threading

# tkinter creates GUI.
# messagebox is used to display messages in dialogue boxes.
# requests makes HTTP requests to fetch web pages.
# BeautifulSoup is used to parse HTML and extract data.
# threading allows tasks to run concurrently.
# pandas is used for data manipulation and analysis.

class WebCrawlerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Web Crawler 3000")

        tk.Label(root, text = "Enter URL:").grid(row=0, column=0, padx=10, pady=5)
        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.button(root, text="Start Crawling", command=self.start_crawling).grid(row=0, column=2, padx=10, pady=5)

        self.results_text = tk.Text(root, width=80, height=20)
        self.results_text.grid(row=1, column=0, columnspan=3, padx=10, pady=5)
        

# __innit__ is a constructor method for the webcraler class.
# tk.label creates an entry widget for URL input.
# self.results create a text widget displaying results.
# Adds a 'save to csv' button to save results.

    def start_crawling(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a URL")
            return
        
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "Starting Crawl...\n")

        thread = threading.Thread(target=self.crawl, args=(url,))

# Method gets URL from entry widget.
# Checls if URL valid & not empty.
# Starts a new thread to run crawl method with provided URL
# to avoid freezing the GUI.

    def crawl(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            books = self.extract_books(soup)

            if books:
                self.save_to_csv(books)
                self.display_results(books)
            else:
                self.results_text.insert(tk.END, "No books were extracted.\n")

        except requests.RequestException as e:
            self.results_text.insert(tk.END, f"Error fetching {url}: {e}\n")

# Method clears text widget before crawl, web page fetch using requests.get.
# Checks for successful request using raise_for_status.
# Parses HTML content with BeautifulSoup.
# Finds all elements with the class quote and extracts texts and author for each quote.
# Stores extracted quote in quotes list and displays them in widget.

    def extract_books(self, soup):
        books = []
        book_elements = soup.select('.product_pod')
        print(f"Found {len(book_elements)} book elements.")

        for book in book_elements:
            title = book.h3.a['title']
            price = book.select_one('.price_color').get_text(strip=True)
            books.append({'tite': title, 'price': price})
        return books

# books = [] intialises an empty list to store book data.
# book_elements uses BeautifulSoup to find all HTML elements with class product_pod.
# For each book in book_elements, extracts title from h2 element tag.
# Method returns the list of dictionaries containing book titles and prices.

    def save_to_csv(self, books):
        df = pd.DataFrame(books)
        df.to_csv('books.csv', index=False)

        def display_results(self, books):
            self.results_text.insert(tk.END, "Crawl completed. Books extracted:\n")
            for book in books:
                self.results_text.insert(tk.END, f"Title: {book['title']}, Price: {book['price']}\n")
                self.results_results_text.insert(tk.END, "Books saved to books.csv\n")

# Method checks if there are any quotes to save.
# Saves the DataFrame to a csv file quotes.csv.
# shows a success message if the data is saved, otherwise an error message if no quotes to save. 

    if __name__ == "__main__":
        root = tk.Tk()
        app = WebCrawlerApp(root)
        root.mainloop()

# root = tk.Tk(): forms main application window usng tkinter function.
# alarm_clock = WebCrawlerApp(root): forms an instance of the WebCrawlerApp class, passing root
# as an argument. Initialises the crawler application.
# root.mainloop(): starts Tkinter event loop, which listens for events and updates the GUI.  