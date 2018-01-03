<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>{{title}}'s Psst</title>
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
    <div>
<div class='collection'>

       <div class = 'content'>{{message}}</div>

</div>
    </div>
<div class='collection'>
    %if (len(users) != 0):
% for user in users:
        <div class = 'userList'>
            <div class="avatarBig">
                <a href = "/users/{{user[1]}}">
                    <img src={{user[0]}} alt="avatar" alt="avatarBig">
                </a>
            </div>
            <a href = "/users/{{user[1]}}">
                <usernameBig>{{user[1]}}</usernameBig>
            </a>
        </div>
          % end
    %end
  </body>
</html>
