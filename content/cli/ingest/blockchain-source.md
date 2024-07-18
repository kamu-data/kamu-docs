---
Title: Blockchain Sources
weight: 60
categories: []
aliases:
---

Blockchains, especially those that run smart contracts, have turned into real treasure troves of data and can be viewed as datasets that aggregate millions of smaller datasets within them. Kamu allows you to directly use data from any EVM-compatible blockchain.

Currently we support reading logs, but access to fully reconcilable transaction information is planned.


## Configuring RPC Node
Data is read directly from blockchain nodes, so to ingest data your CLI needs to have the RPC URL configured:

```yaml
kind: CLIConfig
version: 1
content:
  source:
    ethereum:
      rpcEndpoints:
        - chainId: 1
          chainName: Ethereum Mainnet
          nodeUrl: wss://localhost:8545
```

You can also specify `nodeUrl` directly in the {{<schema "FetchStep::EthereumLogs">}} (see below).


## Accessing Specific Log
Logs can be accessed using {{<schema "FetchStep::EthereumLogs">}} ([full example](https://github.com/kamu-data/kamu-cli/blob/master/examples/reth-vs-snp500/net.rocketpool.reth.tokens-minted.yaml)):

```yaml
kind: DatasetSnapshot
version: 1
content:
  name: net.rocketpool.reth.tokens-minted
  kind: Root
  metadata:
    - kind: SetPollingSource
      fetch:
        kind: EthereumLogs
        # Ethereum Mainnet
        # See: https://chainlist.org/
        chainId: 1
        # Optional signature can be used to decode
        # the event into a nested struct
        signature: |
          TokensMinted(
            address indexed to,
            uint256 amount,
            uint256 ethAmount,
            uint256 time
          )
        # Filter by contract address and the deployment
        # block to limit scanning. Syntax is the same as
        # in SQL WHERE clause.
        filter: |
          address = X'ae78736cd615f374d3085123a210448e74fc6393'
          and
          block_number > 13325304
      read:
        kind: Parquet
      preprocess:
        kind: Sql
        engine: datafusion
        query: |
          select
            to_timestamp_seconds(
              cast(event.time as bigint)
            ) as event_time,
            block_number,
            block_hash,
            transaction_index,
            transaction_hash,
            log_index,
            event.to as to,
            event.amount as amount,
            event."ethAmount" as eth_amount
          from input
      merge:
        kind: Append
```

The above source declaration will use `filter` to create the **most efficient RPC request** to the blockchain node and stream the events using .

The output of the `EthereumLogs` fetch step is a data structure that corresponds directly to the output of [`eth_getLogs`](https://ethereum.org/en/developers/docs/apis/json-rpc/#eth_getlogs) endpoint, with the addition of optional decoded `event` field:

| Name                |    Type     | Nullable | Description                                                                                                                  |
| ------------------- | :---------: | :------: | ---------------------------------------------------------------------------------------------------------------------------- |
| `block_number`      |  `uint64`   |          |                                                                                                                              |
| `block_hash`        |  `binary`   |          |                                                                                                                              |
| `block_timestamp`   | `timestamp` |    V     | Many providers [don't yet return](https://github.com/ethereum/execution-apis/issues/295) `blockTimestamp` from `eth_getLogs` |
| `transaction_index` |  `uint64`   |          |                                                                                                                              |
| `transaction_hash`  |  `binary`   |          |                                                                                                                              |
| `log_index`         |  `uint64`   |          |                                                                                                                              |
| `address`           |  `binary`   |          |                                                                                                                              |
| `topic0`            |  `binary`   |    V     |                                                                                                                              |
| `topic1`            |  `binary`   |    V     |                                                                                                                              |
| `topic2`            |  `binary`   |    V     |                                                                                                                              |
| `topic3`            |  `binary`   |    V     |                                                                                                                              |
| `data`              |  `binary`   |          |                                                                                                                              |
| **`event`**         |  `struct`   |          | If `signature` is specified, will contain a decoded version of the event as a nested struct field                            |


## Decoding Raw Logs in SQL
It's also possible to ingest raw logs without decoding them with `signature`.

In this example we read all logs of the specific contract and decode them later in SQL ([full example](https://github.com/kamu-data/kamu-contrib/blob/master/net.rocketpool/reth.mint-burn-2in1.yaml)):

```yaml
kind: DatasetSnapshot
version: 1
content:
  name: net.rocketpool.reth.mint-burn
  kind: Root
  metadata:
    - kind: SetPollingSource
      fetch:
        kind: EthereumLogs
        # Ethereum Mainnet
        # See: https://chainlist.org/
        chainId: 1
        # Read raw logs, filtering by signatures we care about
        filter: |
          address = X'ae78736cd615f374d3085123a210448e74fc6393'
          and (
            topic0 = eth_event_selector(
              'TokensMinted(address indexed to, uint256 amount, uint256 ethAmount, uint256 time)'
            )
            or topic0 = eth_event_selector(
              'TokensBurned(address indexed from, uint256 amount, uint256 ethAmount, uint256 time)'
            )
          )
          and block_number > 13325304
      read:
        kind: Parquet
      preprocess:
        kind: Sql
        engine: datafusion
        query: |
          select
            to_timestamp_seconds(
              cast(json_get_str(event, 'time') as bigint
            ) as event_time,
            block_number,
            block_hash,
            transaction_index,
            transaction_hash,
            log_index,
            json_get_str(event, 'name') as event_name,
            decode(
              coalesce(
                json_get_str(event, 'to'),
                json_get_str(event, 'from')
              ),
              'hex'
            ) as holder_address,
            json_get_str(event, 'amount') as amount,
            json_get_str(event, 'ethAmount') as eth_amount
          from (
            select
              *,
              coalesce(
                eth_try_decode_event(
                  'TokensMinted(address indexed to, uint256 amount, uint256 ethAmount, uint256 time)',
                  topic0,
                  topic1,
                  topic2,
                  topic3,
                  data
                ),
                eth_try_decode_event(
                  'TokensBurned(address indexed from, uint256 amount, uint256 ethAmount, uint256 time)',
                  topic0,
                  topic1,
                  topic2,
                  topic3,
                  data
                )
              ) as event
            from input
          )
      merge:
        kind: Append
```

The above code is using `eth_try_decode_event` function provided by [`datafusion-ethers`](https://github.com/kamu-data/datafusion-ethers) extension to the SQL engine. Upon success this function returns a decoded event as JSON string, which we then take apart using [`datafusion-functions-json`](https://github.com/datafusion-contrib/datafusion-functions-json) set of functions.


## Future Work
Blockchain data satisfies all properties of an ODF dataset (history-preserving, reproducible, verifiable), with differences primarily in encoding. We therefore see Kamu NOT as an indexer (solutions that copy data from blockchains into queryable databases, leading to recentralization concerns). Instead we see **blockchains as a natural extension of the Open Data Fabric network**.

Integrating blockchains as data sources and consumers of data via [Kamu Oracle]({{<relref "oracle">}}) makes Kamu the first system where you can go through the whole cycle (reading on-chain data, merging it with off-chain data, providing data back on-chain to a smart contract) within one solution, with just SQL, with full verifiability.

Our future work will focus on further **erasing the boundary between on- and off-chain data**.
