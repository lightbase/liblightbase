#!/bin/bash
: 'Trata-se de um módulo que oferece uma série de funcionalidades para 
criar um instalador usando "bash".

Version 1.0.0b

Apache License
Version 2.0, January 2004
http://www.apache.org/licenses/
Copyright 2016 Eduardo Lúcio Amorim Costa
'

# NOTE: Obtêm a pasta do script atual para que seja usado como 
# caminho base/referência durante a instalação! By Questor
EZ_I_DIR_V="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# NOTE: Quando setado faz "ez_i" desabilitar algumas funções, 
# notadamente aquelas que envolvem "perguntas ao usuário" e as 
# gráficas! By Questor
EZ_I_SKIP_ON_V=0

# > --------------------------------------------------------------------------
# UTILITÁRIOS!
# --------------------------------------

f_enter_to_cont() {
    : 'Solicitar ao usuário que pressione enter para continuar.

    Args:
        INFO_P (Optional[int]): Se informado apresenta uma mensagem ao 
    usuário. Padrão 0.
    '

    INFO_P=$1
    if [ ${EZ_I_SKIP_ON_V} -eq 1 ] ; then
        return 0
    fi

    if [ ! -z "$INFO_P" ] ; then
        f_div_section
        echo "$INFO_P"
        f_div_section
    fi

    read -p "Press enter to continue..." nothing
}

GET_USR_INPUT_R=""
f_get_usr_input() {
    : 'Obter entradas digitadas pelo usuário.

    Permite autocomplete (tab). Enter para submeter a entrada.

    Args:
        QUESTION_P (str): Pergunta a ser feita ao usuário.
        ALLOW_EMPTY_P (Optional[int]): 0 - Não permite valor vazio; 1 - Permite 
    valor vazio. Padrão 0.

    Returns:
        GET_USR_INPUT_R (str): Entrada digitada pelo usuário.
    '

    if [ ${EZ_I_SKIP_ON_V} -eq 1 ] ; then
        return 0
    fi
    QUESTION_P=$1
    ALLOW_EMPTY_P=$2
    if [ -z "$ALLOW_EMPTY_P" ] ; then
        ALLOW_EMPTY_P=0
    fi
    GET_USR_INPUT_R=""
    read -e -r -p "$QUESTION_P (use enter to confirm): " RESP_V
    if [ -n "$RESP_V" ] ; then
        GET_USR_INPUT_R="$RESP_V"
    elif [ ${ALLOW_EMPTY_P} -eq 0 ] ; then
        f_get_usr_input "$QUESTION_P" 0
    fi
}

