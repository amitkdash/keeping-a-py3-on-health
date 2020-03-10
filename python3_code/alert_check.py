#!/bin/python3

from python3_code import alert_mechanism, utilities, status_enum
from python3_code.global_vars import interval_before_next_alert, delimiter, current_mode_path


def update_mode_and_alert_team():
    utilities.append_to_file(current_mode_path, status_enum.MonitoringStatus.ALERTING.name)
    alert_mechanism.alert_the_team()


def update_mode_to_healthy():
    utilities.append_to_file(current_mode_path, status_enum.MonitoringStatus.HEALTHY.name)


def should_I_alert_the_team():
    # current_status can be one of the enums registered in 'status_enum.py' read from the below CSV file
    current_mode_content = utilities.get_trimmed_content_from_file('../files/current_mode.csv')

    if len(current_mode_content) <= 1:
        print("No records in the CSV file. An alert will be issued.")
        update_mode_and_alert_team()
    else:
        last_element_as_list = current_mode_content[len(current_mode_content) - 1].split(delimiter)
        last_status = last_element_as_list[0]
        last_change_timestamp = last_element_as_list[1]
        if last_status == status_enum.MonitoringStatus.HEALTHY.name or \
                int(utilities.get_current_time_millis()) - int(last_change_timestamp) >= \
                int(interval_before_next_alert):
            update_mode_and_alert_team()
        else:
            print(utilities.current_human_time() + ": Within cooling off "
                                                   "interval. Will not update"
                                                   " mode and not send alerts "
                                                   "at this point.")


if __name__ == "__main__":
    print("This file has been invoked directly. Will run failure alert check logic now.")
    should_I_alert_the_team()
