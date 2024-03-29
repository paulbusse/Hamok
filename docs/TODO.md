# Todo list

- use unavailability, for all sensors
  - requires birth and will messages
    - requires birth message
    - requires will message
- more secure usage of MQTT
- validate that all monitors in the list exist
- detect if hamok runs in virtual env
- reload config on signal (systemctl?) or use an MQTT topic
- reverse engineer state bitmap
- config file through environment variable
- extract version information from the system
- [23]Make the max number of failures configurable
- set the urllib timeout
- MQTT callbacks: make jobs out of the different callbacks
- Test the config file errors
- Make the return codes in on_connect user readable
- handle forecast section of ökofen
- handle weather section of ökofen
- config: MQTT keepalive
- config: failure timeout
- config: time between 2 connects to Ökofen min 2.5 secs
- config validation by voluptuous
- mqttdebug should be part of the mqtt setting.

# Issues




# Refactoring

- entity.factory: oekofen specific part should go to oekofen.py
- create_entity needs to go (back) to entitylist.py
- move the initial connect to run in service.py

# Low priority

- allow extended clientids for MQTT
- delete monitors in HA that are no longer configured, by deleting the corresponding topics (there is a description in the docs that explains how to do this)

# Under discussion

## Needs a valid use case

- use attributes for the sensors
- send updates on regular basis (after a given period) instead of only when it changes


## create all entities disabled

HA allows entities to be disabled. We could create all entities, Ökofen provides, disabled and the user could enable them in HA

- PRO: we do not need to maintain the `monitor` list in the configuration file
- CONTRA: we will be sending a lot of useless information

Solution: make this configurable?

# Declined Todo's

'No' is an eligible answer. In this section we explain why we won't implement certain things.

## MQTT on exit disconnect
Sometimes it is just a hickup. In Paho reconnects are automatic. Only if
we cannot reconnect after a certain amount of time we will exit.

## disconnect from the terminal

In production we use systemd. This means that the process is not connected to any terminal. If we run it from a terminal we want to see logs on the terminal, so disconnectin is not a useful feature.

Note that when we run from a terminal, we should make sure the output is directed to the terminal. That requirement remains.