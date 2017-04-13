

PWD=`pwd`
cd `dirname $0`


SRCDIR="../"
DSTDIR="alladmin@172.19.73.168:/media/sf_c/Users/ozu/Documents/program/paper_graph"

rsync -av --delete -e "ssh -p 50022 -i ~/.ssh/id_rsa" $SRCDIR/ $DSTDIR/
#rsync -av ../* ozu@172.19.73.168:/cygdrive/c/Users/ozu/Documents/program/paper_graph



cd $PWD

exit 0
