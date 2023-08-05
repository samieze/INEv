#!/bin/bash
BASE_DIR=$(realpath "$(dirname "$0")") #directory where this script is
JAVA_DIR="$BASE_DIR/java-cep"
JAVA_TARGET_DIR="$JAVA_DIR/target"
PY_DIR="$BASE_DIR/python"
JAR="$JAVA_DIR/target/beispiel-1.0-SNAPSHOT.jar"

N_NODES=10

generateConfig() {
    # substitute nodeX in IPCONFIG/config.json by IP adress of piX
    prev_workdir="$(pwd)"
    cd "$BASE_DIR" || exit 1
    python3 setConfig.py
    cd "$prev_workdir" || exit 1
}

compile() {
        prev_workdir="$(pwd)"
        cd "$JAVA_DIR" || exit 1
        mvn clean package || exit 1
        cd "$prev_workdir" || exit 1
}

node() {
	echo "pi$(($1))"
}

install () {
  for ((i=0; i<10; i++)); do
	  #delete everything on the remote
	  ssh "$(node "$i")" "rm -rf flink_experiments"

	  #create folder on the remote
	  ssh "$(node "$i")" "mkdir -p flink_experiments/java-cep"

	  #copy JAR
	  scp "$JAR" "$(node "$i"):~/flink_experiments/java-cep/cep-node.jar"

	  #copy config.json (contains ip addresses, etc) to same folder as JAR
      scp "$BASE_DIR/IPCONFIG/config.json" "$(node "$i"):~/flink_experiments/java-cep/"

	  #copy conf folder (contains flink-config.yaml) to same folder as JAR
      scp -r "$JAVA_DIR/conf" "$(node "$i"):flink_experiments/java-cep/"

      #contains python sender and inputfiles and config.json
   	  scp -r "$PY_DIR/" "$(node "$i"):flink_experiments/" 	

 	  scp "$BASE_DIR/IPCONFIG/config.json" "$(node "$i"):flink_experiments/python"
  done;
}

run() { 
	for query in 1 2 3 4; do
	    #start everywhere
        for ((i=0; i<N_NODES; i++)); do
	        echo "starting $i"
            REMOTE_CMD="cd flink_experiments/java-cep && nohup java -Xmx256M -jar cep-node.jar $query config.json $i >../run_$i""_$query.log 2>../run.err &"
	        ssh "$(node "$i")" "$REMOTE_CMD" &
  	    done;
	    sleep 60;

	    #check that all processes are running
      	for ((i=0; i<N_NODES; i++)); do
		    if ! ssh "$(node "$i")" "pgrep java >/dev/null"; then
			    echo "cep not running on node $i"
			    exit 1
		    fi
	    done

	    #start input srcs
      for ((i=0; i<N_NODES; i++)); do
		    echo starting inputs on "$i"
		    ssh "$(node "$i")" "cd flink_experiments/python && nohup python3 send_eventstream.py $query $i >../py.log 2>../py.err &" & 
	    done

	    #wait for process termination
      sleep 5h
      kill_processes
  done
}

collect_results() {
   mkdir -p "results_flink"
   for ((i=0; i<N_NODES; i++)); do
        #copy results		
        scp "$(node "$i"):flink_experiments/run*log" "./results_flink/"
  done
}

kill_processes() {
  for ((i=0; i<N_NODES; i++)); do
		echo "TERM $i"
	  ssh "$(node "$i")" "killall -q -w java"
      ssh "$(node "$i")" "killall -q -w python3"
  done;
}
