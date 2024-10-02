#!/bin/bash
echo "starting icecast2"
sudo service icecast2 restart
ices2 /etc/ices2.xml
echo "Started icecast2"
