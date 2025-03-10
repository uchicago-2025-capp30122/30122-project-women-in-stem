import sys
from mortality.predict_model import user_input_dash
from mortality.map_viz import run_app
from mortality.scrapers.kff_web_scraping import run_kff_scrapers
from mortality.scrapers.abortion_web_scraping import run_abortion_policy_scraper

def main():
    if (len(sys.argv) != 2) or (sys.argv[1] not in ["prediction", "map", "scrape"]):
        print("Please run one the following:\nuv run python -m mortality map\nuv run python -m mortality prediction\nuv run python -m mortality scrape")
        sys.exit(1)
    elif sys.argv[1] == "prediction":
        print("To close Dash, press Control+C")
        user_input_dash()
    elif sys.argv[1] == "map":
        print("To close Dash, press Control+C")
        run_app()
    elif sys.argv[1] == "scrape":
        run_kff_scrapers()
        run_abortion_policy_scraper()
    else:
        print("Please run the following: uv run python -m mortality map or uv run python -m mortality prediction or uv run python -m mortality scrape")

if __name__ == "__main__":
    main()