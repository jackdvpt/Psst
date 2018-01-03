import bottle
import uuid
from random import randint


# this variable MUST be used as the name for the cookie used by this application
COOKIE_NAME = 'sessionid'

def check_login(db, usernick, password):
    """returns True if password matches stored"""
    cur = db.cursor()
    sql = "SELECT nick, password FROM users WHERE nick = ?"
    cur.execute(sql,(usernick,))

    for rows in cur:
        if rows[1] == db.crypt(password):
            return True

    return False


def generate_session(db, usernick):
    """create a new session and add a cookie to the response object (bottle.response)
    user must be a valid user in the database, if not, return None
    There should only be one session per user at any time, if there
    is already a session active, use the existing sessionid in the cookie
        WARNING : Do not reset database.py (ie run it) whilst a cookie is in a browser
            It will cause an error and you will not be able to log out
    """
    cur = db.cursor()
    sql = "SELECT * FROM sessions WHERE usernick = ?"
    cur.execute(sql,(usernick,))
    key = ""
    if len(cur.fetchall()) == 0:
        cur_new = db.cursor()
        sqled = "SELECT nick FROM users WHERE nick = ?"
        cur_new.execute(sqled, (usernick,))
        if len(cur_new.fetchall()) == 0:
            return None
        key = str(uuid.uuid4())
        cur = db.cursor()
        newSql = "INSERT INTO sessions (sessionid, usernick) VALUES (?, ?)"
        cur.execute(newSql, (key, usernick,))
        db.commit()
        bottle.response.set_cookie(COOKIE_NAME, key)

    else:
        cur.execute(sql, (usernick,))
        for rows in cur:
            key=rows[0]
            bottle.response.set_cookie(COOKIE_NAME, key)
    return key


def delete_session(db, usernick):
    """remove all session table entries for this user"""
    cur = db.cursor()
    sql = "DELETE FROM sessions WHERE usernick = ?"
    cur.execute(sql, (usernick,))
    bottle.response.set_cookie(COOKIE_NAME, "")


def session_user(db):
    """try to
    retrieve the user from the sessions table
    return usernick or None if no valid session is present"""
    key = bottle.request.get_cookie(COOKIE_NAME)
    cur = db.cursor()
    cur.execute("SELECT * FROM sessions WHERE sessionid=?", (key,))
    row = cur.fetchone()
    if not row:
        return None
    return row[1]


def find_user(db, username):
    """
    Returns the infromation to the username provided
    """
    cur = db.cursor()
    sql = "SELECT * FROM users WHERE nick = ?"
    cur.execute(sql, (username,))
    return cur.fetchall()


def randEnd():
    """
    :return:A suffex for the robohash website that changes the type of picture used
    """
    type =randint(1, 30)
    if type <10 :
        return "s"
    if 11 < type < 20:
        return "?set=set2"
    if 21 < type < 30:
        return "?set=set3"


def add_user(db, username, password, pic):
    """
        Originally for internal testing
        Now used to add a new user to the database
        Returns -1 if it fails
            usually because the username already exists
        Casts username, password & pic to string so it doesnt insert them as numbers if they are just numbers
    :return: -1 if insert failed
    """
    temp = randEnd()
    picture = "http://robohash.org/" + str(pic) + str(temp)
    cur = db.cursor()
    cur.execute("SELECT count(*) from users where nick = ?", (username,))
    data = cur.fetchone()[0]
    if data == 0:
        sql = "INSERT INTO users (nick, password, avatar) VALUES (?,?,?)"
        cur.execute(sql, (str(username), db.crypt(str(password)), picture,))
        db.commit()
    else :
        return -1

def checkValid(nickname, password, picture):
    """
    Checks if the username , password and picture are valid
        IE no spaces in username or picture
        And none are empty
    :return:
        return -1 if nicknane is not valid
        return -2 if password is not valid
        return -3 if picture is not valid
        Returns 3 (more than 0) if valid
    """
    symbol = """ ~`!@#$%^&*()_-+={}[]:>;',</?*-+"'"""
    if len(nickname.split()) > 1:  # The username has more than one word ie a space character
        return -1
    elif len(nickname) == 0:
        return -1
    elif len(password) == 0:
        return -2
    elif len(picture) == 0:
        return -3
    elif len(picture.split()) > 1:  # The picture has more than one word ie a space character
        return -3
    else:
        for i in nickname:
            if i in symbol:
                return -1
        for i in picture:
            if i in symbol:
                return -3
        return 3


def make_follow(db, user, following):
    """
    As a user i can follow another user and see there posts
    :param db:
    :param user:    User who wants to follow following
    :param following:   USer they want to follow
    :return:
    """
    cur = db.cursor()
    cur.execute("SELECT count(*) from follows where follower = ? AND followed = ?", (user , following,))
    data = cur.fetchone()[0]
    if data == 0:
        sql = "INSERT INTO follows (follower, followed) VALUES (?, ?)"
        cur.execute(sql, (user, following,))
        db.commit()


def make_unfollow(db, user, following):
    """
    Removes user from following another user
    :param db:
    :param user:    User
    :param following:   USer they want to stop following
    :return:
    """
    cur = db.cursor()
    cur.execute("SELECT count(*) from follows where follower = ? AND followed = ?", (user, following,))
    data = cur.fetchone()[0]
    if data == 1:
        sql = "DELETE FROM follows WHERE follower = ? AND followed = ?"
        cur.execute(sql, (user, following,))
        db.commit()



def does_follow(db, user, following):
    """
        Checks if user is currently following 'following'
    :param db:
    :param user: The user
    :param following:   The user to check
    :return: 0 if they dont follow, 1 if they do
    """
    cur = db.cursor()
    cur.execute("SELECT count(*) from follows where follower = ? AND followed = ?", (user, following,))
    data = cur.fetchone()[0]
    return data


def follows(db, user):
    """
    Check if a user follows any other users
    :param user: The user to check
    :return: -1 if user is None (ie no one is logged in)
        or the length of the db (0 means they dont follow anyone)
    """
    cur = db.cursor()
    if user is None:
        return -1
    else:
        cur.execute("SELECT * from follows where follower = ?", (user,))
        data = cur.fetchall()
        return len(data)


def get_following(db, user):
    """
    :param user: The user in question
    :return: Returns a list of users that user follows
    """
    cur = db.cursor()
    cur.execute("SELECT * from follows where follower = ? ", (user,))
    data = cur.fetchall()
    test =[]
    for name in data:
        test.append(name[1])
    return test
