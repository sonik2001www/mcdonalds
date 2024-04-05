import time

from bs4 import BeautifulSoup
import requests
import json

from selenium import webdriver
from selenium.webdriver.common.by import By

from config.parser import load_config


class Bot:
    def __init__(self):
        self.DEBUG = False
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--enable-javascript")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--lang=en")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.maximize_window()

    def get_nutritions(self, link):
        nutritions = {}

        self.driver.get(link)

        self.driver.find_element(
            By.XPATH,
            "//span[contains(text(), 'Енергетична цінність та вміст поживних речовин')]",
        ).click()
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        all_li_primary_nutritions = self.driver.find_elements(
            By.XPATH,
            "//li[contains(@class, 'cmp-nutrition-summary__heading-primary-item')]",
        )

        nutritions["calories"] = (
            all_li_primary_nutritions[0].text.strip().split("\n")[0]
        )
        nutritions["fats"] = all_li_primary_nutritions[1].text.strip().split("\n")[0]
        nutritions["carbs"] = all_li_primary_nutritions[2].text.strip().split("\n")[0]
        nutritions["proteins"] = (
            all_li_primary_nutritions[3].text.strip().split("\n")[0]
        )

        card_html = self.driver.execute_script("return document.body.innerHTML")
        soup = BeautifulSoup(card_html, "lxml")

        all_li_nutrition = soup.find(
            "div", {"class": "cmp-nutrition-summary__details-column-view-desktop"}
        ).find_all("li")

        for li_nutrition in all_li_nutrition:
            name_li_nutrition = li_nutrition.find("span").text.strip()

            if name_li_nutrition == "НЖК:":
                nutritions["unsaturated_fats"] = (
                    li_nutrition.find("span", {"aria-hidden": "true"})
                    .text.strip()
                    .replace("  ", "")
                    .replace("\n", " ")
                )
            elif name_li_nutrition == "Цукор:":
                nutritions["sugar"] = (
                    li_nutrition.find("span", {"aria-hidden": "true"})
                    .text.strip()
                    .replace("  ", "")
                    .replace("\n", " ")
                )
            elif name_li_nutrition == "Сіль:":
                nutritions["salt"] = (
                    li_nutrition.find("span", {"aria-hidden": "true"})
                    .text.strip()
                    .replace("  ", "")
                    .replace("\n", " ")
                )
            elif name_li_nutrition == "Порція:":
                nutritions["portion"] = (
                    li_nutrition.find("span", {"aria-hidden": "true"})
                    .text.strip()
                    .replace("  ", "")
                    .replace("\n", " ")
                )

        return nutritions


def init_link(link):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(link, headers=headers)

    return BeautifulSoup(response.text, "lxml")


def get_all_category_links(soup, domain):
    category_links_ul = soup.find(
        "ul", {"class": "cmp-category__links-section cmp-category__row"}
    )
    category_links_a = category_links_ul.find_all("a", class_="category-link")
    category_links = [domain + link["href"] for link in category_links_a]

    return category_links


def get_all_item_links(soup, domain):
    items = soup.find_all("li", class_="cmp-category__item")
    items_link = [domain + item.find("a")["href"] for item in items]

    return items_link


def get_detail_data(soup, link, pk):
    name = soup.find(
        "span", {"class": "cmp-product-details-main__heading-title"}
    ).text.strip()
    description = soup.find(
        "div", {"class": "cmp-product-details-main__description"}
    ).text.strip()

    b = Bot()
    nutritions = b.get_nutritions(link)

    return {
        "pk": pk,
        "model": "mcdonalds_app.product",
        "fields": {"name": name, "description": description, **nutritions},
    }


def to_json(items_detail_list):
    json_data = json.dumps(items_detail_list, ensure_ascii=False, indent=4)

    with open("all_items.json", "w", encoding="utf-8") as f:
        f.write(json_data)


def main(url_config):
    url = url_config.url
    domain = url_config.domain

    soup = init_link(url)
    category_links = get_all_category_links(soup, domain)

    all_item_links = []

    for link in category_links:
        soup = init_link(link)
        all_item_links += get_all_item_links(soup, domain)

    all_item_links = list(set(all_item_links))

    items_detail_list = []

    for idx, link in enumerate(all_item_links, start=1):
        soup = init_link(link)
        items_detail_list.append(get_detail_data(soup, link, pk=idx))

    to_json(items_detail_list)


if __name__ == "__main__":
    url_config = load_config().url_config
    main(url_config)
