#!/bin/bash

# Baixa e instala todas as ferramentas necessarias

sudo apt-get update
sudo apt-get install git python3.4 python3.4-dev python-pip  postgresql-9.3 postgresql-server-dev-all zlib1g python-virtualenv -y

#
# repositorios git
#

LBAPP="http://git.lightbase.cc/LBApp.git"
LBGENERATOR="http://git.lightbase.cc/LBGenerator.git"
LIBLIGHTBASE="http://git.lightbase.cc/liblightbase.git"

#
# Cria WorkSpace para projeto lightbase
#

if [ ! -d "$HOME/workpace_lightbase" ]; then
	mkdir $HOME/workspace_lightbase
	cd $HOME/workspace_lightbase
	PATH_WORKSPACE=`pwd`
else
	cd $HOME/workspace_lightbase
	PATH_WORKSPACE=`pwd`
fi

cd $PATH_WORKSPACE

#
# Cria ambiente virtual
#

virtualenv -p `which python3.4` env

BIN=$PATH_WORKSPACE/env/bin
PYTHON=$BIN/python3.4
PIP=$BIN/pip3.4
ALEMBIC=$BIN/alembic

$PIP install psycopg2 --upgrade
$PIP install setuptools --upgrade
$PIP install waitress --upgrade
$PIP install alembic --upgrade
$PIP install pyramid --upgrade

#
# Clonar projeto do GITHUB para repositorio local
#

git clone $LBAPP
git clone $LBGENERATOR
git clone $LIBLIGHTBASE

#
# Altera arquivos de configuracao da aplicacao
#

OLD="postgresql:\/\/rest:rest@localhost\/neolight"
NEW="postgresql:\/\/lightbase:lightbase@localhost\/neolight"

cat $PATH_WORKSPACE/LBGenerator/production.ini-dist | sed s"/$OLD/$NEW/" | sed s'/6543/6544/' > $PATH_WORKSPACE/LBGenerator/production.ini
cat $PATH_WORKSPACE/LBApp/production.ini-dist | sed 's/http:\/\/lbgenerator_url/http:\/\/0.0.0.0:6544/' > $PATH_WORKSPACE/LBApp/production.ini

#
# Cria Base de dados e tabelas no POSTGRES
#

sudo su postgres << EOF
psql << 1
CREATE USER lightbase PASSWORD 'lightbase';
CREATE DATABASE neolight OWNER lightbase;
1
EOF

source $BIN/activate
cd $PATH_WORKSPACE/liblightbase/
$PYTHON setup.py develop

cd $PATH_WORKSPACE/LBGenerator/
$ALEMBIC -c production.ini upgrade +1
$PYTHON setup.py develop

cd $PATH_WORKSPACE/LBApp/
$PYTHON setup.py develop

if [ ! -e $PATH_WORKSPACE/.start  ]; then
	echo "$BIN/pserve $PATH_WORKSPACE/LBGenerator/production.ini" > $PATH_WORKSPACE/.start.sh
	echo "$BIN/pserve $PATH_WORKSPACE/LBApp/production.ini" > $PATH_WORKSPACE/.startapp.sh
	echo 'kill `ps -aux | grep pserve | grep LBGenerator | awk -F' ' ' { print \$2 } '`' > $PATH_WORKSPACE/.stop.sh
	echo 'kill `ps -aux | grep pserve | grep LBGenerator | awk -F' ' ' { print \$2 } '`' > $PATH_WORKSPACE/.stopapp.sh
	chmod +x $PATH_WORKSPACE/.start.sh
	chmod +x $PATH_WORKSPACE/.startapp.sh
	chmod +x $PATH_WORKSPACE/.stop.sh
	chmod +x $PATH_WORKSPACE/.stopapp.sh
fi

START="alias lbgeneratorStart='~/workspace_lightbase/.start.sh &'"
STARTAPP="alias lbappStart='~/workspace_lightbase/.startapp.sh &'"
STOP="alias lbgeneratorStop='~/workspace_lightbase/.stop.sh'"
STOPAPP="alias lbappStop='~/workspace_lightbase/.stopapp.sh'"
BASHRC=`cat "$HOME/.bashrc" | grep "$START"`

if [ ! "$BASHRC" ]; then
        echo "$START\n$STOP" >> "$HOME/.bashrc"
        echo "$STARTAPP\n$STOPAPP" >> "$HOME/.bashrc"
fi
