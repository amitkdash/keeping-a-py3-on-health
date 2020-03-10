#!/bin/python3
from enum import Enum


class MonitoringStatus(Enum):
    HEALTHY = 0
    ALERTING = 1
