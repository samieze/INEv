# DCEP Ambrosia
Distributed Complex Event Processing with Microsoft Ambrosia

## Related Links
- https://github.com/microsoft/AMBROSIA

## Run

The distributed query processor can be used within a simulation and with Ambrosia.


### using Ambrosia
Running our distributed query processor with Ambrosia requires a full installation and setup of Ambrosia as described in https://github.com/microsoft/AMBROSIA.
More concretely, we recommend running the **hello world** example (https://github.com/microsoft/AMBROSIA/tree/master/Samples/HelloWorld) first before starting DCEP-Ambrosia.

Before the DCEP Ambrosia engine can be started, the connection string from the Azure account must be exported. To do this, you have to login into your Azure account, click on the previously created storage account and then click on "Access keys". The connection string must then be copied and exported within the command line using the command "export". Make sure that the part after AZURE_STORAGE_CONN_STRING=".." is put in quotation marks, i.e.,

`export AZURE_STORAGE_CONN_STRING="DefaultEndpointsProtocol=https;AccountName=ExampleUser;AccountKey=AOSIDJiojsad48nj34EKMRkxBaQPW0Puy14mk32m4nvmPZ1y/6Ohx8lzE124ok4116Vm0L3d/M941BPyTo412nj4A==;EndpointSuffix=core.windows.net"`

To start the Ambrosia implementation for 20 nodes using the input example `Q1_douleUpdate.txt`, run the following command from inside the directory `/bin`:

`../bin/run_all_linux.sh ../inputexamples/google_cluster/Q1_doubleUpdate/Q1_douleUpdate.txt -t Minute -w 30 -d 10 > output.txt`

The last lines of the created file `output.txt` contain the totally generated primitve events and projections, as well as number of events sent.

### using Simulation

Likewise, our distributed query processor can be started as a simulation using the follwing command from inside the directory `/bin`:

`../bin/DCEP.Simulation ../inputexamples/google_cluster/Q1_doubleUpdate/Q1_douleUpdate.txt -t Minute -w 30 -d 10 > output.txt`

The last lines of the created file `output.txt` contain the totally generated primitve events and projections, as well as number of events sent.

#### Parameters

The most important parameters of our distributed query processor are given in the following table:

Parameter | Meaning
------------ | -------------
-t| Required. The time unit events will be generated at rate (n events / time unit).
 -w | Required. The global time window in which event components must occur to trigger a match. The time unit is specified with -t.
-d |  The execution duration of the simulation. Per default it wil run indefinitely. If set to a value, the number of exchanged events within the time period will be measured and eventually printed to stdout. The time unit is specified with -t.


### How to build
- Before building the project, install the .NET SDK version 5.0.404.

To build this project, the script `../scripts/build_dotnetcore.sh` needs execution permissions (e.g., using Linux `cd ../scripts` and `chmod +x build_dotnetcore.sh`). Afterward, the script must be run from the main directory:

`cd ../DCEP Ambrosia` and type `./scripts/buildotnet_core.sh`.

After the project has been built successfully, a `/publish` folder is created in the directory that contains two folders, `/bin` and `/inputdata`. Inside the `/bin` folder are all files needed to run the engine, and inside `/inputdata` are all input files. Now, the engine can be started using the following command:

`../publish/bin/DCEP.Simulation ../inputexamples/google_cluster/Q1_doubleUpdate/Q1_douleUpdate.txt -t Minute -w 30 -d 10 > output.txt`


### Case Study Parameters

- Citi Bike: -w 1440 -t Minute (corresponds to 24h time window defined in Citi Bike Queries)
- Google Cluster: -w 30 -t Minute (corresponds to 30 minute time window in Google Cluster Queries)

