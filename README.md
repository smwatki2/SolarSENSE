# SolarSENSE

This project aims to help farmers by providing the necessary information that will enable them to adapt their farming behaviors to the changing climactic conditions, finding the right balance between high yields and low environmental impact. More specifically, this will be done by providing farmers with valuable data from soil sensors to boost their yields while accurately identifying correct levels
of fertilizers and water needs.

Existing commercial soil sensors were developed for large agricultural concerns (for “big ag”) and require internet connectivity, cloud-based solutions,and on going subscription fees (at rates of thousands of dollars per month). Rural small-scale farms are challenged with lack of networks, electric power, and the extremely high cost of these commercial solutions. 

## Setup
### Hardware Setup

If you have access to a Raspberry Pi SolarSENSE Server, then you can follow the instructions given in the GitHub repo [rpi-clone](https://github.com/billw2/rpi-clone.git)

If you are setting up this project without a pre-existing pi, you will need the following:
1. Raspberry Pi 3
2. 32GB+ SD Card

Download the latest version of [Raspbian Stretch Lite](https://www.raspberrypi.org/downloads/raspbian/)
Follow the instructions on [Raspberry Pi's website](https://www.raspberrypi.org/documentation/installation/installing-images/README.md) to install the image to the SD card

After successfully writing the image to the SD card, insert the SD card into the Raspberry Pi and provide power. If you plan to connect to the Raspberry Pi without a monitor, mouse and keyboard, please reinsert the SD card back into your own computer and open the boot drive on the SD card. In the boot drive, create a new file named `ssh`. Also create a second file called `wpa_supplicant.conf`. Edit this `conf` file to contain your Wi-Fi information according to [this site](https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md). Once done, eject the SD card and insert it back into the Raspberry Pi

### Software Setup

Once Raspbian Lite is installed, run the following command to install `git`:

```bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install git
```

Once completed, run the command `git clone https://github.com/smwatki2/SolarSENSE.git`

When the clone has completed, enter the `SolarSENSE` folder and execute the setup script with this command: 

`sudo bash setup_script`

This script will install the necessary python packages, setup the WiFi hotspot for access to the server, and initialize the backend database. This script may take several minutes and will also reboot at the end of the script.

At this point, your Raspberry Pi is setup and ready to go! To access the SolarSENSE platform, simply type `11.11.11.11` in any web browser and begin monitoring your farm/garden

---

*This is a Capstone Project done by ASU seniors during the 2018-2019 School Year*
