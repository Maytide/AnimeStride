from html.parser import HTMLParser


class AnimePageGetter(HTMLParser):
    def __init__(self):
        super().__init__()
        self.data = []

    def handle_starttag(self, tag, attr):
        if tag == 'a':
            # print(attr)
            if attr[0][0] == 'class' and attr[0][1] == 'hoverinfo_trigger fl-l ml12 mr8' and attr[1][0] == 'href':
                # print(attr[1][1])
                self.data.append(attr[1][1])