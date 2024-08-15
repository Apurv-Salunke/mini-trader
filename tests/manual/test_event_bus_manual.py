# test_event_bus_manual.py

import time
from src.mini_trader.event_bus.bus import EventBus
from src.mini_trader.event_bus.event import Event, EventType

def price_update_callback(event: Event):
    print(f"Received price update: {event.data['price']} for {event.data['symbol']}")

def order_filled_callback(event: Event):
    print(f"Order filled: {event.data['order_id']} for {event.data['quantity']} shares of {event.data['symbol']}")

def main():
    # Create an instance of EventBus
    event_bus = EventBus()

    # Subscribe to events
    event_bus.subscribe(EventType.NEW_PRICE_DATA, price_update_callback)
    event_bus.subscribe(EventType.ORDER_FILLED, order_filled_callback)

    # Start the event bus
    event_bus.start()

    # Publish some events
    event_bus.publish(Event(EventType.NEW_PRICE_DATA, {"symbol": "AAPL", "price": 150.25}))
    event_bus.publish(Event(EventType.ORDER_FILLED, {"order_id": "12345", "symbol": "GOOGL", "quantity": 100}))
    event_bus.publish(Event(EventType.NEW_PRICE_DATA, {"symbol": "MSFT", "price": 280.75}))

    # Wait for a moment to allow events to be processed
    time.sleep(2)

    # Stop the event bus
    event_bus.stop()

if __name__ == "__main__":
    main()