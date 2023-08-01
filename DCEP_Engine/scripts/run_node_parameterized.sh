#!/bin/bash
# first argument: port offset - the port numbers to be used (n, n+1, n+2)
# second argument: node name

[[ "$AZURE_STORAGE_CONN_STRING" =~ ';AccountName='[^\;]*';' ]] && \
  echo "Using AZURE_STORAGE_CONN_STRING with account "${BASH_REMATCH}
set -euo pipefail
# cd `dirname $0`

echo "$@"

INPUTFILE=$1

RECEIVEPORT=$2
SENDPORT=$(($2+1))
CRAPORT2=$(($2+2))

ME=`whoami | sed 's/[^a-zA-Z0-9]//g'`
SERVICENAME="adcep"${3}
NODENAME=$3


if ! which Ambrosia 2> /dev/null; then
    echo "'Ambrosia' not found."
    echo "You need Ambrosia on your PATH.  Please download an AMBROSIA binary distribution."
    exit 1
fi

if ! [ -e "DCEP.AmbrosiaNode.dll" ]; then
    echo "Build products don't exist."
    echo "Did you run ./build_dotnetcore.sh yet and run this script from the publish folder?"
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
# AMBROSIA_SILENT_COORDINATOR=TRUE
set -x
AMBROSIA_INSTANCE_NAME=$SERVICENAME AMBROSIA_IMMORTALCOORDINATOR_PORT=$CRAPORT2 \
COORDTAG=Coord$SERVICENAME AMBROSIA_IMMORTALCOORDINATOR_LOG=$slog  \
  runAmbrosiaService.sh dotnet $(realpath publish/DCEP.AmbrosiaNode.dll) $INPUTFILE --receivePort=$SENDPORT --sendPort=$RECEIVEPORT --serviceName=$SERVICENAME "$@"
set +x
