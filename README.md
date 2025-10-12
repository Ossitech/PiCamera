# PiCamera
Portable pi camera projekt with pygame UI for camera settings.
This projects aims to provide a simple and usable camera app
providing a user interface
for touch screens on a raspberry pi using the raspberry pi HQ camera module.

## Motivation
With the HQ camera module you can take actually good photos.
These of course can't be compared to pictures taken with
professional equipment but they can be compared
to pictures taken with a smartphone. The HQ camera additionally provides
a lot of configuration options, which many smartphones don't have.
And it also has the ability to use a range of different optics.
The control over the whole process of taking a picture
is quite unique using this setup and it enabled me to
quickly learn how a digital camera works and how
the resulting picture is influenced by the many
parameters the camera module and the optic provides.

## Installation
Clone the repo onto your Raspberry Pi and create a python virtual environment using
the system site packages:
```
python3 -m venv --system-site-packages venv
```
This is necessary for picamera2 to work proberly because it depends
on some system packages.

Install the requirements from `requirements.txt` using pip
in your virtual environment:
```
venv/bin/pip install -r requirements.txt
```

Run the program:
```
venv/bin/python3 main.py
```

## Usage
The python program creates a fullscreen window that shows the
camera preview with the current camera configuration.
To take a picture, press the physical photo button on the camera
or tap the photo button in the top right corner of the screen.
After a picture is taken, the resulting image is shown
on screen for 5 seconds.
To change configuration parameters of the
camera module tap the menu button
in the top left corner.
The menu shows multiple buttons that lead
to sub menus.
This enables the user to change paramters like
ISO value, exposure time and color gains.
Taken pictures are saved with the current time stamp as file name.
The output directory can by changed by changing
the value of ```PHOTOS_PATH``` in ```camera.py```

### Example pictures
These where taken during the development process.
I added the settings the picture where taken with.
![image_1](example%20pictures/winter_landscape.jpg)
ISO: auto, exposure: auto, color gains: auto

![image_2](example%20pictures/winter_cabin.jpg)
ISO: auto, exposure: auto, color gains: auto

![image_3](example%20pictures/leaves.jpg)
ISO: 100, exposure: auto, color gains: red 2.0, blue 2.7

![image_4](example%20pictures/heart.jpg)
ISO: 100, exposure: 2 seconds, color gains: red 2.0, blue 3.0

![image_5](example%20pictures/fall.jpg)
ISO: auto, exposure: auto, color gains: red 2.0, blue 2.7

![image_6](example%20pictures/door.jpg)
ISO: auto, exposure: auto, color gains: red 2.0, blue 2.7

## Hardware
### Lens
For this project I am currently using the official Raspberry Pi
high quality camera module with a zoom lens.
This lens has 3 rotating rings, which control
focus, aperture and zoom.
The HQ camera has an adapter ring installed by default.
This ring can be turned to change the distance
between the sensor and the lens.
This was very importand for my specific lens
because the distance to the sensor
defines the range in which the focus can be changed
on the lens.
After trying around I found a position
where I could focus the image with both low
and high zoom.

### Raspberry Pi
I am using a Raspberry Pi 4 with 4GB of ram.
My specific Raspberry has lost its SD-Card slot,
so I had to design and 3d print an SD-Card holder
that could be screwed onto the underside of the Pi
to hold the SD-Card in place, on which the OS is stored.
This of course won't be necessary for others
but it had to be considered while designing the camera housing.

### Screen
The screen is a touch screen with a resolution of 800 x 480 pixels.
It is powered using a USB-C cable and driven via a short HDMI cable.
The USB-C power cable is plugged into one of the Pis USB ports.
It doubles as a data connection to the Pi, through which
the touch screen interface is driven.
This screens default rotation is vertical but I needed it
to work horizontally. To correct this
the screen orientation had to be changed
in the raspi config file located in /boot.
I will add the correct entry that worked for me to this readme later.

### Hardware buttons
For taking pictures I added a hardware button that is connected to
GPIO pin 40.
Originally I had planned to add a rotary encoder as an
alternative way of navigating the menus on the screen.
But this turned out to be much harder than I thought,
so I skipped this part for the moment.
The screen also has 3 buttons for turning
it on and off and for controlling the brightness of the display.
These buttons need to be accessible for the user.

### Providing power
As of now I did not find a good solution yet.
I am currently just using a power bank and
a USB-C cable to provide power to the Pi.
I plan to integrate a battery with a
battery management system into the camera housing in the future.

### Housing the parts
Currently I have the Pi, screen and button
inside a 3d printed housing.
The camera module is attached to the front and
the ribbon cable goes through a small slit.
I already found someone that will help
me design a much better housing,
that will look nice and be much more ergonomic.
Once this is done, I will provide pictures and
files of the design.
The design needs to incorporate:
+ the screen
* the Raspberry pi
* a mounting point for the HQ camera module
* a hole or slit to pass the camera ribbon cable through
* the button for taking pictures
* a way of reaching the buttons on the touch screen module
* the battery and USB-C port of the BMS

Additional stuff:
* At least one USB port of the Raspberry Pi should be accessible from the outside.
* The tripod mount on the HQ camera module should still be usable.
This would eliminate the need for a dedicated tripod mount.
* Any indicator lights on the BMS should be visible to the user.