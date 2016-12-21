from html.parser import HTMLParser

class UserShowGetter(HTMLParser):
    def __init__(self):
        super().__init__()
        self.data = ''

    def handle_starttag(self, tag, attr):
        if tag == 'table':
            # print(attr)
            if attr[0][0] == 'class' and attr[0][1] == 'list-table' and attr[1][0] == 'data-items':
                # print(attr[1][1])
                self.data = attr[1][1]