from pathlib import Path
import re
from datetime import datetime

ROOT = Path(".")
BOOKMARKS = ROOT / "bookmarks"

regexp = re.compile(".*HREF=\"(.*)\".*TAGS=\"(.*)\" ADD_DATE=\"(.*)\">(.*)</A>")

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

with open("bookmark.html", "r") as f:
    lines = f.readlines()

    for l in lines:
        if l.startswith("<DT>"):
            m = regexp.match(l)
            if not m:
                print("No match? "  + l)
                continue

            url = m.group(1)
            tags = [make_tag(t) for t in m.group(2).split(",")]
            date = m.group(3)
            title = m.group(4)

            filename = make_name(title) + ".md"
            with open(BOOKMARKS/filename, "w") as f:
                f.write("# %s\n\n" % title)
                f.write("Date: %s\n" % (datetime.fromtimestamp(int(date))))
                f.write("%s\n\n" % " ".join("[[%s]]" % t for t in tags))
                f.write("URL: [%s]\n" % url)





            
