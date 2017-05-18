FROM ubuntu:latest

RUN  apt-get update &&  apt-get -y dist-upgrade
RUN apt-get install -y passwd
RUN useradd graph
RUN mkdir -p /home/graph
RUN chown graph:graph /home/graph
RUN echo "graph ALL=(ALL) ALL" >> /etc/ers.d/graph

RUN  apt-get install -y zsh vim git curl
RUN  apt-get install -y default-jre default-jdk mysql-server python3-yaml
RUN  apt-get install -y build-essential chrpath libssl-dev libxft-dev
RUN  apt-get install -y libfreetype6 libfreetype6-dev
RUN  apt-get install -y libfontconfig1 libfontconfig1-dev

RUN git clone https://github.com/yyuu/pyenv.git /home/graph/.pyenv
RUN export PYENV_ROOT="/home/graph/.pyenv"
RUN export PATH="$PYENV_ROOT/bin:$PATH"
RUN pyenv install anaconda3-4.3.0
RUN export PATH="$PYENV_ROOT/versions/anaconda3-4.3.0/bin/:$PATH"
RUN pyenv rehash
RUN pyenv global anaconda3-4.3.0
RUN conda update conda
RUN conda create -n python35 python=3.5 anaconda
RUN export PATH="$PYENV_ROOT/versions/anaconda3-4.3.0/envs/python35/bin:$PATH"

#RUN mkdir /tmp/phantomjs
#RUN wget -P /tmp/phantomjs/ https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-1.1.1-linux-x86_64.tar.bz2
#RUN  tar xvjf /tmp/phantomjs/phantomjs-2.1.1-linux-x86_64.tar.bz2 -C /tmp/phantomjs/
#RUN  mv /tmp/phantomjs/phantomjs-2.1.1-linux-x86_64 /usr/local/share
#RUN  ln -sf /usr/local/share/phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/local/
