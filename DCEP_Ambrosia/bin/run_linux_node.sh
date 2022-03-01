#!/bin/bash
# first argument: port offset - the port numbers to be used (n, n+1, n+2)
# second argument: node name

# Clear logs for this demonstration.
#rm -rf ./ambrosia_logs/
#rm healthMonitorContinue.*
#rm *.log
#rm *.stackdump 

function EPHEMERAL_PORT() {
    LOW_BOUND=49152
    RANGE=16384
    while true; do
        CANDIDATE=$[$LOW_BOUND + ($RANDOM % $RANGE)]
        (echo "" >/dev/tcp/127.0.0.1/${CANDIDATE}) >/dev/null 2>&1
        if [ $? -ne 0 ]; then
            echo $CANDIDATE
            break
        fi
    done
}

[[ "$AZURE_STORAGE_CONN_STRING" =~ ';AccountName='[^\;]*';' ]] && \
  echo "Using AZURE_STORAGE_CONN_STRING with account "${BASH_REMATCH}
set -euo pipefail
# cd `dirname $0`

echo "run_linux_node.sh with args: $@"

RECEIVEPORT=$1
SENDPORT=$(($1+1))
CRAPORT2=$(($1+2))

ME=`whoami | sed 's/[^a-zA-Z0-9]//g'`
SERVICENAME="adcep"${2}
NODENAME=$2


if ! which Ambrosia 2> /dev/null; then
    echo "'Ambrosia' not found."
    echo "You need Ambrosia on your PATH.  Please download an AMBROSIA binary distribution."
    exit 1
fi

if ! [ -e "DCEP.AmbrosiaNode" ]; then
    echo "Build products don't exist."
    exit 1
fi

echo
echo "Node Starting, name $SERVICENAME"
echo "Running RegisterInstance with -i $SERVICENAME --rp $RECEIVEPORT --sp $SENDPORT -l "
set -x
Ambrosia RegisterInstance -i $SERVICENAME --rp $RECEIVEPORT --sp $SENDPORT -l "./ambrosia_logs/"
set +x

slog=`mktemp $SERVICENAME-coord.XXXX.log`

# removing the script arguments to pass on all remaining arguments
shift
shift

# AMBROSIA_SILENT_COORDINATOR=TRUE
set -x
AMBROSIA_INSTANCE_NAME=$SERVICENAME AMBROSIA_IMMORTALCOORDINATOR_PORT=$CRAPORT2 \
COORDTAG=Coord$SERVICENAME AMBROSIA_IMMORTALCOORDINATOR_LOG=$slog  \
  runAmbrosiaService.sh "$(realpath DCEP.AmbrosiaNode)" --receivePort=$SENDPORT --sendPort=$RECEIVEPORT --serviceName=$SERVICENAME "$@"
set +x 