f_get_usr_input_mult() {
    : 'Obter determinada opção do usuário à partir de uma lista de 
    entrada.

    Permite autocomplete (tab). Enter para submeter a entrada.

    Args:
        QUESTION_P (str): Pergunta a ser feita ao usuário (as 
    opções são exibidas automaticamente).
        OPT_ARR_P (array): Array com a lista de opções possíveis. As posições 
    pares do array são as opções e as ímpares são a descrição dessas opções.
        ALLOW_EMPTY_P (Optional[int]): 0 - Não permite valor vazio; 1 - Permite 
    valor vazio. Padrão 0.

    Returns:
        GET_USR_INPUT_MULT_R (str): Entrada digitada pelo usuário.
    '

    if [ ${EZ_I_SKIP_ON_V} -eq 1 ] ; then
        return 0
    fi
    QUESTION_P=$1
    OPT_ARR_P=("${!2}")
    TOTAL_0=${#OPT_ARR_P[*]}
    ALLOW_EMPTY_P=$3
    if [ -z "$ALLOW_EMPTY_P" ] ; then
        ALLOW_EMPTY_P=0
    fi
    USE_PIPE=""
    POSSIBLE_OPT="(select your option and press enter: "
    for (( i=0; i<=$(( $TOTAL_0 -1 )); i++ )) ; do
        if [ $((i%2)) -eq 0 ]; then
            # "even"
            POSSIBLE_OPT=$POSSIBLE_OPT${OPT_ARR_P[$i]}" - "
        else
            # "odd"
            if (( i <= $(( TOTAL_0 -2 )) )) ; then
                USE_PIPE=" | "
            else
                USE_PIPE=""
            fi
            POSSIBLE_OPT=$POSSIBLE_OPT${OPT_ARR_P[$i]}$USE_PIPE
        fi
    done
    POSSIBLE_OPT=$POSSIBLE_OPT")"
    GET_USR_INPUT_MULT_R=""
    read -e -r -p "$QUESTION_P 
$POSSIBLE_OPT: " RESP_V
    if [ -n "$RESP_V" ] ; then
        for (( o=0; o<=$(( $TOTAL_0 -1 )); o++ )) ; do
            if [ $((i%2)) -eq 0 ] && [ "$RESP_V" == "${OPT_ARR_P[$o]}" ] ; then
                # "even"
                GET_USR_INPUT_MULT_R="$RESP_V"
                break
            fi
        done
        if [ -z "$GET_USR_INPUT_MULT_R" ] ; then
            f_get_usr_input_mult "$QUESTION_P" OPT_ARR_P[@] $ALLOW_EMPTY_P
        fi
    elif [ ${ALLOW_EMPTY_P} -eq 0 ] ; then
        f_get_usr_input_mult "$QUESTION_P" OPT_ARR_P[@] 0
    fi
}

F_EZ_SED_ECP_R=""
f_ez_sed_ecp() {
    : '"Escapar" strings para o comando "sed".

    Como há muitas semelhanças entre o escape para "sed" ("f_ez_sed") e 
    escape para "grep" ("f_fl_cont_str") optei por colocar essa 
    função como utilitária para as outras duas citadas.

    Args:
        VAL_TO_ECP (str): Valor a ser "escapado".
        DONT_ECP_NL (Optional[int]): 1 - Não "escapa" "\n" (quebra de 
    linha); 0 - "Escapa" "\n". Padrão 1.
        DONT_ECP_SQ (Optional[int]): 1 - Não "escapa" "'" (aspas 
    simples); 0 - "Escapa" "'". Padrão 1. NOTE: Usado apenas pela 
    função "f_fl_cont_str".

    Returns:
        F_EZ_SED_ECP_R (str): Valor "escapado".
    '

    VAL_TO_ECP=$1
    DONT_ECP_NL=$2
    if [ -z "$DONT_ECP_NL" ] ; then
        DONT_ECP_NL=1
    fi
    DONT_ECP_SQ=$3
    if [ -z "$DONT_ECP_SQ" ] ; then
        DONT_ECP_SQ=0
    fi
    F_EZ_SED_ECP_R=$VAL_TO_ECP
    if [ ${DONT_ECP_NL} -eq 1 ] ; then
        F_EZ_SED_ECP_R=$(echo "$F_EZ_SED_ECP_R" | sed 's/\\n/C0673CECED2D4A8FBA90C9B92B9508A8/g')
    fi
    F_EZ_SED_ECP_R=$(echo "$F_EZ_SED_ECP_R" | sed 's/[]\/$*.^|[]/\\&/g')
    if [ ${DONT_ECP_SQ} -eq 0 ] ; then
        F_EZ_SED_ECP_R=$(echo "$F_EZ_SED_ECP_R" | sed "s/'/\\\x27/g")
    fi
    if [ ${DONT_ECP_NL} -eq 1 ] ; then
        F_EZ_SED_ECP_R=$(echo "$F_EZ_SED_ECP_R" | sed 's/C0673CECED2D4A8FBA90C9B92B9508A8/\\n/g')
    fi
}

f_ez_sed() {
    : 'Facilitar o uso da funcionalidade "sed".

    Args:
        TARGET (str): Valor a ser substituído por pelo valor de REPLACE.
        REPLACE (str): Valor que irá substituir TARGET.
        FILE (str): Arquivo no qual será feita a substituição.
        ALL_OCCUR (Optional[int]): 0 - Fazer replace apenas na primeira 
    ocorrência; 1 - Fazer replace em todas as ocorrências. Padrão 0.
        DONT_ESCAPE (Optional[int]): 0 - Faz escape das strings em 
    TARGET e REPLACE; 1 - Não faz escape das strings em TARGET e 
    REPLACE. Padrão 0.
        DONT_ECP_NL (Optional[int]): 1 - Não "escapa" "\n" (quebra de 
    linha); 0 - "Escapa" "\n". Padrão 1.
        REMOVE_LN (Optional[int]): 1 - Remove a linha que possui o 
    valor em TARGET; 0 - Faz o replace convencional. Padrão 0.
        NTH_OCCUR (Optional[int]): Executará a operação escolhida 
    apenas sobre a ocorrência indicada; Se -1, não executa. Padrão -1.
    '

    FILE=$3
    ALL_OCCUR=$4
    if [ -z "$ALL_OCCUR" ] ; then
        ALL_OCCUR=0
    fi
    DONT_ESCAPE=$5
    if [ -z "$DONT_ESCAPE" ] ; then
        DONT_ESCAPE=0
    fi
    DONT_ECP_NL=$6
    if [ -z "$DONT_ECP_NL" ] ; then
        DONT_ECP_NL=1
    fi
    REMOVE_LN=$7
    if [ -z "$REMOVE_LN" ] ; then
        REMOVE_LN=0
    fi
    NTH_OCCUR=$8
    if [ -z "$NTH_OCCUR" ] ; then
        NTH_OCCUR=-1
    fi
    if [ ${DONT_ESCAPE} -eq 1 ] ; then
        TARGET=$1
        REPLACE=$2
    else
        f_ez_sed_ecp "$1" $DONT_ECP_NL
        TARGET=$F_EZ_SED_ECP_R
        f_ez_sed_ecp "$2" $DONT_ECP_NL
        REPLACE=$F_EZ_SED_ECP_R
    fi
    if [ ${REMOVE_LN} -eq 1 ] ; then
        if [ ${ALL_OCCUR} -eq 0 ] ; then
            SED_RPL="'0,/$TARGET/{//d;}'"
        else
            SED_RPL="'/$TARGET/d'"
        fi
        eval "sed -i $SED_RPL $FILE"
    else
        if [ ${NTH_OCCUR} -gt -1 ] ; then

            # TODO: Tá TOSCO no último! Mas, não consegui uma forma de fazer 
            # replace em apenas determinada posição usando o "sed"! Para ser 
            # bem franco não sei se dá para fazer isso com o "sed"! By Questor
            ((NTH_OCCUR++))
            for (( i=0; i<$(( $NTH_OCCUR - 1 )); i++ )) ; do
                SED_RPL="'0,/$TARGET/s//£§¢¬¨/g'"
                eval "sed -i $SED_RPL $FILE"
            done
            SED_RPL="'0,/$TARGET/s//$REPLACE/g'"
            eval "sed -i $SED_RPL $FILE"
            SED_RPL="'s/£§¢¬¨/$TARGET/g'"
            eval "sed -i $SED_RPL $FILE"
        else
            if [ ${ALL_OCCUR} -eq 0 ] ; then
                SED_RPL="'0,/$TARGET/s//$REPLACE/g'"
            else
                SED_RPL="'s/$TARGET/$REPLACE/g'"
            fi
            eval "sed -i $SED_RPL $FILE"
        fi
    fi
}

FL_CONT_STR_R=0
f_fl_cont_str() {
    : 'Checar se um arquivo contêm determinada string.

    Args:
        STR_TO_CH (str): Valor de string a ser verificado.
        FILE (str): Arquivo no qual será feita a verificação.
        COND_MSG_P (Optional[str]): Mensagem a ser exibida se 
    verdadeira a verificação. Se vazio ou não informado não será 
    exibida mensagem.
        CHK_INVERT (Optional[int]): Inverter a lógica da checagem. 
    Padrão 0.
        DONT_ESCAPE (Optional[int]): 0 - Faz escape da string em 
    STR_TO_CH; 1 - Não faz escape das strings em STR_TO_CH. Padrão 0.
        DONT_ECP_NL (Optional[int]): 1 - Não "escapa" "\n" (quebra de 
    linha); 0 - "Escapa" "\n". Padrão 1.

    Returns:
        FL_CONT_STR_R (int): 1 - Se verdadeiro para a condição 
    analisada; 0 - Se falso para a condição analisada.
    '

    STR_TO_CH=$1
    FILE=$2
    COND_MSG_P=$3
    CHK_INVERT=$4
    DONT_ESCAPE=$5

    if [ -z "$DONT_ESCAPE" ] ; then
        DONT_ESCAPE=0
    fi
    if [ ${DONT_ESCAPE} -eq 0 ] ; then
        DONT_ECP_NL=$6
        if [ -z "$DONT_ECP_NL" ] ; then
            DONT_ECP_NL=1
        fi
        f_ez_sed_ecp "$STR_TO_CH" $DONT_ECP_NL 1
        STR_TO_CH=$F_EZ_SED_ECP_R
    fi

    if [ -z "$CHK_INVERT" ] ; then
        CHK_INVERT=0
    fi
    FL_CONT_STR_R=0
    if [ ${CHK_INVERT} -eq 0 ] ; then
        if grep -q "$STR_TO_CH" "$FILE"; then
            FL_CONT_STR_R=1
        fi
    else
        if ! grep -q "$STR_TO_CH" "$FILE"; then
            FL_CONT_STR_R=1
        fi
    fi
    if [ ${EZ_I_SKIP_ON_V} -eq 0 ] && [ ${FL_CONT_STR_R} -eq 1 ] && [ ! -z "$COND_MSG_P" ] ; then
        f_div_section
        echo "$COND_MSG_P"
        f_div_section
        f_enter_to_cont
    fi
}

CHK_FD_FL_R=0
f_chk_fd_fl() {
    : 'Verificar se determinado diretório ou arquivo existe.

    Args:
        TARGET (str): Diretório ou arquivo qual se quer verificar.
        CHK_TYPE (str): "d" - Checar por diretório; "f" - Checar por 
    arquivo.

    Returns:
        CHK_FD_FL_R (int): 1 - True; 0 - False.
    '

    CHK_FD_FL_R=0
    TARGET=$1
    CHK_TYPE=$2
    if [ "$CHK_TYPE" == "f" ] ; then
        if [ -f "$TARGET" ] ; then
            CHK_FD_FL_R=1
        fi
    fi
    if [ "$CHK_TYPE" == "d" ] ; then
        if [ -d "$TARGET" ] ; then
            CHK_FD_FL_R=1
        fi
    fi
}

F_PACK_IS_INST_R=0
f_pack_is_inst() {
    : 'Checar se um pacote está instalado.

    Args:
        PACKAGE_NM_P (str): Nome do pacote.
        PACK_MANAG (str): Tipo de gerenciador de pacotes. "yum", 
    "apt-get" e "zypper" são suportados. Em caso diverso o script 
    exibe erro e para.
        EXIST_MSG_P (Optional[str]): Mensagem a ser exibida se o 
    pacote já estiver instalado. Se vazio ou não informado não será 
    exibida mensagem.
        SKIP_MSG_P (Optional[int]): 1 - Omite a mensagem; 0 - Não omite a 
    mensagem. Padrão 1.

    Returns:
        F_PACK_IS_INST_R (int): 1 - Instalado; 0 - Não instalado.
    '

    PACKAGE_NM_P=$1
    PACK_MANAG=$2
    EXIST_MSG_P=$3
    SKIP_MSG_P=$4

    if [ -z "$SKIP_MSG_P" ] ; then
        SKIP_MSG_P=1
    fi
    if [ ${EZ_I_SKIP_ON_V} -eq 1 ] ; then
        SKIP_MSG_P=1
    fi

    F_PACK_IS_INST_R=0
    if [ "$PACK_MANAG" == "yum" ] ; then
        if yum list installed "$PACKAGE_NM_P" >/dev/null 2>&1; then
            if [ ${SKIP_MSG_P} -eq 0 ] && [ ! -z "$EXIST_MSG_P" ] ; then
                f_div_section
                echo "$EXIST_MSG_P"
                f_div_section
                f_enter_to_cont
            fi
            F_PACK_IS_INST_R=1
        else
            F_PACK_IS_INST_R=0
        fi
    elif [ "$PACK_MANAG" == "apt-get" ] ; then
        if dpkg -s "$PACKAGE_NM_P" &> /dev/null; then
            if [ ${SKIP_MSG_P} -eq 0 ] && [ ! -z "$EXIST_MSG_P" ] ; then
                f_div_section
                echo "$EXIST_MSG_P"
                f_div_section
                f_enter_to_cont
            fi
            F_PACK_IS_INST_R=1
        else
            F_PACK_IS_INST_R=0
        fi
    elif [ "$PACK_MANAG" == "zypper" ] ; then
        if zypper se -i --match-word "$PACKAGE_NM_P" > /dev/null 2>&1; then
            if [ ${SKIP_MSG_P} -eq 0 ] && [ ! -z "$EXIST_MSG_P" ] ; then
                f_div_section
                echo "$EXIST_MSG_P"
                f_div_section
                f_enter_to_cont
            fi
            F_PACK_IS_INST_R=1
        else
            F_PACK_IS_INST_R=0
        fi
    else
        f_div_section
        echo "ERROR! Not implemented for \"$PACK_MANAG\"!"
        f_div_section
        f_enter_to_cont
    fi
}

F_CHK_BY_PATH_HLP_R=0
f_chk_by_path_hlp() {
    : 'Checar se um aplicativo/pacote/arquivo está presente/instalado 
    verificando-o através do seu caminho físico informando.

    Args:
        PATH_VER_P (str): Caminho físico para o aplicativo/pacote.
        VER_TYPE_P (str): Se o caminho físico é para um diretório ("d") 
    ou arquivo ("f").
        EXIST_MSG_P (Optional[str]): Mensagem a ser "printada" caso o 
    aplicativo/pacote/arquivo exista. Se não informado ou vazio não 
    exibe a mensagem.
        SKIP_MSG_P (Optional[int]): Não exibir mensagem.

    Returns:
        F_CHK_BY_PATH_HLP_R (int): 0 - Não existe; 1 - Existe 
    ("printa" menssagem contida em EXIST_MSG_P).
    '

    PATH_VER_P=$1
    VER_TYPE_P=$2
    EXIST_MSG_P=$3
    SKIP_MSG_P=$4
    if [ -z "$SKIP_MSG_P" ] ; then
        SKIP_MSG_P=0
    fi
    if [ ${EZ_I_SKIP_ON_V} -eq 1 ] ; then
        SKIP_MSG_P=1
    fi

    F_CHK_BY_PATH_HLP_R=0
    f_chk_fd_fl "$PATH_VER_P" "$VER_TYPE_P"
    if [ ${CHK_FD_FL_R} -eq 0 ] ; then
        F_CHK_BY_PATH_HLP_R=0
    else
        if [ ${SKIP_MSG_P} -eq 0 ] && [ ! -z "$EXIST_MSG_P" ]; then
            f_div_section
            echo "$EXIST_MSG_P"
            f_div_section
            f_enter_to_cont
        fi
        F_CHK_BY_PATH_HLP_R=1
    fi
}

F_CHK_IPTABLES_R=0
f_chk_iptables() {
    : 'Fazer verificações usando "iptables".

    Trata-se de um utilitário para fazer verificações diversas usando o 
    comando "iptables" NORMALMENTE CHECAR DE DETERMINADA PORTA ESTÁ 
    ABERTA.

    Ex 1.: f_chk_iptables 80
    Ex 2.: f_chk_iptables 80 "Já está aberta!"
    Ex 3.: f_chk_iptables 80 "Já está aberta!" 0 "ACCEPT" "tcp" "NEW"
    Ex 4.: f_chk_iptables 80 "Já está aberta!" 0 "ACCEPT" "tcp" "NEW" 5

    Args:
        PORT_P (int): Porta a ser verificada.
        MSG_P (Optional[str]): Mensagem a ser exibida em caso de 
    verdadeiro para a verificação (normalmente porta aberta). Se vazio 
    ou não informado não será exibida mensagem.
        SKIP_MSG_P (Optional[int]): Não exibir mensagem. 
    Padrão 0.
        TARGET_P (Optional[str]): Padrão "ACCEPT".
        PROT_P (Optional[str]): Padrão "tcp".
        STATE_P (str): Padrão "".
        POS_IN_CHAIN_P (int): Padrão "".

    Returns:
        F_CHK_IPTABLES_R (int): 1 - Verdadeiro para a verificação; 
    0 - Falso para a verificação.
    '

    PORT_P=$1
    MSG_P=$2
    SKIP_MSG_P=$3

    if [ -z "$SKIP_MSG_P" ] ; then
        SKIP_MSG_P=0
    fi
    if [ ${EZ_I_SKIP_ON_V} -eq 1 ] ; then
        SKIP_MSG_P=1
    fi

    TARGET_P=$4
    if [ -z "$TARGET_P" ] ; then
        TARGET_P="ACCEPT"
    fi
    PROT_P=$5
    if [ -z "$PROT_P" ] ; then
        PROT_P="tcp"
    fi
    STATE_P=$6
    if [ -z "$STATE_P" ] ; then
        STATE_P=""
    else
        STATE_P="state $STATE_P "
    fi
    POS_IN_CHAIN_P=$7
    if [ -z "$POS_IN_CHAIN_P" ] ; then
        POS_IN_CHAIN_P=""
    else
        POS_IN_CHAIN_P=$(printf "%-9s" $POS_IN_CHAIN_P)
    fi
    # GREP_OUT=$(iptables -vnL --line-numbers | grep "$POS_IN_CHAIN_P" | grep "$TARGET_P" | grep "$PROT_P" | grep "$STATE_P$PROT_P dpt:$PORT_P ")
    GREP_OUT=$(iptables -vnL --line-numbers | grep "$POS_IN_CHAIN_P" | grep "$TARGET_P" | grep "$PROT_P" | grep "dpt:$PORT_P ")
    if [ $? -eq 1 ] ; then
        F_CHK_IPTABLES_R=1
    else
        if [ ${SKIP_MSG_P} -eq 0 ] && [ ! -z "$MSG_P" ] ; then
            f_div_section
            echo "$MSG_P"
            f_div_section
            f_enter_to_cont
        fi
        F_CHK_IPTABLES_R=0
    fi
}

F_IS_NOT_RUNNING_R=0
f_is_not_running() {
    : 'Checar de determinado processo (pode ser um serviço) está 
    rodando.

    Args:
        PROC_NM_P (str): Nome do processo (pode ser um serviço).
        COND_MSG_P (Optional[str]): Mensagem a ser exibida se 
    verdadeira a verificação. Se vazio ou não informado não será 
    exibida mensagem.
        CHK_INVERT (Optional[int]): Inverter a lógica da checagem. 
    Padrão 0.

    Returns:
        F_IS_NOT_RUNNING_R (int): 1 - Se verdadeiro para a condição 
    analisada; 0 - Se falso para a condição analisada.
    '

    PROC_NM_P=$1
    COND_MSG_P=$2
    CHK_INVERT=$3
    if [ -z "$CHK_INVERT" ] ; then
        CHK_INVERT=0
    fi
    F_IS_NOT_RUNNING_R=0

    # NOTE: A verificação "grep -v grep" é para que ele não dê positivo 
    # para o próprio comando grep! By Questor
    F_IS_NOT_RUNNING_R=0
    if [ ${CHK_INVERT} -eq 0 ] ; then
        if ! ps aux | grep -v "grep" | grep "$PROC_NM_P" > /dev/null ; then
            F_IS_NOT_RUNNING_R=1
        fi
    else
        if ps aux | grep -v "grep" | grep "$PROC_NM_P" > /dev/null ; then
            F_IS_NOT_RUNNING_R=1
        fi
    fi
    if [ ${EZ_I_SKIP_ON_V} -eq 0 ] && [ ${F_IS_NOT_RUNNING_R} -eq 1 ] && [ ! -z "$COND_MSG_P" ] ; then
        f_div_section
        echo "$COND_MSG_P"
        f_div_section
        f_enter_to_cont
    fi
}

F_GET_STDERR_R=""
F_GET_STDOUT_R=""
F_GET_EXIT_CODE_R=0
f_get_stderr_stdout() {
    : 'Executar um comando e colocar a saída de stderr e stdout nas 
    variáveis "F_GET_STDERR_R" e "F_GET_STDOUT_R"!.

    Args:
        CMD_TO_EXEC (str): Comando a ser executado.

    Returns:
        F_GET_STDERR_R (str): Saída para stderr.
        F_GET_STDOUT_R (str): Saída para stdout.
    '

    CMD_TO_EXEC=$1
    F_GET_STDERR_R=""
    F_GET_STDOUT_R=""
    unset t_std t_err t_ret
    eval "$( eval "$CMD_TO_EXEC" 2> >(t_err=$(cat); typeset -p t_err) > >(t_std=$(cat); typeset -p t_std); t_ret=$?; typeset -p t_ret )"
    F_GET_EXIT_CODE_R=$t_ret
    F_GET_STDERR_R=$t_err
    F_GET_STDOUT_R=$t_std
}

F_BAK_PATH_R=""
F_BAK_MD_R=0
f_ez_mv_bak() {
    : 'Modifica o nome de um arquivo ou pasta para um nome de backup.

    Adiciona um sufixo ao nome no formato: "-D%Y-%m-%d-T%H-%M-%S.bak".

    Args:
        TARGET (str): Caminho para o arquivo ou pasta alvo.
        CONF_MSG_P (Optional[str]): Verificar se o usuário deseja ou 
    não backup. Se vazio ou não informado não será exibida mensagem.
        SKIP_MSG_P (Optional[int]): 0 - Exibe a mensagem informada; 1 - Não 
    exibe a mensagem informada. Padrão 0.
        USE_COPY_P (Optional[int]): 0 - Define um novo nome para o alvo; 1 - 
    Faz uma cópia do alvo com um novo nome. Padrão 0.
        DONT_CONFIRM_IF_EXISTS_P (Optional[int]): 0 - Verifica; 1 - Não verifica. 
    Padrão 0.

    Returns:
        F_BAK_PATH_R (str): Caminho para o arquivo ou pasta alvo com o 
    novo nome.
        F_BAK_NAME_R (str): Nome do arquivo recém criado.
        F_BAK_MD_R (int): 1 - Backup realizado; 0 - Backup não 
    realizado.
    '

    TARGET=$1
    CONF_MSG_P=$2
    SKIP_MSG_P=$3
    if [ -z "$SKIP_MSG_P" ] ; then
        SKIP_MSG_P=0
    fi
    if [ ${EZ_I_SKIP_ON_V} -eq 1 ] ; then
        SKIP_MSG_P=1
    fi
    USE_COPY_P=$4
    if [ -z "$USE_COPY_P" ] ; then
        USE_COPY_P=0
    fi
    DONT_CONFIRM_IF_EXISTS_P=$5
    if [ -z "$DONT_CONFIRM_IF_EXISTS_P" ] ; then
        DONT_CONFIRM_IF_EXISTS_P=0
    fi
    MK_BAK=1
    F_BAK_PATH_R=""
    F_BAK_NAME_R=""
    F_BAK_MD_R=0

    if [[ -e $TARGET ]]; then
        if [ ${SKIP_MSG_P} -eq 0 ] && [ ! -z "$CONF_MSG_P" ] ; then
            f_div_section
            f_yes_no "$CONF_MSG_P"
            f_div_section
            MK_BAK=$YES_NO_R
        fi
        if [ ${MK_BAK} -eq 1 ] ; then
            SUFFIX=$(date +"-D%Y-%m-%d-T%H-%M-%S.bak")
            NEW_NAME="$TARGET$SUFFIX"
            if [ ${USE_COPY_P} -eq 0 ] ; then
                mv "$TARGET" "$NEW_NAME"
            elif [ ${USE_COPY_P} -eq 1 ] ; then
                cp "$TARGET" "$NEW_NAME"
            fi
            F_BAK_PATH_R=$NEW_NAME
            F_BAK_NAME_R="${NEW_NAME##*/}"
            F_BAK_MD_R=1
        fi
    else
        if [ ${DONT_CONFIRM_IF_EXISTS_P} -eq 0 ] ; then
            f_enter_to_cont "ERROR! The target does not exist!"
        fi
    fi
}

f_error_exit() {
    : '"Printa" uma mensagem de erro e encerra o instalador.

    Args:
        ERROR_CAUSE_P (Optional[str]): Causa do erro.
    '

    EZ_I_S_ON_HOLDER=$EZ_I_SKIP_ON_V
    EZ_I_SKIP_ON_V=0
    ERROR_CAUSE_P=$1
    echo 
    f_open_section "E R R O R !"
    ERROR_MSG_NOW_P="AN ERROR OCCURRED AND THIS INSTALLER WAS CLOSED!"
    if [ ! -z "$ERROR_CAUSE_P" ] ; then
        ERROR_MSG_NOW_P="$ERROR_MSG_NOW_P ERROR: \"$ERROR_CAUSE_P\""
    fi
    echo "$ERROR_MSG_NOW_P"
    echo 
    f_close_section
    EZ_I_SKIP_ON_V=$EZ_I_S_ON_HOLDER
    exit 1
}

f_warning_msg() {
    : '"Printa" uma mensagem de aviso.

    Args:
        WARNING_P (str): aviso.
        ASK_FOR_CONT_P (Optional[int]): 1 - Checa se o usuário deseja 
    continuar com a instalação; 0 - Solicita que pressione "enter". 
    Padrão 0.
    '

    EZ_I_S_ON_HOLDER=$EZ_I_SKIP_ON_V
    EZ_I_SKIP_ON_V=0
    WARNING_P=$1
    ASK_FOR_CONT_P=$2
    if [ -z "$ASK_FOR_CONT_P" ] ; then
        ASK_FOR_CONT_P=0
    fi
    echo 
    f_open_section "W A R N I N G !"
    echo "$WARNING_P"
    echo 
    f_close_section
    if [ ${ASK_FOR_CONT_P} -eq 0 ] ; then
        f_enter_to_cont
    else
        f_continue
    fi
    EZ_I_SKIP_ON_V=$EZ_I_S_ON_HOLDER
}

f_continue() {
    : 'Questionar ao usuário se deseja continuar ou parar a instalação.

    Args:
        NOTE_P (Optional[str]): Informações adicionais ao usuário.
    '

    NOTE_P=$1
    f_div_section
    if [ -z "$NOTE_P" ] ; then
        NOTE_P=""
    else
        NOTE_P=" (NOTE: \"$NOTE_P\")"
    fi

    f_yes_no "CONTINUE? (USE \"n\" TO STOP THIS INSTALLER)$NOTE_P"
    f_div_section
    if [ ${YES_NO_R} -eq 0 ] ; then
        exit 0
    fi
}

F_SPLIT_R=()
f_split() {
    : 'Faz "split" em uma dada string e devolve um array.

    Args:
        TARGET_P (str): String alvo do "split".
        DELIMITER_P (Optional[str]): Delimitador usado no "split". 
    Se não informado o split vai ser feito por espaços em branco.

    Returns:
        F_SPLIT_R (array): Array com a string fornecida separada pelo 
    delimitador informado.
    '

    F_SPLIT_R=()
    TARGET_P=$1
    DELIMITER_P=$2
    if [ -z "$DELIMITER_P" ] ; then
        DELIMITER_P=" "
    fi

    REMOVE_N=1
    if [ "$DELIMITER_P" == "\n" ] ; then
        REMOVE_N=0
    fi

    if [ ${REMOVE_N} -eq 1 ] ; then

        # NOTE: Devido a limitações do bash temos alguns problemas para 
        # poder obter a saída de um split via awk dentro de um array e 
        # por isso precisamos do uso da "quebra de linha" (\n) para 
        # termos sucesso! Visto isso, removemos as quebras de linha 
        # momentaneamente depois as reintegramos! By Questor
        TARGET_P=$(echo "$TARGET_P" | awk 'BEGIN {RS="dn" } {gsub("\n","£§¢¬¨") ;printf $0 }')
    fi

    SPLIT_NOW=$(awk -F"$DELIMITER_P" '{for(i=1;i<=NF;i++){printf "%s\n", $i}}' <<<"${TARGET_P}")

    while IFS= read -r LINE_NOW; do
        if [ ${REMOVE_N} -eq 1 ] ; then
            LN_NOW_WITH_N=$(awk 'BEGIN {RS="dn"} {gsub("£§¢¬¨","\n") ;printf $0 }' <<<"${LINE_NOW}")
            F_SPLIT_R+=("$LN_NOW_WITH_N")
        else
            F_SPLIT_R+=("$LINE_NOW")
        fi
    done <<< "$SPLIT_NOW"
}

F_ABOUT_DISTRO_R=()
f_about_distro() {
    : 'Obter informações sobre a distro.

    Returns:
        F_ABOUT_DISTRO_R (array): Array com informações sobre a 
    distro na seguinte ordem: NAME, VERSION, BASED e ARCH.
    '

    F_ABOUT_DISTRO_R=()
    f_get_stderr_stdout "cat /etc/*-release"
    ABOUT_INFO=$F_GET_STDOUT_R

    if [[ $ABOUT_INFO == *"ID=debian"* ]] ; then
        f_split "$ABOUT_INFO" "\n"
        F_SPLIT_R_0=("${F_SPLIT_R[@]}")
        TOTAL_0=${#F_SPLIT_R_0[*]}
        for (( i=0; i<=$(( $TOTAL_0 -1 )); i++ )) ; do
            f_split "${F_SPLIT_R_0[$i]}" "="
            F_SPLIT_R_1=("${F_SPLIT_R[@]}")
            TOTAL_1=${#F_SPLIT_R_1[*]}
            for (( o=0; o<=$(( $TOTAL_1 -1 )); o++ )) ; do
                p=$[$o+1]
                case "${F_SPLIT_R_1[$o]}" in
                    "NAME")
                        f_split "${F_SPLIT_R_1[$p]}" "\""
                        F_SPLIT_R_2=("${F_SPLIT_R[@]}")
                        F_ABOUT_DISTRO_R+=("${F_SPLIT_R_2[1]}")
                    ;;
                    "VERSION_ID")
                        f_split "${F_SPLIT_R_1[$p]}" "\""
                        F_SPLIT_R_3=("${F_SPLIT_R[@]}")
                        F_ABOUT_DISTRO_R+=("${F_SPLIT_R_3[1]}")
                    ;;
                    *)
                        
                    ;;
                esac
            done
        done
        F_ABOUT_DISTRO_R+=("Debian")
    elif [[ $ABOUT_INFO == *"ID=\"sles\""* ]] ; then
        f_split "$ABOUT_INFO" "\n"
        F_SPLIT_R_0=("${F_SPLIT_R[@]}")
        TOTAL_0=${#F_SPLIT_R_0[*]}
        for (( i=0; i<=$(( $TOTAL_0 -1 )); i++ )) ; do
            f_split "${F_SPLIT_R_0[$i]}" "="
            F_SPLIT_R_1=("${F_SPLIT_R[@]}")
            TOTAL_1=${#F_SPLIT_R_1[*]}
            for (( o=0; o<=$(( $TOTAL_1 -1 )); o++ )) ; do
                p=$[$o+1]
                case "${F_SPLIT_R_1[$o]}" in
                    "NAME")
                        f_split "${F_SPLIT_R_1[$p]}" "\""
                        F_SPLIT_R_2=("${F_SPLIT_R[@]}")
                        F_ABOUT_DISTRO_R+=("${F_SPLIT_R_2[1]}")
                    ;;
                    "VERSION_ID")
                        f_split "${F_SPLIT_R_1[$p]}" "\""
                        F_SPLIT_R_3=("${F_SPLIT_R[@]}")
                        F_ABOUT_DISTRO_R+=("${F_SPLIT_R_3[1]}")
                    ;;
                    *)
                        
                    ;;
                esac
            done
        done
        F_ABOUT_DISTRO_R+=("Suse")
    elif [[ $ABOUT_INFO == *"ID=opensuse"* ]] || 
        [[ $ABOUT_INFO == *"ID_LIKE=\"suse\""* ]] ; then
        f_split "$ABOUT_INFO" "\n"
        F_SPLIT_R_0=("${F_SPLIT_R[@]}")
        TOTAL_0=${#F_SPLIT_R_0[*]}
        for (( i=0; i<=$(( $TOTAL_0 -1 )); i++ )) ; do
            f_split "${F_SPLIT_R_0[$i]}" "="
            F_SPLIT_R_1=("${F_SPLIT_R[@]}")
            TOTAL_1=${#F_SPLIT_R_1[*]}
            for (( o=0; o<=$(( $TOTAL_1 -1 )); o++ )) ; do
                p=$[$o+1]
                case "${F_SPLIT_R_1[$o]}" in
                    "NAME")
                        F_ABOUT_DISTRO_R+=("${F_SPLIT_R_1[$p]}")
                    ;;
                    "VERSION_ID")
                        f_split "${F_SPLIT_R_1[$p]}" "\""
                        F_SPLIT_R_3=("${F_SPLIT_R[@]}")
                        F_ABOUT_DISTRO_R+=("${F_SPLIT_R_3[1]}")
                    ;;
                    *)
                        
                    ;;
                esac
            done
        done
        F_ABOUT_DISTRO_R+=("Suse")
    elif [[ $ABOUT_INFO == *"DISTRIB_ID=Ubuntu"* ]] || 
        [[ $ABOUT_INFO == *"ID_LIKE=debian"* ]] ; then
        f_split "$ABOUT_INFO" "\n"
        F_SPLIT_R_0=("${F_SPLIT_R[@]}")
        TOTAL_0=${#F_SPLIT_R_0[*]}
        for (( i=0; i<=$(( $TOTAL_0 -1 )); i++ )) ; do
            f_split "${F_SPLIT_R_0[$i]}" "="
            F_SPLIT_R_1=("${F_SPLIT_R[@]}")
            TOTAL_1=${#F_SPLIT_R_1[*]}
            for (( o=0; o<=$(( $TOTAL_1 -1 )); o++ )) ; do
                p=$[$o+1]
                case "${F_SPLIT_R_1[$o]}" in
                    "DISTRIB_ID")
                        F_ABOUT_DISTRO_R+=("${F_SPLIT_R_1[$p]}")
                    ;;
                    "DISTRIB_RELEASE")
                        F_ABOUT_DISTRO_R+=("${F_SPLIT_R_1[$p]}")
                    ;;
                    *)
                        
                    ;;
                esac
            done
        done
        F_ABOUT_DISTRO_R+=("Debian")
    elif [[ $ABOUT_INFO == *"CentOS release 6"* ]] ; then
        # NOTE: Para a geração CentOS 6.X! By Questor

        f_split "$ABOUT_INFO" "\n"
        F_SPLIT_R_0=("${F_SPLIT_R[1]}")
        f_split "${F_SPLIT_R_0[0]}" " "
        F_SPLIT_R_1=("${F_SPLIT_R[@]}")
        F_ABOUT_DISTRO_R+=("${F_SPLIT_R_1[0]}")
        F_ABOUT_DISTRO_R+=("${F_SPLIT_R_1[2]}")
        F_ABOUT_DISTRO_R+=("RedHat")
    elif [[ $ABOUT_INFO == *"CentOS Linux release 7"* ]] ; then
        # NOTE: Para a geração CentOS 7.X! By Questor

        f_split "$ABOUT_INFO" "\n"
        F_SPLIT_R_0=("${F_SPLIT_R[@]}")
        TOTAL_0=${#F_SPLIT_R_0[*]}
        for (( i=0; i<=$(( $TOTAL_0 -1 )); i++ )) ; do
            f_split "${F_SPLIT_R_0[$i]}" "="
            F_SPLIT_R_1=("${F_SPLIT_R[@]}")
            TOTAL_1=${#F_SPLIT_R_1[*]}
            for (( o=0; o<=$(( $TOTAL_1 -1 )); o++ )) ; do
                p=$[$o+1]
                case "${F_SPLIT_R_1[$o]}" in
                    "NAME")
                        f_split "${F_SPLIT_R_1[$p]}" "\""
                        F_SPLIT_R_2=("${F_SPLIT_R[@]}")
                        F_ABOUT_DISTRO_R+=("${F_SPLIT_R_2[1]}")
                    ;;
                    "VERSION_ID")
                        f_split "${F_SPLIT_R_1[$p]}" "\""
                        F_SPLIT_R_3=("${F_SPLIT_R[@]}")
                        F_ABOUT_DISTRO_R+=("${F_SPLIT_R_3[1]}")
                    ;;
                    *)
                        
                    ;;
                esac
            done
        done
        F_ABOUT_DISTRO_R+=("RedHat")
    elif [[ $ABOUT_INFO == *"Red Hat Enterprise Linux Server"* ]] || 
            [[ $ABOUT_INFO == *"VERSION_ID=\"7."* ]]; then
        # NOTE: Para a geração RHEL 7.X! By Questor

        f_split "$ABOUT_INFO" "\n"
        F_SPLIT_R_0=("${F_SPLIT_R[@]}")
        TOTAL_0=${#F_SPLIT_R_0[*]}
        for (( i=0; i<=$(( $TOTAL_0 -1 )); i++ )) ; do
            f_split "${F_SPLIT_R_0[$i]}" "="
            F_SPLIT_R_1=("${F_SPLIT_R[@]}")
            TOTAL_1=${#F_SPLIT_R_1[*]}
            for (( o=0; o<=$(( $TOTAL_1 -1 )); o++ )) ; do
                p=$[$o+1]
                case "${F_SPLIT_R_1[$o]}" in
                    "NAME")
                        f_split "${F_SPLIT_R_1[$p]}" "\""
                        F_SPLIT_R_2=("${F_SPLIT_R[@]}")
                        F_ABOUT_DISTRO_R+=("${F_SPLIT_R_2[1]}")
                    ;;
                    "VERSION_ID")
                        f_split "${F_SPLIT_R_1[$p]}" "\""
                        F_SPLIT_R_3=("${F_SPLIT_R[@]}")
                        F_ABOUT_DISTRO_R+=("${F_SPLIT_R_3[1]}")
                    ;;
                    *)
                        
                    ;;
                esac
            done
        done
        F_ABOUT_DISTRO_R+=("RedHat")
    elif [[ $ABOUT_INFO == *"Red Hat Enterprise Linux Server release "* ]] ; then
        f_split "$ABOUT_INFO" "\n"
        F_SPLIT_R_0=("${F_SPLIT_R[1]}")
        f_split "${F_SPLIT_R_0[0]}" " "
        F_SPLIT_R_1=("${F_SPLIT_R[@]}")
        F_ABOUT_DISTRO_R+=("Red Hat Enterprise Linux Server")
        F_ABOUT_DISTRO_R+=("${F_SPLIT_R_1[6]}")
        F_ABOUT_DISTRO_R+=("RedHat")
    else
        F_ABOUT_DISTRO_R+=("Unknown")
        F_ABOUT_DISTRO_R+=("Unknown")
        F_ABOUT_DISTRO_R+=("Unknown")
    fi
    F_ABOUT_DISTRO_R+=($(arch))
}

