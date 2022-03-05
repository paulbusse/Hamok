# Deployment

You need:

- Home assistant
- An MQTT broker like ```mosquitto```
- Of course an Ökofen system

## Step 1: Download the source

Yep at this point in time you have to download the source. This can be done by cloning the repository or by downloading the zip file from the repository. If you don't know how to do the first, I'll explain the second:

1.  Go to the repository: [paulbusse/hamok](https://github.com/paulbusse/Hamok)
2.  Click on the green button ```code```
3.  Select ```Download ZIP```
4.  You should have a file ```hamok-main.zip```. Move it to a directory where you want it to reside and unpack the code there

I run hamok on the raspberry pi that also runs HA, mosquitto and a couple of other things.

## Step 2: Configuration


We suppose that you have a device on which you run HA. I run my MQTT broker on the same machine.
