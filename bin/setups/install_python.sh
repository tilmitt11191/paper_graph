
PWD=`sudo pwd`
cd `dirname $0`

echo "conda create -n paper_graph python=3.5 anaconda"
#conda create -n paper_graph python=3.5 anaconda
echo "source ~/.pyenv/versions/anaconda3-4.3.0/envs/paper_graph/bin/activate paper_graph"
#source ~/.pyenv/versions/anaconda3-4.3.0/envs/paper_graph/bin/activate paper_graph

sudo apt-get update
sudo apt-get install -y build-essential chrpath libssl-dev libxft-dev
sudo apt-get install -y libfreetype6 libfreetype6-dev
sudo apt-get install -y libfontconfig1 libfontconfig1-dev
wget -P ../../tmp/ https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
cd ../../tmp/
sudo tar xvjf phantomjs-2.1.1-linux-x86_64.tar.bz2
sudo mv phantomjs-2.1.1-linux-x86_64 /usr/local/share
sudo ln -sf /usr/local/share/phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/local/bin

sudo apt-get install -y python3-yaml
pip install selenium
pip install SQLAlchemy
pip install PyMySQL

cd $PWD

exit 0
