from hostedpi import PiCloud, Pi
from dotenv import load_dotenv
import os

with open("sm22-repro.pub", "r") as f:
    SSH_PUBKEY = f.read()

H = "inevrepro"

def get_pi(API: PiCloud, index :int) -> Pi :
    return API.pis[f"{H}{index}"]  # type:Pi

def provision(API: PiCloud, min=0, maxplus1=10):
     for i in range(min, maxplus1):
         pi = API.create_pi(f"{H}{i}", model=4, disk_size=20, ssh_keys={SSH_PUBKEY}, os_image="rpi-buster-armhf")

     for i in range(min, maxplus1):
         print(f"{i}: {API.pis[f'{H}{i}'].provision_status}")

    #create the IPs file
def generate_configuration_files(API: PiCloud, min : int, maxplus1 : int):
    with open("IPs.txt", "w") as IPFile:
        for i in range(min, maxplus1):
            pi = API.pis[f"{H}{i}"] #type:Pi
            IPFile.write(f"{i},{pi.ipv6_address}\n")

    #create local ssh config settings
    with open ("config-local", "w") as f:
        f.write("\nHost pi*\n"
                "IdentitiesOnly yes \n"
                "IdentityFile ~/.ssh/sm22-repro\n"
                "StrictHostKeyChecking accept-new\n")
        for i in range(min, maxplus1):
            pi = API.pis[f"{H}{i}"]  # type:Pi
            entry = pi.ipv4_ssh_config.replace(f"Host {H}", "Host pi")
            f.write(entry + "\n")


    with open ("config", "w") as f:
        f.write("\nHost pi*\n"
                "IdentitiesOnly yes \n"
                "StrictHostKeyChecking accept-new\n")
        for i in range(min, maxplus1):
            pi = API.pis[f"{H}{i}"]  # type:Pi
            entry = pi.ipv6_ssh_config.replace(f"Host {H}", "Host pi") + "\n"
            f.write(entry + "\n")

def unprovision(API: PiCloud, min :int, count : int):
    for i in range(min, min+count):
        print(f"Deprovisioning {i}")
        try:
            pi = API.pis[f"{H}{i}"]  # type:Pi
            print(pi.provision_status)
            pi.cancel()
        except Exception as e:
            print(e)

def main():
    load_dotenv()
    # Connect to Mythic Beasts API
    API = PiCloud(os.getenv("API_KEY"), os.getenv("API_SECRET"))  # type:PiCloud
    provision(API, 0, 10)
    generate_configuration_files(API, 0, 10)
    #unprovision(API, 0, 10)
if __name__ == '__main__':
    main()
