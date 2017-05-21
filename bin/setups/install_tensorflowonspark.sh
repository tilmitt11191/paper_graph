
sudo mkdir /usr/local/lib/tensorflowonspark
cd /usr/local/lib/tensorflowonspark
sudo git clone --recurse-submodules https://github.com/yahoo/TensorFlowOnSpark.git
cd ./TensorFlowOnSpark
sudo git submodule init
sudo git submodule update --force
sudo git submodule foreach --recursive git clean -dfx
pushd src 
zip -r ../tfspark.zip *
popd

sudo sh /usr/local/lib/TensorFlowOnSpark/scripts/local-setup-spark.sh
sudo SPARK_HOME=/usr/local/lib/TensorFlowOnSpark/spark-1.6.0-bin-hadoop2.6
sudo PATH=/usr/local/lib/TensorFlowOnSpark/src:${PATH}
sudo PATH=${SPARK_HOME}/bin:${PATH}
sudo PYTHONPATH=/usr/local/lib/TensorFlowOnSpark/src

export LOG_DIRS=$HOME/program/test/tensorFlow_test/var/log/log
export LOG_DIRS=$HOME/program/test/tensorFlow_test/var/log/
export HADOOP_HOME=/usr/local/lib/hadoop/hadoop
export PATH=$HADOOP_HOME/bin:$PATH
export HADOOP_CONF_DIR=/usr/local/lib/hadoop/hadoop/etc/hadoop
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native