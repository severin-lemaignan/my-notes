from pathlib import Path
import re
from datetime import datetime

ROOT = Path(".")
BOOKMARKS = ROOT / "bookmarks"

re_url = re.compile(".*HREF=\"(.*?)\"")
re_tags = re.compile(".*TAGS=\"(.*?)\"")
re_date = re.compile(".*ADD_DATE=\"(.*?)\"")
re_title = re.compile(".*HREF.*>(.*)</A>")

def make_name(name):
    name = name.lower().replace(" ", "-")
    keep = ["-"]
    name = "".join([l for l in name if l.isalnum() or l in keep])
    name = name.replace("--","-")
    if len(name)>100:
        name = name[:100]
        name = "-".join(name.split("-")[:-1])
    return name

def make_tag(tag):

    safetag = make_name(tag)

    filename = ROOT/(safetag + ".md")

    if not filename.exists():
        with open(filename, "w") as f:
            f.write("# %s\n\n" % tag)

    return safetag

with open("ff_bookmarks.html", "r") as f:
    lines = f.readlines()

    for l in lines:
        if l.strip().startswith("<DT>"):
            m_url = re_url.match(l)
            m_tags = re_tags.match(l)
            m_date = re_date.match(l)
            m_title = re_title.match(l)
            if not m_title:
                print("No match? "  + l)
                continue

            url = m_url.group(1)
            if not m_tags:
                continue
            tags = [make_tag(t) for t in m_tags.group(1).split(",")]
            date = m_date.group(1)
            title = m_title.group(1)

            filename = make_name(title) + ".md"

            with open(BOOKMARKS/filename, "w") as f:
                f.write("# %s\n\n" % title)
                f.write("Date: %s\n" % (datetime.fromtimestamp(int(date))))
                f.write("%s\n\n" % " ".join("[[%s]]" % t for t in tags))
                f.write("URL: [%s]\n" % url)





            
