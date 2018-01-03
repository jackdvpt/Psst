import re
import html


def find_url(message):
    """
        Finds any url inside of the message and adds it to a list
    :param message: The original message with html codes intact (Url's can contain "&")
    :return: All url's that begin with either (www. | http:// | https:// ) and end with a whitespace
    """
    url = re.findall(r'(?:(www.)|(http://)|(https://))([^\s]+)', message)
    return url


def replace_url(message, list):
    """ Takes the message and replaces any url's found with an HTML link
    :param message: Message from the user
    :param list:    List of url's inside of the message
    :return:    The original message but with all url's replaced with html link
    """
    temp = message
    for url in list:
        num = 0
        if len(url[1]) != 0:
            num = 1
        if len(url[2]) != 0:
            num = 2
        temp = temp.replace(url[num]+url[3], "<a href='" + url[num]+url[3] + "'>" + url[num]+url[3] + "</a>")
    return temp


def find_mentions(string):
    """
        Finds all mentions inside of the message
            with_ful searches for any word then fullstop and word after it
            without_full searches for just a word
            IT then checks if with_ful is longer than without_full by more than one to ensure that there is text
                after the fullstop
    :param string: The message
    :return:    A list of mentions found in the message
    """
    with_ful = re.findall(r'@([\w\.\w]+)', string)
    without_full = re.findall(r'@([\w]+)', string)
    for dot, no in zip(with_ful, without_full):
        if len(dot) == len(no)+1:
            return without_full
        else :
            return with_ful


def replace_mentions(string, newt):
    """
        Takes a message and a list of names mentioned and converts them to html
            Any extra occurences of the name will not convert
            Only items in newt that begin with @ in the message will be converted
    :param string: Message with html tags replaced
    :param newt: The list of found mentions
    :return: Message but with mentions replaced with the html code
    """
    temp = string
    if newt != None:
        for names in newt:
            temp = temp.replace("@" + names, "<a href='/users/"+ names +"'>" + "@"+ names + "</a>")
    return temp


def find_hashtag(string):
    """Searches for hashtags in the message
        Seperated to ensure that extra characters made when converting
            html characters are not included
    :param string: Messsage with html characters still intact
    :return: A list containing all hashtags found inside of the message
    """
    hash = re.findall(r'^#(\w+)|#(\w+)', string)
    return hash


def replace_pound_sign(string,newt):
    """
        Takes the list (newt) of hashtags and converts them to the strong class
            Checks first if the first or second regualr expression was used
    :param string:
    :param newt:
    :return:
    """
    temp = string
    for names in newt:
        num = 0
        if len(names[1]) != 0:
            num = 1
        temp = temp.replace("#" + names[num], "<strong class='hashtag'>"+ "#"+ names[num] +"</strong>")
    return temp


def post_to_html(content):
    """Convert a post to safe HTML, quote any HTML code, convert
    URLs to live links and spot any @mentions or #tags and turn
    them into links.  Return the HTML string
    """
    mentions = find_mentions(content)
    hashtag = find_hashtag(content)
    url = find_url(content)
    temp=  html.escape(content, quote=False)
    temp = replace_mentions(temp, mentions)
    temp = replace_pound_sign(temp,hashtag)
    temp = replace_url(temp, url)
    return temp


def post_list(db, usernick=None, limit=50):
    """Return a list of posts ordered by date
    db is a database connection (as returned by PsstDb())
    if usernick is not None, return only posts by this user
    return at most limit posts (default 50)

    Returns a list of tuples (id, timestamp, usernick, avatar,  content)
    """
    cursor = db.cursor()
    avatarCursoru = db.cursor()
    if (usernick == None):
        query = """
        SELECT id, timestamp, usernick, content
        FROM posts
        WHERE id <= ?
        ORDER BY timestamp DESC
        """
        cursor.execute(query, (limit,))
    if (usernick != None):
        query = """
        SELECT id, timestamp, usernick, content
        FROM posts
        WHERE id <= ? AND usernick = ?
        ORDER BY timestamp DESC
        """
        cursor.execute(query, (limit,usernick,))

    results = []
    post_id = None
    post_time = None
    post_user = None
    post_avatar = None
    post_content = None
    for row in cursor:
        post_id = row[0]
        post_time = row[1]
        post_user = row[2]
        avatarCursoru.execute("SELECT avatar FROM users where users.nick =" + repr(post_user))
        for newRow in avatarCursoru:
            post_avatar = newRow[0]
            post_content = row[3]
        tup = (post_id, post_time, post_user, post_avatar, post_content)
        results.append(tup)
    return results



