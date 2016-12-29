from FetchMALData.ParseUserPage import UserShowGetter, UserShowGetterT2
from FetchMALData.GetUserPage import UserPageGetter
from FetchMALData.User import User
import urllib.request as urllib

def write_user_data(filename, MAL_URL, minimal=False, db=True):
    success = False

    response = urllib.urlopen(MAL_URL)
    html = str(response.read())

    if '<div id="list_surround">' in html:
        usg = UserShowGetterT2()
        usg.feed(html)
        usg.reformat_data()
        user_data = usg.reformatted_data
    else:
        usg = UserShowGetter()
        usg.feed(html)
        usg.reformat_data()
        # user_data = usg.reformatted_data
        user_data = usg.data

    # if user_data == []:
    #     print('Unable to parse user MAL page html!')
    #     return

    # f = open('sample_user_data_tagged.txt', 'w')
    # f.write(user_data)

    user = User(user_data)
    entry_list_tagged = user.entry_list_tagged
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
            success = write_user_data('sample_user_list.db', MAL_URL, minimal=True, db=True)
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