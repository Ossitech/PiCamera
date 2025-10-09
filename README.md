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
```python3
-m venv --system-site-packages env
```
This is necessary for picamera2 to work proberly because it depends
on some system packages.

Install the requirements from `requirements.txt` using pip
in your virtual environment:
```
pip install -r requirements.txt
```

Run the program:
```
python3 main.py
```

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