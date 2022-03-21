# User documentation

Version: 22.4

[TOC]

## Introduction

This integration translates Ökofen heating systems into a set of MQTT
entities and devices in a Home Assistant environment.

Some high level functionality:
* Monitoring the system
* Changing some settings of the system

## The `hamok` command

Command line options

| Option                    | Description                                                  |
| ------------------------- | ------------------------------------------------------------ |
| `-h` or `--help`          | prints a help page with a short description of each of the options |
| `-c` or `--config` <file> | Specify the configuration file. This option is mandatory except with the help option |
| `-p` or `--print`         | Prints the configuration that will be used. It includes all the defaults. This option is there for debugging purposes. The process will exit after the printing the configuration. |
| `-l` or `--list`          | Prints a list of all available entities for your system and exits. See below in the configuration section how this is useful. |

Examples:

```bash
$ hamok -h # print the help message
$ hamok -c <configfile> # starts the process
$ hamok -p -c <configfile> # prints the configuration that would be used if the process is started
$ hamok -l -c <configfile> # list all available entities
```

## Which values you want to monitor

The list of values you want to monitor, depends

* on the appliances that you added to your system
* how the system is configured

The list of available monitors can be found by executing

```shell
$ hamok -l -c configfile
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
The output shows

* The name of value that can be monitored.
* The type of entity that will be created when this value is monitored. See below for a list of types.
* Whether or not that value appears in the list of monitored values in the configuration file.

We use the following entity types:

* ```binary sensor```: this monitors an on/off state. An example is ```system.L_usb_stick```, which validates if the USB stick is present or not.
* ```sensor```: this monitors an more complex state. It can be numerical or a value list. An example is ```system.L_ambient```, which returns the outside temperature.
* ```switch```: this monitors an on/off state, but you can change the state. An example is ```ww1.heat_once```, which pushes the system to heat the warm water one single time outside the normal schedule.
* ```number```: this monitors a numerical state, but you can change the state. An example is ```hk1.temp_vacation```, which set the temperature when you are on holiday
* ```select```: this monitors a value list state, but you can change the state. An example is ```hk1.time_prg```, which determines which time program to use.

For more information on these entity types please look at the HA documentation for [MQTT discovery](https://www.home-assistant.io/docs/mqtt/discovery/)

Note that you although HA will allow you to change the states of switch, number and select, those changes will not trickle through to the Ökofen system (yet). This is under development.

For sensors with numeric values, like temperatures and power values, the data sent to HA will have one decimal digit, if this is provided by the Ökofen system.

## Naming

### HA Entity names

The entity name defined by Hamök and sent to HA to create new entities consists of 3 components, joined by an underscore :

* the device name, as taken from the [configuration file](#configuration-file). The name is taken as it stands. If this causes HA to refuse the name, that is for you to fix.
* the sub-system name. The Ökofen system exists out of a set of sub-systems each with a name determined by Ökofen. These Ökofen names read `hk1`or `pe1`. You can name these sub-systems yourself in the Ökofen interface e.g. `hk1` may become `ground floor`. By preference the name entered by the user will be taken, if not we take the Ökofen name. In the user provided name all characters. All characters that are not letters or numbers, so also spaces, will be replaced by '_' (underscores)
* The name of the value. Ökofen indicates read-only values by preceding them by 'L_'. Hamök removes that prefix.

An example of HA entity name is then

```
oekofen_ground_floor_roomtemp_act
```

### MQTT Topics

We follow the HA guidelines here. 

MQTT topic names have 4 components

* the first is `homeassistant`
* the second is the entity type. This is explained in the section [Which values you want to monitor](#which-values-you-want-to-monitor).
* the third is the HA entity name as described above.
* the fourth is the message type:
  * `config`: contains the latest definition of the HA entity. Messages here are send in retain mode
  * `state`: contains the latest value for the entity. Messages here are send in retain mode
  * `cmd`: is the topic where HA publishes changes to the Hamök on.

```
homeassistant/switch/oekofen/oekofen_ww1_heat_once/state
```

### Changing names

Changing names has effect on what you see in HA.

If you change the Ökofen component name (these are case insensitive):

* the MQTT topic queue changes
* The HA entity name changes
* The default friendly name for the entity name changes

If you change the `device` configuration setting:

* the MQTT topic queue changes
* The HA entity name changes
* The default friendly name for the entity name changes
* the internal ID for the HA entity changes: HA will consider this a new entity.

When the MQTT topic changes HA may get confused and show errors like

```
Platform mqtt does not generate unique IDs. ID oekofen_system_L_usb_stick already exists - ignoring binary_sensor.oekofen_system_usb_stick
```

This usually means that there are 2 MQTT topics trying to create devices with the same ID. It means that you have to cleanup the retained MQTT messages. 

The preferred way, to do is to remove the unneeded topics. Install a tool like [MQTT Explorer](http://mqtt-explorer.com/) and find the topics causing the issue and remove them. If you remove one to many, do not worry, restart hamok and they will reappear.

```bash
$ sudo systemctl restart hamok
```

## HA configuration

We try to do as much as we can in Hamök to avoid changes in HA. However, we believe that Home Assistant is good at what it does. So, whatever that can be done in HA, should be done in HA. I'm well aware that Hamök is not where it needs to be on this point. Improvements can be expected in the future.

Some remarks

* In the MQTT configuration, we do not care about birth and will messages. Note that other MQTT integrations may care.
* You can assign friendly names to your entity, we do not override them from Hamök.
* If you want to set the area, you can do this on the device instead of every individual entity.

## Configuration file

The configuration file is a YAML file. Which means that indentation is important. Here is an overview of the configuration file.

Besides these values, other keys may be entered in the configuration file but they will be ignored, silently.

**MQTT broker and port**

The MQTT broker and port are specified as sub-keys to the an `mqtt` key. The broker specifies the host on which the MQTT broker runs. The broker must be specified otherwise the system won't start.

If the broker does not listen on the standard port, 1883, you can specify the port here.

```yaml
mqtt:
  broker: 192.168.1.100
  port: 1883 # optional