F_IS_ROOT_R=1
f_is_root() {
    : 'Checar se o usuário é root.

    Args:
        CHK_ONLY_P (Optional[int]): 1 - Apenas verifica e retorna o 
    resultado; 0 - Se não for root emite erro e encerra a execução. 
    Padrão 0.

    Returns:
        F_IS_ROOT_R (int): 1 - É root; 0 - Não é root.
    '

    CHK_ONLY_P=$1
    if [ -z "$CHK_ONLY_P" ] ; then
        CHK_ONLY_P=0
    fi

    F_IS_ROOT_R=1
    if [[ $EUID -ne 0 ]]; then
        f_enter_to_cont "ERROR! You need to be root!"
        F_IS_ROOT_R=0
        if [ ${CHK_ONLY_P} -eq 0 ] ; then
            f_error_exit
        fi
    fi
}

F_CHK_DISTRO_STATUS_R=""
f_chk_distro_status() {
    : 'Verifica se a distro informada está subscrita e/ou registrada 
    e/ou ativa perante os recursos informados.

    Args:
        DISTRO_NAME_P (str): Nome da distro sobre a qual será executada 
    verificação.
        RESOURCES_ARR_P (array): Array com a lista de recursos a serem 
    verificados na distro alvo.

    Returns:
        F_CHK_DISTRO_STATUS_R (str): Possui a saída do comando de 
    verificação executado.
    '

    F_CHECK_RHEL_R=""
    DISTRO_NAME_P=$1
    RESOURCES_ARR_P=("${!2}")
    TOTAL_2=${#RESOURCES_ARR_P[*]}
    RES_OK_ARR=()
    REDHAT_ACTV=0

    CHK_RES_CMD=""
    if [ "$DISTRO_NAME_P" == "RedHat" ] ; then
        CHK_RES_CMD="subscription-manager list --consumed"
        f_get_stderr_stdout "$CHK_RES_CMD"
        F_CHK_DISTRO_STATUS_R=$F_GET_STDOUT_R

        # NOTE: To debug! By Questor
#         F_GET_STDOUT_R="No consumed subscription pools to list
# "

        if [[ $F_GET_STDOUT_R == *"No consumed subscription pools to list"* ]] ; then
            f_get_stderr_stdout "yum repolist"
            F_CHK_DISTRO_STATUS_R=$F_GET_STDOUT_R

            # NOTE: To debug! By Questor
#             F_GET_STDOUT_R="Loaded plugins: product-id, rhnplugin, security, subscription-manager
# This system is receiving updates from RHN Classic or RHN Satellite.
# repo id                            repo name                              status
# epel                               Extra Packages for Enterprise Linux 6  12125
# rhel-x86_64-server-6               Red Hat Enterprise Linux Server (v. 6  14725
# rhel-x86_64-server-optional-6      RHEL Server Optional (v. 6 64-bit x86_  8257
# rhel-x86_64-server-supplementary-6 RHEL Server Supplementary (v. 6 64-bit   483
# repolist: 35590
# "

            if [[ $F_GET_STDOUT_R == *"RHN Classic or Red Hat Satellite"* ]] ; then
                WAR_MSGS_STR="THE REDHAT IS APPARENTLY USING \"RHN Classic\" OR \"Red Hat Satellite\" TO ACCESS ITS RESOURCES!
THIS INSTALLER WILL NOT VALIDATE THESE RESOURCES!"
                WAR_MSGS_STR+=$'\n\n'"FOR MORE INFORMATION TRY: \"yum repolist\"."
                f_warning_msg "$WAR_MSGS_STR" 1
                return 0
            fi
        else
            f_split "$F_GET_STDOUT_R" "Subscription Name:"
        fi
    elif [ "$DISTRO_NAME_P" == "SLES" ] ; then
        CHK_RES_CMD="zypper sl"
        f_get_stderr_stdout "$CHK_RES_CMD"
        f_split "$F_GET_STDOUT_R" "\n"
        F_CHK_DISTRO_STATUS_R=$F_GET_STDOUT_R
    fi

    F_SPLIT_R_0=("${F_SPLIT_R[@]}")
    TOTAL_0=${#F_SPLIT_R_0[*]}
    for (( i=0; i<=$(( $TOTAL_0 -1 )); i++ )) ; do
        if [[ "$DISTRO_NAME_P" == "RedHat" ]] ; then
            f_split "${F_SPLIT_R_0[$i]}" "\n"
            F_SPLIT_R_1=("${F_SPLIT_R[@]}")
            TOTAL_1=${#F_SPLIT_R_1[*]}
            CHK_ACTV=0
            for (( o=0; o<=$(( $TOTAL_1 -1 )); o++ )) ; do
                if [[ "${F_SPLIT_R_1[$o]}" == "Provides:"* ]] ; then
                    CHK_ACTV=1
                fi
                if [ ${CHK_ACTV} -eq 1 ] ; then
                    for (( w=0; w<=$(( $TOTAL_2 -1 )); w++ )) ; do
                        if [[ "${F_SPLIT_R_1[$o]}" == *"${RESOURCES_ARR_P[$w]}" ]] ; then
                            RES_OK_ARR+=($w)
                            break
                        fi
                    done
                    if [ ${REDHAT_ACTV} -eq 0 ] && 
                            [[ "${F_SPLIT_R_1[$o]}" == "Active:"* ]] && 
                            [[ "${F_SPLIT_R_1[$o]}" == *"True" ]] ; then
                        REDHAT_ACTV=1
                    fi
                fi
            done
        elif [[ "$DISTRO_NAME_P" == "SLES" ]] ; then
            REDHAT_ACTV=1
            f_split "${F_SPLIT_R_0[$i]}" "|"
            F_SPLIT_R_1=("${F_SPLIT_R[@]}")
            for (( w=0; w<=$(( $TOTAL_2 -1 )); w++ )) ; do
                if [[ "${F_SPLIT_R_1[1]}" == *"${RESOURCES_ARR_P[$w]}"* ]] ; then
                    if [[ "${F_SPLIT_R_1[3]}" == *"Yes"* ]] ; then
                        if [[ "${F_SPLIT_R_1[5]}" == *"Yes"* ]] ; then
                            RES_OK_ARR+=($w)
                            break
                        fi
                    fi
                fi
            done
        fi
    done

    WARNINGS_MSGS=()
    TOTAL_3=${#RES_OK_ARR[*]}
    for (( z=0; z<=$(( $TOTAL_2 -1 )); z++ )) ; do
        RES_OK_NOW=1
        for (( t=0; t<=$(( $TOTAL_3 -1 )); t++ )) ; do
            if (( ${RES_OK_ARR[$t]} == $z )); then
                RES_OK_NOW=0
                break
            fi
        done
        if (( $RES_OK_NOW == 1 )); then
            WARNINGS_MSGS+=("$DISTRO_NAME_P does not have access to this resource: \"${RESOURCES_ARR_P[$z]}\".")
        fi
    done

    # NOTE: Essa verificação é específica para o SLES. Não encontrei uma forma 
    # melhor de fazê-la... mas funciona bem! By Questor
    if [[ "$DISTRO_NAME_P" == "SLES" ]] ; then
        CHK_RES_CMD=""
        f_get_stderr_stdout "zypper --non-interactive se hfsdfsdufnmfdns"
        f_split "$F_GET_STDERR_R" "\n"
        F_SPLIT_R_2=("${F_SPLIT_R[@]}")
        if [[ "${F_SPLIT_R_2[0]}" == *"Permission to access "* ]] && [[ "${F_SPLIT_R_2[0]}" == *" denied."* ]] ; then
            WARNINGS_MSGS+=("${F_SPLIT_R_2[0]}")
        fi
    fi

    TOTAL_4=${#WARNINGS_MSGS[*]}
    WAR_MSGS_STR=""
    USE_NEWLINE=""
    if [ ! $TOTAL_4 -eq 0 ] || [ $REDHAT_ACTV -eq 0 ]; then
        WAR_MSGS_STR="SOME PROBLEM APPEAR TO HAVE BEEN DETECTED ON"
        if [[ "$DISTRO_NAME_P" == "RedHat" ]] ; then
            WAR_MSGS_STR+=" REDHAT SUBSCRIPTION! "
        elif [[ "$DISTRO_NAME_P" == "SLES" ]] ; then
            WAR_MSGS_STR+=" SLES REGISTRATION! "
        fi
        WAR_MSGS_STR+="PLEASE CHECK IT!"
        for (( y=0; y<=$(( $TOTAL_4 -1 )); y++ )) ; do
            if (( $y == 0 )); then
                WAR_MSGS_STR+=$'\n\n'
            else
                USE_NEWLINE=$'\n'
            fi
            WAR_MSGS_STR+="$USE_NEWLINE -> ${WARNINGS_MSGS[$y]}"
        done
        if [ ! -z "$CHK_RES_CMD" ] ; then
            WAR_MSGS_STR+=$'\n\n'"FOR MORE INFORMATION TRY: \"$CHK_RES_CMD\"."
        fi
        f_warning_msg "$WAR_MSGS_STR" 1
    fi
}

F_STR_TRIM_R=""
f_str_trim(){
    : 'Remover caracteres em branco (espaços) antes e/ou depois da string 
    informada.

    Args:
        STR_VAL_P (str): String a ser ajustada.
        TRIM_MODE_P (Optional[int]): 0 - Remove à esquerda (leading); 1 - 
    Remove à direita (trailing); 2 - Remove em ambos os lados. Padrão 0.

    Returns:
        F_STR_TRIM_R (str): String ajustada.
    '

    STR_VAL_P=$1
    TRIM_MODE_P=$2
    if [ -z "$TRIM_MODE_P" ] ; then
        TRIM_MODE_P=0
    fi

    case $TRIM_MODE_P in
        0)
            STR_VAL_P="${STR_VAL_P#"${STR_VAL_P%%[![:space:]]*}"}"
        ;;
        1)
            STR_VAL_P="${STR_VAL_P%"${STR_VAL_P##*[![:space:]]}"}"
        ;;
        2)
            STR_VAL_P="${STR_VAL_P#"${STR_VAL_P%%[![:space:]]*}"}"
            STR_VAL_P="${STR_VAL_P%"${STR_VAL_P##*[![:space:]]}"}"
        ;;
    esac
    F_STR_TRIM_R="$STR_VAL_P"
}

F_SRV_MEMORY_R=0
f_srv_memory() {
    : 'Informar sobre a memória do servidor.

    Returns:
        F_SRV_MEMORY_R (int): Quantidade de memória RAM do servidor em KBs.
    '

    f_get_stderr_stdout "cat /proc/meminfo"
    f_split "$F_GET_STDOUT_R" "\n"
    f_split "${F_SPLIT_R[0]}" "MemTotal:"
    f_split "${F_SPLIT_R[1]}" "kB"
    f_str_trim "${F_SPLIT_R[0]}" 2
    F_SRV_MEMORY_R=$F_STR_TRIM_R
}

# < --------------------------------------------------------------------------

# > --------------------------------------------------------------------------
# GRAFICO!
# --------------------------------------

f_indent() {
    : 'Definir uma tabulação para uma string informada.

    Exemplo de uso: echo "<STR_VALUE>" | f_indent 4

    Args:
        LEVEL_P (int): 2, 4 ou 8 espaços.
    '

    LEVEL_P=$1
    if [ ${LEVEL_P} -eq 2 ] ; then
        sed 's/^/  /';
    fi
    if [ ${LEVEL_P} -eq 4 ] ; then
        sed 's/^/    /';
    fi
    if [ ${LEVEL_P} -eq 8 ] ; then
        sed 's/^/        /';
    fi
}

f_open_main_section() {
    : 'Printar abertura de uma seção principal (agrupa outras seções).'

    if [ ${EZ_I_SKIP_ON_V} -eq 1 ] ; then
        return 0
    fi
    TITLE_P=$1
    echo "> =================================================================="
    if [ -n "$TITLE_P" ] ; then
        echo "$TITLE_P"
        f_div_section
        echo 
    fi
}

f_close_main_section() {
    : 'Printar fechamento de uma seção principal (agrupa outras seções).'

    if [ ${EZ_I_SKIP_ON_V} -eq 1 ] ; then
        return 0
    fi
    echo "< =================================================================="
    echo 
}

f_open_section() {
    : 'Printar abertura de uma seção.'

    if [ ${EZ_I_SKIP_ON_V} -eq 1 ] ; then
        return 0
    fi
    TITLE_P=$1
    echo "> ------------------------------------------------"
    if [ -n "$TITLE_P" ] ; then
        echo "$TITLE_P"
        f_div_section
        echo 
    fi
}

f_close_section() {
    : 'Printar fechamento de uma seção.'

    if [ ${EZ_I_SKIP_ON_V} -eq 1 ] ; then
        return 0
    fi
    echo "< ------------------------------------------------"
    echo 
}

f_div_section() {
    : 'Printar divisão em uma seção.'

    if [ ${EZ_I_SKIP_ON_V} -eq 1 ] ; then
        return 0
    fi
    echo "----------------------------------"
}

f_sub_section() {
    : 'Printar uma subseção.

    Args:
        TITLE_P (str): Título da subseção.
        TEXT_P (str): Texto da subseção.
    '

    if [ ${EZ_I_SKIP_ON_V} -eq 1 ] ; then
        return 0
    fi
    TITLE_P=$1
    TEXT_P=$2
    echo "> $TITLE_P" | f_indent 2
    echo 
    echo "$TEXT_P" | f_indent 4
    echo 
}

# < --------------------------------------------------------------------------

# > --------------------------------------------------------------------------
# APRESENTAÇÃO!
# --------------------------------------

f_begin() {
    : 'Printar uma abertura/apresentação para o instalador do produto.

    Usar no início da instalação.

    Args:
        TITLE_P (str): Título.
        VERSION_P (str): Versão do produto.
        ABOUT_P (str): Sobre o produto.
        WARNINGS_P (str): Avisos antes de continuar.
        COMPANY_P (str): Informações sobre a empresa.
    '

    clear
    if [ ${EZ_I_SKIP_ON_V} -eq 1 ] ; then
        return 0
    fi
    TITLE_P=$1
    VERSION_P=$2
    ABOUT_P=$3
    WARNINGS_P=$4
    COMPANY_P=$5
    f_open_section "$TITLE_P ($VERSION_P)"
    f_sub_section "ABOUT:" "$ABOUT_P"
    f_sub_section "WARNINGS:" "$WARNINGS_P"
    f_div_section
    echo "$COMPANY_P"
    f_close_section
    f_enter_to_cont
    clear
}

f_end() {
    : 'Printar uma fechamento/encerramento para o instalador do produto.

    Usar no final da instalação.

    Args:
        TITLE_P (str): Título.
        USEFUL_INFO_P (str): Informações úteis (uso básico etc...).
    '

    if [ ${EZ_I_SKIP_ON_V} -eq 1 ] ; then
        return 0
    fi
    TITLE_P=$1
    USEFUL_INFO_P=$2
    f_open_section "$TITLE_P"
    f_sub_section "USEFUL INFORMATION:" "$USEFUL_INFO_P"
    f_close_section
}

f_terms_licen() {
    : 'Printar os termos de licença/uso do produto.

    Pede que o usuário concorde com os termos.

    Args:
        TERMS_LICEN_P (str): Termos de licença/uso do produto.
    '

    if [ ${EZ_I_SKIP_ON_V} -eq 1 ] ; then
        return 0
    fi
    TERMS_LICEN_P=$1
    f_open_section "LICENSE/TERMS:"
    echo "$TERMS_LICEN_P" | f_indent 2
    echo 
    f_div_section
    TITLE_F="BY ANSWERING YES (y) YOU WILL AGREE WITH TERMS AND CONDITIONS "\
"PRESENTED! PROCEED?"
    f_yes_no "$TITLE_F"
    TITLE_F=""
    f_close_section
    sleep 1
    if [ ${YES_NO_R} -eq 0 ] ; then
        exit 0
    fi
    clear
}

f_instruct() {
    : 'Printar instruções sobre o produto.

    Args:
        INSTRUCT_P (str): Instruções sobre o produto.
    '

    if [ ${EZ_I_SKIP_ON_V} -eq 1 ] ; then
        return 0
    fi
    INSTRUCT_P=$1
    f_open_section "INSTRUCTIONS:"
    echo "$INSTRUCT_P" | f_indent 2
    echo 
    f_close_section
    f_enter_to_cont
    clear
}

# < --------------------------------------------------------------------------

# > --------------------------------------------------------------------------
# ESQUEMAS CONDICIONAIS!
# --------------------------------------

YES_NO_R=0
f_yes_no() {
    : 'Questiona ao usuário "yes" ou "no" sobre determinado algo.

    Args:
        QUESTION_P (str): Questionamento a ser feito.

    Returns:
        YES_NO_R (int): 1 - Yes; 0 - No.
    '

    if [ ${EZ_I_SKIP_ON_V} -eq 1 ] ; then
        return 0
    fi
    QUESTION_P=$1
    YES_NO_R=0
    read -r -p "$QUESTION_P (y/n) " RESP_V
    if [[ $RESP_V =~ ^([sS]|[yY])$ ]] ; then
        YES_NO_R=1
    elif [[ $RESP_V =~ ^([nN])$ ]] ; then
        echo "NO!"
        YES_NO_R=0
    else
        f_yes_no "$QUESTION_P"
    fi
}

# < --------------------------------------------------------------------------
