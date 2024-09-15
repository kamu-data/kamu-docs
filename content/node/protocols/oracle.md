---
Title: Blockchain Oracle
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
| Network                                                          | Contract Address                                                                                                                       | Oracle Fee |
| :--------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| [Ethereum Sepolia Testnet](https://chainlist.org/chain/11155111) | [`0xf1960569d1b4a23c34109d9341af6496ed90c0c3`](https://sepolia.etherscan.io/address/0xf1960569d1b4A23c34109D9341Af6496Ed90C0c3#events) | 0          |
| [BNB Smart Chain Testnet](https://chainlist.org/chain/97)        | [`0x83857865971e941933dd36ebbf9475a867f67ca6`](https://testnet.bscscan.com/address/0x83857865971e941933dd36ebbf9475a867f67ca6#events)  | 0          |
| Ethereum Mainnet                                                 | *coming soon*                                                                                                                          | 0          |
| Optimism                                                         | *coming soon*                                                                                                                          | 0          |

ODF oracle can be deployed on any EVM-compatible chain - you can request network support by filing an issue on the [contracts repository](https://github.com/kamu-data/kamu-contracts).

Oracle contract and all providers currently operate with **zero fees**.


## Verifiability
Every response submitted to the oracle by data providers includes special data that allows the query to be reproduced later against the same exact version of input data.

In REST API semantics an oracle request that looks like this:
```json
{
    "query": "select offset, city, population from populations order by offset desc",
    "queryDialect": "SqlDataFusion",
    "datasets": [{
        "id": "did:odf:fed0119d20360650afd3d412c6b11529778b784c697559c0107d37ee5da61465726c4",
        "alias": "populations"
    }],
    "dataFormat": "JsonAoA",
    "include": ["input"],
}
```

Will be given a result such as:
```json
{
    "input": {
        "query": "select offset, city, population from populations order by offset desc",
        "queryDialect": "SqlDataFusion",
        "dataFormat": "JsonAoA",
        "include": ["Input"],
        "datasets": [{
            "id": "did:odf:fed0119d20360650afd3d412c6b11529778b784c697559c0107d37ee5da61465726c4",
            "alias": "populations",
            "blockHash": "f1620708557a44c88d23c83f2b915abc10a41cc38d2a278e851e5dc6bb02b7e1f9a1a"
        }]
    },
    "output": {
        "data": [
            [1, "B", 200], 
            [0, "A", 100]
        ],
        "dataFormat": "JsonAoa"
    }
}
```

The `input.datasets` block of the response contains state information that associates every input dataset with the hash of the last block that was considered during the query.

Whenever a provider supplies a response - this state information is recorded in the events emitted by the oracle contract on the blockchain.

This data acts as a **commitment** using which a data consumer can **dispute** results of a query. If another party repeats the same computations using the state data and arrives at different result - this means that the original provider has acted maliciously. See [commitments documentation]({{<ref "node/commitments">}}) for details.

The reproducibility and verifiability of queries therefore make ODF the first of a kind **optimistic oracle** where:
- Queries can be fulfilled fast and cheap just by one provider
- Without going through a complex consensus mechanism
- While validity of data can still be ensured through the dispute resolution and sampling mechanisms along with staking and slashing.


## Commitment Properties
Using the criteria discussed in the [commitments documentation]({{<ref "node/commitments">}}) the oracle commitment can be described as follows:
- **Hiding** - NO
  - The entire request and response data is publicly available, but this as an inherent limitation of non-ZK blockchains
- **Binding** - YES
  - All inputs and outputs are immutably stored on-chain
- **Succinct** - YES*
  - All response data ends up stored which we cannot avoid, but the commitment itself does not add much overhead
- **Deterministic** - YES
- **Reproducible** - YES
  - Original query with all of its parameters is stored on-chain and can be repeated against the state information in response
- **Non-repudiable** - YES
  - Automatically achieved as the provider signs the response transaction with its private key
- **Composable** - YES
  - Through recursive nature of the commitment


## Troubleshooting
To better understand what oracle providers return find the incoming oracle transaction in the block explorer e.g. [0x0f3a..4ff6](https://sepolia.etherscan.io/tx/0x0f3af200610ee2a11b13afda14eea808b04cbe012197a352ec95b558bbce4ff6).

Find the `ProvideResults` log:

{{<image filename="/images/node/protocols/oracle-provider-result-data.jpg" alt="ProvideResults event data">}}

Copy the data field and paste it in https://cbor.me/ to get something like this:

{{<image filename="/images/node/protocols/oracle-provider-cbor.jpg" alt="Decoded CBOR data">}}

The first three fields are: `version`, `success`, `data`. Refer to [`OdfResponse`](https://github.com/kamu-data/kamu-contracts/blob/e25e896ede177fdac7d34e9a4a3330094d23cc6f/src/OdfResponse.sol#L9) to understand the layout of the other fields.

Once you have one oracle response - you can use it as input in your unit tests to fully debug the decoding and processing logic without constantly re-deploying the contract and spending a lot of gas.

Here's an example of one such tests in `foundry`:

```solidity
function testResponseDecoding() public pure {
    bytes memory responseBytes = hex"8501F58A826..92AFE32";
    OdfResponse.Res memory res = OdfResponse.fromBytes(0, responseBytes);
    assertEq(res.numRecords(), 10);
    CborReader.CBOR[] memory record = res.record(0);
    string memory voiceId = record[0].readString();
    int256 playtimeTotal = record[1].readInt();
    assertEq(voiceId, "lana-del-rey");
    assertEq(playtimeTotal, 6449);
}
```


## Registering Your Own Provider
**🚧 Under construction 🚧** - contact us if you'd like to use ODF oracle contract along with your private ODF node.
