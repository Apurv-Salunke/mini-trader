# DataHandler Brainstorming Session

## 1. Core Concepts

- What is the primary purpose of the DataHandler?
- How should it fit into the overall system architecture?
- Should it be a single class or a collection of related classes?
    - Multiple classes, each responsible for a specific aspect of data handling.
    - Follow good design principles here.

## 2. Data Sources

- What types of data sources do we need to support? (e.g., real-time feeds, historical databases, CSV files)
    - Live data sources
        - Candlestick data API for live data. 
        - Websocket for last trading prices(ticker).
            - Websockets to be started for instruments in obervable list only.
            - Therefore Websockets interface will change the observable instruments in the runtime for the live data.
    - Historical data sources
        - Should be retrieved from a master data store which is already created and servers as an API.
        - on historical data we dont have ticker data we only have candles data. 
    - Additional remarks: Ideal is to keep a local data store (sqlite) for all operations related to the system. It will pre-populate the data store with the data from the master data store before the system starts (both for backtest and live trading).
- How can we design for easy addition of new data sources in the future?
    - Use an interface for data sources.
        - For historical data sources, we can use it to interact with the master data store.
        - For live data sources, we can use it to interact with the live data feed.
    - Additional remarks: We have a python package which interfaces as common wrapper for all the brokers in indian stock market called 'indian-stocks-api'. We can use it to interact with the live data feed.
- Should we support multiple simultaneous data sources?
    - Simultaneous data sources are not supported.
    - multiple symbols would be fetched though from the same data source.
    - Additional remarks: We can use a queue to store the data from the live data feed and process it in a separate thread (just a thought but clever ways like this needs to be explored).

## 3. Data Types

- What types of financial data do we need to handle? (e.g., tick data, OHLCV, order book data, fundamental data)
    - Candlestick data
    - Last trading price (ticker data)
    - Order book data/depth data (not required for now)
    - Fundamental data (not required for now)
    - Market events data (not required for now)
    - News data (not required for now)
- How can we design a flexible system to accommodate different data types?
    - Use an interface for data types.
    - Each will have its own resposibility to handle the data.
- Should we have a standardized internal data format?
    - Yes, we should have a standardized internal data format.
    - for candlestic data, we get standaardized data from the indian-stocks-api.
    - for ticker data, we get standaardized data from the indian-stocks-api.
    - for websocket data, we get standaardized data from the indian-stocks-api.
    - for histroical data, we get standaardized data from the master data store.


## 4. Data Operations

- What operations do we need to perform on the data? (e.g., cleaning, normalization, aggregation)
    - Cleaning: for any duplication,  missing data, etc.
    - Normalization: for any standardization of the data if any error in ingestion.
    - Aggregation: 
        - for any aggregation of the from live & historical sources for the live trading.
        - We will fetch the data from the master data store and combine it will current data for live trading, saving us API calls to the broker.
- How can we make these operations configurable and extensible?
    - Use an interface for data operations.
    - Use a common configurations file which will act as a main discriptor for the system.
- Should data processing be done in real-time or in batches?
    - Data processing should be done in real-time & batches as well.
        - websocket will be real-time.
        - candles will be done in batches at 1 minute intervals.

## 5. Data Access Patterns

- How will other components of the system interact with the DataHandler?
    - DataHandler will be a part of the system and will be used by other components of the system.
    - DataHandler will act as a common interface for all the data needs throughout the system.
- What query patterns do we need to support? (e.g., latest price, historical range, time-series operations)
    - time-series operations.
    - laest price.
    - historical range.
    - additonal remarks: We need a common interface for interacting will the local data store.
- How can we optimize for both real-time and historical data access?
    - Bactest:
        - Fetch the 1 minute candles from the master data store and store it in the local data store.
    - Live trading:
        - Fetch the 1 minute candles from the master data store and store it in the local data store for past x candles.
        - start appending data from the live data sources.
            - append live candles data at 1 mins interval.
            - update the close data at each tick recieved from the websocket.
        

## 6. Scalability and Performance

- How can we design the DataHandler to handle large volumes of data efficiently?
    - Use of local data store will solve the problem at some extent.
    - We will accept these limitations for now. 
- Should we implement caching mechanisms? If so, at what level?
    - local data store will act as a cache for the data.
- How can we minimize latency for real-time data handling?
    - websocket will be real-time.
    - candles data would be fetched by muiltithreading.

## 7. Fault Tolerance and Error Handling

- How should the DataHandler handle data source outages or errors?
    - We will think of this post initial developemt (1st focus of POC developement) 
    - We will wait for some time & add retries wherever needed, but we will HALT the system if any erros occur.
- What types of data quality checks should we implement?
    - duplciate data, missing data, etc.
- How can we design for easy debugging and monitoring?
    - We will use logging to log the errors.
    - Later will add some realtime system to monitor the system (not required for now).

## 8. Event Generation

- What types of events should the DataHandler generate?
- How can we make event generation configurable and extensible?
- Should event generation be synchronous or asynchronous?
    - asynchronous, a lot of operations are happening at data handler therefore they need to happen simulataneously.

## 9. Configuration and Flexibility

- What aspects of the DataHandler should be configurable?
- How can we design for easy testing and simulation?
- Should we support different modes of operation (e.g., live trading, backtesting, paper trading)?
    - Yes offcourse, thats the whole point.

## 10. Integration with Other Components

- How will the DataHandler interact with other system components (e.g., Strategy, Portfolio, Risk Management)?
- Should the DataHandler be aware of the trading system's state?
- How can we design for loose coupling while ensuring efficient data flow?