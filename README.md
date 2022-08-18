# snmp-bootstrap-api-puller
This is a quick python script that will use the API to search for devices with a specific label for bootstrapping snmp

It will write the device list to an enviromental file for use by kproxy:  /etc/default/snmp_device_list.env
You will need to edit your kproxy service in order to include this new environment file.
The "best practice" for doing this is to use the command "systemctl edit kproxy.service".  This will open a new file editor where you may input additional service file lines or create overrides instead of directly editing the service file.
Your systemctl edit file may looks something like this:

```
[Service]
EnvironmentFile=-/etc/default/snmp_device_list.env
ExecStart=
ExecStart=/usr/bin/kproxy  -dns internal:192.168.1.2:53 -my_network 192.168.1.0/24,192.168.2.0/24 -api_email=${KENTIK_API_EMAIL} -log_level=info -host=0.0.0.0  -proxy_host=127.0.0.1 -healthcheck=0.0.0.0 -auto_update=false -port=${KENTIK_PORT_LISTEN} -bootstrap_devices=${BOOTSTRAP_DEVICES}
```

This will add an additional EnvironmentFile, remove the existing ExecStart line (via the initial blank entry) and then replace that ExecStart with the one listed here.

You may either enter your credentials (email and API key) as part of the command line, or hard code it into the script itself.

Usage:
``` sudo ./getDeviceByLabel.py --label SNMP-Only --email <YOUR PORTAL EMAIL LOGIN> --api <YOUR API KEY> ```
