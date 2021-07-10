def link_old(html: str):
    from re import compile
    pattern = compile(r"\[(.*?)\]\((.*?)\)")

    a_tags = []
    for tag in pattern.findall(html):
        a_tags.append({
            "text": tag[0],
            "href": tag[1],
            "target": "_blank",
            "rel": "noreferrer"
        })

    return a_tags


def link(html: str):
    from re import compile
    pattern = compile(r"\[(.*?)\]\((.*?)\)")

    for tag in pattern.findall(html):
        print(tag)

    return html


# do not touch this
filter_list = [name for name in dir() if not name.startswith("_")]
# do not touch this
