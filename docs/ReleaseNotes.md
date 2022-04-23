# Release History

## Version 22.6

### Functionality

* Hamök monitors the MQTT connection and exits if the connection is down for longer than 5 minutes. Note that `systemd` will restart it
* When the connection to the Pellematic fails longer than 5 minutes the process exits. Note that `systemd` will restart it.
* Hamök now listens to the return codes of MQTT subscribe and publish commands
* When Hamök reconnects it resends the definitions and the latest values for the HA sensors. This was not necessary as the latest versions were sent in `retain` mode
* Added the -f option to parse a JSON file retrieved from Ökofen. Primarily for testing purposes

### Bug Fixes

* Reconnections in calls to publish and subscribe were not needed as they are handle by the MQTT library
* Reconnections no longer start a new threat
* True and false values are now recognized as 1 and 0 respectively.

### Upgrade



## Version 22.5

### Functionality

* Device name gets normalized wherever it is used as part of an identifier
* Hamök exits properly when it can: it closes connections, sends the necessary messages.
* When Hamök could not execute its functions (no MQTT broker, no Pellematic) it returns an error code.
* ~~When the connection to the Pellematic fails 5 times the process exits. Note that `systemd` will restart it.~~ Improved  in 22.6
* Hamök sets the sensors to 'unavailable' if the Pellematic is not reachable, and back to available when it becomes reachable again.

### Bug fixes

* In the topic names the Ökofen identifier was used not the friendly

* If Hamök has collisions with the Pellematic app, it sometimes continues these collisions after restart.

* Some code cleanup has been done.
  * Added the `service.py` module
  * `hamqqt.py`handles only communication with MQTT, no business logic
  * cleaning up of debug messages.
  
### Upgrade

When upgrading use the deployment document and you can skip steps 2 (MQTT setup), 3 (Hamok setup), 4 (HA setup).  


## Version 22.4

Release date: 2022-03-17

### Functionality

- Hamök reconnects automatically if the communication with the broker is restored after an interruption

#### Changes entered in HA will be forwarded to Ökofen

When HA sends information to Hamök, Hamök forwards that state change to Ökofen. Hamök will send the new state to HA.
This means that if the update towards Ökofen fails, HA will be updated by the previous value. If the update succeeds, HA will receive the new update.

It introduces threading to handle incoming message.

### Bug fixes

- The values sent to HA now have one decimal digit.

## Version 22.3

### Functionality
- Connect to the JSON interface of the Ökofen system
- Translate the information from the Ökofen system into information HA understands
- Generate MQTT messages HA understands
- Generate MQTT messages HA can use to create the necessary sensors
- Update the sensors (only when they change)