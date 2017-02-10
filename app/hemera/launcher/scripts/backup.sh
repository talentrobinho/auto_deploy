#!/bin/bash
DIR="/search/odin/flasky/app/hemera/launcher/scripts"
RES_COL="60"

ECHO ()
{
    echo -ne "$1 <br />"
}

usage () 
{
    echo -e "USAGE: sh backup.sh service ip version"
    echo -ne "service in fllowing list:\n"
    echo -ne "\t\t\tcpc\n"
    echo -ne "\t\t\tpush\n"
    echo -ne "\t\t\tlead\n"
    echo -ne "\t\t\tbrand\n"
    echo -ne "\t\t\tlead_music\n"
    echo -ne "\t\t\tlead_research\n"
    echo -ne "\t\t\tbill_cpc\n"
    echo -ne "\t\t\tbill_push\n"
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

if [ $# -ne 3 ]; then
        usage
		exit 1
fi

cfg_name=$1.cfg
ip=$2
version=$3

check_file $DIR/$cfg_name

If_Back_Data="n"

. $DIR/$cfg_name


#echo -en "\n"
#echo -en "[\\033[1;31m"Start To Backup Env On" $ip \\033[0;39m\\033[0;39m ]\n\n"
ECHO "Start To Backup Env On $ip"
now=`date`
ECHO "$now"

suffix=1
#while [ $suffix -le 2 ]
while [ $suffix -le 1 ]
do
	Current_Back_Dir="$Service_Backup_Dir/$version.$suffix"
	Current_Service_Dir="$Service_Home_Dir"
	ssh $ip "mkdir -p $Current_Back_Dir"
	
    if [ "$If_Back_Bin" == "y" ]
	then
		ECHO "Backuping bin ... "
	    ssh $ip "cd $Current_Service_Dir; cp -rf bin $Current_Back_Dir"
    fi
	
    if [ "$If_Back_Conf" == "y" ]
	then
		ECHO "Backuping conf ... "
	    ssh $ip "cd $Current_Service_Dir; cp -rf conf $Current_Back_Dir"
    fi
	
	#echo "Backuping bin lib conf  script"
	#ssh $ip "cd $Current_Service_Dir; cp -rf bin $Current_Back_Dir; cp -rf conf $Current_Back_Dir; cp -f *.sh $Current_Back_Dir"
	
	if [ "$If_Back_Data" == "y" ]
	then
		ECHO "Backuping data ... "

		#for datafile in $Rollback_Data_List
		#do
		#	ssh $ip "cd $Current_Back_Dir; mkdir -p data; cp -f $Current_Service_Dir/data/$datafile data/;"
		#done
	fi
	
	suffix=`echo $suffix+1 | bc -l`
done

now=`date`
ECHO "$now"
#echo -en "\n[\\033[1;32m"Succeed To Backup Env On" $ip \\033[1;32mOK\\033[0;39m ]\n\n"
ECHO "Succeed To Backup Env On $ip"
