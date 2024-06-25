---
Title: Oracle (blockchain)
description:
categories: []
aliases:
---

Oracle API allows you to perform SQL queries over massive volumes of data in the ODF network directly from smart contracts.

It's the first of a kind **optimistic oracle** that enables reproducibility and verifiability of requests without an expensive consensus protocol (more on this [below](#verifiability)).

## Example
Example of the Solidity contract using ODF oracle:

```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.25;

import { OdfRequest, OdfResponse, IOdfClient, CborReader } from "@opendatafabric/contracts/Odf.sol";

// This sample contract makes an ODF oracle query to calculate
// a Canadian province with the most recorded COVID-19 cases
contract TestConsumer {
    using OdfRequest for OdfRequest.Req;
    using OdfResponse for OdfResponse.Res;
    using CborReader for CborReader.CBOR;

    IOdfClient private oracle;
    string public province;
    int public totalCases;

    // Initialize contract with the oracle address
    constructor(address oracleAddr) {
        oracle = IOdfClient(oracleAddr);
    }

    function initiateQuery() public {
        OdfRequest.Req memory req = OdfRequest.init();

        // Specify ID of the dataset(s) we will be querying.
        // Repeat this call for multiple inputs.
        req.dataset(
            "covid19.canada.case-details",
            "did:odf:fed01c8788dc7825dc95dfaa6c67f989b758d3ebcb1efcb9f47ea914470bd1f7f2bbb"
        );

        // Specify an arbitrary complex SQL query.
        // Queries can include even JOINs
        req.sql(
            "with by_provice as ( "
            "  select "
            "    province, "
            "    count(*) as count "
            "  from 'covid19.canada.case-details' "
            "  group by 1 "
            "), "
            "ranked as ( "
            "  select "
            "    row_number() over (order by count desc) as rank, "
            "    province, "
            "    count "
            "  from by_provice "
            ") "
            "select "
            "  province, "
            "  count "
            "from ranked where rank = 1"
        );

        // Send request to the oracle and specify a callback
        oracle.sendRequest(req, this.onResult);
    }

    // This function will be called by the oracle when
    // request is fulfilled by some data provider
    function onResult(OdfResponse.Res memory result) external {
        // Important: Make sure only the ODF oracle can supply you data
        require(msg.sender == address(oracle), "Can only be called by oracle");

        // We expect only one row: [province, totalCases]
        require(result.numRecords() == 1, "Expected one record");

        CborReader.CBOR[] memory record = result.record(0);
        province = record[0].readString();
        totalCases = record[1].readInt();
    }
}
```

## Getting Started
Start by installing [`@opendatafabric/contracts`](https://www.npmjs.com/package/@opendatafabric/contracts) package that contains oracle interface and request/response types.

```sh
npm i @opendatafabric/contracts
```

See the example above for the recommended way of forming requests and decoding results.

More examples, documentation, and tests can be found in the [contracts repository](https://github.com/kamu-data/kamu-contracts).

## Supported Networks

| Network                  | Contract Address                                                                                                                       | Oracle Fee |
| :----------------------- | :------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| Ethereum Mainnet         | *coming soon*                                                                                                                          | 0          |
| Ethereum Sepolia Testnet | [`0xf1960569d1b4a23c34109d9341af6496ed90c0c3`](https://sepolia.etherscan.io/address/0xf1960569d1b4A23c34109D9341Af6496Ed90C0c3#events) | 0          |
| Optimism                 | *coming soon*                                                                                                                          | 0          |

ODF oracle can be deployed on any EVM-compatible chain - you can request network support by filing an issue on the [contracts repository](https://github.com/kamu-data/kamu-contracts).

Oracle contract and all providers currently operate with **zero fees**.

## Verifiability
Every response submitted to the oracle by data providers includes special data that allows the query to be repeated later on the exactly the same version of input data.

In REST API semantics an oracle request looking like this:
```json
{
  "query": "select offset, city, population from populations order by offset desc",
  "dataFormat": "JsonAoA",
  "aliases": [{
    "alias": "populations",
    "id": "did:odf:fed01df230b49615d175307d580c33d6fda61fc7b9aec91df0f5c1a5ebe3b8cbfee02"
  }]
}
```

Will be given a result such as:
```json
{
    "data": [
        [1, "B", 200], 
        [0, "A", 100]
    ],
    "schema": "...",
    "resultHash": "f9680c001200b3483eecc3d5c6b50ee6b8cba11b51c08f89ea1f53d3a334c743199f5fe656e",
    "state": {
        "inputs": [{
            "id": "did:odf:fed01df230b49615d175307d580c33d6fda61fc7b9aec91df0f5c1a5ebe3b8cbfee02",
            "blockHash": "f16204cec6245fadfbf0663b0e9e9a01c73268cc13e29087b33ce3454af08eb4d3e0b",
        }]
    }
}
```

The state information therefore associates every input dataset with the hash of the last block that was considered during the query.

Whenever a provider supplies a response - this state information is recorded in the events emitted by the oracle contract on the blockchain.

This data acts as a **commitment** using which a data consumer can **dispute** results of a query. If another party repeats the same computations using the state data and arrives at different result - this means that the original provider has acted maliciously.

The reproducibility and verifiability of queries therefore make ODF the first of a kind **optimistic oracle** where:
- Queries can be fulfilled fast and cheap just by one provider
- Without going through a complex consensus mechanism
- While validity of data can still be ensured through the dispute resolution and sampling mechanisms along with staking and slashing.

## Registering Your Own Provider
**🚧 Under construction 🚧** - contact us if you'd like to use ODF oracle contract along with your private ODF node.