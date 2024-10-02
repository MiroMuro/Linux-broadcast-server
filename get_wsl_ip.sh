#!/bin/bash
ip addr show eth0 | grep 'inet' | grep -v 'inet6'| awk '{print $2}' | cut -d/ -f1
