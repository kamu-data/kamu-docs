---
Title: Oracle (blockchain)
description:
categories: []
aliases:
---

**🚧 This page is under construction 🚧**

Please refer to [`kamu-contracts`](https://github.com/kamu-data/kamu-contracts) repository for examples of using ODF oracle contract.

Example of the Solidity contract using ODF oracle:

```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.25;

import { OdfRequest, OdfResponse, IOdfClient } from "@kamu-data/contracts/Odf.sol";

contract Consumer {
    using OdfRequest for OdfRequest.Req;
    using OdfResponse for OdfResponse.Res;

    IOdfClient private oracle;

    string public province;
    uint64 public totalCases;

    constructor(address oracleAddr) {
        oracle = IOdfClient(oracleAddr);
    }

    modifier onlyOracle() {
        assert(msg.sender == address(oracle));
        _;
    }

    function requestTopProvinceByCovidCases() public {
        OdfRequest.Req memory req = OdfRequest.init();
        req.sql(
            "with by_provice as ("
            "select province, count(*) as count "
            "from 'kamu/covid19.canada.case-details' "
            "group by 1"
            "), "
            "ranked as ("
            "select row_number() over (order by count desc) as rank, province, count "
            "from by_provice"
            ") "
            "select province, count from ranked where rank = 1"
        );
        oracle.sendRequest(req, this.onResult);
    }

    function onResult(OdfResponse.Res memory result) external onlyOracle {
        assert(result.numRecords() == 1);
        CborReader.CBOR[] memory record = result.record(0);
        province = record[0].readString();
        totalCases = uint64(int64(record[1].readInt()));
    }
}

```