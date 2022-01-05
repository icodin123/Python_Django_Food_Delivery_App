# Django Food Delivery Web App

## Description

Feeding Canadian Kids is a non-profit organization that takes in applications from after-school *Programs*, which are in need of food for kids, and *Restaurants*, which are looking to donate food. The *Admins* from Feeding Canadian Kids would then browse new applications and manually fill in the information that a *Restaurant* or *Program* provided into an excel sheet. Then, manually pair them up according to the dates when they can deliver or accept food.

The problem we are trying to solve is that their current process is manual, and as they are trying to expand their program, it would be very hard for admins at Feeding Canadian Kids to continue to complete everything manually.

The web-application we are creating is meant to automate their current registration process and make the pairing process easier. We enable the end-users, *Programs* and *Restaurants*, to register accounts and then fill their profiles with their information and schedules. Then, the *Admins* can see all the applications and create new pairings accordingly.


## Key Features
Our product consists of two almost-separate applications. We have designed the admin and end-user portals. Here we list the features of each:

**Admin Portal**: 
1.    Multiple admins can log in to their accounts.
2.    There, they can access new notifications (which are updated in real-time)
3.    They can access a settings page in which they can change their profile information. 
4.    In the settings page, they can add additional admin accounts. 
5.    They can access pages with lists of individual programs and restaurants. 
6.    They can manually add and edit new programs and restaurants.
7.    They can access the users' information, reply to their requests, 
8.    They can accept/deny new-account applications. 
9.    They can visit pairings, review them, make new ones, and remove the selected ones.
10.    Then can review and accept/deny requests made by users.
 
**End-users**:
1.    End-users of two kinds (Restaurant owners and Program representatives) can sign-up, login, and make an application to become a partner. 
2.    After their application is reviewed, if they are accepted by Feeding Canadian Kids’ admins, the end-users can access their dashboard.
3. Users, they can see their information and their schedule. 
4. Users can access their pairing with other partners.
5. Users can make requests to Feeding Canadian Kids admins.
6. Users can edit their requests.
7. Users can access the settings page, in which they can change their account information. 



## Development requirements
You can run this application on any modern Operating System that supports Python 3.6. Additional installations need to be done to run the project:
* First you need to install conda on your machine. Instructions for how to install can be found here: https://docs.conda.io/projects/conda/en/latest/user-guide/install/macos.html
* Create a new folder, call it [YOUR_FOLDER_NAME]
* Open console and navigate to [YOUR_FOLDER_NAME]
* Clone our GitHub repository into your folder by using 
   * git clone [OUR_REPOSITORY_URL]
* Make sure you're branch is master
* Navigate into folder called "team-project-feeding-canadian-kids-team-1"
* Navigate into project called "project"
* Type conda create --name djangoEnv in your terminal and press Enter
* Confirm location by typing 'y' in your terminal
* Type conda activate djangoEnv in your terminal and press Enter
* Type conda install python=3.6 in your terminal and press Enter
* Confirm installation by typing 'y'
* Type conda install django=1.11 in your terminal and press Enter
* Type 'y' to confirm installation
* Type pip install django-misaka in your terminal and press Enter
* Type pip install django-bootstrap3 in your terminal and press Enter
* Type pip install django-braces in your terminal and press Enter
* Type pip install pymysql in your terminal and press Enter
* Type pip install pillow in your terminal and press Enter
* Type pip install faker and press Enter
* Type ./run.sh to run the shell script that will make migrations and run the application
* If you want to populate database with some data before testing, type python populate_db.py
* Running Django server can be turned off by typing Ctrl + C



## Licences
* We are applying MIT License to our codebase.
 
* MIT license allows us to modify the original source code, which provides us with additional flexibility in terms of planning further development strategy. MIT license also allows Feeding Canadian Kids to claim copyright in case their property rights are violated.

* Our decision was to use MIT license for our project because it is very permissive and also because it allows for our project to be freely distributed. MIT license provides us with additional flexibility in terms of modifying our project, which allows us to worry more about the product and less about paperwork.
