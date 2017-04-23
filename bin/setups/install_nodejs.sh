
#sudo dpkg-divert --local --rename --add /sbin/initctl
#sudo ln -s /bin/true /sbin/initctl

sudo apt-get install -y nodejs
sudo apt-get install -y npm
sudo npm cache clean
sudo npm install n -g
sudo n stable
sudo ln -sf /usr/local/bin/node /usr/bin/node
node -v

sudo npm update -g npm

##sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6#echo "deb [ arch=amd64 ] http://repo.mongodb.org/apt/ubuntu precise/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list
#sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
#echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list
#sudo apt update

#sudo apt-get update
#sudo apt-get install -y mongodb-org


npm install express --save --no-bin-links
npm install log4js --save --no-bin-links
sudo npm install -g node-dev --save #-g needs sudo
npm install react-social-sharebuttons --save --no-bin-links
npm install pug-cli --save --no-bin-links
npm install cytoscape --save --no-bin-links
npm install mysqljs/mysql --save --no-bin-links
npm install js-yaml --save --no-bin-links
npm install synchronize --save --no-bin-links