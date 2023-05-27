class Config:
    def __init__(self, config_dict):
        self.username = config_dict["username"]
        self.title = config_dict["title"]
        self.theme = config_dict["theme"]
        self.theme_path = self.theme["path"]
        self.selectors = config_dict["selectors"]

class Gist:
    def __init__(self, title, href, category, tags):
        self.id = href
        self.title = title
        self.created_ts = ""
        self.editted_ts = ""
        self.content = ""
        self.category = category
        self.tags = tags
