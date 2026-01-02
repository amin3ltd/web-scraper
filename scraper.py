import requests
import lxml.html

# --------------------------------------------------
# Step 1: Send HTTP request to Steam "New Releases"
# --------------------------------------------------
STEAM_NEW_RELEASES_URL = "https://store.steampowered.com/explore/new/"

response = requests.get(STEAM_NEW_RELEASES_URL)
response.raise_for_status()  # Fail fast if request fails

# --------------------------------------------------
# Step 2: Parse HTML content using lxml
# --------------------------------------------------
document = lxml.html.fromstring(response.content)

# Main container that holds new release games
new_releases_section = document.xpath('//div[@id="tab_newreleases_content"]')[0]

# --------------------------------------------------
# Step 3: Extract game titles and prices
# --------------------------------------------------
game_titles = new_releases_section.xpath(
    './/div[@class="tab_item_name"]/text()'
)

game_prices = new_releases_section.xpath(
    './/div[@class="discount_final_price"]/text()'
)

# --------------------------------------------------
# Step 4: Extract game tags
# --------------------------------------------------
raw_tags = []

for tag_div in new_releases_section.xpath('.//div[@class="tab_item_top_tags"]'):
    raw_tags.append(tag_div.text_content())

# Convert comma-separated tags into lists
game_tags = [tags.split(', ') for tags in raw_tags]

# --------------------------------------------------
# Step 5: Extract supported platforms
# --------------------------------------------------
platform_details_divs = new_releases_section.xpath(
    './/div[@class="tab_item_details"]'
)

all_game_platforms = []

for details_div in platform_details_divs:
    platform_spans = details_div.xpath(
        './/span[contains(@class, "platform_img")]'
    )

    platforms = [
        span.get("class").split(" ")[-1]
        for span in platform_spans
    ]

    # Remove unwanted separator class if present
    if "hmd_separator" in platforms:
        platforms.remove("hmd_separator")

    all_game_platforms.append(platforms)

# --------------------------------------------------
# Step 6: Combine extracted data into structured output
# --------------------------------------------------
games_data = []

for title, price, tags, platforms in zip(
    game_titles, game_prices, game_tags, all_game_platforms
):
    game_info = {
        "title": title.strip(),
        "price": price.strip(),
        "tags": tags,
        "platforms": platforms
    }
    games_data.append(game_info)

# --------------------------------------------------
# Step 7: Output result
# --------------------------------------------------
print(games_data)
