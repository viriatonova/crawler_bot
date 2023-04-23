import json

import typer

from bot.entity.financial_bot import FinancialBot
from settings import PAGE, REGIONS


def main(
    region: str = typer.Option(..., "-r", help="set region"),
    save_as: str = typer.Option("print", "-s", help="save format (json or csv)"),
) -> None:
    if region not in REGIONS:
        print("Região invalida")
        return
    scraper = FinancialBot(PAGE, region)
    scraper.scrape()
    if save_as == "json":
        scraper.save_as_json()
    elif save_as == "csv":
        scraper.save_as_csv()
    elif save_as == "print":
        print(json.dumps(scraper.financial_data, indent=2))


if __name__ == "__main__":
    typer.run(main)
