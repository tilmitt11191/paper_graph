

PWD=`pwd`
cd `dirname $0`


SRCDIR="../"
DSTDIR="alladmin@172.19.73.168:/media/sf_c/Users/ozu/Documents/program/paper_graph"

rsync -av --delete\
 --exclude="node_modules/*"\
 --exclude=".git/*"\
 --exclude="__pycache__/*"\
 -e "ssh -p 50022 -i ~/.ssh/id_rsa" $SRCDIR/ $DSTDIR/ 

cd $PWD

exit 0
