#!/bin/bash
BINFOLDER="$HOME/publish/bin"
IPS="$HOME/publish/IPs.txt"

function process {
	INFILE=$(realpath "$1")
	INDIR=$(dirname "$INFILE")
	ID=$(basename -s ".txt" "$INFILE")
	OUTDIR="$INDIR/results/$ID"
	shift 1
	for i in {0..9}; do
		ssh "pi$i" "mkdir -p $OUTDIR"
		ssh "pi$i" "rm -rf $BINFOLDER/benchmark\\\\ && ln -s $OUTDIR $BINFOLDER/benchmark\\\\"
		ssh "pi$i" "cd $BINFOLDER && (nohup $BINFOLDER/DCEP.Simulation $INFILE $* --nodeID $i --useIP6 --path $IPS --doBenchmarkTo CSV >$OUTDIR/$i.out 2>$OUTDIR/$i.err &)" &
	if [[ i -eq 1 ]]; then
		sleep 1;
	fi;
	done
}

for planfile in "$@";do
	process "$planfile" -w 1440 -d 5 -t Minute;
	sleep 10m;
	for i in {0..9}; do
		ssh "pi$i" "killall -w DCEP.Simulation"
	done
	sleep 5
done



