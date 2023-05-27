import requests
import os.path as path
from bs4 import BeautifulSoup
from selgist.types_ import Gist

base_gist_url = "https://gist.github.com/"

class Fetcher:
    def __init__(self, config):
        self.config = config
        self.base_url = path.join(base_gist_url, config.username)

    def get_candidates_soup_in_page(self, page_id):
        page_url = self.base_url + "?page=" + str(page_id)
        response = requests.get(page_url)
        html = response.content.decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        return soup.find_all("div", class_ = "gist-snippet")

    def check_sel_desp(self, sel_desp):
        mtags = list(map(lambda x: x[1:], filter(lambda x: len(x) > 1 and x.startswith("#"), sel_desp.split(" "))))
        if len(mtags) > 0:
            for sel in self.config.selectors:
                if mtags[0] == sel["anchor"]:
                    category = mtags[0]
                    tags = list(filter(lambda x: len(x) > 0, mtags[1:]))
                    return True, category, tags        
        return False, None, None

    def get_gist_from_soup(self, soup):
        title_node = soup.find("strong", class_="css-truncate-target")
        title = title_node.text.strip()
        href = path.join(base_gist_url, title_node.parent.get("href"))
        sel_desp = soup.find("span", class_ = "f6 color-fg-muted").text.strip()
        valid, category, tags = self.check_sel_desp(sel_desp)
        if valid:
            # content = soup.find("article").parent
            # time = soup.find("relative-time").get("datetime")
            return Gist(title, href, category, tags)
        else:
            return None

    def get_selected_gists(self):
        gist_soups = []
        for i in range(1, 101):
            page_soups = self.get_candidates_soup_in_page(i)
            if len(page_soups) == 0:
                break
            gist_soups.extend(page_soups)
        gists = []
        for soup in gist_soups:
            gist = self.get_gist_from_soup(soup)
            if gist != None:
                gists.append(gist)
        return gists
