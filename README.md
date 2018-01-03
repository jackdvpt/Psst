# Psst!

This is PSST! a simplistic social media, not all that different from tiwtter. 

Users are able to register on the site (with a unique username and password) and then can make posts/Psst's on the site,
They can then follow other users and see there posts on the home page.
Users can Tag (using @Barfoo) another user in a post, or can use a Hashtag, which are searchable, as well.

The default test posts added in DB
### How do I get set up? ###

* Clone this repository or download via the zip file link on the web page
* Make sure you have bottle and Webtest modules installed for Python
* You can run main.py to get a basic response from the app


#### Following ####
A user on another user's page can now "follow" that user, meaning that when they are logged in on the homepage `"/"`,
they will only see posts that have been made by users they are following

On a users own page (ie `'/users/Barfoo'`) they can see the list of users they are following

The behind the scenes stuff is simple

`users.py` has new functions which make this possible
```pythonstub
make_follow(db, user, following) #Makes user follow following
make_unfollow(db, user, following)  #Make user unfollow following
does_follow(db, user, following)    #Checks if user follows following
follows(db, user)                   # Check if user is following anyone
get_following(db, user)             # Returns who user is folloiwng
```

`interface.py` has some new functions as well
``` python
post_list_follows(db, follwoing, usernick, limit=50)   
    Which returnes all posts by the users followed by usernick (and there own posts)
```

There are also additional unit and function tests for this new function
```python
level3_functional.py
     def test_follow_only(self)
     def test_followpage(self):
     
level3_unit.py
     def test_add_user(self)
     def test_fail_login(self):
```

#### Register ####
When a user is not logged in they are able to click register and then register as a new user on the site.
If they meet the following criteria

* The username is unique 
* The Username is one word (including fullstops but nothing else)
* The picture provided is a string which uses robohash.org to create a new picture, 
and randomly changes to the alternative pictures
* The picture is also one word (and can include any special characters)
* The password can contain special characters (and code) because it never executes and is always hashed 

The data is validated by a method 
``` python 
users.checkValid(nickname, password, picture)
    :nickname:  the new username
    :password:  the new password
    :picture:   the new picture
    :returns:
        A positive integer (3) if data is valid
        -1 if nickname is not valid
        -2 if password is not valid
        -3 is picture is not valid

```
The data is added into the database by 
``` python 
add_user(db, username, password, pic)
    : returns :     -1 if the insert fails
```
Once the user is registered they are redirected to the homepage, 
auto logon was intended but wasn't finished in time

There are also additional unit and function tests for this new function
```python
level3_functional.py
     def doRegister(self, nick, password, pic)
     
level3_unit.py
     def test_follow(self)
```
#### Searching ####
All pages now contain a search bar. This can be used to search the posts
        Advanced search changes the wildcard characters, to either
* Any Position
* Exact Match
* Ends with
* Starts with

The search is completed by 
``` python 
interface.post_search(db, serach, type)
    :db :       Database to search in
    :search :   The term to search
    :type :     Any advanced searches that will be taken into account
    :return:    A list of all messages in db that contain the term
```
Any messages that meet this criteria are then returned, 
with the term searched for bold in the messages

There are also additional unit and function tests for this new function
```python
level3_functional.py
      def testsearchOnPAge(self)
      def testBoldingSerach(self)
     
level3_unit.py
     def test_serach_adv(self)
     def test_search(self)
     
```
#### List of Users ####
When a user visits /users They see a list of all users on the website, this allows them to jump directly to a user
on the site. However if this was a legitimate website would be a terrible idea. 

Uses 
``` python 
interface.return_users(db)
    :db:        The database to use
    :returns:   A list of all users inside of db
```

There are also additional unit and function tests for this new function
```python
level3_functional.py
       def test_user_page(self)
     
level3_unit.py
     def test_user_list(self)
```
