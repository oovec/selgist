from jinja2 import Environment, FileSystemLoader
import os
import shutil


def render(template_name, folder, **context):
    env = Environment()
    env.loader = FileSystemLoader(folder)
    template = env.get_template(template_name)
    return template.render(context)


def render_all(config, gists, output_folder):
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.mkdir(output_folder)
    os.mkdir(os.path.join(output_folder, "tag"))
    os.mkdir(os.path.join(output_folder, "category"))
    os.mkdir(os.path.join(output_folder, "posts"))
    
    context = {}
    context["title"] = config.title
    context["theme"] = config.theme
    theme_folder = config.theme["path"]
    context["categories"] = list(map(lambda x: x["name"], config.selectors))
    index_category = context["categories"][0]
    # render tags
    tags = []
    for p in gists:
        for t in p.tags:
            if t not in tags:
                tags.append(t)
    for t in tags:
        posts = list(filter(lambda x: t in x.tags, gists))
        tag_html = render("layout/_default/posts.html", theme_folder, posts=posts, tag=t, **context)
        with open(os.path.join(output_folder, "tag", t + ".html"), "w") as f:
            f.write(tag_html)
    # render categories
    for c in context["categories"]:
        posts = list(filter(lambda x: x.category == c, gists))
        category_html = render("layout/_default/posts.html", theme_folder, posts=posts, category=c, **context)
        with open(os.path.join(output_folder, "category", c + ".html"), "w") as f:
            f.write(category_html)
    # render post
    for gist in gists:
        post_html = render("layout/_default/post.html", theme_folder, post=gist, **context)
        with open(os.path.join(output_folder, "posts", gist.id[7:] + ".html"), "w") as f:
            f.write(post_html)