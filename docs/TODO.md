# Todo list

- use unavailability, for all sensors
  - requires birth and will messages
    - requires birth message
    - requires will message
- more secure usage of MQTT
- validate that all monitors in the list exist
- delete monitors in HA that are no longer configured, by deleting the corresponding topics
- upgrade to Python 3.9 and 3.10.
- detect if hamok runs in virtual env
- reload config on signal (systemctl?)
- Validate return codes in callback on connect
- Validate return codes in callback on publish
- Validate return codes in callback on subscribe
- refactoring: parse.py should be integrated in oekofen.py
- refactoring: entity.factory: oekofen specific part should go to oekofen.py
- set device class for HA devices
- refactoring: use f-strings everywhere
- refactoring: remove dependency of hamqtt on entity
- refactoring: all jobs should be created using schedule
- on re_connect publish all the available values
- reverse engineer state bitmap
- config file through environment variable

## detect that we are running from a terminal and use devel logger

Subtask: the 'Devel' logger cannot be set in the configuration file and becomes an illegal value.

# Low priority

- allow extended clientids

# Under discussion

## Needs a valid use case

- use attributes for the sensors
- send updates on regular basis (after a given period)


## create all entities disabled

HA allows entities to be disabled. We could create all entities disabled and the user should enable them in HA

- PRO: we do not need to maintain the `monitor` list in the configuration file
- CONTRA: we will be sending a lot of useless information

Solution: make this configurable?

# Declined Todo's

'No' is an eligible answer. In this section we explain why we won't implement certain things.

## disconnect from the terminal

In production we use systemd. This means that the process is not connected to any terminal. If we run it from a terminal we want to see logs on the terminal, so disconnectin is not a useful feature.

Note that when we run from a terminal, we should make sure the output is directed to the terminal. That requirement remains.