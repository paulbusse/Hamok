# Release History

## Next version
## Functionality

- Hamök reconnects automatically if the communication with the broker is restored after an interruption

### Bug fixes

- The values sent to HA now have one decimal digit.

## V22.3

### Funtionality
- Connect to the JSON interface of the Ökofen system
- Translate the information from the Ökofen system into information HA understands
- Generate MQTT messages HA understands
- Generate MQTT messages HA can use to create the necessary sensors
- Update the sensors (only when they change)