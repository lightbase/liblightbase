#!/bin/bash

# Instalação das dependências do liblightbase no python?!

. ./ez_i.bash

EZ_I_SKIP_ON_V=$1
if [ -z "$EZ_I_SKIP_ON_V" ] ; then
    EZ_I_SKIP_ON_V=0
fi

BASE_INST_DIR_V=$2
# > -----------------------------------------
# Informar o diretório base da instalação!

if [ -z "$BASE_INST_DIR_V" ] ; then
    f_open_section
    BASE_INST_DIR_V="/usr/local/lb"

    QUESTION_F="Enter the installation directory. 
Use empty for \"$BASE_INST_DIR_V\"!"

    f_get_usr_input "$QUESTION_F" 1
    QUESTION_F=""
    if [ -n "$GET_USR_INPUT_R" ] ; then
        BASE_INST_DIR_V="$GET_USR_INPUT_R/lb"
    fi
    f_close_section
fi

# < -----------------------------------------

f_open_section

TITLE_F="Install liblightbase dependencies for python??"
f_yes_no "$TITLE_F"
TITLE_F=""

if [ ${YES_NO_R} -eq 1 ] || [ ${EZ_I_SKIP_ON_V} -eq 1 ] ; then

    cd "$SCRIPTDIR_V"
    cd ./py-packs-liblightbase

    tar -zxvf ./decorator-3.4.0.tar.gz
    cd ./decorator-3.4.0
    eval "$BASE_INST_DIR_V/lb?_ve??/bin/python? setup.py install"
    cd ..
    rm -rf decorator-3.4.0

    tar -zxvf ./six-1.7.2.tar.gz
    cd ./six-1.7.2
    eval "$BASE_INST_DIR_V/lb?_ve??/bin/python? setup.py install"
    cd ..
    rm -rf six-1.7.2

    tar -zxvf ./ply-3.4.tar.gz
    cd ./ply-3.4
    eval "$BASE_INST_DIR_V/lb?_ve??/bin/python? setup.py install"
    cd ..
    rm -rf ply-3.4

    tar -zxvf ./jsonpath-rw-1.3.0.tar.gz
    cd ./jsonpath-rw-1.3.0
    eval "$BASE_INST_DIR_V/lb?_ve??/bin/python? setup.py install"
    cd ..
    rm -rf jsonpath-rw-1.3.0

    tar -zxvf ./python-dateutil-2.2.tar.gz
    cd ./python-dateutil-2.2
    eval "$BASE_INST_DIR_V/lb?_ve??/bin/python? setup.py install"
    cd ..
    rm -rf python-dateutil-2.2

    tar -zxvf ./requests-1.2.3.tar.gz
    cd ./requests-1.2.3
    eval "$BASE_INST_DIR_V/lb?_ve??/bin/python? setup.py install"
    cd ..
    rm -rf requests-1.2.3

    tar -zxvf ./voluptuous-0.8.7.tar.gz
    cd ./voluptuous-0.8.7
    eval "$BASE_INST_DIR_V/lb?_ve??/bin/python? setup.py install"
    cd ..
    rm -rf voluptuous-0.8.7

fi
f_close_section
