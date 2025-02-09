from playwright.sync_api import sync_playwright

URL = "https://www.mff.se/lag/herr/spelare/"

def scrape_mff_players():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL, timeout=60000)
        page.wait_for_load_state("networkidle")  # Ensure JS is fully loaded

        players = []
        player_cards = page.locator(".person-card")

        for card in player_cards.element_handles():
            name = card.query_selector(".person-name")
            number = card.query_selector(".person-number")
            image = card.query_selector(".person-card-image img")

            if name and number and image:
                players.append({
                    "name": name.inner_text(),
                    "number": number.inner_text(),
                    "image": image.get_attribute("src"),
                })

        browser.close()
        return {"players": players}

if __name__ == "__main__":
    print(scrape_mff_players())