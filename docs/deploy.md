<img src="pics/hamok.png" style="zoom: 50%;" />

# Deployment (Version 23.1)

You need:

- Home assistant
- An MQTT broker like ```mosquitto```
- Of course an Ökofen system

The deployment is manual at this time. I may simplify this in the future. Getting the thing running was my first priority.

## Upgrade vs Fresh install

If you are upgrading you can skip steps 3, 4 and 6. You may want to look at step 7 as new functionality was added. But step 7 can be skipped as well.

## Step 1: Download the source

_Last changes: version 22.8_

You can download the source here

* [ZIP file](https://github.com/paulbusse/Hamok/archive/refs/tags/v23.1.zip)
* [Compressed tarball(.tgz)](https://github.com/paulbusse/Hamok/archive/refs/tags/v23.1.tar.gz)

You should now have a file `Hamok-v23.1.[zip|tar.gz]`in your current directory. Unpack this archive where you want to install Hamök. I install it in the home directory of my `homeassistant`account.

The  rest of this guide assumes that you are located in the top directory of the code.

```bash
$ cd Hamok
```

## Step 2: Configure the MQTT broker

_Last changes: v22.3_

You are free to use whatever broker you like. It never hurt anyone to read the manual. We are using QoS 1 messages. Make sure that the messages that are sent persist.

Hamök always uses the same clientid to connect to the broker and should be able to pick up messages that were send while it was down. This also requires that the broker must be set up to forget about Hamök should you no longer need it.

Below is the very simple set up I use for the `mosquitto` broker.

Install the broker:

```bash
$ sudo apt install mosquitto
```

Edit the configuration file in `/etc/moquitto/mosquitto.conf`

```
pid_file /var/run/mosquitto.pid

persistence true
persistence_location /var/lib/mosquitto/
persistent_client_expiration 2m
queue_qos0_messages true

log_dest file /var/log/mosquitto/mosquitto.log
```

We like persistence to be on. This means that HA picks up the latest definitions and values when he restarts. For the other configuration settings please refer to the broker's manual.




## Step 3: Configure Hamök

_Last changes: v22.7_

In the directory you will find a file called `config_sample.yaml`. Copy or rename it to `config.yaml`. You will need the following pieces of information to get Hamök to work correctly.

1. The IP address of your MQTT broker.
2. If the broker does not run on the standard port (1883), you also need that port.
3. The IP address of your Ökofen machine.
4. The JSON port and JSON password.

The elements of point 4 you need to retrieve from your Ökofen machine. Yes, you must walk there. Once you open the console,

* Tap on the 9 dot icon
* Use the arrows to go all the way down
* Tap `General`(`Algemeen` in Dutch) and use the arrows again to down
* There you will find `IP config` and guess what scroll down until you see a box `JSON mode`.
* Make sure the `JSON mode` is on. Turn it on if necessary.
* Copy the values for JSON port and JSON password.

Equipped with these values, we can now edit the configuration file. At the top of the file you will find a section that looks like

```yaml
mqtt:
  broker: <Host name or IP address of MQTT broker>
#  port: 1883


# Ökofen JSON connection
oekofen:
  host: <Host name or IP address of MQTT broker>
  jsonport: <Ökofen JSON port>
  jsonpassword: <Ökofen JSON password>
```

After editing it should look something like

```yaml
mqtt:
  broker: 192.168.1.100
#  port: 1883


# Ökofen JSON connection
oekofen:
  host: 192.168.1.200
  jsonport: 1234
  jsonpassword: AbCd
```

You should consider changing the `device` name now, if you want. Setting the device is only interesting if you will have two independent Ökofen installs. Changing the device name later, requires an additional procedure. I will describe later.

You must also list at least one value to monitor. For this and other configuration settings please read the [user guide](usage.md)

Note: in 22.7 we changed the configuration of the monitors. Your current configuration file will cause failures.

## Step 4: Configure Home Assistant

_Last changes: v22.3_

This is the simplest of steps.

* Go to `Configuration/Devices and Services/Integrations`
* Select MQTT.
* In the first screen you re-enter the broker host and port, you used in the previous step.
* After clicking `next`, make sure the `enable discovery`box is checked.
* Click `Submit.

If everything goes well you will see a success message.

## Step 5: Running Hamok

_Last changes: v22.7_

Before running Hamok you need to install its dependencies:

```bash
$ pip3 install -r requirements.txt
```

Note: the dependencies are

* `paho-mqtt`

* `pyyaml`

Make sure that Home Assistant is running before you continue.

Ensure that the file `hamok`in bin is executable. If not

```bash
$ chmod +x bin/hamok
```

Now we are ready to launch Hamök.

```bash
$ bin/hamok -c ./config.yaml
```

Now validate syslog in `/var/log`.

You should see messages appear like

```
Mar 16 16:07:31 <host> hamok[115318] INFO     starting process
Mar 16 16:07:31 <host> hamok[115318] INFO     Connected to MQTT broker at <ip-address>:<port> as hamok.
Mar 16 16:07:31 <host> hamok[115318] INFO     Defining a new entity for oekofen_system_ambient[Mid:1].
Mar 16 16:07:31 <host> hamok[115318] INFO     Sending 14.1 on homeassistant/sensor/oekofen/oekofen_system_L_ambient/state[Mid:2].
Mar 16 16:07:31 <host> hamok[115318] INFO     Defining a new entity for oekofen_verwarming_temp_vacation[Mid:5].
Mar 16 16:07:31 <host> hamok[115318] INFO     Sending 15.0 on homeassistant/number/oekofen/oekofen_hk1_temp_vacation/state[Mid:6].
Mar 16 16:07:31 <host> hamok[115318] INFO     Defining a new entity for oekofen_warm_water_heat_once[Mid:7].
Mar 16 16:07:31 <host> hamok[115318] INFO     Sending OFF on homeassistant/switch/oekofen/oekofen_ww1_heat_once/state[Mid:8].
Mar 16 16:07:31 <host> hamok[115318] INFO     Subscribing to topics: ['homeassistant/number/oekofen/oekofen_hk1_temp_vacation/cmd', 'homeassistant/switch/oekofen/oekofen_ww1_heat_once/cmd', 'homeassistant/select/oekofen/oekofen_pe1_mode/cmd'][Mid:11].
```

In the `home-assistant.log` file you should see a line

```
home-assistant.log:2022-03-07 18:58:09 INFO (MainThread) [homeassistant.helpers.entity_registry] Registered new sensor.mqtt entity: sensor.oekofen_system_ambient
```

If everything works well, you should see 2 things appear in Home assistant. You can check this by going to  `Configuration/Devices and Services/Integrations`. The MQTT box should show 1 device and 1 entity more than before.

The device is named `Oekofen`. The entity is called `sensor.oekofen_system_ambient`. If this is all there. You're ready for the next step.

## Step 6: Integrating in systemd

_last changes: v22.5_

First of all you must change `bin/hamok`if you are running this in a python virtual env. Add the line

```bash
source <virtual env root>/bin/activate
```

As a second line in that file. (I consider this a bug to be fixed)

Note this step is not really necessary, but ensures that Hamök is restarted at reboot. This is focused on Raspberry OS. On other systems you may want to do different things.

In the directory where you unpacked the Hamök source, there is a file `hamok_sample.service`. Copy it to `hamok.service`

```bash
$ cp hamok_sample.service hamok.service
```

The file looks like

```
[Unit]
Description=Integrate Ökofen with HA over MQTT
After=mosquitto.service
Requires=mosquitto.service
Wants=home-assistant.service

[Service]
Type=simple
User=homeassistant
ExecStart=<installdir>/bin/hamok -c <installdir>/config.yaml
RestartSec=15
Restart=always

[Install]
WantedBy=multi-user.target
```

Of course you have to change the `installdir`but other changes may be needed depending on your system. Hamok fails if it cannot connect to the broker. Run the following commands.

```bash
$ sudo cp hamok.service /etc/systemd/system/
$ sudo systemctl enable hamok.service
$ sudo systemctl start hamok.service
```

To really validate if this works properly you should reboot your system and validate that Hamök runs.

## Step 7: Add entities

Now is a good time to read the [manual](usage.md) and configure a few entities.
