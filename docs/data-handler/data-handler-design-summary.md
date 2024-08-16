# DataHandler Design Summary

## Architecture
1. Multiple classes, each responsible for a specific aspect of data handling
2. Use interfaces for data sources, data types, and data operations
3. Central configuration file as the main descriptor for the system

## Data Sources
1. Live data: 
   - Candlestick data API
   - Websocket for last trading prices (ticker)
2. Historical data: 
   - Retrieved from a master data store
3. Local data store (SQLite) for all operations

## Data Types
1. Candlestick data
2. Last trading price (ticker data)
3. Standardized internal data format using indian-stocks-api

## Data Operations
1. Cleaning: Handle duplication, missing data
2. Normalization: Standardize data if ingestion errors occur
3. Aggregation: Combine live & historical data for live trading
4. Real-time processing for websocket data
5. Batch processing for candles at 1-minute intervals

## Data Access
1. Common interface for interacting with the local data store
2. Support for time-series operations, latest price, and historical range queries
3. Optimization strategy:
   - Backtest: Fetch 1-minute candles from master store to local store
   - Live trading: 
     - Fetch past x candles from master store to local store
     - Append live candles data at 1-min intervals
     - Update close data at each tick from websocket

## Scalability and Performance
1. Use local data store as a cache
2. Multithreading for fetching candles data

## Error Handling
1. Implement retries and system HALT for critical errors
2. Logging for debugging and monitoring

## Event Generation
1. Asynchronous event generation

## Modes of Operation
1. Support for live trading, backtesting, and paper trading