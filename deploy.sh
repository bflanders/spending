PROJECT='spending'
USR='pi'
# Project specific
sudo cp -r /home/$USR/projects/$PROJECT/web/app/html/* /var/www/html/projects/$PROJECT

sudo cp -r /home/$USR/projects/$PROJECT/web/app/js /var/www/html/projects/$PROJECT

sudo cp -r /home/$USR/projects/$PROJECT/web/app/css /var/www/html/projects/$PROJECT

sudo cp /home/$USR/projects/$PROJECT/web/cgi-bin/* /usr/lib/cgi-bin/$PROJECT

# Lib 
sudo cp -r /home/$USR/projects/$PROJECT/lib/web/* /var/www/html/lib

# Back up to git
sudo git push origin master
#sudo git remote -v
