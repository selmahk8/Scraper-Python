import requests
from bs4 import BeautifulSoup
import csv

def extract_apple_product_titles(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Modifiez ces lignes en fonction de la structure HTML du site Apple
    product_titles = soup.find_all('h3', class_='product-title')

    return [title.text.strip() for title in product_titles]

# URL du site Apple (celui-ci est fictif, remplacez-le par le site réel que vous avez en tête)
apple_url = 'https://www.apple.com/airpods/'

# Extraire les titres des produits Apple
apple_product_titles = extract_apple_product_titles(apple_url)

# Écrire les données dans un fichier CSV
with open('apple_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Titre']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Écrire les titres des produits dans le fichier CSV
    for title in apple_product_titles:
        writer.writerow({'Titre': title})
