**** Introduciton ***
The purpose of this project is to create a non-trivial app to track monthly 
spending.

The idea is that there will be a Dashboard view of recent activity and easy 
ways to add spending events. Old activities can be easily edited or deleted. 

Spending events will be stored in a DB (start with postgresql) and I will
use Bootstrap CSS framework as the front end.

*** Milestones ***
* Initialize DB
    - Users
    - Spending categories (FK constraints)
    - Spending events
* Dashboard
    - Branding
    - Nav sidebar
	> User preferences
	> Reports
    - Charting (this month, annual)
    - Activity table (Add, Edit, Delete)
* CGI scripts to get data
* Process old data into DB

*** File Structure ***
Below is the file structure that I will be using. I can git init this 
directory and push this to different parts of the computer to sync
code for different applicaitons (DB, web, scripting)
projects
 > web
    > lib
	> name: dir of js files to include in apps
 > spending 
    > web
	> app
	    > html: structural files
	    > js: behavioral files
	    > css: formatting files
	> cgi-bin: list of cgi scripts that will support the app. This will
	  deploy to /usr/lib/cgi-bin dir
    > python
	> scripts: main scripts for init and even-based execution
	> pkgs: dir of app related packages
    > postgresql: dir of SQL files
