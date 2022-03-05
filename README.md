# Hamök

- HA: stands for Home Assistant
- M: stands for MQTT
- ÖK: stands for Ökofen

<p float="left">
  <img src="docs/pics/ha.png" height="50" />
  <img src="docs/pics/mqtt-logo.svg" height="50" /> 
  <img src="docs/pics/okofen.png" height="50" />
</p>

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

There is a todo list (link) and you can always send in requests in the form of a GitHub issue, and I will fit it in. Or, you can contribute.

## Deployment

Deployment is manual for now and the different steps are listed here (link). An easier deployment is in the todo-list.

Enjoy.

Paul

