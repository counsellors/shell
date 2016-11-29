#!/bin/bash

#-----------------------------------------------------------------------------
# File:          split_pcap.sh
# Creation Date: 2016-11-29 17:34
# Author:        Sun on <zhaoxing-5@163.com>
# License:       See the LICENSE file
#-----------------------------------------------------------------------------

function show_help {
    echo "Usage: $0 -r <pcap_file> -o <out_dir> -t <stream_type>"
    echo ""
    echo "    This script will help you to split pcap in TCP or UDP protocal."
    echo -e "    \t-r <pcap_file> is a pcap file, not directory."
    echo -e "    \t-t <stream_type> should be tcp,udp or both."
    echo -e "    \t-o <out_dir> is a directory is new splited pcap will be saved to."
    echo "    Require tshark, and good luck~"
    exit 0
}

function create_dir {
 if [ ! -d $1 ]
 then
  /bin/mkdir -p $1 >/dev/null 2>&1 && echo "Directory $1 created." ||  echo "Error: Failed to create $1 directory."
 fi
}

function parse_udp {
    stream_num=`tshark -r $pcap_name -T fields -e udp.stream 2>/dev/null | sort -n | uniq|tail -n 1 `
    if [[ $stream_num == "" ]]; then
        echo ">>Found UDP stream num: empty"
        return
    else
        echo ">>Found UDP stream num: ${stream_num}"
    fi
    for (( INDEX = 0; INDEX <= ${stream_num}; INDEX++ )); do
        echo "Processing UDP stream $INDEX ..."
        tshark -r $pcap_name -Y "udp.stream eq $INDEX" -w $out_dir/${filename}-$INDEX.pcap 2>/dev/null
    done
}

function parse_tcp {
    stream_num=`tshark -r $pcap_name -T fields -e tcp.stream 2>/dev/null | sort -n | uniq|tail -n 1 `
    if [[ $stream_num == "" ]]; then
        echo ">>Found TCP stream num: empty"
        return
    else
        echo ">>Found TCP stream num: ${stream_num}"
    fi
    for (( INDEX = 0; INDEX <= ${stream_num}; INDEX++ )); do
        echo "Processing TCP stream $INDEX ..."
        tshark -r $pcap_name -Y "tcp.stream eq $INDEX" -w $out_dir/${filename}-$INDEX.pcap 2>/dev/null
    done
}

if [ $# -eq 0 ]; then
    show_help
fi
pcap_name=""
out_dir=""
stream_type="both"
while getopts "h?r:o:t:" opt;
do
    case "$opt" in
    h|\?)
        show_help
        ;;
    r)  pcap_name=$OPTARG
        ;;
    o)  out_dir=$OPTARG
        ;;
    t)  stream_type=$OPTARG
        ;;
    *) 
        show_help
    esac
done
filename=$(basename "$pcap_name")
extension="${filename##*.}"
filename="${filename%.*}"

create_dir $out_dir
if [[ $stream_type == "udp" ]]; then
    parse_udp
elif [[ $stream_type == "tcp" ]]; then
    parse_tcp
elif [[ $stream_type == "both" ]]; then
    root_dir=$out_dir
    out_dir=$root_dir/udp
    create_dir $out_dir
    parse_udp
    out_dir=$root_dir/tcp
    create_dir $out_dir
    parse_tcp
fi
