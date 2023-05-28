class Config:

    def __init__(self, config_dict):
        self.username = config_dict["username"]
        self.title = config_dict["title"]
        self.theme = config_dict["theme"]
        self.selectors = config_dict["selectors"]


class Gist:

    def __init__(self, title, href, category, tags, raw_content, timestamps):
        self.id = href.split("/")[-1]
        self.title = title
        self.created_ts = timestamps[-1]
        self.editted_ts = timestamps[0]
        self.content = raw_content
        self.category = category
        self.tags = tags
