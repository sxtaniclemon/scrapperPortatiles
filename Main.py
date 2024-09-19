from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
import csv
import time

URL = "https://listado.mercadolibre.com.co/computador-portatil"


def scrape_laptops():
    driver = webdriver.Chrome()  # Make sure you have ChromeDriver installed
    driver.get(URL)

    laptops = []

    # Wait for the product cards to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "poly-card"))
    )

    # Scroll down to load more items (adjust the range as needed)
    for _ in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    product_cards = driver.find_elements(By.CLASS_NAME, "poly-card")

    for card in product_cards:
        try:
            title = card.find_element(By.CLASS_NAME, "poly-component__title").text.strip()

            price_element = card.find_element(By.CLASS_NAME, "andes-money-amount__fraction")
            price = price_element.text.strip().replace('.', '')

            shipping = card.find_element(By.CLASS_NAME, "poly-component__shipping").text.strip()
            free_shipping = "Envío gratis" in shipping or "Llega gratis" in shipping

            try:
                rating = card.find_element(By.CLASS_NAME, "poly-reviews__rating").text.strip()
            except NoSuchElementException:
                rating = "N/A"

            try:
                condition = card.find_element(By.CLASS_NAME, "poly-component__item-condition").text.strip()
            except NoSuchElementException:
                condition = "N/A"

            laptops.append({
                "Title": title,
                "Price": price,
                "Free Shipping": free_shipping,
                "Rating": rating,
                "Condition": condition
            })
        except Exception as e:
            print(f"Error processing a product card: {e}")

    driver.quit()
    return laptops


def save_to_csv(data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"laptops_{timestamp}.csv"

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["Title", "Price", "Free Shipping", "Rating", "Condition"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for laptop in data:
            writer.writerow(laptop)

    print(f"Data saved to {filename}")


if __name__ == "__main__":
    laptop_data = scrape_laptops()
    save_to_csv(laptop_data)
