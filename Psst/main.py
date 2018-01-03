__author__ = 'Jack Davenport'
from bottle import Bottle, template, static_file, request, response, HTTPError, redirect, error
import interface
import users
from database import PsstDb

COOKIE_NAME = 'sessionid'

application = Bottle()


def has_visited():
    """Check if a cookie exists (ie a user is logged in)
    Returns 1 if no
    returns -1 if user is logged in"""
    cook = request.get_cookie(COOKIE_NAME)
    if cook:
        return -1
    else:
        return 1


@application.route('/')
def index():
    """Home page, displays the welcome message and the most recent posts"""
    db = PsstDb()
    name = users.session_user(db)
    if users.follows(db,users.session_user(db)) > 0:
        re = interface.post_list_follows(db, users.get_following(db,name ),name, 50)
    else :
        re = interface.post_list(db, None, 50)
    info = {
        'login': has_visited(),
        'searchVal': "",
        'usernamed': users.session_user(db),
        'title': "Welcome to Psst",
        'content': 'Welcome to Psst',
        'posts': re
    }
    return template('index', info)


@application.route('/reg')
def reg():
    """As a user i can register as an new user.
        This page displays the forms required for the user to register
            The username must be unique, if the username is not then an error is displayed
    """
    db = PsstDb()
    info = {
        'login': has_visited(),
        'usernamed': users.session_user(db),
        'title': "Register to Psst",
        'comment': """""",

    }
    return template('register', info)


@application.post('/register')
def register():
    """
    As a user when i register for PSST! i should be told if any of my information is wrong
        Handels the forms for users registration
        Checks that the details are valid (not null, username doesnt have space)
        Then adds to the database
            If the username already exists it returns an page with an error
    """
    db = PsstDb()
    nickname = request.forms.get('username')
    password = request.forms.get('pass')
    picture = request.forms.get('pic')
    valid = users.checkValid(nickname, password, picture)
    if valid < 0:
        info = {'login': has_visited(),
                'searchVal': "",
                'usernamed': users.session_user(db),
                'title': "Welcome to Psst",
                'comment': 'Registration Failed',
                'posts': []
                }
        if valid == -1:
            info['comment'] = 'Registration Failed, Looks like your username has something wrong with it'
        if valid == -2:
            info['comment'] = 'Registration Failed, Looks like your password has something wrong with it'
        if valid == -3:
            info['comment'] = 'Registration Failed, Looks like your picture has something wrong with it'
        return template('register', info)
    else:
        temp = users.add_user(db, nickname, password, picture)
        if temp == -1:
            info = {'login': has_visited(),
                    'searchVal': "",
                    'usernamed': users.session_user(db),
                    'title': "Welcome to Psst",
                    'content': 'Registration Failed, Please try again. Error. Go back. Nothing more to see here. Youll need to try again (your username may already exist)',
                    'posts': []
                    }
            return template('index', info)
        else:
            redirect('/')


@application.route('/follow/<who>')
def follow(who):
    db = PsstDb()
    users.make_follow(db,users.session_user(db), who)
    redirect('/users/'+who)


@application.route('/unfollow/<who>')
def follow(who):
    db = PsstDb()
    users.make_unfollow(db,users.session_user(db), who)
    redirect('/users/'+who)


@application.post('/login')
def login():
    """
    As a Registered user i am able to insert my username and password to log into PSST!
    When a user logs in, check if the username and password is valid
    If so then add there session, and set cookie value
    If not then display an page saying failed login
    """
    db = PsstDb()
    username = request.forms.get('nick')
    password = request.forms.get('password')
    if users.check_login(db, username, password) == True:
        users.generate_session(db, username)
        redirect('/')
    else:
        info = {'login': has_visited(),
                'searchVal': "",
                'usernamed': users.session_user(db),
                'title': "Welcome to Psst",
                'content': 'Login Failed, Please try again. Error',
                'posts': []
                }
        return template('index', info)


