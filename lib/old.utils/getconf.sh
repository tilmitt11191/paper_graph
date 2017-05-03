#bash
export LANG=C

function getconf(){
	#set PATH of CONFIG_FILE
	if [ ! -z $2 ];then
		CONFIG_FILE=$2
	else
		CONFIG_FILE="../../etc/config.yml"
	fi
	LOG_LEVEL=`cat $CONFIG_FILE | grep loglevel | awk -F ": " '{print $2}'`
	LOG_FILE=`cat $CONFIG_FILE | grep logdir | awk -F ": " '{print $2}'``cat $CONFIG_FILE | grep logfile | awk -F ": " '{print $2}'`

	if [ $LOG_LEVEL == "DEBUG" ];then
		echo "--------"`date +%Y%m%d%H%M%S` $0 "--------" >> $LOG_FILE;echo -e "[DEBUG] getconf start. ARGV[1]=$1, ARGV[2]=$2, CONFIG_FILE=$CONFIG_FILE, LOG_LEVEL=$LOG_LEVEL, LOG_FILE=$LOG_FILE" >> $LOG_FILE
	fi
	if [ -z "$1" ];then
		LOG_FILE=`cat $CONFIG_FILE | grep LOG_FILE | awk -F " " '{print $2}'`
		echo "--FATAL-- "`date +%Y%m%d%H%M%S` $0"--------" >> $LOG_FILE
		echo "[[[FATAL]]]] ARGV[1] $1 is empty." >> $LOG_FILE
		exit 1
	fi
	if [ ! -e "$CONFIG_FILE" ];then
		LOG_FILE=`cat $CONFIG_FILE | grep LOG_FILE | awk -F " " '{print $2}'`
		echo "--FATAL-- "`date +%Y%m%d%H%M%S` $0"--------" >> $LOG_FILE
		echo "[[[FATAL]]]] CONFIG_FILE $CONFIG_FILE NOT exist." >> $LOG_FILE
		exit 1
	fi
	conf=`cat $CONFIG_FILE | grep $1 | awk -F " " '{print $2}'`
	if [ -z "$conf" ];then
		echo "--FATAL-- "`date +%Y%m%d%H%M%S` $0"--------" >> $LOG_FILE
		echo "[[[FATAL]]]] getconf [$1] NOT hit." >> $LOG_FILE
		exit 1
	fi
	if [ $LOG_LEVEL == "DEBUG" ];then
		echo "--------"`date +%Y%m%d%H%M%S` $0 "--------" >> $LOG_FILE;echo -e "[DEBUG] return $conf" >> $LOG_FILE
	fi
	echo $conf
	exit 0
}
