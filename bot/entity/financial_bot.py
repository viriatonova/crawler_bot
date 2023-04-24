import csv
import errno
import json
import os

from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from settings import ROOT_DIR
from settings import SELECTORS as selectors


class FinancialBot:
    """Entidade para pagina de news financeiras do site yahoo,
    pega a tabela de informações e faz scraping dos dados.
    """

    service = Service(executable_path=f"{ROOT_DIR}/chromedriver")
    driver = Chrome(service=service)
    wait = WebDriverWait(driver, timeout=5, poll_frequency=1)

    def __init__(self, page: str, region: str) -> None:
        self.page = page
        self.region = region
        self._raw_stocks_table: str = ""
        self.financial_data = {}

        self._setup()

    def _setup(self) -> None:
        """Metódo que ordena a chamada das funções de crawler e scraper"""
        self._create_folder()
        self.open_page()
        self._set_region()
        self._find_stocks()
        self._get_stocks_table()

    def _create_folder(self) -> None:
        if not os.path.exists(f"{ROOT_DIR}/out/"):
            try:
                os.makedirs(os.path.dirname(f"{ROOT_DIR}/out/"))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise

    def save_as_json(self) -> None:
        """Salva os dados obtidos no formato json"""
        json_file = json.dumps(self.financial_data, indent=4)
        with open(f"{ROOT_DIR}/out/financial.json", "w+") as json_outfile:
            json_outfile.write(json_file)

    def save_as_csv(self) -> None:
        """Salva os dados obtidos no formato csv"""
        with open(f"{ROOT_DIR}/out/financial.csv", "w+") as csv_outfile:
            field_names = ["Symbol", "Name", "Price"]
            writer = csv.DictWriter(csv_outfile, fieldnames=field_names)
            writer.writeheader()
            for item in self.financial_data.values():
                writer.writerow(
                    {
                        "Symbol": item["symbol"],
                        "Name": item["name"],
                        "Price": item["price"],
                    }
                )

    def open_page(self) -> None:
        FinancialBot.driver.get(self.page)

    def _set_region(self) -> None:
        # Remove the default region to avoid select two regions
        FinancialBot.driver.find_element(
            By.CSS_SELECTOR, selectors["region_item"]
        ).click()
        FinancialBot.driver.find_element(
            By.CSS_SELECTOR, selectors["region_add"]
        ).click()
        FinancialBot.driver.find_element(
            By.XPATH, f'//span[.="{self.region}"]/..'
        ).click()

    def _find_stocks(self) -> None:
        stocks_button = FinancialBot.driver.find_element(
            By.XPATH, selectors["stocks_button"]
        )
        FinancialBot.wait.until(EC.element_to_be_clickable(stocks_button))
        stocks_button.click()

    def _get_stocks_table(self) -> None:
        html_source = FinancialBot.wait.until(
            EC.presence_of_element_located((By.ID, selectors["table"]))
        )
        self._raw_stocks_table = html_source.get_attribute("innerHTML")

    def scrape(self) -> None:
        """Faz o scraping dos dados na tabela obtida"""
        soup = BeautifulSoup(self._raw_stocks_table, "html.parser")
        for index, line in enumerate(soup.find_all("tr", class_="simpTblRow")):
            symbol = line.find("td", attrs={"aria-label": "Symbol"})
            name = line.find("td", attrs={"aria-label": "Name"})
            price = line.find("td", attrs={"aria-label": "Price (Intraday)"})
            self.financial_data[index] = {
                "symbol": symbol.contents[1].text,
                "name": name.text,
                "price": price.contents[0]["value"],
            }
