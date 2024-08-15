# src/mini_trader/event_bus/event.py

import time
import uuid
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, Optional


class EventType(Enum):
    # Market Data Events
    NEW_PRICE_DATA = auto()
    NEW_VOLUME_DATA = auto()
    NEW_OHLC_DATA = auto()
    MARKET_OPEN = auto()
    MARKET_CLOSE = auto()
    TRADING_HALT = auto()
    DIVIDEND_ANNOUNCEMENT = auto()

    # Strategy Events
    SIGNAL_GENERATED = auto()
    STRATEGY_STARTED = auto()
    STRATEGY_STOPPED = auto()
    PARAMETER_UPDATED = auto()

    # Order Events
    ORDER_CREATED = auto()
    ORDER_SUBMITTED = auto()
    ORDER_FILLED = auto()
    ORDER_CANCELLED = auto()
    ORDER_REJECTED = auto()

    # Portfolio Events
    POSITION_OPENED = auto()
    POSITION_CLOSED = auto()
    POSITION_UPDATED = auto()
    CASH_ADJUSTED = auto()

    # Risk Management Events
    RISK_LIMIT_REACHED = auto()
    MARGIN_CALL = auto()
    STOP_LOSS_TRIGGERED = auto()

    # System Events
    BACKTEST_STARTED = auto()
    BACKTEST_COMPLETED = auto()
    OPTIMIZATION_STARTED = auto()
    OPTIMIZATION_COMPLETED = auto()
    ERROR = auto()


@dataclass
class Event:
    type: EventType
    data: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    source: Optional[str] = None
    target: Optional[str] = None

    def __post_init__(self):
        if not isinstance(self.type, EventType):
            raise ValueError(f"Invalid event type: {self.type}")
        if not isinstance(self.data, dict):
            raise ValueError("Event data must be a dictionary")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "type": self.type.value,
            "data": self.data,
            "timestamp": self.timestamp,
            "source": self.source,
            "target": self.target,
        }

    @classmethod
    def from_dict(cls, event_dict: Dict[str, Any]) -> "Event":
        event_dict["type"] = EventType(event_dict["type"])
        return cls(**event_dict)
