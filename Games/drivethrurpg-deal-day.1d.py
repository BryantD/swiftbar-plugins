#!/usr/bin/env PYTHONIOENCODING=UTF-8 /usr/local/bin/python3

# The MIT License (MIT)
#
# Copyright (c) 2021 Bryant Durrell
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# <bitbar.title>DriveThruRPG Deal of the Day</bitbar.title>
# <bitbar.version>v1.0.1</bitbar.version>
# <bitbar.author>Bryant Durrell</bitbar.author>
# <bitbar.author.github>BryantD</bitbar.author.github>
# <bitbar.desc>Displays the current DriveThruRPG Deal of the Day</bitbar.desc>
# <bitbar.dependencies>python3, BeautifulSoup, Requests</bitbar.dependencies>
# <bitbar.image></bitbar.image>
# <bitbar.abouturl>https://github.com/BryantD/swiftbar-plugins</bitbar.abouturl>

from bs4 import BeautifulSoup
import requests
import re


def extract_data(tooltip, css_class):
    return re.search(f'{css_class}\\\\"[^>]+>([^<]+)', tooltip).group(1)


def main():

    dtrpg_url = "http://www.drivethrurpg.com/"
    dtrpg_tooltip_url = (
        "https://www.drivethrurpg.com/includes/ajax/tooltip_request_handler.php"
    )

    try:
        req = requests.get(dtrpg_url)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    soup = BeautifulSoup(req.text, "html.parser")

    product_url = soup.find("img", alt="Deal of the Day").find_parent("a")["href"]
    product_id = re.search("\d{5,}", product_url).group()

    try:
        tooltip_req = requests.get(dtrpg_tooltip_url, {"products_id": product_id})
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    tooltip = tooltip_req.text.replace("\\", "")[2:-1]
    tooltip_soup = BeautifulSoup(tooltip, "html.parser")

    product_name = tooltip_soup.find(
        "span", class_="tooltip-information-item-title"
    ).string
    product_price = tooltip_soup.find(
        "div", class_="product-price-special"
    ).string.rstrip()
    product_rules = list(
        filter(
            lambda y: y != "None",
            map(
                lambda x: x.li.string,
                tooltip_soup.find_all("ul", class_="rules-system-list"),
            ),
        )
    )
    if len(product_rules) == 0:
        product_rules.append("No system listed")

    print(f"{product_name} ({product_price})")
    print("---")
    for rules in product_rules:
        print(f"{rules}| href={product_url}")


if __name__ == "__main__":
    main()
