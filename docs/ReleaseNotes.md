# Release History

## V 22.4

Release date: 2022-03-17

### Functionality

- Hamök reconnects automatically if the communication with the broker is restored after an interruption

#### Changes entered in HA will be forwarded to Ökofen

When HA sends information to Hamök, Hamök forwards that state change to Ökofen. Hamök will send the new state to HA.
This means that if the update towards Ökofen fails, HA will be updated by the previous value. If the update succeeds, HA will receive the new update.

It introduces threading to handle incoming message.

### Bug fixes

- The values sent to HA now have one decimal digit.

## V 22.3

### Functionality
- Connect to the JSON interface of the Ökofen system
- Translate the information from the Ökofen system into information HA understands
- Generate MQTT messages HA understands
- Generate MQTT messages HA can use to create the necessary sensors
- Update the sensors (only when they change)