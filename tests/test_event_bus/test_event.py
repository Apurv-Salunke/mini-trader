import pytest
from mini_trader.event_bus.event import Event, EventType


def test_event_creation():
    event = Event(EventType.NEW_PRICE_DATA, {"symbol": "AAPL", "price": 150.25})
    assert event.type == EventType.NEW_PRICE_DATA
    assert event.data == {"symbol": "AAPL", "price": 150.25}
    assert isinstance(event.timestamp, float)
    assert isinstance(event.event_id, str)


def test_event_validation():
    with pytest.raises(ValueError):
        Event("INVALID_TYPE", {"price": 100})

    with pytest.raises(ValueError):
        Event(EventType.NEW_PRICE_DATA, "Not a dictionary")


def test_event_serialization():
    original_event = Event(EventType.SIGNAL_GENERATED, {"symbol": "AAPL", "action": "BUY"})
    event_dict = original_event.to_dict()
    reconstructed_event = Event.from_dict(event_dict)

    assert original_event.type == reconstructed_event.type
    assert original_event.data == reconstructed_event.data
    assert original_event.timestamp == reconstructed_event.timestamp
    assert original_event.event_id == reconstructed_event.event_id


def test_event_optional_fields():
    event = Event(
        EventType.ORDER_CREATED,
        {"symbol": "GOOGL", "quantity": 100},
        source="strategy_1",
        target="executor",
    )
    assert event.source == "strategy_1"
    assert event.target == "executor"


def test_market_data_events():
    price_event = Event(EventType.NEW_PRICE_DATA, {"symbol": "AAPL", "price": 150.25})
    assert price_event.type == EventType.NEW_PRICE_DATA
    assert price_event.data["symbol"] == "AAPL"
    assert price_event.data["price"] == 150.25

    ohlc_event = Event(
        EventType.NEW_OHLC_DATA,
        {"symbol": "AAPL", "open": 150.0, "high": 151.0, "low": 149.5, "close": 150.5},
    )
    assert ohlc_event.type == EventType.NEW_OHLC_DATA
    assert "open" in ohlc_event.data


def test_strategy_events():
    signal_event = Event(
        EventType.SIGNAL_GENERATED, {"symbol": "AAPL", "action": "BUY", "quantity": 100}
    )
    assert signal_event.type == EventType.SIGNAL_GENERATED
    assert signal_event.data["action"] == "BUY"

    strategy_start_event = Event(
        EventType.STRATEGY_STARTED, {"strategy_name": "MovingAverageCrossover"}
    )
    assert strategy_start_event.type == EventType.STRATEGY_STARTED


def test_order_events():
    order_created_event = Event(
        EventType.ORDER_CREATED,
        {"order_id": "12345", "symbol": "AAPL", "quantity": 100, "price": 150.0},
    )
    assert order_created_event.type == EventType.ORDER_CREATED
    assert "order_id" in order_created_event.data

    order_filled_event = Event(
        EventType.ORDER_FILLED, {"order_id": "12345", "fill_price": 150.1, "filled_quantity": 100}
    )
    assert order_filled_event.type == EventType.ORDER_FILLED


def test_portfolio_events():
    position_opened_event = Event(
        EventType.POSITION_OPENED, {"symbol": "AAPL", "quantity": 100, "price": 150.0}
    )
    assert position_opened_event.type == EventType.POSITION_OPENED

    cash_adjusted_event = Event(EventType.CASH_ADJUSTED, {"amount": 10000, "reason": "Deposit"})
    assert cash_adjusted_event.type == EventType.CASH_ADJUSTED


def test_risk_management_events():
    risk_limit_event = Event(
        EventType.RISK_LIMIT_REACHED, {"limit_type": "max_drawdown", "current_value": 0.1}
    )
    assert risk_limit_event.type == EventType.RISK_LIMIT_REACHED


def test_system_events():
    backtest_start_event = Event(
        EventType.BACKTEST_STARTED, {"start_date": "2023-01-01", "end_date": "2023-12-31"}
    )
    assert backtest_start_event.type == EventType.BACKTEST_STARTED

    error_event = Event(EventType.ERROR, {"message": "Data feed disconnected", "severity": "high"})
    assert error_event.type == EventType.ERROR


def test_event_equality():
    event1 = Event(EventType.NEW_PRICE_DATA, {"symbol": "AAPL", "price": 150.25})
    event2 = Event(EventType.NEW_PRICE_DATA, {"symbol": "AAPL", "price": 150.25})
    assert event1 != event2  # They should not be equal due to different event_ids

    event3 = Event.from_dict(event1.to_dict())
    assert event1 == event3  # They should be equal after serialization and deserialization
