from enum import Enum


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Environment(str, Enum):
    PROD = "prod"
    STAGING = "staging"
    QA = "qa"

class Action(str, Enum):
    ROLLBACK = "rollback"
    RESTART = "restart"
    SCALE_UP = "scale_up"
    NOTIFY_HUMAN = "notify_human"
    NO_ACTION = "no_action"