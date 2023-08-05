#!/bin/bash
# first argument: port offset - the port numbers to be used (n, n+1, n+2)
# second argument: node name

# Clear logs for this demonstration.
rm -rf ./ambrosia_logs/
rm healthMonitorContinue.*
rm *.log
rm *.stackdump 

[[ "$AZURE_STORAGE_CONN_STRING" =~ ';AccountName='[^\;]*';' ]] && \
  echo "Using AZURE_STORAGE_CONN_STRING with account "${BASH_REMATCH}
set -euo pipefail
# cd `dirname $0`

echo "$@"

RECEIVEPORT=$1
SENDPORT=$2
CRAPORT2=$3

ME=`whoami | sed 's/[^a-zA-Z0-9]//g'`
SERVICENAME="adcep"${4}
NODENAME=$4


if ! which Ambrosia 2> /dev/null; then
    echo "'Ambrosia' not found."
    echo "You need Ambrosia on your PATH.  Please download an AMBROSIA binary distribution."
    exit 1
fi

if ! [ -e "../../bin/DCEP.AmbrosiaNode" ]; then
    echo "Build products don't exist."
    exit 1
fi

echo
echo "Node Starting, name $SERVICENAME"
echo
set -x
Ambrosia RegisterInstance -i $SERVICENAME --rp $RECEIVEPORT --sp $SENDPORT -l "./ambrosia_logs/"
set +x

slog=`mktemp $SERVICENAME-coord.XXXX.log`

# removing the script arguments to pass on all remaining arguments
shift
shift
shift
shift
# AMBROSIA_SILENT_COORDINATOR=TRUE
set -x
AMBROSIA_INSTANCE_NAME=$SERVICENAME AMBROSIA_IMMORTALCOORDINATOR_PORT=$CRAPORT2 \
COORDTAG=Coord$SERVICENAME AMBROSIA_IMMORTALCOORDINATOR_LOG=$slog  \
  runAmbrosiaService.sh ../../bin/DCEP.AmbrosiaNode --receivePort=$SENDPORT --sendPort=$RECEIVEPORT --serviceName=$SERVICENAME "$@"
set +x 