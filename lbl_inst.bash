#!/bin/bash

rm -rf /var/log/lb?.log
cd "/usr/local/lb/lb?_ve??/src/liblightbase"
/usr/local/lb/lb?_ve??/bin/python? setup.py install
cd "/usr/local/lb/lb?_ve??/src/LBGenerator"
/usr/local/lb/lb?_ve??/bin/python? setup.py install
service nginx stop
service uwsgi stop
sleep 5
service uwsgi start
service nginx start
less +F /var/log/lb?.log