```

**Ökofen JSON setup**

For the Ökofen set up, you need 3 items

* The IP address of the system
* The JSON port
* The JSON password

On the Ökofen console,

* Tap on the 9 dot icon
* Use the arrows to go all the way down
* Tap `General`(`Algemeen` in Dutch) and use the arrows again to down
* There you will find `IP config`
* The top line gives you the IP-address
* Scroll down until you see a box `JSON mode`.
* Make sure the `JSON mode` is on. Turn it on if necessary.
* Copy the values for JSON port and JSON password.

The configuration looks like

```yaml
oekofen:
  host: 192.168.1.200
  jsonport: 1234
  jsonpassword: abcd
```

**Monitored entities**

This is a list of names that you get by executing

```shell
$ hamok -l -c configfile
```

The list must contain at least one element for the process to start. For more information, see [this section](#which-values-you-want-to-monitor).

```yaml
monitor:
  - system.L_ambient
  - hk1.L_flowtemp_act
```

**Time between measurements**

You can specify the time between 2 communications with the Ökofen system. The value is the number of seconds between two requests. The default value is 60 seconds.

The value must be between 1 and  86400 (1 day) and not contain any characters. If an illegal value is configured, the default value is used.

```yaml
interval: 120 # 2 minutes
```

Note that values are not updated in HA until they change.

**Device name**

Hamök will create a single the device. The name of this device is specified here. The default value is `Oekofen`. If you want to monitor multiple Ökofen systems with a single HA instance, you must run multiple instances of Hamök, each with a unique device name. Otherwise, they will appear as the same device.

If an empty value is specified, the default value will be used.

```yaml
device: newyork
```

NOTE: changing the device name also changes the internal id for Home Assistant. This means that new sensors will be defined and the old ones won't be usable.

**Client Identifier**

Hamök will connect with the MQTT broker using this ID. It must a valid MQTT Client ID. The default value is `hamok` We take the restrictive approach to the standard:

* Between 1 and 23 characters long
* Containing only small and capital latin letters and numbers \[a-z]\[A-Z][0-9].

Some servers may support other character sets and other lengths, but that is not supported.

Changing the clientid is only needed when you want to support multiple Ökofen systems on the same MQTT broker and HA. You must run one instance of Hamök per Ökofen instance each with a unique clientid.

```yaml
clientid: hamoknewyork
```

**Logging**

Hamök has 3 logging modes.

| mode    | description                                                  |
| ------- | ------------------------------------------------------------ |
| default | This is also the default value. Logging is only sent to syslog. Only messages of severity info or higher will be printed. |
| debug   | This is similar to default except that messages of severity debug and higher will be printed |
| devel   | This is similar to debug, except that messages will also be printed on the screen. |

```yaml
logger: debug
```



**<u>Overview</u>**

| key                    | default   | description                                                  |
| ---------------------- | --------- | ------------------------------------------------------------ |
| `mqtt.broker`          | -         | Mandatory field. Host where the MQTT broker runs             |
| `mqtt.port`            | 1883      | Port on which the MQTT broker listens.                       |
| `oekofen.host`         | -         | Mandatory field. IP address of the Ökofen system. This may be a host name if that works for you |
| `oekofen.jsonport`     | -         | Mandatory field. The JSON port retrieved from the Ökofen system. |
| `oekofen.jsonpassword` | -         | Mandatory field. The JSON password retrieved from the Ökofen system |
| `monitor`              | -         | Mandatory field. A list of values to monitor. Must contain at least one value. |
| `interval`             | 60        | The number of seconds between 2 requests. A value between 1 and 86400. |
| `device`               | `Oekofen` | The name of the created device.                              |
| `clientid`             | `hamok`   | The clientid used with the MQTT broker                       |
| `logger`               | `default` | The logging level of the MQTT broker                         |
