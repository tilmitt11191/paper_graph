

export LANG=C

pwd=`sudo pwd`
cd `dirname $0`

sudo rsync -av ../var/www/html/paper_graph /var/www/html/
sudo chown -R www-data:www-data /var/www/html/paper_graph     

cd $pwd
