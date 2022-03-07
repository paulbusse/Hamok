- use attributes for the sensors
- use unavailability, for all sensors
- send commands back to the oekofen
- send updates on regular basis
- send one message with all updates
- disconnect from the terminal
- exit the process properly
- allow extended clientids 

## Client hamok has exceeded timeout, disconnecting. MQTT message.
```
Mar  6 12:21:54 Nukkie mosquitto.mosquitto[120444]: 1646565714: New connection from 127.0.0.1:53847 on port 1883.
Mar  6 12:21:54 Nukkie mosquitto.mosquitto[120444]: 1646565714: New client connected from 127.0.0.1:53847 as hamok (p2, c0, k60).
Mar  6 12:21:54 Nukkie hamok[211496] INFO     Connected to MQTT broker at 127.0.1.1:1883 as hamok.
Mar  6 12:21:55 Nukkie mosquitto.mosquitto[120444]: 1646565715: Client hamok closed its connection.
Mar  6 12:21:55 Nukkie mosquitto.mosquitto[120444]: 1646565715: New connection from 127.0.0.1:49189 on port 1883.
Mar  6 12:21:55 Nukkie mosquitto.mosquitto[120444]: 1646565715: New client connected from 127.0.0.1:49189 as hamok (p2, c0, k60).
Mar  6 12:21:55 Nukkie hamok[211496] INFO     Connected to MQTT broker at 127.0.1.1:1883 as hamok.
Mar  6 12:21:55 Nukkie hamok[211496] INFO     Defining a new entity for oekofen_system_ambient.
Mar  6 12:21:55 Nukkie mosquitto.mosquitto[120444]: 1646565715: Client hamok closed its connection.
```
