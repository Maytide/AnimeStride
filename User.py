import urllib.request as urllib
import sqlite3

from FetchMALData.ParseUserPage import UserShowGetter, UserShowGetterT2
from Recommender.Recommender import Recommender

class User():

    def write_to_file_data(self, filename, entry_list_tagged):
        #sample_user_data_tagged.txt
        with open(filename, 'a') as file:
            i = 0
            file.write('++[''Newuser'']++' + ' :-: ' + str(i) + '\n')
            for entry_tagged in entry_list_tagged:
                # print(item)
                file.write('**[''Newshow'']**' + ' :-: ' + str(i) + '\n')
                for attribute in entry_tagged:
                    # f.write(str(i) + ';-; Attribute: ' + attribute[0] + ' ;-; Value: ' + attribute[1])
                    file.write(attribute[0] + ' :-: ' + attribute[1])
                    file.write('\n')
                    # print(i)
                i += 1

    def write_to_file_data_minimal(self, filename, entry_list_tagged, MAL_URL):
        #sample_user_data_tagged.txt
        with open(filename, 'a') as file:
            i = 0
            file.write('++[''Newuser'']++' + ' :-: ' + MAL_URL + '\n')
            for entry_tagged in entry_list_tagged:
                # print(entry_tagged)
                # file.write(str(entry_tagged) + '\n')
                file.write('**[''Newshow'']**' + ' :-: ' + str(i) + '\n')
                for attribute in entry_tagged:
                    # f.write(str(i) + ';-; Attribute: ' + attribute[0] + ' ;-; Value: ' + attribute[1])
                    if attribute[0] == '"score"' or attribute[0] == '"anime_title"':
                        file.write(attribute[0] + ' :-: ' + attribute[1])
                        file.write('\n')
                        # print(i)

                i += 1
                file.write('\n')

    def valid_table_name(self, table_name):
        # Prevent injections
        return not ('drop table' in table_name.lower())
        # return all(char.isalnum() for char in table_name)

    def write_to_db_data_minimal(self, db, entry_list_tagged, MAL_URL):
        # TODO:
        # Vulnerable to SQL Injection! Fix in the future!
        # Remove quotes from anime name! - Done in create_user_show_list_tagged(...). Removed quotes when parsing from MAL directly.
        if not self.valid_table_name(MAL_URL):
            raise Exception('Invalid MAL username ' + MAL_URL + '; will cause problems with SQL.')

        # Format so can use any characters in SQL table name
        MAL_URL_formatted = '[' + MAL_URL + ']'

        conn = sqlite3.connect(db)
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS {}
                  (anime TEXT, score TEXT, UNIQUE (anime))'''.format(MAL_URL_formatted))

        for entry_tagged in entry_list_tagged:
            anime_title = ''
            score = ''
            for attribute in entry_tagged:
                if attribute[0] == '"score"':
                    score = attribute[1]
                elif attribute[0] == '"anime_title"':
                    anime_title = attribute[1]
            # http://stackoverflow.com/questions/3634984/insert-if-not-exists-else-update
            # Method does not work to update 1 field at a time - this shouldn't be a problem for this.
            c.execute('INSERT OR REPLACE INTO ' + MAL_URL_formatted + ' VALUES (?,?)', (anime_title, score))

        conn.commit()
        conn.close()

    def print_entry_list(self, entry_list):
        for index, entry in enumerate(entry_list):
            print(entry)

    def print_entry_list_tagged(self, entry_list_tagged):
        for index, (tag, entry) in enumerate(entry_list_tagged):
            print('Tag: ' + tag + ', Entry: ' + entry)

    #Unused
    def get_text_between_quot(self, user_show_data):
        # str_index = 0
        #
        # while str_index < len(entry) - 6:
        entry_list = user_show_data.split('&quot;')
        entry_list = [entry for entry in entry_list if entry != ':' and entry != ',' and entry != '},{']
        return entry_list

    def get_text_between_bracket(self, user_show_data_list):
        # str_index = 0
        # show_data_current = ''
        # show_data_list = []
        # add_info = False
        # while str_index < len(user_show_data_list):
        #     if add_info == True and user_show_data_list[str_index] != '}':
        #         # print('getting text between bracket')
        #         show_data_current += user_show_data_list[str_index]
        #     if user_show_data_list[str_index] == '{':
        #         add_info = True
        #     elif user_show_data_list[str_index] == '}':
        #         add_info = False
        #         show_data_list.append(show_data_current)
        #         show_data_current = ''
        #     str_index += 1
        #
        # return show_data_list
        str_index = 0
        show_data_current = ''
        show_data_list = []
        add_info = 0
        while str_index < len(user_show_data_list):
            if add_info == 1 and user_show_data_list[str_index] != '}':
                # print('getting text between bracket')
                current_char = user_show_data_list[str_index]
                # if current_char == ',':
                #     current_char = '[Comma]'
                show_data_current += current_char
            elif add_info > 1 and user_show_data_list[str_index] != '}' and user_show_data_list[str_index] != '{':
                show_data_current += user_show_data_list[str_index]
            if user_show_data_list[str_index] == '{':
                add_info = add_info + 1
            if add_info == 1 and user_show_data_list[str_index] == '}':
                add_info = add_info - 1
                show_data_list.append(show_data_current)
                show_data_current = ''
            elif add_info > 1 and user_show_data_list[str_index] == '}':
                add_info = add_info = 1
            str_index += 1
        # print(show_data_list)
        return show_data_list
    # user
    # entry_list
    # attribute_list
    # attribute_list_tagged

    def replace_comma_between_quote(self, entry):
        str_index = 0
        commaless_entry_str = ''
        in_string = False
        while str_index < len(entry):
            current_char = entry[str_index]
            if entry[str_index] == ',' and in_string == True:
                #Special value for comma character
                current_char = '[Comma]'
            if entry[str_index] == '"' and in_string == False:
                in_string = True
            elif entry[str_index] == '"' and in_string == True:
                in_string = False
            commaless_entry_str += current_char
            str_index += 1
        return commaless_entry_str

    def get_attributes(self, entry):
        user_show_data_list = entry.split(',')
        # User page with additional comments: https://myanimelist.net/animelist/AnimaticLunatic
        # Breaks because comma inside quote inside comment :/
        # Possible solution: If comma is not beside a quot, remove it?
        # for user_show_data in user_show_data_list:
        #     if (':' not in user_show_data):
        #         print('Data missing colon: ' + user_show_data)
        #     else:
        #         print('Data with colon: ' + user_show_data)

        return [user_show_data for user_show_data in user_show_data_list if user_show_data != '']

    def create_user_show_list_tagged(self, MAL_URL, minimal = False):
        self.MAL_URL = MAL_URL
        response = urllib.urlopen(self.MAL_URL)
        html = str(response.read())

        if '<div id="list_surround">' in html:
            usg = UserShowGetterT2()
            usg.feed(html)
            usg.reformat_data()
            sample_user_data = usg.reformatted_data
        else:
            usg = UserShowGetter()
            usg.feed(html)
            usg.reformat_data()
            # user_data = usg.reformatted_data
            sample_user_data = usg.data
            # print(sample_user_data)


        table_entry = sample_user_data
        entry_list = self.get_text_between_bracket(table_entry)
        # print(len(entry_list))
        self.entry_list_tagged = []
        for entry in entry_list:
            attribute_list_tagged = []
            # print('create_user_show_list_tagged: ' + entry)
            entry = self.replace_comma_between_quote(entry)
            # attribute_list = self.get_text_between_quot(entry)
            attribute_list = self.get_attributes(entry)
            tagged_entry = ['', '']
            # for index, attribute in enumerate(attribute_list):
            #     if index % 2 == 1:
            #         tagged_entry = ['', '']
            #         tagged_entry[0] = attribute
            #         print('attribute: ' + attribute)
            #     elif index % 2 == 0 and index > 0:
            #         tagged_entry[1] = attribute
            #         print('attribute: ' + attribute)
            #         attribute_list_tagged.append(tagged_entry)
            for attribute_item in attribute_list:
                # print('attribute; ' + attribute)
                try:
                    (attribute, value) = attribute_item.split(':', 1)
                except ValueError as e:
                    print('Unable to parse user MAL page html!')
                    print('attribute; ' + attribute_item)
                    print(e)
                    return []
                    # print('Error: ' + attribute)
                if minimal:
                    # print(attribute)
                    if attribute != '"score"' and attribute != '"anime_title"':
                        continue
                tagged_entry[0] = attribute
                tagged_entry[1] = value

                tagged_entry[1] = tagged_entry[1][:-1] if tagged_entry[1].endswith('"') else tagged_entry[1]
                tagged_entry[1] = tagged_entry[1][1:] if tagged_entry[1].startswith('"') else tagged_entry[1]
                # print('attribute; ' + tagged_entry[0] + ' ; ' + tagged_entry[1])
                # print(tagged_entry)
                attribute_list_tagged.append((tagged_entry[0], tagged_entry[1]))
            self.entry_list_tagged.append(attribute_list_tagged)
            # print_entry_list_tagged(attribute_list_tagged)
            # entry_list_tagged.append(attribute_list_tagged)

        # print(attribute_list_tagged)
        return self.entry_list_tagged

    # def get_user_data_from_db(self, db):
    #     pass

    # Enforce that recommendations must be made from entering a new user from the web:
    # User data cannot be taken from database for this purpose.
    def get_user_recommendation(self, recommender = 'c', verbose = False):
        if self.MAL_URL == '':
            raise Exception('User has no MAL URL defined.')
        entry_dict_tagged = dict()

        # print(self.entry_list_tagged)

        # filtered_list_tagged = []
        # # Filter entry list tagged
        # for show in self.entry_list_tagged:
        #     anime_title = ''
        #     score = ''
        #     for attribute_item in show:


        for score, anime_title in self.entry_list_tagged:
            score = score[1] if score[1] != '-' else '0'
            # print(score)
            anime_title = anime_title[1]
            entry_dict_tagged[anime_title] = score

        r = Recommender()
        return r.get_recommendation_c(entry_dict_tagged, verbose = verbose)




    # @classmethod
    # def from_untagged_data(user_class, user_data):
    #     entry_list_tagged = user_class.create_user_show_list_tagged(user_data)
    #     return entry_list_tagged

    def __init__(self):
        self.MAL_URL = ''
        self.username = ''
        self.entry_list_tagged = []
        # self.entry_list_tagged = self.create_user_show_list_tagged(user_data)

        # sample_user_data = open('sample_user_data.txt', 'r').read()
        # self.entry_list_tagged = self.create_user_show_list_tagged(sample_user_data)



