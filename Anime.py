import sqlite3
import urllib.request as urllib
from collections import OrderedDict, defaultdict
import time
from datetime import datetime

from master import UNMODELED_DATABASES, string_SQL_safe, escape_db_string
from FetchMALData.ParseShow import ParseShowContentInHTMLTag, ParseShowContentInHTMLElement, ParseShowInformation, ParseShowStatistics, ParseShowRelated


# TODO: class Anime should know which databases to import from when called.
# Remove all references to them (except in settings.py, where it is safer to
# link directly to them for django models).
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
        media = 'Type:'
        episodes = 'Episodes:'
        air_date = 'Aired:'
        broadcast_time = 'Broadcast:'
        licensors = 'Licensors:'
        studios = 'Studios:'
        source = 'Source:'
        genres = 'Genres:'
        duration = 'Duration:'
        rating = 'Rating:'

        p_data_raw = ((media, ''), (episodes, ''), (air_date, ''), (broadcast_time, ''), (licensors, []),
                      (studios, []), (source, ''), (genres, []), (duration, ''), (rating, ''))

        p_data = OrderedDict(p_data_raw, key = lambda t: t[0])
        for i in range(len(data)):
            # print(data[i], type(data[i]))
            if isinstance(data[i], str):
                data[i] = data[i].strip(' \\n')

            if data[i] == media:
                # data[i+2] is special case for media.
                p_data[media] = data[i+2]
            elif data[i] == 'Episodes:':
                data[i + 1] = data[i + 1].strip(' \\n')
                if 'Unknown' in data[i+1]:
                    data[i+1] = 0

                try:
                    data[i+1] = int(data[i+1])
                except Exception as ex:
                    data[i+1] = 0

                p_data[episodes] = data[i+1]
            elif data[i] == 'Aired:':
                data[i + 1] = data[i + 1].strip(' \\n')
                air_datetime = data[i+1]

                if 'to' in air_datetime:
                    air_datetime = air_datetime.split('to')[0].strip()

                try:
                    # print(air_datetime)
                    datetime_obj = datetime.strptime(air_datetime, '%b %d, %Y')
                except Exception as e:
                    datetime_obj = datetime.strptime('Jan 1, 1970', '%b %d, %Y')
                    pass

                data[i+1] = int(datetime_obj.timestamp())

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
                data[i+2] = data[i+2].strip(' \\n')
                if data[i+2] == 'N/A':
                    data[i+2] = 0
                else:
                    try:
                        data[i+2] = float(data[i+2])
                    except Exception as ex:
                        print(ex)
                        data[i+2] = 0

                p_data[score] = data[i+2]
            elif data[i] == rank:
                data[i+1] = data[i+1].strip(' \\n')
                if data[i+1] == 'N/A':
                    data[i+1] = 0
                else:
                    try:
                        if data[i+1][0] == '#':
                            data[i+1] = int(data[i+1][1:])
                    except Exception as ex:
                        print(ex)
                        data[i+1] = -1

                p_data[rank] = data[i+1]
            elif data[i] == members:
                data[i+1] = data[i+1].strip(' \\n')
                data[i+1] = data[i+1].replace(',','')

                try:
                    data[i+1] = int(data[i+1])
                except Exception as ex:
                    print(ex)
                    data[i+1] = -1

                p_data[members] = data[i+1]
            elif data[i] == popularity:
                data[i+1] = data[i+1].strip(' \\n')
                if data[i+1] == 'N/A':
                    data[i+1] = -1
                else:
                    try:
                        if data[i+1][0] == '#':
                            data[i+1] = int(data[i+1][1:])
                    except Exception as ex:
                        print(ex)
                        data[i+1] = -1

                p_data[popularity] = data[i+1]
            elif data[i] == favorites:
                data[i+1] = data[i+1].strip(' \\n')
                data[i+1] = data[i+1].replace(',','')

                try:
                    data[i+1] = int(data[i+1])
                except Exception as ex:
                    print(ex)
                    data[i+1] = -1

                p_data[favorites] = data[i+1]

        # print(p_data)
        p_data = self.trim_output(p_data)
        # print(p_data)

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
            # Function item in ordered dict data?
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
                else:
                    db_list.append(value)



        # db_string = db_string.replace('"', '[Quot]')
        return db_list

    # def create_db(self, db):
    #     conn = sqlite3.connect(db)
    #     c = conn.cursor()
    #     c.execute('''CREATE TABLE content_data
    #               (name text, image_url text, synposis text)''')

    # In the future:
    # Port this db stuff to ReadMALShows...

    def write_to_db(self, anime_url, individual_db, aggregated_db, write_individual_entry = True, write_aggregated_entry = False):
        if write_aggregated_entry == True:
            self.write_to_db_aggregated(aggregated_db, self.content_data, self.name_data, self.info_data, self.statistics_data, self.related_data, anime_url)
        if write_individual_entry == True:
            self.write_to_db_individual(individual_db, self.content_data, self.name_data, self.info_data, self.statistics_data, self.related_data)

    def write_to_db_individual(self, db, content_data, name_data, info_data, statistics_data, related_data):
        # Only write data which is useful for statistics - score, ranked, members, popularity, favourites.
        # Also the time/date data was accessed.

        table_name = content_data['Name:']
        # table_name = table_name.replace()
        # table_name = escape_db_string(table_name)

        # datetime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        datetime = int(round(time.time()))

        if not self.valid_table_name(table_name):
            raise Exception('Invalid MAL username ' + table_name + '; will cause problems with SQL.')

        conn = sqlite3.connect(db)
        c = conn.cursor()
        # print(table_name)
        c.execute('''CREATE TABLE IF NOT EXISTS [{}]
                  (score REAL, ranked INTEGER, members INTEGER, popularity INTEGER, favourites INTEGER, datetime INTEGER)'''.format(table_name))

        # statistics_data_list = self.OD_to_db_list(statistics_data)

        c.execute('INSERT OR IGNORE INTO [{}] VALUES (?,?,?,?,?,?)'.format(table_name),
                  (statistics_data['Score:'], statistics_data['Ranked:'], statistics_data['Members:'], statistics_data['Popularity:'], statistics_data['Favorites:'], datetime))
        conn.commit()

        conn.close()



    def trim_quotations(self, item):
        item = item.strip('"')
        return item

    def write_to_db_aggregated(self, db, content_data, name_data, info_data, statistics_data, related_data, anime_url):
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS content_data
                  (anime_url text,
                  name text PRIMARY KEY, image_url text, synopsis text,
                  english_name text, synonyms text, japanese_name text,
                  media text, episodes INTEGER, aired INTEGER, broadcast text, licensors text, studios text, source text, genres text, duration text, rating text,
                  score REAL, ranked INTEGER, members INTEGER, popularity INTEGER, favourites INTEGER,
                  adaptation text, alternative_version text, side_story text, spinoff text, prequel text, sequel text, summary text)''')
                # Content: Name, pv image URL, synopsis
                # Name: English, synonyms, jp
                # Info: Type, episodes, aired, broadcast, licensors, studios, source, genre, duration, rating
                # Stats: Score, ranked, popularity, members, favourites
                # Related: Adaptation, alternative, side-story, spinoff, prequel, sequel, summary

        # print(content_data)
        content_data_list = self.OD_to_db_list(content_data)
        name_data_list = self.OD_to_db_list(name_data)
        info_data_list = self.OD_to_db_list(info_data)
        statistics_data_list = self.OD_to_db_list(statistics_data)
        related_data_list = self.OD_to_db_list(related_data)

        data_list = [anime_url] + content_data_list + name_data_list + info_data_list + statistics_data_list + related_data_list
        # print(len(data_list))
        # print(content_data_str)
        # content_data_values = (content_data_list[0][1], content_data[1][1], content_data[0][1])

        # Is this susceptible to SQL injections?
        c.execute('INSERT OR REPLACE INTO content_data VALUES (' + '?,'*(len(data_list)-1) + '?)', data_list)
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

    def build_data_from_web(self, MAL_URL):
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
                                            key=lambda t: t[0])
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
    # Done: Add ability to create anime object from anime name only if anime name in database.
    def build_stats_from_db(self, show_name, max_recall):
        db = UNMODELED_DATABASES['show_data_individual']['location']
        conn = sqlite3.connect(db)
        c = conn.cursor()

        # self.declare_stats()
        self.full_stats = [[]]
        self.timestamp = [[]]
        # c.execute('SELECT * FROM sqlite_master WHERE type="table" AND name="[{}]"'.format(show_name))
        # print(c.fetchall())

        if not string_SQL_safe(show_name):
            self.full_stats = [['Why are you doing this?']]
            self.timestamp = [['Nope']]
        else:
            try:
                # http://stackoverflow.com/questions/16856647/sqlite3-programmingerror-incorrect-number-of-bindings-supplied-the-current-sta
                c.execute('''SELECT * FROM [{}] ORDER BY datetime DESC LIMIT (?)'''.format(show_name), (max_recall,))
            except sqlite3.OperationalError:
                self.full_stats = [['Show does not exist in database']]
            else:
                # Returns the transpose of the table data
                # Ordered so that it returns:
                # [(score1, score2, ... ), (popularity1, popularity2, ...), ... , (timestamp1, timestamp2, ...)]
                # Which is easier to handle for Chart.js
                tags = ['score', 'ranked', 'members', 'popularity', 'favorites']
                # print(*c.fetchall())
                full_stats = list(zip(*c.fetchall()))
                timestamp = full_stats[-1:]
                full_stats = full_stats[:-1]
                # print(self.axis_labels)
                self.full_stats = dict(zip(tags, full_stats))
                self.timestamp = dict(zip(['timestamp'], timestamp))

                for key, value in self.full_stats.items():
                    self.full_stats[key] = list(self.full_stats[key])

                for key, value in self.timestamp.items():
                    self.timestamp[key] = list(self.timestamp[key])

                # for index in range(len((self.full_stats['favorites']))):
                #     self.full_stats['score'][index] = float(self.full_stats['score'][index])
                #
                #     self.full_stats['favorites'][index] = int(self.full_stats['favorites'][index].replace(',',''))
                #     self.full_stats['members'][index] = int(self.full_stats['members'][index].replace(',', ''))
                #
                #     self.full_stats['popularity'][index] = int(self.full_stats['popularity'][index][1:]) if \
                #     self.full_stats['popularity'][index][0] == '#' else int(self.full_stats['popularity'][index])
                #     self.full_stats['ranked'][index] = int(self.full_stats['ranked'][index][1:]) if \
                #     self.full_stats['ranked'][index][0] == '#' else int(self.full_stats['ranked'][index])

                # print(dict(zip(*c.fetchall())))
                # print(list(zip([tags ,list(zip(*c.fetchall()))])))
                # self.full_stats = dict(zip([tags ,list(zip(*c.fetchall()))]))
                # self.full_stats = {list(self.p_stats.items())[index]:statistic for index, statistic in enumerate(self.full_stats)}

        # conn.close()

        conn.close()

    def __init__(self):

        pass


# print(parse_titles(data))


