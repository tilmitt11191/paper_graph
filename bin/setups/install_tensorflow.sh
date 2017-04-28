
PWD=`sudo pwd`
cd `dirname $0`

#wget "https://repo.continuum.io/archive/Anaconda3-4.3.1-Windows-x86_64.exe" -P "../../tmp/"

echo -n "mannualy execute ../../tmp/Anaconda3-4.3.1-Windows-x86_64.exe. had the job finished?[y]"
read ANSWER
if [ $ANSWER != "y" ]; then
	echo "exit"
	exit 1
fi
#https://developer.nvidia.com/cuda-downloads
#https://developer.nvidia.com/rdp/cudnn-download

##for windows with cygwin and anaconda
pip install tensorflow-gpu
#pip install tensorflow #cpu
pip install --upgrade https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow_gpu-1.0.1-cp35-cp35m-linux_x86_64.whl
pip install theano


cd $PWD

exit 0
