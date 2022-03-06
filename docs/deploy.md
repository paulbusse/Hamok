<img src="pics/hamok.png" style="zoom: 50%;" />

# Deployment

You need:

- Home assistant
- An MQTT broker like ```mosquitto```
- Of course an Ökofen system

The deployment is manual at this time. I may simplify this in the future. Getting the thing running was my first priority.

## Step 1: Download the source

Yep at this point in time you have to download the source. This can be done by cloning the repository or by downloading the zip file from the repository. If you don't know how to do the first, I'll explain the second:

1.  Go to the repository: [paulbusse/hamok](https://github.com/paulbusse/Hamok)
2.  Click on the green button ```code```
3.  Select ```Download ZIP```
4.  You should have a file ```hamok-main.zip```. Move it to a directory where you want it to reside and unpack the code there

The  rest of this guide assumes that you are located in the top directory of the code.

```bash
$ cd Hamok
```

## Step 2: Configure the MQTT broker

You are free to use whatever broker you like. It never hurt anyone to read the manual. We are using QoS 1 messages. Make sure that the messages that are sent persist. 

Hamök always uses the same clientid to connect to the broker and should be able to pick up messages that were send while it was down. This also requires that the broker must be set up to forget about Hamök should you no longer need it.

## Step 3: Configure Hamök

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

For other configuration settings please read the [user guide](usage.md)

## Step 4: Configure Home Assistant

This is the simplest of steps. 

* Go to `Configuration/Devices and Services/Integrations`
* Select MQTT.
* In the first screen you re-enter the broker host and port, you used in the previous step.
* After clicking `next`, make sure the `enable discovery`box is checked.
* Click `Submit.

If everything goes well you will see a success message.

## Step 5: Running Hamok

Before running Hamok you need to install its dependencies:

```bash
$ pip3 install -r requirements.txt
```

Make sure that Home Assistant is running before you continue.

Ensure that the file `hamok`in bin is executable. If not

```bash
$ chmod +x bin/hamok
```

Now we are ready to launch Hamök.

```bash
$ bin/hamok -c ./config.yaml
2022-03-06 07:57:55,938 INFO       starting process
2022-03-06 07:57:55,939 INFO       Connected to MQTT broker at <ipaddress>:<port> as hamok.
2022-03-06 07:57:56,647 INFO       Connected to MQTT broker at <ipaddress>:<port> as hamok.
2022-03-06 07:57:56,648 INFO       Defining a new entity for oekofen_system_ambient.
2022-03-06 07:57:56,650 INFO       Connected to MQTT broker at <ipaddress>:<port> as hamok.
2022-03-06 07:57:56,650 DEBUG      Sending {"val": 0.5, "last_update": "2022-03-06T07:57:56"} on homeassistant/sensor/oekofen/oekofen_system_L_ambient/state.
2022-03-06 07:57:56,650 INFO       Setting the value of entity oekofen_system_ambient to 0.5.
```

Note that the DEBUG message may not appear.

If everything works well, you should see 2 things appear in Home assistant. You can check this by going to  `Configuration/Devices and Services/Integrations`. The MQTT box should show 1 device and 1 entity more than before.

The device is named `Oekofen`. The entity is called `sensor.oekofen_system_ambient`. If this is all there. You're ready for the next step.

## Step 6: Integrating in systemd

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
RestartSec=3
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

Now is a good time to read the [manual](usage.md) and add a few entities.



