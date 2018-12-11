PROJECT='spending'
USR='pi'
# Project specific
sudo cp -r /home/$USR/projects/$PROJECT/web/app/* /var/www/html/projects/$PROJECT

# Lib 
sudo cp -r /home/$USR/projects/$PROJECT/lib/web/* /var/www/html/lib

# Back up to git
sudo git push origin master
#sudo git remote -v
