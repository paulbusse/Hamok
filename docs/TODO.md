- use unavailability, for all sensors
- send commands back to the oekofen
- send updates on regular basis (after a given period)
- exit the process properly
- more secure usage of MQTT
- validate that all monitors in the list exist
- Exec the python in the shell script
- Is sending the value on state sufficient
- delete monitors in HA that are no longer configured, by deleting the corresponding topics

## detect that we are running from a terminal and use devel logger

Subtask: the 'Devel' logger cannot be set in the configuration file and becomes an illegal value.

# Low priority

- allow extended clientids

# Under discussion

## use attributes for the sensors

We need a use case

## disconnect from the terminal

  - As we start through systemd, it is running in the background. When started from terminal we probably want to it run.