#!/bin/bash
# if you have a docker server and many docker container with ssh-service,
# maybe you need login a different container use an used port.
# like jenkins docker plugin. 

read -p "input a port :" PORT

if [ ! -n "$PORT" ]; then
  $PORT=65430
fi

ssh-keygen -R [172.17.0.1]:$PORT;
ssh jenkins@172.17.0.1 -p $PORT
