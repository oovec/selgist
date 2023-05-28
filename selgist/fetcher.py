import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from selgist.types_ import Gist

base_gist_url = "https://gist.github.com/"


class Fetcher:

    def __init__(self, config):
        self.config = config
        self.base_url = urljoin(base_gist_url, config.username)

    def get_candidates_soup_in_page(self, page_id):
        page_url = self.base_url + "?page=" + str(page_id)
        response = requests.get(page_url)
        html = response.content.decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        return soup.find_all("div", class_="gist-snippet")

    def check_sel_desp(self, sel_desp):
        mtags = list(
            map(
                lambda x: x[1:],
                filter(lambda x: len(x) > 1 and x.startswith("#"),
                       sel_desp.split(" "))))
        if len(mtags) > 0:
            for sel in self.config.selectors:
                if mtags[0] == sel["anchor"]:
                    category = sel["name"]
                    tags = list(filter(lambda x: len(x) > 0, mtags[1:]))
                    return True, category, tags
        return False, None, None

    def get_raw_content(self, href):
        html = requests.get(urljoin(base_gist_url,
                                    href)).content.decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        raw_url = soup.find("a", class_="Button--secondary").get("href")
        return requests.get(urljoin(base_gist_url,
                                    raw_url)).content.decode("utf-8")

    def get_timestamp(self, href):
        url = urljoin(base_gist_url, href) + "/revisions"
        print("xxx", url)
        html = requests.get(url).content.decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        tss = list(
            map(lambda x: x.get("datetime"),
                soup.find_all("relative-time", class_="no-wrap")))
        return tss

    def get_gist_from_soup(self, soup):
        title_node = soup.find("strong", class_="css-truncate-target")
        title = title_node.text.strip()
        if title.endswith(".md"):
            title = title[:-3]
        else:
            return None
        href = title_node.parent.get("href")
        sel_desp = soup.find("span", class_="f6 color-fg-muted").text.strip()
        valid, category, tags = self.check_sel_desp(sel_desp)
        if valid:
            content = self.get_raw_content(href)
            tss = self.get_timestamp(href)
            return Gist(title, href, category, tags, content, tss)
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
