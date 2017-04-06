
sudo dpkg-divert --local --rename --add /sbin/initctl
sudo ln -s /bin/true /sbin/initctl

sudo apt-get install -y nodejs
sudo apt-get install -y npm
sudo npm cache clean
sudo npm install n -g
sudo n stable
sudo ln -sf /usr/local/bin/node /usr/bin/node
node -v

sudo apt-get purge -y nodejs npm

sudo npm update -g npm

#sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6#echo "deb [ arch=amd64 ] http://repo.mongodb.org/apt/ubuntu precise/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list
#sudo apt-get update
#sudo apt-get install -y mongodb-org


