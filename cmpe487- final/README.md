Collaborated with @srknzl

![Screenshot1](./ss/1.png)
# Transporter ~ LAN video/group video chat, text chat application
* Use this application with ethernet in order to get good video and audio quality, this application is not intended for wifi. We tried optimizing wifi but due to packet losses we could not achive it.   
* How to use:
    * You can send message, start 1-1 video chat and attend to group video chats. In order to attend a group video chat you need to enter a group. Groups are stored locally so that when you quit the application your groups do not disappear.
    * In order to create or enter a group press 6 "Manage groups" in the main menu, then press enter 3 "enter/create a group", enter a name that is alphanumeric. That's it. 
    * You can see all the groups that are created by using all groups option in manage group options.
    * Once you are in a group you can attend a video chat in that group. 

* Note related to group storage:

    * Groups folder holds the currently attended groups. So please do not put a folder called groups in the same folder with main.py in order the application to work properly. 

## To run the program run main.py with python3
## 1.1. Dependencies

* gstreamer
* Python 3 (3.5 or later)
* notify-send


## System Requirements

* psmisc -> for killall command that we use to kill all gstreamer processes occasionally 
* gstreamer -> for streaming video and audio, also for rendering them.
* notify-send -> for visual notification of messages or app related information.


### Installation 
You can use our installation script to install all the dependencies at one shot: installation.sh 
### gstreamer Installation:

```
sudo apt install v4l-utils

sudo apt-get install libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio

sudo apt install gstreamer1.0-plugins-*
```

### notify-send Installation
```
sudo apt-get install libnotify-bin
```
### Possible problems related to missing libraries

* x264enc not found: 
```
sudo apt-get install gstreamer1.0-plugins-ugly
```
* avdev_h264 no element: 
```
sudo apt install gstreamer1.0-libav
```
