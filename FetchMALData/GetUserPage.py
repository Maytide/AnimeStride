from html.parser import HTMLParser


class UserPageGetter(HTMLParser):
    def __init__(self):
        super().__init__()
        self.data = []

    def handle_starttag(self, tag, attr):
        if tag == 'a':
            # print(attr)
            if attr[0][0] == 'href' and 'animelist' in attr[0][1] and len(attr) > 1 and attr[1][0] == 'target':
                # print(attr[1][1])
                self.data.append(attr[0][1].replace('http', 'https'))