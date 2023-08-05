## How to start the cluster and event streams

1. Navigate to the raspberry_pi_cluster/java-cep directory and execute the following commands to start Flink CEP:

	- mvn package (compiles the project)

	- java -jar target/beispiel-1.0-SNAPSHOT.jar (starts the cluster waiting for the event streams to start)

	- abort using str+c

2. Navigate to the raspberry_pi_cluster/python directory to start the event stream, sockets etc.:

    - nohup python3.7 sender.py &
    
    - nohup python3.7 send_eventstream.py &
    
    - abort event stream using killall python3.7

