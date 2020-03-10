#!/bin/python3

import json

# URL to get health check response. Default points to AuthTokens health endpoint.
global health_endpoint
# cooling-off period in milliseconds before we send out another alert. Default 10 minutes.
global interval_before_next_alert
# email address where the alerts should go to. Default will be the AuthTokens DL.
global email_address_for_alerts
# delimiter that separates the values in the csv file. Default value is pipe '|'
global delimiter
# Path for the ledger file that records health updates every time the status goes from UP to DOWN and DOWN to UP and
# while it stays down
global health_ledger_path
# Path for the file that records the current state ("mode") of the stateless monitoring solution.
# If we're HEALTHY or ALERTING and when was the last such event
global current_mode_path

# default inits
health_endpoint = "https://my-api-endpoint.com/api/health"
interval_before_next_alert = 600000
email_address_for_alerts = "team_email_dl@gmail.com"
delimiter = "|"
health_ledger_path = '../files/health_ledger.csv'
current_mode_path = '../files/current_mode.csv'


def read_json_value(config_json, key_name, default_value):
    return config_json[key_name] if key_name in init_config_json and \
                                    init_config_json[key_name].strip() != "" else default_value


# initialization from config file happens here:
with open("../files/init_config.json", "r") as config_file:
    init_config_json = json.load(config_file)
health_endpoint = read_json_value(init_config_json, "health_endpoint", health_endpoint)
email_address_for_alerts = read_json_value(init_config_json, "alert_email_address", email_address_for_alerts)
health_ledger_path = read_json_value(init_config_json, "health_ledger_path", health_ledger_path)
current_mode_path = read_json_value(init_config_json, "current_mode_path", current_mode_path)

# cool off interval can't be below 1 minute
interval_value_placeholder = int(read_json_value(init_config_json, "cool_off_interval", interval_before_next_alert))
interval_before_next_alert = interval_value_placeholder \
    if interval_value_placeholder > 60000 else interval_before_next_alert

print("Initialization successful for health check parameters. Health Check will be performed on: " + health_endpoint)

