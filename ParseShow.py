from html.parser import HTMLParser
import urllib
### Making some of these classes more general sounds like a recipe for suicide. MAL HTML = unpredictable.


class ParseShowContentInHTMLTag(HTMLParser):
    def __init__(self):
        super().__init__()
        self.description = ''
        self.title = ''
        self.image_url = ''
        self.data = []


    def handle_starttag(self, tag, attr):
        if tag == 'meta':
            # print(attr)
            MAL_description_name = 'og:description'
            MAL_title_name = 'og:title'
            MAL_image_name = 'og:image'
            for index, (name, values) in enumerate(attr):
                if attr[0][1] == MAL_description_name and name == 'content':
                    # print(values)
                    self.description = values
                    self.data.append(self.description)
                if attr[0][1] == MAL_title_name and name == 'content':
                    # print(values)
                    self.title = values
                    self.data.append(self.title)
                if attr[0][1] == MAL_image_name and name == 'content':
                    # print(values)
                    self.image_url = values
                    self.data.append(self.image_url)


class ParseShowContentInHTMLElement(HTMLParser):
    # Code from:
    # http://stackoverflow.com/questions/3276040/how-can-i-use-the-python-htmlparser-library-to-extract-data-from-a-specific-div
    def __init__(self):
        super().__init__()
        self.recording = 0
        self.data = []

    def handle_starttag(self, tag, attr):
        if tag != 'div':
            return
        if self.recording:
            self.recording += 1
            return
        for name, value in attr:
            if name == 'class' and value == 'spaceit_pad':
                break
        else:
            return
        self.recording = 1

    def handle_endtag(self, tag):
        if tag == 'div' and self.recording:
            self.recording -= 1

    def handle_data(self, data):
        if self.recording:
            self.data.append(data)
        # print(data)


class ParseShowContentInHTMLElementNoName(HTMLParser):

    def __init__(self, split_1, split_2):
        super().__init__()
        self.split_1 = split_1
        self.split_2 = split_2
        self.recording = 0
        self.data = []

    def feed(self, data):
        data = data.split(self.split_1)[1]
        data = data.split(self.split_2)[0]
        # print(data)
        super().feed(data)


    def handle_starttag(self, tag, attr):
        # print('tag: ' + tag)
        if tag != ('div'):
            return
        if self.recording:
            self.recording += 1
            return
        # print(attr)
        if not attr:
            # MAL html is weird - it alternates between null attr and class spaceit. So if either null or name = class && value = spaceit, start recording.
            self.recording = 1
            # self.recording = 1
        for name, value in attr:
            # print(name, value)
            if name == 'class':
                break
        else:
            return
        self.recording = 1

    def handle_endtag(self, tag):
        if tag == ('div') and self.recording:
            self.recording -= 1

    def handle_data(self, data):
        if self.recording:
            self.data.append(data)


class ParseShowInformation(ParseShowContentInHTMLElementNoName):

    def __init__(self):
        super().__init__('<h2>Information</h2>', '<h2>Statistics</h2>')

class ParseShowStatistics(ParseShowContentInHTMLElementNoName):

    def __init__(self):
        # Old argument 2: <h2>External Links</h2> header in html view source exists on chrome, but not firefox? wtf...
        super().__init__('<h2>Statistics</h2>', '<div class="clearfix mauto mt16"')

class ParseShowRelated(HTMLParser):
    def __init__(self):
        super().__init__()
        # <table class="anime_detail_related_anime" style="border-spacing:0px;">
        # </table><br>
        self.split_1 = '<table class="anime_detail_related_anime" style="border-spacing:0px;">'
        self.split_2 = '</table><br>'
        self.recording = 0
        self.data = []

    def feed(self, data):
        data = data.split(self.split_1)[1]
        data = data.split(self.split_2)[0]
        # print(data)
        super().feed(data)

    def handle_starttag(self, tag, attr):
        if tag == 'a':
            for index, (name, values) in enumerate(attr):
                if name == 'href':
                    self.data.append(values)

        if tag != 'td':
            return
        if self.recording:
            self.recording += 1
            return
        # print(attr)

        for name, value in attr:
            if (name == 'class' and value == 'ar fw-n borderClass' or value == 'borderClass'):
                break
        else:
            return
        self.recording = 1

    def handle_endtag(self, tag):
        if (tag == 'td') and self.recording:
            self.recording -= 1

    def handle_data(self, data):
        if self.recording:
            self.data.append(data)

# class ParseShowInformation(HTMLParser):
#
#     def __init__(self):
#         super().__init__()
#         self.recording = 0
#         self.data = []
#
#     def feed(self, data):
#         data = data.split('<h2>Alternative Titles</h2>')[1]
#         data = data.split('<h2>Statistics</h2>')[0]
#         print(data)
#         super().feed(data)
#
#
#     def handle_starttag(self, tag, attr):
#         if tag != 'div':
#             return
#         if self.recording:
#             self.recording += 1
#             return
#         for name, value in attr:
#             if name == 'class':
#                 break
#         else:
#             return
#         self.recording = 1
#
#     def handle_endtag(self, tag):
#         if tag == 'div' and self.recording:
#             self.recording -= 1
#
#     def handle_data(self, data):
#         if self.recording:
#             self.data.append(data)