import urllib.request as urllib
import os

from FetchMALData.GetUserPage import UserPageGetter
from User import User

user_list_db = os.path.dirname(__file__) + '/../data/sample_user_list.db'


def write_user_data(filename, MAL_URL, minimal=False, db=True):
    success = False

    # Move this top portion to User class?

    user = User()
    entry_list_tagged = user.create_user_show_list_tagged(MAL_URL)
    # for item in user_data:
    #     print(item)
    # print(user_data)
    if len(entry_list_tagged) != 0:
        if minimal == True and db == False:
            user.write_to_file_data_minimal(filename, entry_list_tagged, MAL_URL)
        elif minimal == True and db == True:
            user.write_to_db_data_minimal(filename, entry_list_tagged, MAL_URL)
        elif minimal == False and db == False:
            user.write_to_file_data(filename, entry_list_tagged)
        elif minimal == False and db == True:
            # Currently no option to write extended info into db
            user.write_to_db_data_minimal(filename, entry_list_tagged, MAL_URL)
        success = True
    else:
        print('Empty entry list tagged.')
    # print('entry list tagged: ')
    return success
    # print(entry_list_tagged)
    # i=0
    # for entry_tagged in entry_list_tagged:
    #     # print(item)
    #     f.write('**[''Newshow'']**' + ' ;-; ' + str(i) + '\n')
    #     for attribute in entry_tagged:
    #         # f.write(str(i) + ';-; Attribute: ' + attribute[0] + ' ;-; Value: ' + attribute[1])
    #         f.write(attribute[0] + ' ;-; ' + attribute[1])
    #         f.write('\n')
    #         # print(i)
    #     i+=1

    # f.close()

def get_users(filename):

    f = open(filename)
    html = f.read()
    upg = UserPageGetter()
    upg.feed(html)
    user_list = upg.data

    for index, user in enumerate(user_list):

        # print(user)
        if index > 6:
            break

    return user_list



user_list = get_users('users.php.html')
#Start writing from:
start_point = 5166
end_point = 10000
success_count = 0
for index, MAL_URL in enumerate(user_list):
    if index >= start_point:
        print(str(index) + ' : ' + MAL_URL)
        try:
            success = write_user_data(user_list_db, MAL_URL, minimal=True, db=True)
            if success == True:
                success_count += 1
        except urllib.HTTPError as e:
            print('User no longer exists/has changed name.')
        except Exception as e:
            print('Error!')
            print(e)

    if index == end_point:
        break

print(success_count/(end_point - start_point))

# response = urllib.urlopen('https://myanimelist.net/animelist/Nosreme?status=7&order=4&tag=')
# html = str(response.read())
# usg = UserShowGetterT2()
# usg.feed(html)
# usg.reformat_data()
# user_data = usg.reformatted_data
#
# print(user_data)
#
# f = open('sample_user_data_2.txt', 'w')
# f.write(user_data)
# f.close()

# Should never have to call this function again, ever. (After parsing in User class fixed to remove outer quotes)
# def remove_outer_quotes(db = 'sample_user_list.db'):
#     # Prone to injection
#     conn = sqlite3.connect(db)
#     c = conn.cursor()
#
#     c.execute('''SELECT name FROM sqlite_master WHERE type="table";''')
#     tables_list = ['[' + item[0] + ']' for item in c.fetchall()]
#     # tables_list = c.fetchall()
#
#     for i, table in enumerate(tables_list):
#         # print(type(table))
#         print('index: ' + str(i) + ', table: ' + table)
#         c.execute('''SELECT "anime" FROM {}'''.format(table))
#         row_list = [item[0] for item in c.fetchall()]
#         # print(row_list)
#         # table = table[:-1] if table.endswith(']') else table
#         # table = table[1:] if table.startswith('[') else table
#         # print(table)
#         for index, row in enumerate(row_list):
#             # print(row)
#             row_list[index] = row[:-1] if row.endswith('"') else row
#             row_list[index] = row_list[index][1:] if row.startswith('"') else row
#             # print(row_list[index])
#             # http://stackoverflow.com/questions/25387537/sqlite3-operationalerror-near-syntax-error
#             # Use String.format for database object;
#             # Use sql parameter formatting for non-database objects
#             c.execute('''UPDATE {} SET "anime" = ? WHERE "anime" = ?'''.format(table), (row_list[index], row))
#             # print(row)
#         # print(table)
#         c.execute('''SELECT "anime" from {}'''.format(table))
#         # print(len(c.fetchall()))
#
#         #
#         #     print(row)
#         #     c.execute('''SELECT "anime" from {}'''.format(row))
#
#         # c.execute('''UPDATE {} '''.format(table))
#     conn.commit()
#     conn.close()
# # remove_outer_quotes()