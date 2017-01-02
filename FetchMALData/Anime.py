import sqlite3
import urllib.request as urllib
from FetchMALData.ParseShow import ParseShowContentInHTMLTag, ParseShowContentInHTMLElement, ParseShowInformation, ParseShowStatistics, ParseShowRelated
from collections import OrderedDict
from time import gmtime, strftime


class Anime():

    def trim_output(self, data):
        for key, value in data.items():

            if type(value) == type([]):
                value = [entry.strip(' ').replace('\\n', '') for entry in value]
                value = [entry for entry in value if entry != '\\n' and entry != '' and entry != ',']
            elif type(value) == type(''):
                # print(value)
                x=5
                value = value.strip('\\n')
                value = value.strip(' ')
                value = value.replace('\\n', '')
                # print(value)
            data[key] = value

        return data

    def parse_content(self, data):
        # print(data)
        key = ['Name:', 'Image:', 'Synopsis']
        return OrderedDict(zip(key, data), key = lambda t: t[0])

    def parse_titles(self, data):
        english_title = ''
        synonyms = []
        japanese_title = ''
        for i in range(len(data)):
            data[i] = data[i].strip(' \\n')
            if data[i] == 'English:':
                english_title = data[i + 1]
            if data[i] == 'Synonyms:':
                synonyms = data[i + 1].split(',')
            if data[i] == 'Japanese:':
                japanese_title = data[i + 1]


        return self.trim_output(OrderedDict((('English:', english_title), ('Synonyms:', synonyms), ('Japanese:', japanese_title)), key = lambda t: t[0]))


    def parse_info(self, data):
        type = 'Type:'
        episodes = 'Episodes:'
        air_date = 'Aired:'
        broadcast_time = 'Broadcast:'
        licensors = 'Licensors:'
        studios = 'Studios:'
        source = 'Source:'
        genres = 'Genres:'
        duration = 'Duration:'
        rating = 'Rating:'

        p_data_raw = ((type, ''), (episodes, ''), (air_date, ''), (broadcast_time, ''), (licensors, []),
                      (studios, []), (source, ''), (genres, []), (duration, ''), (rating, ''))

        p_data = OrderedDict(p_data_raw, key = lambda t: t[0])
        for i in range(len(data)):
            data[i] = data[i].strip(' \\n')
            if data[i] == type:
                # Yes, type has to be special and use i+2.
                p_data[type] = data[i+2]
            elif data[i] == 'Episodes:':
                p_data[episodes] = data[i+1]
            elif data[i] == 'Aired:':
                p_data[air_date] = data[i+1]
            elif data[i] == 'Licensors:':
                j = i + 1
                while j < len(data) and data[j] != ('Studios:') and data[j] != ('Source:'):
                    p_data[licensors].append(data[j])
                    j = j + 1
            elif data[i] == 'Studios:':
                # print('Studios success!')
                j = i + 1
                while j < len(data) and data[j] != ('Source:') and data[j] != ('Genres:'):
                    p_data[studios].append(data[j])
                    j = j + 1
            elif data[i] == 'Source:':
                # print('Source success!')
                p_data[source] = data[i+1]

            elif data[i] == 'Genres:':
                j = i + 1
                while j < len(data) and data[j] != ('Duration:') and data[j] != ('Rating:'):
                    p_data[genres].append(data[j])
                    j = j + 1
            elif data[i] == 'Duration:':
                # print('Duration success!')
                p_data[duration] = data[i+1]
            elif data[i] == 'Rating:':
                p_data[rating] = data[i+1]

        p_data = self.trim_output(p_data)

        return p_data
        # return (('Episodes:', p_data[episodes]), ('Aired:', p_data[air_date]), ('Licensors:', p_data[licensors]), ('Studios:', p_data[studios]),
        #         ('Source:', p_data[source]), ('Genres:', p_data[genres]), ('Duration:', p_data[duration]), ('Rating:', p_data[rating]))

    def parse_statistics(self, data):
        score = 'Score:'
        rank = 'Ranked:'
        members = 'Members:'
        popularity = 'Popularity:'
        favorites = 'Favorites:'

        p_data_raw = ((score, ''), (rank, ''), (members, ''), (popularity, ''), (favorites, ''))
        p_data = OrderedDict(p_data_raw, key = lambda t: t[0])

        for i in range(len(data)):
            if data[i] == score:
                p_data[score] = data[i+2]
            elif data[i] == rank:
                p_data[rank] = data[i+1]
            elif data[i] == members:
                p_data[members] = data[i+1]
            elif data[i] == popularity:
                p_data[popularity] = data[i+1]
            elif data[i] == favorites:
                p_data[favorites] = data[i+1]

        p_data = self.trim_output(p_data)

        return p_data

    def parse_related(self, data):
        data = [item for item in data if item != ', ']
        adaptation = 'Adaptation:'
        alternate = 'Alternative version:'
        side_story = 'Side story:'
        spinoff = 'Spin-off:'
        prequel = 'Prequel:'
        sequel = 'Sequel:'
        summary = 'Summary:'

        p_data_raw = ((adaptation, []), (alternate, []), (side_story, []), (spinoff, []), (prequel, []), (sequel, []), (summary, []))
        p_data = OrderedDict(p_data_raw, key=lambda t: t[0])

        for i in range(len(data)):
            # print(data[i])
            if data[i] == adaptation:
                # print(data[i], data[i+1])
                j = i + 1
                while j < len(data) and data[j] not in p_data:
                    p_data[adaptation].append(data[j])
                    j = j + 1
            elif data[i] == alternate:
                j = i + 1
                while j < len(data) and data[j] not in p_data:
                    p_data[alternate].append(data[j])
                    j = j + 1
            elif data[i] == side_story:
                # print('side story success!')
                j = i + 1
                while j < len(data) and data[j] not in p_data:
                    p_data[side_story].append(data[j])
                    j = j + 1
            elif data[i] == spinoff:
                # print('side story success!')
                j = i + 1
                while j < len(data) and data[j] not in p_data:
                    p_data[spinoff].append(data[j])
                    j = j + 1
            elif data[i] == prequel:
                # print('side story success!')
                j = i + 1
                while j < len(data) and data[j] not in p_data:
                    p_data[prequel].append(data[j])
                    j = j + 1
            elif data[i] == sequel:
                # print('side story success!')
                j = i + 1
                while j < len(data) and data[j] not in p_data:
                    p_data[sequel].append(data[j])
                    j = j + 1
            elif data[i] == summary:
                j = i + 1
                while j < len(data) and data[j] not in p_data:
                    p_data[summary].append(data[j])
                    j = j + 1
        return p_data

    def write_data(self, *data_list):
        for data in data_list:
            self.data.append(self.return_data(data))
            # print(i)
            # i+=1

    def write_to_file(self):

        with open('show_data.txt', 'a') as file:
            file.write('**[''Newshow'']**')
            file.write('\n')
            self.write_to_file_data(file, self.content_data, 'Content')
            self.write_to_file_data(file, self.name_data, 'Titles')
            self.write_to_file_data(file, self.info_data, 'Information')
            self.write_to_file_data(file, self.statistics_data, 'Statistics')
            self.write_to_file_data(file, self.related_data, 'Related')


    def write_to_file_data(self, file, data, section):
        #Ordered Dict
        file.write('--[' + section + ']--')
        file.write('\n')
        for key, value in data.items():
            if type(value) == type([]):
                file.write(key + ':')
                for item in value:
                    file.write(item + ', ')
            elif type(value) == type(''):
                file.write(key + '-: ' + value)
            file.write('\n')
            #List

    def valid_table_name(self, table_name):
        # Prevent injections
        return not ('drop table' in table_name.lower())

    #OrderedDict to SQL-compatible string
    def OD_to_db_list(self, data):
        db_list = []
        # print(data.items())
        for key, value in data.items():
            #Function item in ordered dict data?
            # print(value)
            if key != 'key':
                if type(value) == type([]):
                    db_string = ''
                    for item in value:
                        db_string += item + ', '
                    db_list.append(db_string)
                elif type(value) == type(''):
                    value = value.replace('"', '[Quot]')
                    db_list.append(value)



        # db_string = db_string.replace('"', '[Quot]')
        return db_list

    def create_db(self, db):
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute('''CREATE TABLE content_data
                  (name text, image_url text, synposis text)''')

    # In the future:
    # Port this db stuff to ReadMALShows...

    def write_to_db(self, individual_db, aggregated_db, write_individual_entry = True, write_aggregated_entry = False):
        if write_aggregated_entry == True:
            self.write_to_db_aggregated(aggregated_db, self.content_data, self.name_data, self.info_data, self.statistics_data, self.related_data)
        if write_individual_entry == True:
            self.write_to_db_individual(individual_db, self.content_data, self.name_data, self.info_data, self.statistics_data, self.related_data)

    def write_to_db_individual(self, db, content_data, name_data, info_data, statistics_data, related_data):
        # Only write data which is useful for statistics - score, ranked, members, popularity, favourites.
        # Also the time/date data was accessed.

        table_name = '[' + content_data['Name:'] + ']'
        datetime = strftime("%Y-%m-%d %H:%M:%S", gmtime())

        if not self.valid_table_name(table_name):
            raise Exception('Invalid MAL username ' + table_name + '; will cause problems with SQL.')

        conn = sqlite3.connect(db)
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS {}
                  (score text, ranked text, members text, popularity text, favourites text, datetime text)'''.format(table_name))

        # statistics_data_list = self.OD_to_db_list(statistics_data)

        c.execute('INSERT INTO {} VALUES (?,?,?,?,?,?)'.format(table_name),
                  (statistics_data['Score:'], statistics_data['Ranked:'], statistics_data['Members:'], statistics_data['Popularity:'], statistics_data['Favorites:'], datetime))
        conn.commit()

        conn.close()




    def trim_quotations(self, item):
        item = item.strip('"')
        return item

    def write_to_db_aggregated(self, db, content_data, name_data, info_data, statistics_data, related_data):
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS content_data
                  (name text, image_url text, synposis text,
                  english_name text, synonyms text, japanese_name text,
                  type text, episodes text, aired text, broadcast text, licensors text, studios text, source text, genres text, duration text, rating text,
                  score text, ranked text, members text, popularity text, favourites text,
                  adaptation text, alternative_version text, side_story text, spinoff text, prequel text, sequel text, summary text)''')
                # Content: Name, pv image URL, synopsis
                # Name: English, synonyms, jp
                # Info: Type, episodes, aired, broadcast, licensors, studios, source, genre, duration, rating
                # Stats: Score, ranked, popularity, members, favourites
                # Related: Adaptation, alternative, side-story, spinoff, prequel, sequel, summary

        content_data_list = self.OD_to_db_list(content_data)
        name_data_list = self.OD_to_db_list(name_data)
        info_data_list = self.OD_to_db_list(info_data)
        statistics_data_list = self.OD_to_db_list(statistics_data)
        related_data_list = self.OD_to_db_list(related_data)

        data_list = content_data_list + name_data_list + info_data_list + statistics_data_list + related_data_list

        # print(len(content_data_list) + len(name_data_list) + len(info_data_list) + len(statistics_data_list) + len(related_data_list))
        # print(content_data_str)
        # content_data_values = (content_data_list[0][1], content_data[1][1], content_data[0][1])

        # Is this susceptible to SQL injections?
        c.execute('INSERT OR REPLACE INTO content_data VALUES (' + '?,'*27 + '?)', data_list)
        conn.commit()




        conn.close()



    def return_data(self, data):
        l_data = []
        for key, value in data.items():
            if type(value) == type([]):
                l_data.append(key + ':')
                for item in value:
                    l_data.append(item + ', ')
            elif type(value) == type(''):
                l_data.append(key + '-: ' + value)
            l_data.append('\n')
        return l_data

    def parse_data(self, html, ps, parse):
        ps.feed(html)
        data = ps.data
        data = parse(data)
        ps.close()
        return data

    def __init__(self, MAL_URL):
        response = urllib.urlopen(MAL_URL)
        html = str(response.read())
        self.data = []

        # raw_html = response.read()
        # html = parse(response).getroot()

        # print(lxml.html.tostring(html))
        # pst = ParseShowContentInHTMLTag()
        # pst.feed(html)
        # content_data = pst.data
        # content_data = self.parse_content(content_data)
        # pst.close()
        ########################################
        pst = ParseShowContentInHTMLTag()
        self.content_data = self.parse_data(html, pst, self.parse_content)
        pst.close()
        ########################################
        # pse = ParseShowContentInHTMLElement()
        # pse.feed(html)
        # name_data = pse.data
        # name_data = self.parse_titles(name_data)
        # # print(name_data)
        # pse.close()
        #########################################
        pse = ParseShowContentInHTMLElement()
        self.name_data = self.parse_data(html, pse, self.parse_titles)
        pse.close()
        #########################################
        # psi = ParseShowInformation()
        # psi.feed(html)
        # info_data_list = psi.data
        # # print(info_data_list)
        # info_data = self.parse_info(info_data_list)
        # psi.close()
        #########################################
        psi = ParseShowInformation()
        self.info_data = self.parse_data(html, psi, self.parse_info)
        psi.close()
        #########################################
        # pss = ParseShowStatistics()
        # pss.feed(html)
        # statistics_data = pss.data
        # # print(statistics_data)
        # statistics_data = self.parse_statistics(statistics_data)
        # # print(statistics_data)
        # pss.close()
        #########################################
        pss = ParseShowStatistics()
        self.statistics_data = self.parse_data(html, pss, self.parse_statistics)
        pss.close()
        #########################################
        #########################################
        # psr = ParseShowRelated()
        # psr.feed(html)
        # related_data = psr.data
        # print(related_data)
        # related_data = self.parse_related(related_data)
        ## When i get back: work on related data
        #########################################
        if '<table class="anime_detail_related_anime" style="border-spacing:0px;">' in html:
            psr = ParseShowRelated()
            self.related_data = self.parse_data(html, psr, self.parse_related)
            psr.close()
        else:
            self.related_data = OrderedDict([['Adaptation: ', ''], ['Alternative: ', ''], ['Side Story: ', ''],
                                             ['Spinoff: ', ''], ['Prequel: ', ''], ['Sequel: ', ''], ['Summary: ', '']],
                                            key = lambda t: t[0])
        #########################################

        # print(info_data)
        # data = info_data + content_data + name_data + info_data + statistics_data
        # data = [element.strip(' \\n') for element in data]
        # data = [element for element in data if element != '\\n']

        # self.write_data(self.content_data, self.name_data, self.info_data, self.statistics_data, self.related_data)
        # self.write_data(name_data)
        # self.write_data(info_data)
        # self.write_data(statistics_data)
        # self.write_data(related_data)


# print(parse_titles(data))


