
## package check
log_info 'package check start.'
PACKAGES=(tmux mysql-server)
for package in ${PACKAGES[@]}; do
	dpkg -l $package | grep -E "^i.+[ \t]+$package" > /dev/null
	if [ $? -ne 0 ];then
		m="$package not installed. sudo apt-get install -y $package."
		log_info "$m"
		sudo apt-get install -y $package
	else
		m="$package already installed."
		log_info "$m"
	fi

done
