# Hamök

- HA: stands for Home Assistant
- M: stands for MQTT
- ÖK: stands for Ökofen

<img src="/home/homeassistant/Hamok/docs/pics/hamok.png" alt="hamok" style="zoom:50%;" />


## What is this

It is an integration of Ökofen Pellet heating systems in Home Assistant using MQTT.

The Ökofen systems can differ largely and the number of sensors that can be created in HA may be dramatic and unuseful.

Hamok tries to give you some control over this.

Why not build a real HA integration. Well I may do this over time, but this is something I know and I wanted to be quick.

## Current status

We are far from done. In the current version (0.1) we are only moving information from the heating system and convert them into MQTT messages HA understands.

- Connect to the JSON interface of the Ökofen system
- Translate the information from the Ökofen system into information HA understands
- Generate MQTT messages HA understands
- Generate MQTT messages HA can use to create the necessary sensors
- Update the sensors (only when they change)

## Documentation

There are several docs, you can read.

1. The [deployment guide](docs/deploy.md)
2. A [user guide](docs/usage.md)

I also have a [todo](docs/todo.md) list. That is not in any order and should be converted into issues. But currently, I'm focused on other stuff. If you have ideas, create issues and I may put them on my todo-list. Or, you may contribute yourself.

Enjoy.

Paul

