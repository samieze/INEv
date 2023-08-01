# DCEP Engine
Light-Weight Distributed Complex Event Processing Engine.



## Run

Our distributed query processor can be started using the follwing command from inside the directory `/bin` to run query *Q1* of our case study:

`../bin/DCEP.Simulation ../inputexamples/google_cluster/Q1_doubleUpdate/Q1_doubleUpdate.txt -t Minute -w 30 -d 10 --name doubleUpdate > output.txt`

The last lines of the created file `output.txt` contain the totally generated primitve events and projections, as well as number of events sent.
Input files for the distributed query evaluation using our DCEP engine can be generated within the `../INEv` folder.

#### Parameters

The most important parameters of our distributed query processor are given in the following table:

Parameter | Meaning
------------ | -------------
-t| Required. The time unit events will be generated at rate (n events / time unit).
 -w | Required. The global time window in which event components must occur to trigger a match. The time unit is specified with -t.
-d |  Optional. The execution duration of the simulation. Per default it wil run indefinitely. If set to a value, the number of exchanged events within the time period will be measured and eventually printed to stdout. The time unit is specified with -t.
-v | Optional. The event output rate variance as a percentage of the total output rate.
-s | Optional. The event output rate variance seed.
-f | Optional. The factor each event output rate is multiplied with.
--doBenchmarkTo | Optional. Set to 'CSV' to write performance metrics into the /out/benchmark/ directory.
--name | Required. Used as a custom identifier for benchmark file names in /out/benchmark/.


### Case Study Parameters

- Citi Bike: -w 1440 -t Minute (corresponds to 24h time window defined in Citi Bike Queries)
- Google Cluster: -w 30 -t Minute (corresponds to 30 minute time window in Google Cluster Queries)

