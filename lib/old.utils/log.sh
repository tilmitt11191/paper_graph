
#!/bin/bash
export LANG=C
source ../../lib/utils/getconf.sh
LOG_FILE=`getconf "logdir"``getconf "logfile"`
LOG_LEVEL=`getconf "loglevel"`
rotate_size=`getconf "rotate_log_lines"`


function rotate_logfile(){
	if [ ! -z $1 ];then
		LOG_FILE=$1
	fi

	if [ ! -e $LOG_FILE ];then
		:> $LOG_FILE
	fi
	
	logfile_line_num=`wc -l < $LOG_FILE`
	if [ $logfile_line_num -ge $rotate_size ];then
		last_logfile=`ls $LOG_FILE* | xargs -i basename {} | tail -n 1`
		IFS_ORIGINAL="$IFS"
		IFS=.
		arr=($last_logfile)
		num=`expr ${arr[1]} + 1`
		cp $LOG_FILE $LOG_FILE.$num
		:> $LOG_FILE
		IFS="$IFS_ORIGINAL"
	fi
}

function log_debug() {
	if [ $LOG_LEVEL == "DEBUG" ];then
		if [ -n "$2" ];then
			LOG_FILE=$2
		fi
		rotate_logfile $LOG_FILE
		echo "--------"`date +%Y%m%d%H%M%S` $0 "--------" >> $LOG_FILE;echo -e "[DEBUG] $1" >> $LOG_FILE
	fi
}

function log_info() {
	if [ $LOG_LEVEL == "DEBUG" -o $LOG_LEVEL == "INFO" ];then
		if [ -n "$2" ];then
			LOG_FILE=$2
		fi
		rotate_logfile $LOG_FILE
		#echo $1
		echo "--------"`date +%Y%m%d%H%M%S` $0 "--------" >> $LOG_FILE;echo -e "[INFO] $1" >> $LOG_FILE
	fi
}

function log_warning(){
	if [ $LOG_LEVEL == "DEBUG" -o $LOG_LEVEL == "INFO" -o $LOG_LEVEL == "WARN" ];then
		if [ -n "$2" ];then
			LOG_FILE=$2
		fi
		rotate_logfile $LOG_FILE
		echo "--------"`date +%Y%m%d%H%M%S` $0"--------" >> $LOG_FILE
		echo "[[WARNING]] $1" >> $LOG_FILE
		echo "[[WARNING]] $1"
	fi
}

function log_fatal(){
	if [ $LOG_LEVEL == "DEBUG" -o $LOG_LEVEL == "INFO" -o $LOG_LEVEL == "WARN" -o $LOG_LEVEL == "FATAL" ];then
		if [ -n "$2" ];then
			LOG_FILE=$2
		fi
		rotate_logfile $LOG_FILE
		echo "--FATAL-- "`date +%Y%m%d%H%M%S` $0"--------" >> $LOG_FILE
		echo "[[[FATAL]]]] $1" >> $LOG_FILE
		echo "[[[FATAL]]] $1"
		exit 1
	fi
}
