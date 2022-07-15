#!/bin/bash
[[ "$AZURE_STORAGE_CONN_STRING" =~ ';AccountName='[^\;]*';' ]] && \
  echo "Using AZURE_STORAGE_CONN_STRING with account "${BASH_REMATCH}
set -euo pipefail
#cd `dirname $0`

INPUTFILE=$1
INPUTPATH=$(realpath $INPUTFILE)

shift

# Count the number of nodes as in the number of lines in the input file before a - (dash) characters 
NODECOUNT=$(($(sed -n '0,/-/p'  $INPUTPATH | wc -l)-1))

echo "Will now lauch $NODECOUNT nodes on this machine..."
echo "Notice: This script will run indefinitely, even though AmbrosiaDCEP might have terminated already."
echo "Notice: AmbrosiaDCEP processes are independent and may need to be terminated manually."

for i in $(eval echo {0..$((NODECOUNT-1))})
do
   echo "Launching Node $i..."
   ./run_linux_node.sh $((30100+$i*3)) $i $INPUTFILE "$@" &

done

#50100

sleep 10d
 
