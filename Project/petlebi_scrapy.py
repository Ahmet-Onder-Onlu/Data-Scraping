import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


a=0
global all_p_titles

all_types_category = ["Kedi", "Köpek", "Kuş"]

all_p_titles = []
all_p_prices = []
all_p_links = []
all_p_images = []
all_p_descs = []
# I couldn't find these three values in the website.c
all_p_barcodes = [] # Unfortunately Not Found
all_p_stocks = [] # Unfortunately Not Found
all_p_skus = [] # Unfortunately Not Found
all_p_categories = [] 
all_p_ids = []
all_p_brands = []


# All datas are collected from the website. And they are stored in the dataFrame.
while(True):
    try:
        url = f"https://www.petlebi.com/alisveris/ara?personaclick_search_query=t%C3%BCm%20%C3%BCr%C3%BCnler&page={a}"
        respose = requests.get(url)
        url_content = respose.content
        soup = BeautifulSoup(url_content, "html.parser")
        p_titles = soup.find_all("h3", attrs={"class": "commerce-title mt-2 mb-0"})
        p_prices = soup.find_all("span", attrs={"class": "commerce-discounts"})
        p_links = soup.find_all("a", attrs={"class": "p-link"})
        p_images = soup.find_all("img", attrs={"class": "img-fluid lazy mb-2"})
        p_descs = soup.find_all("img", attrs={"class": "img-fluid lazy mb-2"})
        p_categories = soup.find_all("h3", attrs={"class": "commerce-title mt-2 mb-0"})
        p_brands = soup.find_all("h3", attrs={"class": "commerce-title mt-2 mb-0"})
        p_ides = soup.find_all("a", attrs={"class": "p-link"})

        for title in p_titles:
            all_p_titles.append(title.text)
            all_p_barcodes.append("Not Found")
            all_p_stocks.append("Not Found")
            all_p_skus.append("Not Found")
        
        for price in p_prices:
            all_p_prices.append(price.text)

        for link in p_links:
            all_p_links.append(link.get("href"))
        
        for image in p_images:
            all_p_images.append(image.get("data-original"))

        for desc in p_descs:
            all_p_descs.append(desc.get("alt"))

        for category in p_categories:
            array = (category.text.split(" "))

            if all_types_category[0] in array:
                all_p_categories.append(all_types_category[0])
            
            elif all_types_category[1] in array:  
                all_p_categories.append(all_types_category[1])
            
            elif all_types_category[2] in array:
                all_p_categories.append(all_types_category[2])
            
            else:
                all_p_categories.append("Kemirgenler")
        
        for brand in p_brands:
            br = (brand.text.split(" ")[0])
            all_p_brands.append(br)

        for id in p_ides:
            all_p_ids.append(id.get("id"))


        a += 1
        # I got exception end of the page(281).
        # That's why I put it into my code.
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error occurred: {e}")
        break  # Exit the loop on connection error

all_p_titles = np.array(all_p_titles)
all_p_prices = np.array(all_p_prices)
all_p_links = np.array(all_p_links)
all_p_images = np.array(all_p_images)
all_p_descs = np.array(all_p_descs)
all_p_categories = np.array(all_p_categories)
all_p_ids = np.array(all_p_ids)
all_p_brands = np.array(all_p_brands)
all_p_barcodes = np.array(all_p_barcodes)
all_p_stocks = np.array(all_p_stocks)
all_p_skus = np.array(all_p_skus)


df = pd.DataFrame({
    "Title": all_p_titles,
    "Price": all_p_prices,
    "Link": all_p_links,
    "Image": all_p_images,
    "Description": all_p_descs,
    "Category": all_p_categories,
    "ID": all_p_ids,
    "Brand": all_p_brands,
    "Barcode": all_p_barcodes,
    "Stock": all_p_stocks,
    "SKU": all_p_skus
})

# General information about the data.
print(df)

# DataFrame'i JSON formatında bir dosyaya yazma
df.to_json("petlebi_products.json", orient="records", force_ascii=False)

# Başarılı bir şekilde yazıldığını doğrulama
print("It successfully written to the Json File.")






