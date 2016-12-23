from html.parser import HTMLParser

# This is, by no means, efficient. I threw together a bunch of stackoverflow answers to do everything in here.
# MAL pls make official API

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


class UserShowGetterT2(HTMLParser):
    def __init__(self):
        super().__init__()
        self.recording_score = 0
        self.recording_name = 0
        self.score_data = []
        self.name_data = []
        self.reformatted_data = ''

    def handle_starttag(self, tag, attr):
        if tag != 'td' and tag != 'a':
            return

        #Disjoint events: This should be ok?
        if self.recording_score:
            self.recording_score += 1
            return
        if self.recording_name:
            self.recording_name += 1
            return
        # for name, value in attr:
        #     if name == 'class' and value == 'spaceit_pad':
        #         break
        #     else:
        #         return

        if len(attr) > 2 and attr[0][0] == 'class' and (attr[0][1] == 'td1' or attr[0][1] == 'td2') and attr[1][0] == 'align' and attr[1][1] == 'center' and attr[2][0] == 'width' and attr[2][1] == '45':
            self.recording_score = 1
        elif len(attr) > 2 and attr[0][0] == 'href' and attr[1][0] == 'target' and attr[1][1] == '_blank' and attr[2][0] == 'class' and attr[2][1] == 'animetitle':
            self.recording_name = 1
        return


    def handle_endtag(self, tag):
        if tag == 'td' and self.recording_score:
            self.recording_score -= 1
        if tag == 'a' and self.recording_name:
            self.recording_name -= 1

    def handle_data(self, data):
        if self.recording_score:
            self.score_data.append(data)
        if self.recording_name:
            self.name_data.append(data)
            # print(data)

    def reformat_data(self):
        # self.name_data = [anime_name.strip('\\n ') for anime_name in self.name_data]
        self.name_data = [anime_name.strip(' ').replace('\r\n', '') for anime_name in self.name_data]
        self.score_data = [score.strip('\\n ') for score in self.score_data]
        self.reformatted_data = ''
        # self.name_data = [anime_name for index, anime_name in enumerate(self.name_data) if index % 2 == 1]
        self.name_data = [anime_name for index, anime_name in enumerate(self.name_data) if anime_name != '' and anime_name != '\\n']
        for index in range(len(self.score_data)):
            self.reformatted_data += ('{' + '"score"' + ':' + self.score_data[index].strip('\\n ') + ',' +
                                      '"anime_title"' + ':"' + self.name_data[index] + '"},')
            # print(index)

