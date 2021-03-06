<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>{{title}}</title>
    <link rel="stylesheet" href="/static/psst.css" type="text/css">
  </head>

  <body>
  <header>
    <div class = "logo"><p> <a href="/">Psst</a> <p></div>
    <div class="nav">
        <!-- Navigation bar based off http://css-snippets.com/simple-horizontal-navigation/ Alterations made to make style
          inline with website    -->
        <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/about">About</a></li>
            <li><a href="/users">Users</a></li>
        </ul>
    </div>

    <div class='Login'>
        %if login > 0:
        <form action="/login" method="POST" id = "loginform">
            Username
            <input type="text" name="nick">
            Password
            <input type="password" name="password">
            <input type="submit" value="Login">
        </form>
        <p><a href="/reg"><u>Register</u></a></p>
        %else:
         Logged in as <a href = "/users/{{usernamed}}"><u>{{usernamed}}</u></a>
        <form action="/logout" method="POST" id = "logoutform">
            <input type="submit" value="Logout">
        </form>
        <br>
        %if (len(posts) != 0):
        <form action="/post" method="POST" id = "postform">
            Post a Psst <input type="text" name="post"  size="35" rows="2">
            <input type="submit" value="Post">
        </form>
        <br>
        %end
        %end
        <form action="/search" id="searchform" method="get" name="searchform">
            Search: <input name='search'>
            <input type='submit' value='Search'>
            <br>Advanced Search
            <input checked name="adv" type="radio" value="0"> Any Position
            <input name="adv" type="radio" value="1"> Starts with
            <input name="adv" type="radio" value="2"> Ends with
        </form>
    </div>

</header>
  <div class='collection'>
       <div class = 'content'>

      So you want to join psst!
         <br>Some things you will need to know
           <br>Your username can contain a fullstop [ . ] but no other special characters [such as ~`!@#$%^&*()_-+={}[]:>;',< /?*-+], and no spaces.
           Your username <b>is also case sensetive. So be careful</b>
        <br>Your password can be whatever you want (go crazy)
        <br> Your picture is generated by <a href="http://robohash.org">robohash.org</a>
           <br>All you need to do is supply a word
            Or random string of characters to make your own unique and awesome picture for PSST!
           <br>
      <br>
          <form action="/register" method="POST" id = "regForm">
            Username
            <input type="text" name="username">
            Password
            <input type="password" name="pass">
              Picture
            <input type="text" name="pic">
            <input type="submit" value="Register">
        </form>
           {{comment}}
           </div>
  </div>
  </body>
</html>