@application.post('/post')
def post():
    """
    As a registered logged in user i am able to make a new post to PSST!
    Takes the post from the POST request and adds it to teh database.
        Then redirects to the homepage
    :return:
    """
    db = PsstDb()
    post = request.forms.get('post')
    test = interface.post_add(db, users.session_user(db), post)
    redirect('/')


@application.post('/logout')
def login():
    """
    As a registered user when i wish to log out i see a button that will log me out of PSST!
    Removes the users session from the database then redirectes them to the homepage
    """
    db = PsstDb()
    users.delete_session(db, users.session_user(db))
    redirect('/')


@application.route('/about')
def about_page():
    """Returns the about page, which contains the text required about the service and some other text.
            Because there are no posts, the posts field is left empty, which will then not display anything on the page
    """
    db = PsstDb()
    about = {
        'login': has_visited(),
        'searchVal': "",
        'usernamed': users.session_user(db),
        'title': 'About',
        'content': """Psst is a new, exciting, messaging service like nothing you\'ve seen before!
        Have you ever used twitter? Because this isnt twitter. you cant sue us because we said that""",
        'posts': []
    }
    return template('index', about)


@application.route('/users/<name>')
def user_page(name):
    """
    Returns the user about page, with a larger user avatar and username along with the posts made by the user
    """
    db = PsstDb()
    userpage = interface.post_list(db, name, 50)
    av = users.find_user(db, name)

    user = {
        'login': has_visited(),
        'usernamed': users.session_user(db),
        'title': name,
        'avatar': av[0][2],
        'username': name,
        'posts': userpage,
        'follows':users.does_follow(db, users.session_user(db), name),
        'following': users.get_following(db, users.session_user(db))
    }
    return template('userPosts', user)


@application.route('/search')
def search_page():
    """
    As a user i can search for the posts that have been made on the site
    Returns all posts that contain the search term.
    """
    db = PsstDb()
    post = request.query['search']
    type = request.query['adv']
    re = interface.post_search(db, post, type)
    advanced_message = ""
    if int(type) > 1:
        if type == '1':
            advanced_message = ' With the criteria that the post starts with it'
        elif type == '2':
            advanced_message = ' With the criteria that the post ends with it'
        elif type == '3':
            advanced_message = ' With the criteria that the post is an exact match'
    if len(re) > 0:
            contents = 'You have searched for "' + str(post) + '"' + advanced_message
    else:
        contents = 'Your search for "' + str(post) + '" has no results'+ advanced_message
    user = {
        'login': has_visited(),
        'searchVal': str(post),
        'usernamed': users.session_user(db),
        'title': 'Search for "' + str(post) + '"',
        'content': contents,
        'posts': re
    }
    return template('index', user)


@application.route('/users')
def user_page():
    """
    As a user when i go to /uesers i see a list of all users on PSST!
    Returns a page with all users currently in the database
    """
    db = PsstDb()
    users_list = interface.return_users(db)
    user = {
        'login': has_visited(),
        'searchVal' : "",
        'usernamed': users.session_user(db),
        'title': "Users on Psst",
        'message': "Click on a user to see there Pssts",
        'users': users_list
    }
    return template('user', user)


@application.route('/mentions/<name>')
def user_page(name):
    """
    Returns a page with all of the posts that contain @name in them
    """
    db = PsstDb()
    Mentions = interface.post_list_mentions(db, name, 50)
    mention = {
        'login': has_visited(),
        'searchVal': "",
        'usernamed': users.session_user(db),
        'title': name,
        'content': "Mentions for the user @" + name,
        'posts': Mentions
    }
    return template('index', mention)


@application.route('/static/<filename:path>')
def static(filename):
    return static_file(filename=filename, root='static')


@error(500)
def error500():
    """
    For 500 errors it returns an error screen
    :return: Error page, with links back to other pages
    """
    db = PsstDb()
    error1 = {
        'login': has_visited(),
        'usernamed': users.session_user(db),
        'searchVal': "",
        'title': "Woops, Error",
        'content': "Well youve found an error. thats no good",
        'posts': []
    }
    return template('index', error1)


if __name__ == '__main__':
    application.run(debug=True, port=8010)
