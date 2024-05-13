# Mythic Beasts Raspberry Pi provisioning tool

This script rents raspberry pis from the service provider mythic beasts (https://mythic-beasts.com).

## Prerequisites
 - Ubuntu 22.10 or similar (mac os with bash shell may also work)
 - Python 3 (`sudo apt install python3 python3-pip python3-venv`)
 - Credit card

## Setup
### Create and configure mythic beasts API key:
- Sign up for an account at https://mythic-beasts.com/user/login (Enter email, confirm it, enter details, log in.)
- Add a credit card under https://www.mythic-beasts.com/customer/payment-methods
- Generate a new api key at https://www.mythic-beasts.com/customer/api-users/create (Select only 'Rasperry Pi provisioning' at the bottom of the page. Click 'Create API Key'.)
- Add the API_KEY and th API_SECRET to the appropriate lines of the file `.env`

### Create a python virtual environment and install python modules to it:
  ```
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```
## Usage
### Provisioning (renting) Pis

Activate the python virtual environment:
```
source venv/bin/activate
```

Run `python provisionsPis.py`. This will generate three files:
- config-local (SSH configuration to access the raspberry pis remotely)
- config (SSH configuration for the PIs to reach one another)
- IPs.txt (contains IP addresses of the raspberry PIs)

Run install-generated-files.sh to copy these files to the appropriate locations within the project.

This will:
  - Copy config to ../deploy/.ssh/config.
  - Overwrite ../deploy/publish/IPs.txt and ../flink-experiment/IPs.txt with the IPs.txt

Configure your local ssh client to communicate with the PIs. 

  -  Add the key sm22-repro to your ~/.ssh folder
  -  Append the contents of config-local into your ssh configuration (usually ~/.ssh/config). 

	You can run setup-local-ssh.sh to attempt to do this automatically.

You can check that everything works with a loop such as

for i in {0..9};
	do ssh pi$i "echo $i ok"
done;

Mythic beasts sometimes fails to assign an IP address to a pi or two. In this case unprovisioning and reprovisioning will usually help.

Finally deactivate the python virtual environment to avoid interering with other local python programs:
```
deactivate
```

### Unprovisioning (cancelling) rented Pis

Comment out the line 'provision' and 'analyze' in the main() function of provisionPis.py, and uncomment the line begining with 'unprovision'. Then run the python script:

```
source venv/bin/activate
python provisionPis.py
deactivate
```

./setup-local-ssh.sh appends entries for "pi0" to "pi9" to the end of your ~/.ssh/config. You may want to delete these.
