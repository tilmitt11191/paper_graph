# -*- coding: utf-8 -*-

## ARGV[1]: hostname
## ARGV[2]: filepath + name

if [ $# -ne 2 ]; then
	echo "need 2 argvs. exit 1" 1>&2
	exit 1
fi

PWD=`pwd`
cd `dirname $0`

remotename=$1
filename=$2
echo "remotename: $remotename"
echo "filename: $filename"

username="ozu"
if [ $remotename = "aries" ];then
	remoteaddress="172.19.73.72"
elif [ $remotename = "cancer" ];then
	remoteaddress="172.19.73.73"
elif [ $remotename = "gemini" ];then
	remoteaddress="172.19.73.74"
else
	echo "unknown remote name. exit 1"
	exit 1
fi

command="scp -i ~/.ssh/id_rsa -v \
	$username@$remoteaddress:/home/ozu/program/paper_graph/$filename \
	../../$filename.$remotename"
echo $command
eval $command

echo "scp finished. saved to ../../$filename.$remotename"
cd $PWD

exit 0