# Lupusec-Connector
This connector is written in Python and can be used to connect the Lupusec XT1 to your OpenHAB. Please keep in mind that this script only connects to your alarm device and gets the data of sensors or the alarm system itself. There's no caching. The connector should make it easy to integrate the device to your smart home plattform.

**Important note:** This script has been tested with the alarm system Lupusec XT1 Plus

## How to start

Before you can start using this script you need to add the ip address and the username/password combination.

## Packages

This scripts uses the following packages:

- Flask
- Requests
- Json

Also you need python on your computer.

## Address and port

You can use the IP of the device where the script is located. It will start on port 5000. You can change the port.

## APIs

```
http://IP_OF_THE_DEVICE:5000/
http://IP_OF_THE_DEVICE:5000/alarmstate
http://IP_OF_THE_DEVICE:5000/sensor/{SENSOR_ID}
http://IP_OF_THE_DEVICE:5000/alarmstate/{number of the state}
```

You will find more information about the number of the state below.

### Sensor ID

You can find the sensor id in your alarm device. Navigate to the sensor list and click on edit. There's a read-only field with the id of the sensor.

**Please notice you need only the part after "RF:"**

E. g. if your id looks like **RF:11c1a129** you need to copy only **11c1a129**

## OpenHAB

If you want to use this script with OpenHAB you can just define multiple items to receive the values of the alarm device.

### Sensors

```java
String Windows "Window" { http="<[http://IP_OF_THE_DEVICE:5000/sensor/ID_OF_THE_SENSOR:10000:JSONPATH($.status_ex)]" }
```

This API will return the json response from your alarm system.

```json
{
    "alarm_status": "",
    "ammeter": "0",
    "area": 1,
    "battery": "",
    "battery_ok": "1",
    "bypass": 0,
    "bypass_tamper": 0,
    "cond": "",
    "cond_ok": "1",
    "ctemp": "-1",
    "hue": "-1",
    "hue_cie_x": "-1",
    "hue_cie_y": "-1",
    "hue_cmode": "-1",
    "hue_color_cap": "0",
    "name": "Window",
    "nuki": "-1",
    "resp_mode": [
        97,
        1,
        1,
        1,
        1,
        0
    ],
    "rssi": "{WEB_MSG_STRONG}9",
    "sat": "-1",
    "sid": "RF:f3c6a110",
    "status": "{WEB_MSG_DC_CLOSE}",
    "status_ex": "0",
    "su": 1,
    "tamper": "",
    "tamper_ok": "1",
    "type": 4,
    "type_f": "{D_TYPE_4}",
    "ver": "",
    "zone": 2
}
```

With JSONPATH you can extract one of the values to your OpenHAB instance. You can get the root element with $.

### Alarm state

```java
String Alarm "Alarmstate" { http="<[http://IP_OF_THE_DEVICE:5000/alarmstate:10000:JSONPATH($.updates.mode_a1)]" }
```

This will return the current state of the area 1. If you want to get the state of the area 2 you need to change the JSONPATH to

```java
$.updates.mode_a2
```

A full response of this API looks like the following:

```json
{
    "forms": {
        "pcondform1": {
            "f_arm": "0",
            "mode": "2"
        },
        "pcondform2": {
            "f_arm": "0",
            "mode": "0"
        }
    },
    "updates": {
        "ac_activation": "{WEB_MSG_NORMAL}",
        "ac_activation_ok": "1",
        "alarm_ex": "0",
        "battery": "{WEB_MSG_NORMAL}",
        "battery_ex": "0",
        "battery_ok": "1",
        "dc_ex": "1",
        "fw_updated": "0",
        "interference": "{WEB_MSG_NORMAL}",
        "interference_ok": "1",
        "mode_a1": "{AREA_MODE_2}",
        "mode_a2": "{AREA_MODE_0}",
        "rssi": "1",
        "sig_gsm": "{WEB_MSG_NA}",
        "sig_gsm_ok": "1",
        "sys_in_inst": "",
        "tamper": "{WEB_MSG_NORMAL}",
        "tamper_ok": "1"
    }
}
```

To change the alarm state you have to send a get request to the following endpoint:

```
http://IP_OF_THE_DEVICE:5000/setstate/{number of the state}
```
The following numbers of states are available:

- 0: Disarm
- 1: Arm
- 2: Home

In OpenHAB you can use a switch to arm or disarm your system.

The script will return the original response of your alarm system looking like the following:

```json
{
"result" : 1,
"message" : "{WEB_MSG_SUBMIT_SUCCESS}"
}
```

#### X-Token

You can find an x-token if you navigate to your alarm system panel with your browser and open the developer tools (F12). Navigate to network and find the request **panelCondPost**. There's an x-token you need to copy into the head of the python script.

Without an x-token you're not able to control your alarm system!
