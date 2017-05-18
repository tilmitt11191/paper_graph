FROM ubuntu:14.04
RUN sudo apt-get update && sudo apt-get -y dist-upgrade

#zsh vim git curl autossh tmux xclip default-jre default-jdk mysql-server
RUN sudo apt-get install -y git
RUN git clone https://github.com/yyuu/pyenv.git ~/.pyenv
RUN export PYENV_ROOT="$HOME/.pyenv"
RUN export PATH="$PYENV_ROOT/bin:$PATH"
RUN pyenv install anaconda3-4.3.0
RUN export PATH="$PYENV_ROOT/versions/anaconda3-4.3.0/bin/:$PATH"
RUN pyenv rehash
RUN pyenv global anaconda3-4.3.0
RUN conda update conda
RUN conda create -n python35 python=3.5 anaconda
RUN export PATH="$PYENV_ROOT/versions/anaconda3-4.3.0/envs/python35/bin:$PATH"

RUN sudo apt-get update && sudo apt-get -y dist-upgrade
