# SolarSENSE

This project aims to help farmers by providing the necessary information that will enable them to adapt their farming behaviors to the changing climactic conditions, finding the right balance between high yields and low environmental impact. More specifically, this will be done by providing farmers with valuable data from soil sensors to boost their yields while accurately identifying correct levels
of fertilizers and water needs.

Existing commercial soil sensors were developed for large agricultural concerns (for “big ag”) and require internet connectivity, cloud-based solutions,and on going subscription fees (at rates of thousands of dollars per month). Rural small-scale farms are challenged with lack of networks, electric power, and the extremely high cost of these commercial solutions. 

## [Setup](#setup)
### [Hardware Setup](#hardware-setup)
If you have access to a Raspberry Pi SolarSENSE Server, then you can follow the instructions given in the GitHub repo [rpi-clone](https://github.com/billw2/rpi-clone.git)

If you are setting up this project without a pre-existing pi, you will need the following:
1. Raspberry Pi 3
2. 32GB+ SD Card

Download the latest version of [Raspbian Stretch Lite](https://www.raspberrypi.org/downloads/raspbian/)
Follow the instructions on [Raspberry Pi's website](https://www.raspberrypi.org/documentation/installation/installing-images/README.md) to install the image to the SD card

After successfully writing the image to the SD card, insert the SD card into the Raspberry Pi and provide power. If you plan to connect to the Raspberry Pi without a monitor, mouse and keyboard, please reinsert the SD card back into your own computer and open the boot drive on the SD card. In the boot drive, create a new file named `ssh`. Also create a second file called `wpa_supplicant.conf`. Edit this `conf` file to contain your Wi-Fi information according to [this site](https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md). Once done, eject the SD card and insert it back into the Raspberry Pi

### [Software Setup](#software-setup)
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

## [Contributing](#contributing)
Our team uses [Taiga](https://taiga.io/) for our Sprints and Issue tracking. [SolarSENSE Taiga board](https://tree.taiga.io/project/kevinjhale-ser401-fall-2018-solarsense-off-grid-soil-sensors/timeline)

### [Taiga Process:](#taiga-process)
Sprints are generally 2 weeks long as time and meeting schedules with the project sponsor permits. As the sprint is in progress, team members file issues and ehancements in Taiga's built-in Issue Tracker. During Sprint planning select issues are promoted to User stories and tasks are assigned and point values are given. Each Sprint should have at least 6 tasks per developer in the sprint.

### [Github Process:](#github-process)
Create a new branch based on the User Story number from the Taiga process following this naming convention:
`US###_description_of_user_story` where you replace `###` with the respective User Story number from Taiga

Once all of the tasks for the User Story have been committed, a pull-request to `dev` can be made. The pull-request must must be reviewed as stated in the section below, [Code Reviews](#code-reviews).

### [Code Reviews:](#code-reviews)
The code should be reviewed informally by at least one team member other than the team member(s) that participated in writing the code. These code reviews will take place online through the GitHub pull request review area. Comments and fixes will be discussed here. All code should be reviewed before merging into the master or development branches.

---

*This is a Capstone Project done by ASU seniors during the 2018-2019 School Year*
