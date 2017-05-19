FROM ubuntu:16.04
ENV HOSTNAME tensorgraph

RUN apt-get update && apt-get -y upgrade && apt-get -y dist-upgrade
RUN apt-get install -y sudo
RUN sudo apt-get install -y passwd
RUN useradd graph
RUN mkdir -p /home/graph
RUN chown graph:graph /home/graph
RUN echo "graph ALL=(ALL) ALL" >> /etc/sudoers.d/graph
## ohmyzsh, zshrc
RUN sudo apt-get install -y build-essential chrpath libssl-dev libxft-dev
RUN sudo apt-get install -y libfreetype6 libfreetype6-dev
RUN sudo apt-get install -y libfontconfig1 libfontconfig1-dev
RUN sudo apt-get install -y zsh vim git curl tmux
RUN sudo apt-get install -y default-jre default-jdk python3-yaml
RUN echo "mysql-server mysql-server/root_password password root" | debconf-set-selections && \
echo "mysql-server mysql-server/root_password_again password root" | debconf-set-selections && \
sudo apt-get install -y mysql-server

RUN mkdir /usr/local/lib/tensorflowonspark
WORKDIR /usr/local/lib/tensorflowonspark
RUN git clone --recurse-submodules https://github.com/yahoo/TensorFlowOnSpark.git
WORKDIR ./TensorFlowOnSpark
RUN git submodule init
RUN git submodule update --force
RUN git submodule foreach --recursive git clean -dfx
RUN pushd src 
RUN zip -r ../tfspark.zip *
RUN popd

RUN sh /usr/local/lib/tensorflowonspark/TensorFlowOnSpark/scripts/local-setup-spark.sh
ENV SPARK_HOME=/usr/local/lib/tensorflowonspark/TensorFlowOnSpark/spark-1.6.0-bin-hadoop2.6
ENV PATH=/usr/local/lib/tensorflowonspark/TensorFlowOnSpark/src:${PATH}
ENV PATH=${SPARK_HOME}/bin:${PATH}
ENV PYTHONPATH=/usr/local/lib/tensorflowonspark/TensorFlowOnSpark/src

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

RUN pip install --upgrade https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow_gpu-1.0.1-cp35-cp35m-linux_x86_64.whl
RUN pip install theano
RUN pip install selenium
RUN pip install SQLAlchemy
RUN pip install PyMySQL
RUN pip install wget
RUN pip install matplotlib
