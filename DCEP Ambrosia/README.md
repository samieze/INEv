# DCEP Ambrosia
Distributed Complex Event Processing with Microsoft Ambrosia

## Related Links
- https://github.com/microsoft/AMBROSIA

## Run

The distributed query processor can be used within a simulation and with Ambrosia.


### using Ambrosia
Running our distributed query processor with Ambrosia requires a full installation and setup of Ambrosia as described in https://github.com/microsoft/AMBROSIA.
More concretely, we recommend running the **hello world** example (https://github.com/microsoft/AMBROSIA/tree/master/Samples/HelloWorld) first before starting DCEP-Ambrosia.

To start the Ambrosia implementation for 20 nodes using the input example `Filter_doubleUpdate.txt`, run the following command from inside the directory `/bin`:

`../bin/run_all_linux.sh ../inputexamples/queries_google_cluster/DoubleUpdate/Filter_doubleUpdate.txt -t Minute -w 30 -d 10 > output.txt`

The last lines of the created file `output.txt` contain the totally generated primitve events and projections, as well as number of events sent.

### using Simulation

Likewise, our distributed query processor can be started as a simulation using the follwing command from inside the directory `/bin`:

`../bin/DCEP.Simulation ../inputexamples/queries_google_cluster/DoubleUpdate/Filter_doubleUpdate.txt -t Minute -w 30 -d 10 > output.txt`

The last lines of the created file `output.txt` contain the totally generated primitve events and projections, as well as number of events sent.

#### Parameters

The most important parameters of our distributed query processor are given in the following table:

Parameter | Meaning
------------ | -------------
-t| Required. The time unit events will be generated at rate (n events / time unit).
 -w | Required. The global time window in which event components must occur to trigger a match. The time unit is specified with -t.
-d |  The execution duration of the simulation. Per default it wil run indefinitely. If set to a value, the number of exchanged events within the time period will be measured and eventually printed to stdout. The time unit is specified with -t.

