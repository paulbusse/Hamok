# User documentation

requires python3-pycurl (apt)

## Introduction

This integration translates Ökofen heating systems into a set of MQTT 
entities and devices in a Home Assistant environment. 

Some high level functionality:
* Monitoring the system
* Changing some settings of the system

### Upfront remarks

I have not access to a complete system. I may not have access to all
the info in your system. If you have additional info, please create a 
ticket in github and I will look at it as soon as I can.

## Configuration

There are several configuration steps

## Connection to the Ökofen system

The following parameters must be:

* The ip-address of the system
* the JSON port
* the JSON password

## Which values you want to monitor

The list of values you want to monitor, depends

* on the appliances that you added to your system
* how the system is configured

The list of available monitors can be found by executing

```shell
$ okofenmqtt -l
```
This changes between systems, but the result should look like

```
system.L_ambient [sensor/enabled]
system.L_errors [sensor/disabled]
system.L_usb_stick [sensor/disabled]
system.L_existing_boiler [sensor/disabled]
hk1.L_roomtemp_act [sensor/disabled]
hk1.L_roomtemp_set [sensor/disabled]
hk1.L_flowtemp_act [sensor/enabled]
...
```
You need to list the name in the configuration file. The name is everything up to the first space. E.g. ```system.L_ambient```.

Between brackets the type of HA entity is shown that will be created
if you enable that monitor.

We use the following entity types:

* ```binary sensor```: this monitors an on/off state. An example is ```system.L_usb_stick```, which validates if the USB stick is present or not.
* ```sensor```: this monitors an more complex state. It can be numerical or a value list. An example is ```system.L_ambient```, which returns the outside temperature.
* ```switch```: this monitors an on/off state, but you can change the state. An example is ```ww1.heat_once```, which pushes the system to heat the warm water one single time outside the normal schedule.
* ```number```: this monitors a numerical state, but you can change the state. An example is ```hk1.temp_vacation```, which set the temperature when you are on holiday
* ```select```: this monitors a value list state, but you can change the state. An example is ```hk1.time_prg```, which determines which time program to use.

REMARK: it is possible that the system makes mistakes a select with 2 values for a switch. If that is the case please let us know.
  
For more information on these entity types please look at the HA documentation for [MQTT discovery](https://www.home-assistant.io/docs/mqtt/discovery/)