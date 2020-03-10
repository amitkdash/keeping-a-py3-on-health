#!/bin/python3

import ast
import json

import urllib3

from python3_code import status_enum
from python3_code import utilities, alert_check
from python3_code.global_vars import health_endpoint, delimiter, current_mode_path, health_ledger_path


def dial_health():
    # sending get request and saving the response as response object
    response_obj = urllib3.PoolManager().request('GET', health_endpoint, headers={'Content-Type': 'application/json'})
    # parsing the response JSON into a variable
    health_check_response_json = json.loads(response_obj.data.decode('utf-8'))
    if str(health_check_response_json["status"]).strip() != "UP":
        utilities.append_to_file(health_ledger_path, health_check_response_json)
        alert_check.should_I_alert_the_team()
    elif str(health_check_response_json["status"]).strip() == "UP":
        if was_health_down_before_this():
            utilities.append_to_file(health_ledger_path, health_check_response_json)
            utilities.append_to_file(current_mode_path, status_enum.MonitoringStatus.HEALTHY.name)
    else:
        print("This isn't a normal JSON response. Please check why the response to health check is: " +
              health_check_response_json)


def was_health_down_before_this():
    error_ledger_content = utilities.get_trimmed_content_from_file('../files/health_ledger.csv')
    last_health_record = error_ledger_content[-1]
    # json.loads can't decipher single quote JSONs hence using ast.literal_eval here
    last_status = ast.literal_eval(last_health_record.split(delimiter)[0])
    if "status" not in last_status or last_status["status"] != "UP":
        print("Previous status Invalid or Unhealthy. Last record: " + last_health_record)
        return True
    else:
        return False


if __name__ == "__main__":
    # The entry-point of the whole thing
    dial_health()
