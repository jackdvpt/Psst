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
        Logged in as {{usernamed}}
        <br>
        <a href = "/users/{{usernamed}}"><u> Your page</u></a>
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
        <form action="/search" id="searchform" method="get" name="searchform" >
            Search: <input name='search' value = "{{searchVal}}">
            <input type='submit' value='Search'>
            <br>Advanced Search
            <input checked name="adv" type="radio" value="0"> Any Position
            <input name="adv" type="radio" value="3"> Exact Match
            <input name="adv" type="radio" value="1"> Starts with
            <input name="adv" type="radio" value="2"> Ends with
        </form>
    </div>

</header>
<div>
    <div class='collection'>
        <div class = 'content'>{{!content}}</div>
    </div>



</div>

%if (len(posts) != 0):
<div class='collection'>
    % for post in posts:
    <div class='psst'><div class="avatar"><a href = "/users/{{post[2]}}"><img src={{post[3]}} alt="avatar"> </a></div>
        <date>{{post[1]}}</date> <username><a href = "/users/{{post[2]}}">{{post[2]}}</a></username><br>{{!post[4]}}</div>
    % end
</div>
%end

</body>
</html>
