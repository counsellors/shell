#!/bin/bash

# This script will filter all tcp streams from a pcap file in folder named question4, then save result to folder named only_tcp_m.
# Just it, good luck~

sum_num=0
for filename in ./question4/m/*.pcap; do
    echo $filename

	tshark -r $filename -w ./only_tcp_m/$filename -R $(\
    tshark -r $filename -R "tcp.len>0" -T fields -e tcp.stream |\
        sort -n | uniq |\
        awk '{printf("%stcp.stream==%d",sep,$1);sep="||"}'\
	)
	ls -l ./only_tcp_m/$filename
	#good_tcp=`tshark -r $filename -R "tcp.len>0" -T fields -e tcp.stream |sort -n | uniq | wc -l`
	#if [ "$good_tcp" -gt 0 ]; then
	#	$sum_num+=1
    #fi
done
echo $sum_num
