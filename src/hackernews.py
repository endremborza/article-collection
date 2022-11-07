from typing import Union

import aswan
from bs4 import BeautifulSoup

main_url = "https://news.ycombinator.com/"


class GiveUp(aswan.RequestHandler):
    process_indefinitely: bool = True

    def is_session_broken(self, _: Union[int, Exception]):
        return False


class RegTop(aswan.RequestSoupHandler):
    def parse(self, soup: "BeautifulSoup"):

        for tr in soup.find_all("tr", class_="athing")[:5]:
            title_a = tr.find("a", class_="titlelink")
            if title_a is None:
                title_a = tr.find("span", class_="titleline").find("a")
            self.register_links_to_handler([title_a["href"]], GiveUp)

        return soup.encode("utf-8")


if __name__ == "__main__":
    aswan.run_simple_project({RegTop: [main_url]}, name="hackernews", remote=True)