def post_list_follows(db,following,  usernick, limit=50):
    """
        Returns all posts of the users taht are followed by usernick
        Including usernicks posts
    return at most limit posts (default 50)

    Returns a list of tuples (id, timestamp, usernick, avatar,  content)
    """
    test = following

    test.append(usernick)   #show the users posts as well
    #This can cause the name to be listed twice because the test function makes them follow themself
    cursor = db.cursor()
    avatarCursoru = db.cursor()
    placeholders = ', '.join(['?']*len(test))
    query = "SELECT id, timestamp, usernick, content FROM posts WHERE usernick IN ({}) ".format(placeholders)
    cursor.execute(query, tuple(test))
    results = []
    post_id = None
    post_time = None
    post_user = None
    post_avatar = None
    post_content = None
    for row in cursor:
        post_id = row[0]
        post_time = row[1]
        post_user = row[2]
        avatarCursoru.execute("SELECT avatar FROM users where users.nick =" + repr(post_user))
        for newRow in avatarCursoru:
            post_avatar = newRow[0]
            post_content = row[3]
        tup = (post_id, post_time, post_user, post_avatar, post_content)
        results.append(tup)
    return results




def post_list_mentions(db, usernick, limit=50):
    """Return a list of posts that mention usernick, ordered by date
    db is a database connection (as returned by COMP249Db())
    return at most limit posts (default 50)

    Returns a list of tuples (id, timestamp, usernick, avatar,  content)
    """
    cursor = db.cursor()
    avatarCursoru = db.cursor()
    at = '%@' + usernick + '%'
    query = """
        SELECT id, timestamp, usernick, content
        FROM posts
        WHERE id <= ? AND content LIKE ?
        ORDER BY timestamp DESC
        """
    cursor.execute(query, (limit,at))

    results = []
    post_id = None
    post_time = None
    post_user = None
    post_avatar = None
    post_content = None
    for row in cursor:
        post_id = row[0]
        post_time = row[1]
        post_user = row[2]
        avatarCursoru.execute("SELECT avatar FROM users where users.nick =" + repr(post_user))
        for newRow in avatarCursoru:
            post_avatar = newRow[0]
        post_content = row[3]
        tup = (post_id, post_time, post_user, post_avatar, post_content)
        results.append(tup)
    return results


def return_users(db):
    """
    Returns all of the users in the database for the users screen
    """
    cursor = db.cursor()
    cursor.execute("SELECT avatar, nick from users")
    user_id = None
    user_avatar = None
    user_result = []
    for user in cursor:
        user_id = user[0]
        user_avatar = user[1]
        tup = (user_id, user_avatar)
        user_result.append(tup)
    return user_result


def post_add(db, usernick, message):
    """Add a new post to the database.
    The date of the post will be the current time and date.

    Return a the id of the newly created post or None if there was a problem"""
    if len(message) > 150:
        return None
    cursor = db.cursor()
    cursor.execute("INSERT INTO posts (usernick, content) VALUES (?, ?)", (usernick, post_to_html(message),))
    db.commit()

    query = """
            SELECT * FROM posts ORDER BY timestamp DESC, ROWID ASC LIMIT 1
            """
    cursor.execute(query)
    for row in cursor:
        return row[0]
    else:
        return None


def post_search(db, search, type):
    """
    Doesnt work with '@name' for some reason
    :param db: Database to search in
    :param search: The term to search
    :param type : Any advanced searches that will be taken into account (integer)
    :return: A list of all messages in db that contain the term
    """
    cursor = db.cursor()
    avatarCursoru = db.cursor()
    query = """
            SELECT id, timestamp, usernick, content
            FROM posts
            WHERE content LIKE ?
            ORDER BY timestamp DESC
            """
    if type == '0':
        search_term = '%' + search + '%'
    if type == '1':
        search_term = search + '%'
    if type == '2':
        search_term = '%' + search
    if type == '3':
        search_term = search

    cursor.execute(query, (search_term,))

    results = []
    post_id = None
    post_time = None
    post_user = None
    post_avatar = None
    post_content = None
    for row in cursor:
        post_id = row[0]
        post_time = row[1]
        post_user = row[2]
        avatarCursoru.execute("SELECT avatar FROM users where users.nick =" + repr(post_user))
        for newRow in avatarCursoru:
            post_avatar = newRow[0]
        post_content = bolded(row[3], search)
        tup = (post_id, post_time, post_user, post_avatar, post_content)
        results.append(tup)
    return results

def bolded(todo,serach):
    boldbig = "<b>" + serach + "</b>"
    nowbold = todo.replace(serach, boldbig)
    return nowbold
