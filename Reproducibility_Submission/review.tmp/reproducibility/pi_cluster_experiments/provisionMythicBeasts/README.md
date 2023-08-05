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

### Create and activate virtual environment: 

- ```python3 -m venv venv```
- ```source venv/bin/activate```
### Install python modules to virtual environment: 

- ```pip install -r requirements.txt```


## Usage

### Provisioning (renting) Pis
Run provisionsPis.py. This will generate three files:

- config-local (SSH configuration to access the raspberry pis remotely)
- config (SSH configuration for the PIs to reach one another)
- IPs.txt (contains IP addresses of the raspberry PIs)

Add the key sm22-repro to your ~/.ssh folder.

Copy the contents of config-local into your ssh configuration (by default at ~/.ssh/config).

Copy config to ../deploy/.ssh/config.

### Unprovisioning (cancelling) rented Pis

Comment out the line 'provision' and 'analyze' in the main function and comment 'unprovision', then run the script.
