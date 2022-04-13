# Hamök

- HA: stands for Home Assistant
- M: stands for MQTT
- ÖK: stands for Ökofen

<img src="docs/pics/hamok.png" alt="hamok" style="zoom:50%;" />


## What is this

It is an integration of Ökofen Pellet heating systems in Home Assistant using MQTT.

Why not build a real HA integration. Well I may do this over time, but this is something I know and I wanted to be quick. This is not my first MQTT ride (I don't claim to be an expert) but it would be my first HA integration and this is quite a complex one. Especially, if you want the same functionality as I want to put into this little monster.

## Functionality

The Ökofen systems can differ largely and the number of sensors that can be created in HA may be large (127 in my case) and not all of them are useful to monitor, it is unclear what they mean or they are just permanently 0. Hamök gives you control over this.

Hamök connects to the JSON interface of the Ökofen system and translates the information it receives from that interface

*  MQTT messages that allows HA to create a device and a set of sensors
* It regularly connects to the JSON interface and sends updates to HA whenever the value changes. Depending on the monitored value we use [binary sensors](https://www.home-assistant.io/integrations/binary_sensor.mqtt/), or regular [sensors](https://www.home-assistant.io/integrations/sensor.mqtt/)

- If the values can be set on the Ökofen system, you can change them in HA. The entities that can be changed are configured in such a way that you can only set acceptable values. Here we use [select](https://www.home-assistant.io/integrations/select.mqtt/), [numbers](https://www.home-assistant.io/integrations/number.mqtt/), or [switches](https://www.home-assistant.io/integrations/switch.mqtt/)
- When the Ökofen system cannot be reached, the sensors are marked as unavailable. 

## Further documentation

There are several docs, you can read.

1. The [deployment guide](docs/deploy.md)
2. A [user guide](docs/usage.md)

I also have a [todo](docs/todo.md) list. That is not in any order and should be converted into issues. But currently, I'm focused on other stuff. If you have ideas, create issues and I may put them on my todo-list. Or, you may contribute yourself.

Enjoy.

Paul
