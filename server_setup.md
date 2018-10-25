# Raspberry Pi Web Server Set Up

**Prerequisites** : You must have Raspbian or Raspbian Lite installed on your Raspberry Pi, and have it connected to the internet

1. **Download the setup folder to your Raspberry Pi**

2. **Move into the directory where you saved the setup folder**
     
    For example: *`cd /home/pi/setup`*

3. **Run the following command**
    *`sudo bash ./hotspotServerSetup`*

4. **The script will now start setting things up. Wait for it to do it's thing**

    * If you are connecting to your Pi over ssh, your connection will drop after *`Stopping dhcpcd`*, but everything is fine. Wait about a minute or so for the Pi to reboot itself

    * If you are connected to your Pi via HDMI and a keyboard/mouse, you should see all the messages from the script, and will know when it is finished.

5. **Once the script has finished, it will automatically reboot your Raspberry Pi**

6. **Everything should be setup and ready to go.**
  
    * You should be able to see an open wifi network called `solarSENSE` on your phone

    * You should be able to connect to that network, then type in `11.11.11.11` OR `solar.sense` and you should see the basic landing page.

    * Your Pi should still be able to connect to the previous wifi network AND be the solarSENSE hotspot at the same time
