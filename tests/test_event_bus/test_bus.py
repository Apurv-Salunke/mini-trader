import pytest
from mini_trader.event_bus.bus import EventBus, Event, EventType
import time

@pytest.fixture
def event_bus():
    bus = EventBus()
    bus.start()
    yield bus
    bus.stop()

def test_event_bus_start_stop(event_bus):
    assert event_bus._running is True
    event_bus.stop()
    assert event_bus._running is False
def test_event_publish_and_subscribe(event_bus):
    received_events = []
    
    def callback(event):
        received_events.append(event)
    
    event_bus.subscribe(EventType.NEW_PRICE_DATA, callback)
    
    test_event = Event(EventType.NEW_PRICE_DATA, {"symbol": "AAPL", "price": 150.0})
    event_bus.publish(test_event)
    
    # Give some time for the event to be processed
    time.sleep(0.1)
    
    assert len(received_events) == 1
    assert received_events[0].type == EventType.NEW_PRICE_DATA
    assert received_events[0].data == {"symbol": "AAPL", "price": 150.0}

def test_multiple_subscribers(event_bus):
    received_events_1 = []
    received_events_2 = []
    
    def callback1(event):
        received_events_1.append(event)
    
    def callback2(event):
        received_events_2.append(event)
    
    event_bus.subscribe(EventType.NEW_PRICE_DATA, callback1)
    event_bus.subscribe(EventType.NEW_PRICE_DATA, callback2)
    
    test_event = Event(EventType.NEW_PRICE_DATA, {"symbol": "AAPL", "price": 150.0})
    event_bus.publish(test_event)
    
    time.sleep(0.1)
    
    assert len(received_events_1) == 1
    assert len(received_events_2) == 1

def test_unsubscribe(event_bus):
    received_events = []
    
    def callback(event):
        received_events.append(event)
    
    event_bus.subscribe(EventType.NEW_PRICE_DATA, callback)
    event_bus.unsubscribe(EventType.NEW_PRICE_DATA, callback)
    
    test_event = Event(EventType.NEW_PRICE_DATA, {"symbol": "AAPL", "price": 150.0})
    event_bus.publish(test_event)
    
    time.sleep(0.1)
    
    assert len(received_events) == 0

def test_multiple_event_types(event_bus):
    received_price_events = []
    received_order_events = []
    
    def price_callback(event):
        received_price_events.append(event)
    
    def order_callback(event):
        received_order_events.append(event)
    
    event_bus.subscribe(EventType.NEW_PRICE_DATA, price_callback)
    event_bus.subscribe(EventType.ORDER_CREATED, order_callback)
    
    price_event = Event(EventType.NEW_PRICE_DATA, {"symbol": "AAPL", "price": 150.0})
    order_event = Event(EventType.ORDER_CREATED, {"symbol": "AAPL", "quantity": 100})
    
    event_bus.publish(price_event)
    event_bus.publish(order_event)
    
    time.sleep(0.1)
    
    assert len(received_price_events) == 1
    assert len(received_order_events) == 1

def test_event_order(event_bus):
    received_events = []
    
    def callback(event):
        received_events.append(event)
    
    event_bus.subscribe(EventType.NEW_PRICE_DATA, callback)
    
    event1 = Event(EventType.NEW_PRICE_DATA, {"symbol": "AAPL", "price": 150.0})
    event2 = Event(EventType.NEW_PRICE_DATA, {"symbol": "AAPL", "price": 151.0})
    event3 = Event(EventType.NEW_PRICE_DATA, {"symbol": "AAPL", "price": 152.0})
    
    event_bus.publish(event1)
    event_bus.publish(event2)
    event_bus.publish(event3)
    
    time.sleep(0.1)
    
    assert len(received_events) == 3
    assert received_events[0].data["price"] == 150.0
    assert received_events[1].data["price"] == 151.0
    assert received_events[2].data["price"] == 152.0

def test_error_handling(event_bus):
    def callback(event):
        raise Exception("Test exception")
    
    event_bus.subscribe(EventType.NEW_PRICE_DATA, callback)
    
    test_event = Event(EventType.NEW_PRICE_DATA, {"symbol": "AAPL", "price": 150.0})
    
    # This should not raise an exception
    event_bus.publish(test_event)
    
    time.sleep(0.1)
    
    # The event bus should continue running
    assert event_bus._running