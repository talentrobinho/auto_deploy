#!/bin/bash

#. param.conf

usage ()
{
    echo -ne "USAGE: sh op_cluster.sh action service version\n"
    echo -ne "action in fllowing list:\n"
    echo -ne "\t\t\tbackup\n"
    echo -ne "\t\t\trollback\n"
    echo -ne "service in fllowing list:\n"
    echo -ne "\t\t\ttitan\n"
    echo -ne "\t\t\trelated\n"
    echo -ne "\t\t\tbudget\n"
    echo -ne "\t\t\tbrand\n"
    echo -ne "\t\t\torion_lead\n"
    echo -ne "\t\t\torion_lead_instant\n"
    echo -ne "\t\t\tcheating\n"
}

check_file()
{
	local file=$1
	if [ ! -f $file ]
	then
		echo "$file is not exist, exit"
		exit
	fi
}

if [ $# -ne 3 ] 
then
	usage
	exit 1;
fi

action_file=$1.sh

service=$2
service_cfg_file=$2.cfg

host_file=$HOST_DIR/hosts.$2

version=$3

check_file $action_file

check_file $service_cfg_file

check_file $host_file


echo -e "\n[\\033[1;32m"ALL Machine $1" \\033[1;32mStart\\033[0;39m ]\n"
date

for ip in `grep -v -E '^#' $host_file`
do
	sh $action_file $service $ip $version &
done

process_name="sh $action_file $service"
while true
do
	count=`ps -ef | grep "$process_name" | grep -v "grep" | wc -l` 
	if [ $count -eq 0 ]; 
	then
		echo -e '\n'	
		break;
	else
	    sleep 1
	    echo -ne "."
	fi
done

date
echo -e "[\\033[1;32m"ALL Machine $1" \\033[1;32mOK\\033[0;39m ]\n\n"
