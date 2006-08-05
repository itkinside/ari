#! /bin/sh

for ip in $(seq 2 127); do
	ping -q -c4 192.168.0.$ip > /dev/null &
done
