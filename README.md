# GroupChat
This is my another vacation project which is group chatting website.This website is based on Django python web framework and application of Websockets.Websockets are implemented with Django using django-channels and channel-redis.This website is deployed on Heroku with AWS S3 (Amazon Web Services) for storing user files.  
  

You can explore more on : <https://rudresh-chatgroup.herokuapp.com/>  
# Overview Of Website
* First page is a login page Which will ask for username name and password  
![login page](https://raw.githubusercontent.com/RudreshVeerkhare/ChatGroup/master/readme%20images/login.png "login page")  
* At bottom of login container there is a link for Sign Up page for new users  
![sign up page](https://raw.githubusercontent.com/RudreshVeerkhare/ChatGroup/master/readme%20images/register.png "register page")  
* After logging in you will be directed to homepage of website where you can see all your Groups listed.  
![home page](https://raw.githubusercontent.com/RudreshVeerkhare/ChatGroup/master/readme%20images/home.png "home page")  
* You can click on any of the the group to enter chatting lobby.  
![group page](https://raw.githubusercontent.com/RudreshVeerkhare/ChatGroup/master/readme%20images/group.png)  
* From here you will be directed to Group Profile if you click on the group name above, where you can change group profile image and info.  
![group profile](https://raw.githubusercontent.com/RudreshVeerkhare/ChatGroup/master/readme%20images/group_profile.png "group profile")  
* There is a similar page for User Profile also.  
![User Profile](https://raw.githubusercontent.com/RudreshVeerkhare/ChatGroup/master/readme%20images/user_profile.png)  
* There are also features like Search User to search available users on site, search finds the users whose name matchs to initails of entered text.  
![search page](https://raw.githubusercontent.com/RudreshVeerkhare/ChatGroup/master/readme%20images/search_user.png)  
## Modules and packages used :
1) django  
2) django-channels
3) channel-redis  
4) crispy-form-tags  
5) Bootstrap 4  
6) Reconnecting-websockets by  [joewalnes](https://github.com/joewalnes/reconnecting-websocket "reconnecting-websockets github repository")  



