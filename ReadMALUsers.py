from ParseUserPage import UserShowGetter
from GetUserPage import UserPageGetter
from User import User
import urllib.request as urllib

def write_user_data_to_file(filename, MAL_URL):

    response = urllib.urlopen(MAL_URL)
    html = str(response.read())
    usg = UserShowGetter()
    usg.feed(html)
    user_data = usg.data

    # f = open('sample_user_data_tagged.txt', 'w')
    # f.write(user_data)

    user = User(user_data)
    entry_list_tagged = user.entry_list_tagged
    # for item in user_data:
    #     print(item)
    # print(user_data)
    user.write_to_file_data(filename, user.entry_list_tagged)
    print('entry list tagged: ')
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

    return user_list[0:10]


# MAL_URL = 'https://myanimelist.net/animelist/kawaiigirl356'
# write_user_data_to_file(MAL_URL)

user_list = get_users('users.php.html')
for MAL_URL in user_list:
    try:
        write_user_data_to_file('sample_user_list.txt', MAL_URL)
    except urllib.HTTPError as e:
        print('User no longer exists/has changed name.')


# user = User()