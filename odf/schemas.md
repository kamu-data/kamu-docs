---
# !!! THIS FILE IS AUTO-GENERATED - DO NOT MODIFY MANUALLY !!!
title: Schemas
description: Schemas of common metadata objects
---

import {Diagram, Term, Schema, YouTube, YouTubeList} from '/components/common.jsx'

## Auth
### `Account`
Registers an account in an predefined account provider.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `$schema` | `string` | ✔️ | `type-uri` | Identifies this resource type. |
| `headers` | [`ResourceHeadersInput`](#resourceheadersinput) | ✔️ |  | Container for identity and ownership information of a resource. |
| `spec` | [`AccountSpecInput`](#accountspecinput) | ✔️ |  | Specifies the desired state of the resource. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/auth/v1alpha1/Account.json)

### `AccountHandle`
Link to an account.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `id` | `string` | ✔️ | `resource-id` | ID of the account resource. |
| `did` | `string` | ✔️ | `account-id` | DID of the account. |
| `name` | `string` | ✔️ | `account-name` | Name of the account. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/auth/v1alpha1/AccountHandle.json)

### `AccountRef`


| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `id` | `string` |  | `resource-id` | UUID of the account resource. |
| `did` | `string` |  | `account-id` | DID of the account. |
| `name` | `string` |  | `account-name` | Name of the account. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/auth/v1alpha1/AccountRef.json)

### `AccountSpec`
Predefined account specification.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `did` | `string` |  | `account-id` | DID associated with the account by ODF or an external system |
| `accountType` | [`AccountType`](#accounttype) |  |  | Type of the account.<br/><br/>Default: `User` |
| `displayName` | `string` |  |  | Human-friendly display name. |
| `email` | `string` | ✔️ | `email` | Email address of the account. |
| `avatarUrl` | `string` |  | `uri` | URL of the account's avatar image. |
| `password` | [`Secret`](#secret) |  |  | Password for local authentication. Absent for SSO or DID-based accounts. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/auth/v1alpha1/AccountSpec.json)

### `AccountSpecInput`
Predefined account specification.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `did` | `string` |  | `account-id` | DID associated with the account by ODF or an external system |
| `accountType` | [`AccountType`](#accounttype) |  |  | Type of the account.<br/><br/>Default: `User` |
| `displayName` | `string` |  |  | Human-friendly display name. |
| `email` | `string` | ✔️ | `email` | Email address of the account. |
| `avatarUrl` | `string` |  | `uri` | URL of the account's avatar image. |
| `password` | [`Secret`](#secret) |  |  | Password for local authentication. Absent for SSO or DID-based accounts. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/auth/v1alpha1/AccountSpecInput.json)

### `AccountType`
Represents the type of an account.

| Enum Value |
| :---: |
| `User` |
| `Organization` |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/auth/v1alpha1/AccountType.json)

### `Group`
A named group of accounts. Members are assigned via the `Member` relation. Groups can be granted roles on resources, allowing permissions to be managed at the group level rather than per-account.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `$schema` | `string` | ✔️ | `type-uri` | Identifies this resource type. |
| `headers` | [`ResourceHeadersInput`](#resourceheadersinput) | ✔️ |  | Container for identity and ownership information of a resource. |
| `spec` | [`GroupSpecInput`](#groupspecinput) | ✔️ |  | Specifies the desired state of the resource. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/auth/v1alpha1/Group.json)

### `GroupSpec`
Group specification. Groups have no intrinsic properties — membership and permissions are expressed entirely through relations.

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/auth/v1alpha1/GroupSpec.json)

### `GroupSpecInput`
Group specification. Groups have no intrinsic properties — membership and permissions are expressed entirely through relations.

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/auth/v1alpha1/GroupSpecInput.json)

### `Member`
Declares an account as a member of a group. Membership is binary — no value is carried by this relation.

_Type: `null`_

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/auth/v1alpha1/Member.json)

### `Relation`
A directed relationship between two resources, optionally carrying a typed value.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `subject` | [`ResourceHandle`](#resourcehandle) | ✔️ |  | The resource that holds the relation. |
| `relation` | `string` | ✔️ |  | Name of the relation e.g. `role`, `member`, `owner`. |
| `value` | `object` |  |  | Optional value associated with the relation e.g. `maintainer` for a `role` relation. |
| `object` | [`ResourceHandle`](#resourcehandle) | ✔️ |  | The resource that is the target of the relation. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/auth/v1alpha1/Relation.json)

### `RelationInput`
A directed relationship between two resources, optionally carrying a typed value.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `subject` | [`ResourceRef`](#resourceref) | ✔️ |  | The resource that holds the relation. |
| `relation` | `string` | ✔️ |  | Name of the relation e.g. `role`, `member`, `owner`. |
| `value` | `object` |  |  | Optional value associated with the relation e.g. `maintainer` for a `role` relation. |
| `object` | [`ResourceRef`](#resourceref) | ✔️ |  | The resource that is the target of the relation. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/auth/v1alpha1/RelationInput.json)

### `Relations`
Specified relations between resources on which auth policies act upon.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `$schema` | `string` | ✔️ | `type-uri` | Identifies this resource type. |
| `headers` | [`ResourceHeadersInput`](#resourceheadersinput) | ✔️ |  | Container for identity and ownership information of a resource. |
| `spec` | [`RelationsSpecInput`](#relationsspecinput) | ✔️ |  | Specifies the desired state of the resource. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/auth/v1alpha1/Relations.json)

### `RelationsSpec`
Specifies relations between resources on which auth policies act upon.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `relations` | `array(`[`Relation`](#relation)`)` | ✔️ |  | Relations between resources. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/auth/v1alpha1/RelationsSpec.json)

### `RelationsSpecInput`
Specifies relations between resources on which auth policies act upon.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `relations` | `array(`[`RelationInput`](#relationinput)`)` |  |  | Relations between resources. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/auth/v1alpha1/RelationsSpecInput.json)

## Config
### `Secret`


| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `value` | `string` | ✔️ |  | A secret value in raw or encoded form. |
| `contentEncoding` | `string` |  |  | Represents the encoding of the value. Typically will be `jwe` after a raw secret gets encrypted. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/config/v1alpha1/Secret.json)

### `SecretSet`
Defines a set of secrets stored and managed by the ODF node.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `$schema` | `string` | ✔️ | `type-uri` | Identifies this resource type. |
| `headers` | [`ResourceHeadersInput`](#resourceheadersinput) | ✔️ |  | Container for identity and ownership information of a resource. |
| `spec` | [`SecretSetSpecInput`](#secretsetspecinput) | ✔️ |  | Specifies the desired state of the secret set. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/config/v1alpha1/SecretSet.json)

### `SecretSetSpec`
Defines a set of secrets stored and managed by the ODF node and accessible via embedded sercets provider.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `secrets` | [`Secrets`](#secrets) | ✔️ |  | Key value pairs of secrets. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/config/v1alpha1/SecretSetSpec.json)

### `SecretSetSpecInput`
Defines a set of secrets stored and managed by the ODF node and accessible via embedded sercets provider.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `secrets` | [`Secrets`](#secrets) | ✔️ |  | Key value pairs of secrets. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/config/v1alpha1/SecretSetSpecInput.json)

### `Secrets`
Container for key-value secrets. Every key must be a string. Values may be strings with raw unencrypted data or objects that signify the encoding.

_Map of string keys to arbitrary values._

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/config/v1alpha1/Secrets.json)

### `ValueHandle`
Reference to a value within a `VariableSet` or a `SecretSet`.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `account` | [`AccountHandle`](#accounthandle) | ✔️ |  | Account that owns the target resource. |
| `type` | `string` | ✔️ | `type-uri` | Type URI of the target resource. |
| `id` | `string` | ✔️ | `resource-id` | ID of the resource within a node. |
| `name` | `string` | ✔️ | `resource-name` | Name of a resource. |
| `path` | `string` |  |  | JSON path to a value within a `VariableSet` or a `SecretSet`. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/config/v1alpha1/ValueHandle.json)

### `ValueRef`


| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `account` | [`AccountRef`](#accountref) |  |  | Reference to an account that owns the `VariableSet` or the `SecretSet`. |
| `id` | `string` |  | `resource-id` | ID of a resource. |
| `type` | `string` |  | `type-ref` | Short type name or full type URI of the target resource. |
| `name` | `string` |  | `resource-name` | Name of a resource. |
| `path` | `string` |  |  | JSON path to a value within a `VariableSet` or a `SecretSet`. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/config/v1alpha1/ValueRef.json)

### `ValueRefs`
Container for key-value variables. Every key must be a string. Values shoud reference fields in `SecretSet`s and `VariableSet`s.

_Map of string keys to arbitrary values._

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/config/v1alpha1/ValueRefs.json)

### `Variable`


| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `value` | `string` | ✔️ |  | A value in raw or encoded form. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/config/v1alpha1/Variable.json)

### `VariableSet`
Defines a set of variables stored and managed by the ODF node.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `$schema` | `string` | ✔️ | `type-uri` | Identifies this resource type. |
| `headers` | [`ResourceHeadersInput`](#resourceheadersinput) | ✔️ |  | Container for identity and ownership information of a resource. |
| `spec` | [`VariableSetSpecInput`](#variablesetspecinput) | ✔️ |  | Specifies the desired state of the variable set. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/config/v1alpha1/VariableSet.json)

### `VariableSetSpec`
Defines a set of variables stored and managed by the ODF node and accessible via embedded variables provider.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `variables` | [`Variables`](#variables) | ✔️ |  | Key value pairs of variables. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/config/v1alpha1/VariableSetSpec.json)

### `VariableSetSpecInput`
Defines a set of variables stored and managed by the ODF node and accessible via embedded variables provider.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `variables` | [`Variables`](#variables) | ✔️ |  | Key value pairs of variables. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/config/v1alpha1/VariableSetSpecInput.json)

### `Variables`
Container for key-value variables. Every key must be a string. Values may be raw strings or objects that incorporate the encoding.

_Map of string keys to arbitrary values._

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/config/v1alpha1/Variables.json)

## Data
### `DataField`
Represents a named field (column) in a root or nested struct schema

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `name` | `string` | ✔️ |  | Name of the field |
| `type` | [`DataType`](#datatype) | ✔️ |  | Logical type of the field that defines its semantic behavior and value ranges |
| `extra` | [`ExtraAttributes`](#extraattributes) |  |  | ODF extensions |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/data/v1alpha1/DataField.json)

### `DataSchema`
This schema aims to be a human-friendly variant of Arrow. Arrow currently specifies only the [flatbuffer format](https://github.com/apache/arrow/blob/f9301c0ba8a7ed1b0b63275cfdd4c44c26b04675/format/Schema.fbs) which has many legacy to it and is not suited to be defined by humans, so we had to define our own schema format. While inspired by Arrow - this format makes a clear separation between logical data types and encoding (physical layout) of data in the chunks.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `fields` | `array(`[`DataField`](#datafield)`)` | ✔️ |  | Top-level fields (columns) of the schema. |
| `extra` | [`ExtraAttributes`](#extraattributes) |  |  | ODF extensions |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/data/v1alpha1/DataSchema.json)

### `DataType`
Defines a logical type of the field. Logical type determines the semantics and boudaries of a type and how it can be operated on, without a concern about encoding and physical layout of the data in chunks.

| Union Type | Description |
| --- | --- |
| [`DataType::Binary`](#datatypebinary) | A sequence of bytes. Used for arbitrary binary data. |
| [`DataType::Bool`](#datatypebool) | A boolean value representing true or false. |
| [`DataType::Date`](#datatypedate) | A calendar date. |
| [`DataType::Decimal`](#datatypedecimal) | A fixed-point decimal number with a specified precision and scale. |
| [`DataType::Duration`](#datatypeduration) | An elapsed time interval with a specified time unit. |
| [`DataType::Float16`](#datatypefloat16) | A floating-point number. |
| [`DataType::Float32`](#datatypefloat32) | A floating-point number. |
| [`DataType::Float64`](#datatypefloat64) | A floating-point number. |
| [`DataType::Int8`](#datatypeint8) | An integer value. |
| [`DataType::Int16`](#datatypeint16) | An integer value. |
| [`DataType::Int32`](#datatypeint32) | An integer value. |
| [`DataType::Int64`](#datatypeint64) | An integer value. |
| [`DataType::UInt8`](#datatypeuint8) | An integer value. |
| [`DataType::UInt16`](#datatypeuint16) | An integer value. |
| [`DataType::UInt32`](#datatypeuint32) | An integer value. |
| [`DataType::UInt64`](#datatypeuint64) | An integer value. |
| [`DataType::List`](#datatypelist) | A list of values, all having the same data type. |
| [`DataType::Map`](#datatypemap) | A map of key-value pairs, represented as a list of entries (structs with key and value fields). |
| [`DataType::Null`](#datatypenull) | A type representing the absence of a value (null). |
| [`DataType::Option`](#datatypeoption) | A type representing an optional (nullable) value of another data type. |
| [`DataType::Struct`](#datatypestruct) | A collection of named fields, each with its own data type. |
| [`DataType::Time`](#datatypetime) | A time of day value, without a date, with a specified unit of granularity. |
| [`DataType::Timestamp`](#datatypetimestamp) | A point in time, represented as an offset from the Unix epoch in a specific timezone. |
| [`DataType::String`](#datatypestring) | A Unicode string. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/data/v1alpha1/DataType.json)

### `DataType::Binary`
A sequence of bytes. Used for arbitrary binary data.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `fixedLength` | `integer` |  | `uint64` | Number of bytes per value for fixed-size binary. If omitted, the binary is variable-length. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/data/v1alpha1/DataType.json)

### `DataType::Bool`
A boolean value representing true or false.

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/data/v1alpha1/DataType.json)

### `DataType::Date`
A calendar date.

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/data/v1alpha1/DataType.json)

### `DataType::Decimal`
A fixed-point decimal number with a specified precision and scale.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `precision` | `integer` | ✔️ | `uint32` | Total number of decimal digits that can be stored. |
| `scale` | `integer` | ✔️ | `int32` | Number of digits after the decimal point. In certain situations, scale could be negative number. For negative scale, it is the number of padding 0 to the right of the digits.<br/><br/>For example the number 12300 could be treated as a decimal has precision 3 and scale -2. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/data/v1alpha1/DataType.json)

### `DataType::Duration`
An elapsed time interval with a specified time unit.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `unit` | [`TimeUnit`](#timeunit) |  |  | The unit of the duration measurement.<br/><br/>Default: `Millisecond` |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/data/v1alpha1/DataType.json)

### `DataType::Float16`
A floating-point number.

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/data/v1alpha1/DataType.json)

### `DataType::Float32`
A floating-point number.

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/data/v1alpha1/DataType.json)

### `DataType::Float64`
A floating-point number.

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/data/v1alpha1/DataType.json)

### `DataType::Int8`
An integer value.

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/data/v1alpha1/DataType.json)

### `DataType::Int16`
An integer value.

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/data/v1alpha1/DataType.json)

### `DataType::Int32`
An integer value.

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/data/v1alpha1/DataType.json)

### `DataType::Int64`
An integer value.

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/data/v1alpha1/DataType.json)

### `DataType::UInt8`
An integer value.

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/data/v1alpha1/DataType.json)

### `DataType::UInt16`
An integer value.

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/data/v1alpha1/DataType.json)

### `DataType::UInt32`
An integer value.

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/data/v1alpha1/DataType.json)

### `DataType::UInt64`
An integer value.

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/data/v1alpha1/DataType.json)

### `DataType::List`
A list of values, all having the same data type.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `itemType` | [`DataType`](#datatype) | ✔️ |  | Data type of list items. |
| `fixedLength` | `integer` |  | `uint64` | Number of list items per value for fixed-size lists. If omitted, the list is variable-length. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/data/v1alpha1/DataType.json)

### `DataType::Map`
A map of key-value pairs, represented as a list of entries (structs with key and value fields).

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `keyType` | [`DataType`](#datatype) | ✔️ |  | Data type of the map's keys. |
| `valueType` | [`DataType`](#datatype) | ✔️ |  | Data type of the map's values. |
| `keysSorted` | `boolean` |  |  | Set to true if the keys within each value are sorted. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/data/v1alpha1/DataType.json)

### `DataType::Null`
A type representing the absence of a value (null).

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/data/v1alpha1/DataType.json)

### `DataType::Option`
A type representing an optional (nullable) value of another data type.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `inner` | [`DataType`](#datatype) | ✔️ |  | Inner data type for the optional value. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/data/v1alpha1/DataType.json)

### `DataType::Struct`
A collection of named fields, each with its own data type.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `fields` | `array(`[`DataField`](#datafield)`)` | ✔️ |  | Fields that make up the struct. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/data/v1alpha1/DataType.json)

### `DataType::Time`
A time of day value, without a date, with a specified unit of granularity.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `unit` | [`TimeUnit`](#timeunit) |  |  | The unit of the time value.<br/><br/>Default: `Millisecond` |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/data/v1alpha1/DataType.json)

### `DataType::Timestamp`
A point in time, represented as an offset from the Unix epoch in a specific timezone.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `unit` | [`TimeUnit`](#timeunit) |  |  | The unit of the timestamp value that determines its precision.<br/><br/>Default: `Millisecond` |
| `timezone` | `string` |  |  | The timezone is an optional string indicating the name of a timezone<br/>one of<br/><br/>* As used in the Olson timezone database (the "tz database" or<br/>  "tzdata"), such as "America/New_York".<br/>* An absolute timezone offset of the form "+XX:XX" or "-XX:XX",<br/>  such as "+07:30".<br/><br/>Default: `UTC` |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/data/v1alpha1/DataType.json)

### `DataType::String`
A Unicode string.

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/data/v1alpha1/DataType.json)


### `ExtraAttributes`
Container for custom key-value extension attributes. Every key must be in the form of `<domain>/<path>` (e.g. `kamu.dev/archetype`) in order to fully disambiguate the value in the face of multiple extensions. Values may be any valid JSON including nested objects.

_Map of string keys to arbitrary values._

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/data/v1alpha1/ExtraAttributes.json)

### `OperationType`
Defines an operation in a changelog stream.

| Enum Value |
| :---: |
| `Append` |
| `Retract` |
| `CorrectFrom` |
| `CorrectTo` |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/data/v1alpha1/OperationType.json)

### `TimeUnit`
Defines the unit of measurement of time

| Enum Value |
| :---: |
| `Second` |
| `Millisecond` |
| `Microsecond` |
| `Nanosecond` |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/data/v1alpha1/TimeUnit.json)

## Dataset
### `AddData`
Indicates that data has been ingested into a root dataset.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `prevCheckpoint` | `string` |  | [`multihash`](https://github.com/multiformats/multihash) | Hash of the checkpoint file used to restore ingestion state, if any. |
| `prevOffset` | `integer` |  | `uint64` | Last offset of the previous data slice, if any. Must be equal to the last non-empty `newData.offsetInterval.end`. |
| `newData` | [`DataSlice`](#dataslice) |  |  | Describes output data written during this transaction, if any. |
| `newCheckpoint` | [`Checkpoint`](#checkpoint) |  |  | Describes checkpoint written during this transaction, if any. If an engine operation resulted in no updates to the checkpoint, but checkpoint is still relevant for subsequent runs - a hash of the previous checkpoint should be specified. |
| `newWatermark` | `string` |  | [`date-time`](https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.7.3.1) | Last watermark of the output data stream, if any. Initial blocks may not have watermarks, but once watermark is set - all subsequent blocks should either carry the same watermark or specify a new (greater) one. Thus, watermarks are monotonically non-decreasing. |
| `newSourceState` | [`SourceState`](#sourcestate) |  |  | The state of the source the data was added from to allow fast resuming. If the state did not change but is still relevant for subsequent runs it should be carried, i.e. only the last state per source is considered when resuming. |
| `extra` | [`ExtraAttributes`](#extraattributes) |  |  | ODF extensions. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/dataset/v1alpha1/AddData.json)

### `AllowAnonymousRead`
Controls whether the dataset is readable by users who did not authenticate. Materialized into the ReBAC attribute store by the controller.

_Type: `boolean`_

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/dataset/v1alpha1/AllowAnonymousRead.json)

### `AllowPublicRead`
Controls whether the dataset is readable by any authenticated user. Materialized into the ReBAC attribute store by the Dataset controller.

_Type: `boolean`_

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/dataset/v1alpha1/AllowPublicRead.json)

### `AttachmentEmbedded`
Embedded attachment item.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `path` | `string` | ✔️ |  | Path to an attachment if it was materialized into a file. |
| `content` | `string` | ✔️ |  | Content of the attachment. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/dataset/v1alpha1/AttachmentEmbedded.json)

### `Attachments`
Defines the source of attachment files.

| Union Type | Description |
| --- | --- |
| [`Attachments::Embedded`](#attachmentsembedded) | For attachments that are specified inline and are embedded in the metadata. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/dataset/v1alpha1/Attachments.json)

### `Attachments::Embedded`
For attachments that are specified inline and are embedded in the metadata.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `items` | `array(`[`AttachmentEmbedded`](#attachmentembedded)`)` | ✔️ |  | List of embedded items. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/dataset/v1alpha1/Attachments.json)


### `Checkpoint`
Describes a checkpoint produced by an engine

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `physicalHash` | `string` | ✔️ | [`multihash`](https://github.com/multiformats/multihash) | Hash sum of the checkpoint file. |
| `size` | `integer` | ✔️ | `uint64` | Size of checkpoint file in bytes. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/dataset/v1alpha1/Checkpoint.json)

### `CompactionParams`
Optional parameters to control ingestion behavior.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `maxSliceSize` | `string` |  | `byte-size` | Target maximum size of each compacted data slice e.g. `100MiB`. |
| `maxSliceRecords` | `integer` |  | `uint64` | Target maximum number of records per compacted data slice. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/dataset/v1alpha1/CompactionParams.json)

### `DataSlice`
Describes a slice of data added to a dataset or produced via transformation

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `logicalHash` | `string` | ✔️ | [`multihash`](https://github.com/multiformats/multihash) | Logical hash sum of the data in this slice. |
| `physicalHash` | `string` | ✔️ | [`multihash`](https://github.com/multiformats/multihash) | Hash sum of the data part file. |
| `offsetInterval` | [`OffsetInterval`](#offsetinterval) | ✔️ |  | Data slice produced by the transaction. |
| `size` | `integer` | ✔️ | `uint64` | Size of data file in bytes. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/dataset/v1alpha1/DataSlice.json)

### `Dataset`
Represents a desired state of a dataset.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `$schema` | `string` | ✔️ | `type-uri` | Identifies this resource type. |
| `headers` | [`ResourceHeadersInput`](#resourceheadersinput) | ✔️ |  | Container for identity and ownership information of a resource. |
| `spec` | [`DatasetSpecInput`](#datasetspecinput) | ✔️ |  | Specifies the desired state of the resource. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/dataset/v1alpha1/Dataset.json)

### `DatasetHandle`
Link to a dataset.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `account` | [`AccountHandle`](#accounthandle) |  |  | Reference to an account that owns the dataset. |
| `id` | `string` | ✔️ | `resource-id` | ID of the dataset resource. |
| `did` | `string` | ✔️ | `dataset-id` | DID of the dataset. |
| `name` | `string` | ✔️ | `resource-name` | Name of the dataset. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/dataset/v1alpha1/DatasetHandle.json)

### `DatasetKind`
Represents type of the dataset.

| Enum Value |
| :---: |
| `Root` |
| `Derivative` |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/dataset/v1alpha1/DatasetKind.json)

### `DatasetRef`


| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `account` | [`AccountRef`](#accountref) |  |  | Reference to an account that owns the dataset. |
| `id` | `string` |  | `resource-id` | UUID of the dataset resource. |
| `did` | `string` |  | `dataset-id` | DID of the dataset. |
| `name` | `string` |  | `resource-name` | Name of the dataset. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/dataset/v1alpha1/DatasetRef.json)

### `DatasetRole`
Access role granted to a subject on a dataset. Note: in future this fixed enum schema will likely be replaced by a reference to a `DatasetRole` resources that defines granular permissions on different actions available on a dataset.

| Enum Value |
| :---: |
| `Reader` |
| `Editor` |
| `Maintainer` |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/dataset/v1alpha1/DatasetRole.json)

### `DatasetSelector`


| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `account` | [`AccountRef`](#accountref) |  |  | Reference to an account that owns the target resources. |
| `id` | `string` |  | `resource-id` | ID of the singular resource. |
| `name` | `string` |  |  | Name pattern in SQL `LIKE` format. |
| `labels` | [`LabelFilter`](#labelfilter) |  |  | Filter by resource labels. |
| `kind` | [`DatasetKind`](#datasetkind) |  |  | Restricts the selector to datasets of a specific kind. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/dataset/v1alpha1/DatasetSelector.json)

### `DatasetSpec`
Represents a desired state of the dataset metadata.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `did` | `string` | ✔️ | `dataset-id` | DID of the dataset in global ODF network |
| `kind` | [`DatasetKind`](#datasetkind) | ✔️ |  | Type of the dataset. |
| `metadata` | `array(`[`MetadataEvent`](#metadataevent)`)` | ✔️ |  | An array of metadata events that will be used to populate the chain. Here you can define polling and push sources, set licenses, add attachments etc. |
| `volume` | [`ResourceHandle`](#resourcehandle) | ✔️ |  | Reference to a storage volume where dataset data will be stored. If omitted, the node's default storage is used. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/dataset/v1alpha1/DatasetSpec.json)

### `DatasetSpecInput`
Represents a desired state of the dataset metadata.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `did` | `string` |  | `dataset-id` | DID of the dataset in global ODF network |
| `kind` | [`DatasetKind`](#datasetkind) | ✔️ |  | Type of the dataset. |
| `metadata` | `array(`[`MetadataEvent`](#metadataevent)`)` | ✔️ |  | An array of metadata events that will be used to populate the chain. Here you can define polling and push sources, set licenses, add attachments etc. |
| `volume` | [`PersistentVolumeRef`](#persistentvolumeref) |  |  | Reference to a storage volume where dataset data will be stored. If omitted, the node's default storage is used. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/dataset/v1alpha1/DatasetSpecInput.json)

### `DatasetVocabulary`
Specifies the mapping of system columns onto dataset schema.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `offsetColumn` | `string` |  |  | Name of the offset column.<br/><br/>Default: `offset` |
| `operationTypeColumn` | `string` |  |  | Name of the operation type column.<br/><br/>Default: `op` |
| `systemTimeColumn` | `string` |  |  | Name of the system time column.<br/><br/>Default: `system_time` |
| `eventTimeColumn` | `string` |  |  | Name of the event time column.<br/><br/>Default: `event_time` |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/dataset/v1alpha1/DatasetVocabulary.json)

### `ExecuteTransform`
Indicates that derivative transformation has been performed.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `queryInputs` | `array(`[`ExecuteTransformInput`](#executetransforminput)`)` | ✔️ |  | Defines inputs used in this transaction. Slices corresponding to every input dataset must be present. |
| `prevCheckpoint` | `string` |  | [`multihash`](https://github.com/multiformats/multihash) | Hash of the checkpoint file used to restore transformation state, if any. |
| `prevOffset` | `integer` |  | `uint64` | Last offset of the previous data slice, if any. Must be equal to the last non-empty `newData.offsetInterval.end`. |
| `newData` | [`DataSlice`](#dataslice) |  |  | Describes output data written during this transaction, if any. |
| `newCheckpoint` | [`Checkpoint`](#checkpoint) |  |  | Describes checkpoint written during this transaction, if any. If an engine operation resulted in no updates to the checkpoint, but checkpoint is still relevant for subsequent runs - a hash of the previous checkpoint should be specified. |
| `newWatermark` | `string` |  | [`date-time`](https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.7.3.1) | Last watermark of the output data stream, if any. Initial blocks may not have watermarks, but once watermark is set - all subsequent blocks should either carry the same watermark or specify a new (greater) one. Thus, watermarks are monotonically non-decreasing. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/dataset/v1alpha1/ExecuteTransform.json)

### `ExecuteTransformInput`
Describes a slice of the input dataset used during a transformation

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `datasetId` | `string` | ✔️ | `dataset-id` | Input dataset identifier. |
| `prevBlockHash` | `string` |  | [`multihash`](https://github.com/multiformats/multihash) | Last block of the input dataset that was previously incorporated into the derivative transformation, if any. Must be equal to the last non-empty `newBlockHash`. Together with `newBlockHash` defines a half-open `(prevBlockHash, newBlockHash]` interval of blocks that will be considered in this transaction. |
| `newBlockHash` | `string` |  | [`multihash`](https://github.com/multiformats/multihash) | Hash of the last block that will be incorporated into the derivative transformation. When present, defines a half-open `(prevBlockHash, newBlockHash]` interval of blocks that will be considered in this transaction. |
| `prevOffset` | `integer` |  | `uint64` | Last data record offset in the input dataset that was previously incorporated into the derivative transformation, if any. Must be equal to the last non-empty `newOffset`. Together with `newOffset` defines a half-open `(prevOffset, newOffset]` interval of data records that will be considered in this transaction. |
| `newOffset` | `integer` |  | `uint64` | Offset of the last data record that will be incorporated into the derivative transformation, if any. When present, defines a half-open `(prevOffset, newOffset]` interval of data records that will be considered in this transaction. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/dataset/v1alpha1/ExecuteTransformInput.json)

### `MetadataBlock`
An individual block in the metadata chain that captures the history of modifications of a dataset.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `systemTime` | `string` | ✔️ | [`date-time`](https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.7.3.1) | System time when this block was written. |
| `prevBlockHash` | `string` |  | [`multihash`](https://github.com/multiformats/multihash) | Hash sum of the preceding block. |
| `sequenceNumber` | `integer` | ✔️ | `uint64` | Block sequence number, starting from zero at the seed block. |
| `event` | [`MetadataEvent`](#metadataevent) | ✔️ |  | Event data. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/dataset/v1alpha1/MetadataBlock.json)

### `MetadataEvent`
Represents a transaction that occurred on a dataset.

| Union Type | Description |
| --- | --- |
| [`AddData`](#adddata) | Indicates that data has been ingested into a root dataset. |
| [`ExecuteTransform`](#executetransform) | Indicates that derivative transformation has been performed. |
| [`Seed`](#seed) | Establishes the identity of the dataset. Always the first metadata event in the chain. |
| [`SetPollingSource`](#setpollingsource) |  |
| [`SetTransform`](#settransform) | Defines a transformation that produces data in a derivative dataset. |
| [`SetVocab`](#setvocab) | Lets you manipulate names of the system columns to avoid conflicts. |
| [`SetAttachments`](#setattachments) | Associates a set of files with this dataset. |
| [`SetInfo`](#setinfo) | Provides basic human-readable information about a dataset. |
| [`SetLicense`](#setlicense) | Defines a license that applies to this dataset. |
| [`SetDataSchema`](#setdataschema) | Specifies the complete schema of Data Slices added to the Dataset following this event. |
| [`AddPushSource`](#addpushsource) |  |
| [`DisablePushSource`](#disablepushsource) |  |
| [`DisablePollingSource`](#disablepollingsource) |  |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/dataset/v1alpha1/MetadataEvent.json)


### `OffsetInterval`
Describes a range of data as a closed arithmetic interval of offsets

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `start` | `integer` | ✔️ | `uint64` | Start of the closed interval [start; end]. |
| `end` | `integer` | ✔️ | `uint64` | End of the closed interval [start; end]. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/dataset/v1alpha1/OffsetInterval.json)

### `Projection`
Represents a projection of a dataaset history into a state for fast lookups.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `$schema` | `string` | ✔️ | `type-uri` | Identifies this resource type. |
| `headers` | [`ResourceHeadersInput`](#resourceheadersinput) | ✔️ |  | Container for identity and ownership information of a resource. |
| `spec` | [`ProjectionSpecInput`](#projectionspecinput) | ✔️ |  | Specifies the desired state of the resource. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/dataset/v1alpha1/Projection.json)

### `ProjectionSpec`
Represents a projection of a dataaset history into a state for fast lookups.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `inputs` | `array(`[`TransformInput`](#transforminput)`)` | ✔️ |  | Datasets that will be used as sources. |
| `project` | [`Transform`](#transform) | ✔️ |  | Transformation that will be applied to produce new data. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/dataset/v1alpha1/ProjectionSpec.json)

### `ProjectionSpecInput`
Represents a projection of a dataaset history into a state for fast lookups.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `inputs` | `array(`[`TransformInput`](#transforminput)`)` | ✔️ |  | Datasets that will be used as sources. |
| `project` | [`Transform`](#transform) | ✔️ |  | Transformation that will be applied to produce new data. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/dataset/v1alpha1/ProjectionSpecInput.json)

### `Seed`
Establishes the identity of the dataset. Always the first metadata event in the chain.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `datasetId` | `string` | ✔️ | `dataset-id` | Unique identity of the dataset. |
| `datasetKind` | [`DatasetKind`](#datasetkind) | ✔️ |  | Type of the dataset. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/dataset/v1alpha1/Seed.json)

### `SetAttachments`
Associates a set of files with this dataset.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `attachments` | [`Attachments`](#attachments) | ✔️ |  | One of the supported attachment sources. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/dataset/v1alpha1/SetAttachments.json)

### `SetDataSchema`
Specifies the complete schema of Data Slices added to the Dataset following this event.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `rawArrowSchema` | `string` |  | [`flatbuffers`](https://flatbuffers.dev/) | DEPRECATED: Apache Arrow schema encoded in its native flatbuffers representation. |
| `schema` | [`DataSchema`](#dataschema) |  |  | Defines the logical schema of the data files that follow this event. Will become a required field after migration. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/dataset/v1alpha1/SetDataSchema.json)

### `SetInfo`
Provides basic human-readable information about a dataset.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `description` | `string` |  |  | Brief single-sentence summary of a dataset. |
| `keywords` | `array(string)` |  |  | Keywords, search terms, or tags used to describe the dataset. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/dataset/v1alpha1/SetInfo.json)

### `SetLicense`
Defines a license that applies to this dataset.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `shortName` | `string` | ✔️ |  | Abbreviated name of the license. |
| `name` | `string` | ✔️ |  | Full name of the license. |
| `spdxId` | `string` |  |  | License identifier from the SPDX License List. |
| `websiteUrl` | `string` | ✔️ | `uri` | URL where licensing terms can be found. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/dataset/v1alpha1/SetLicense.json)

### `SetTransform`
Defines a transformation that produces data in a derivative dataset.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `inputs` | `array(`[`TransformInput`](#transforminput)`)` | ✔️ |  | Datasets that will be used as sources. |
| `transform` | [`Transform`](#transform) | ✔️ |  | Transformation that will be applied to produce new data. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/dataset/v1alpha1/SetTransform.json)

### `SetVocab`
Lets you manipulate names of the system columns to avoid conflicts.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `offsetColumn` | `string` |  |  | Name of the offset column. |
| `operationTypeColumn` | `string` |  |  | Name of the operation type column. |
| `systemTimeColumn` | `string` |  |  | Name of the system time column. |
| `eventTimeColumn` | `string` |  |  | Name of the event time column. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/dataset/v1alpha1/SetVocab.json)

### `SqlQueryStep`
Defines a query in a multi-step SQL transformation.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `alias` | `string` |  |  | Name of the temporary view that will be created from result of the query. Step without this alias will be treated as an output of the transformation. |
| `query` | `string` | ✔️ |  | SQL query the result of which will be exposed under the alias. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/dataset/v1alpha1/SqlQueryStep.json)

### `TemporalTable`
Temporary Flink-specific extension for creating temporal tables from streams.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `name` | `string` | ✔️ |  | Name of the dataset to be converted into a temporal table. |
| `primaryKey` | `array(string)` | ✔️ |  | Column names used as the primary key for creating a table. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/dataset/v1alpha1/TemporalTable.json)

### `Transform`
Engine-specific processing queries that shape the resulting data.

| Union Type | Description |
| --- | --- |
| [`Transform::Sql`](#transformsql) | Transform using one of the SQL dialects. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/dataset/v1alpha1/Transform.json)

### `Transform::Sql`
Transform using one of the SQL dialects.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `engine` | `string` | ✔️ |  | Identifier of the engine used for this transformation. |
| `version` | `string` |  |  | Version of the engine to use. |
| `query` | `string` |  |  | SQL query the result of which will be used as an output. This is a convenience property meant only for defining queries by hand. When stored in the metadata this property will never be set and instead will be converted into a single-iter `queries` array. |
| `queries` | `array(`[`SqlQueryStep`](#sqlquerystep)`)` |  |  | Specifies multi-step SQL transformations. Each step acts as a shorthand for `CREATE TEMPORARY VIEW <alias> AS (<query>)`. Last query in the array should have no alias and will be treated as an output. |
| `temporalTables` | `array(`[`TemporalTable`](#temporaltable)`)` |  |  | Temporary Flink-specific extension for creating temporal tables from streams. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/dataset/v1alpha1/Transform.json)


### `TransformInput`
Describes a derivative transformation input

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `datasetRef` | `string` | ✔️ | `dataset-ref` | A local or remote dataset reference. When block is accepted this MUST be in the form of a DatasetId to guarantee reproducibility, as aliases can change over time. |
| `alias` | `string` |  |  | An alias under which this input will be available in queries. Will be populated from `datasetRef` if not provided before resolving it to DatasetId. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/dataset/v1alpha1/TransformInput.json)

### `Watermark`
Represents a watermark in the event stream.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `systemTime` | `string` | ✔️ | [`date-time`](https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.7.3.1) | Moment in processing time when watermark was emitted. |
| `eventTime` | `string` | ✔️ | [`date-time`](https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.7.3.1) | Moment in event time which watermark has reached. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/dataset/v1alpha1/Watermark.json)

## Engine
### `RawQueryRequest`
Sent by the coordinator to an engine to perform query on raw input data, usually as part of ingest preprocessing step

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `inputDataPaths` | `array(string)` | ✔️ |  | Paths to input data files to perform query over. Must all have identical schema. |
| `transform` | [`Transform`](#transform) | ✔️ |  | Transformation that will be applied to produce new data. |
| `outputDataPath` | `string` | ✔️ | `path` | Path where query result will be written. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/engine/v1alpha1/RawQueryRequest.json)

### `RawQueryResponse`
Sent by an engine to coordinator when performing the raw query operation

| Union Type | Description |
| --- | --- |
| [`RawQueryResponse::Progress`](#rawqueryresponseprogress) | Reports query progress |
| [`RawQueryResponse::Success`](#rawqueryresponsesuccess) | Query executed successfully |
| [`RawQueryResponse::InvalidQuery`](#rawqueryresponseinvalidquery) | Query did not pass validation |
| [`RawQueryResponse::InternalError`](#rawqueryresponseinternalerror) | Internal error during query execution |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/engine/v1alpha1/RawQueryResponse.json)

### `RawQueryResponse::Progress`
Reports query progress

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/engine/v1alpha1/RawQueryResponse.json)

### `RawQueryResponse::Success`
Query executed successfully

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `numRecords` | `integer` | ✔️ | `uint64` | Number of records produced by the query |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/engine/v1alpha1/RawQueryResponse.json)

### `RawQueryResponse::InvalidQuery`
Query did not pass validation

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `message` | `string` | ✔️ |  | Explanation of an error |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/engine/v1alpha1/RawQueryResponse.json)

### `RawQueryResponse::InternalError`
Internal error during query execution

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `message` | `string` | ✔️ |  | Brief description of an error |
| `backtrace` | `string` |  |  | Details of an error (e.g. a backtrace) |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/engine/v1alpha1/RawQueryResponse.json)


### `TransformRequest`
Sent by the coordinator to an engine to perform the next step of data transformation

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `datasetId` | `string` | ✔️ | `dataset-id` | Unique identifier of the output dataset. |
| `datasetAlias` | `string` | ✔️ | `dataset-alias` | Alias of the output dataset, for logging purposes only. |
| `systemTime` | `string` | ✔️ | [`date-time`](https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.7.3.1) | System time to use for new records. |
| `vocab` | [`DatasetVocabulary`](#datasetvocabulary) | ✔️ |  | Vocabulary of the output dataset. |
| `transform` | [`Transform`](#transform) | ✔️ |  | Transformation that will be applied to produce new data. |
| `queryInputs` | `array(`[`TransformRequestInput`](#transformrequestinput)`)` | ✔️ |  | Defines inputs used in this transaction. Slices corresponding to every input dataset must be present. |
| `nextOffset` | `integer` | ✔️ | `uint64` | Starting offset to use for new data records. |
| `prevCheckpointPath` | `string` |  | `path` | TODO: This will be removed when coordinator will be speaking to engines purely through Arrow. |
| `newCheckpointPath` | `string` | ✔️ | `path` | TODO: This will be removed when coordinator will be speaking to engines purely through Arrow. |
| `newDataPath` | `string` | ✔️ | `path` | TODO: This will be removed when coordinator will be speaking to engines purely through Arrow. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/engine/v1alpha1/TransformRequest.json)

### `TransformRequestInput`
Sent as part of the engine transform request operation to describe the input

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `datasetId` | `string` | ✔️ | `dataset-id` | Unique identifier of the dataset. |
| `datasetAlias` | `string` | ✔️ | `dataset-alias` | Alias of the output dataset, for logging purposes only. |
| `queryAlias` | `string` | ✔️ |  | An alias of this input to be used in queries. |
| `vocab` | [`DatasetVocabulary`](#datasetvocabulary) | ✔️ |  | Vocabulary of the input dataset. |
| `offsetInterval` | [`OffsetInterval`](#offsetinterval) |  |  | Subset of data that goes into this transaction. |
| `dataPaths` | `array(string)` | ✔️ |  | TODO: This will be removed when coordinator will be slicing data for the engine. |
| `schemaFile` | `string` | ✔️ | `path` | TODO: replace with actual DDL or Parquet schema. |
| `explicitWatermarks` | `array(`[`Watermark`](#watermark)`)` | ✔️ |  | Watermarks that should be injected into the stream to separate micro batches for reproducibility. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/engine/v1alpha1/TransformRequestInput.json)

### `TransformResponse`
Sent by an engine to coordinator when performing the data transformation

| Union Type | Description |
| --- | --- |
| [`TransformResponse::Progress`](#transformresponseprogress) | Reports query progress |
| [`TransformResponse::Success`](#transformresponsesuccess) | Query executed successfully |
| [`TransformResponse::InvalidQuery`](#transformresponseinvalidquery) | Query did not pass validation |
| [`TransformResponse::InternalError`](#transformresponseinternalerror) | Internal error during query execution |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/engine/v1alpha1/TransformResponse.json)

### `TransformResponse::Progress`
Reports query progress

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/engine/v1alpha1/TransformResponse.json)

### `TransformResponse::Success`
Query executed successfully

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `newOffsetInterval` | [`OffsetInterval`](#offsetinterval) |  |  | Data slice produced by the transaction, if any. |
| `newWatermark` | `string` |  | [`date-time`](https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.7.3.1) | Watermark advanced by the transaction, if any. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/engine/v1alpha1/TransformResponse.json)

### `TransformResponse::InvalidQuery`
Query did not pass validation

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `message` | `string` | ✔️ |  | Explanation of an error |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/engine/v1alpha1/TransformResponse.json)

### `TransformResponse::InternalError`
Internal error during query execution

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `message` | `string` | ✔️ |  | Brief description of an error |
| `backtrace` | `string` |  |  | Details of an error (e.g. a backtrace) |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/engine/v1alpha1/TransformResponse.json)


## Event
### `EventFilter`
Filters that work on domain event types and fields.

_Map of string keys to arbitrary values._

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/event/v1alpha1/EventFilter.json)

## Flow
### `Flow`
Defines a sequence of tasks to be executed upon certain trigger conditions.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `$schema` | `string` | ✔️ | `type-uri` | Identifies this resource type. |
| `headers` | [`ResourceHeadersInput`](#resourceheadersinput) | ✔️ |  | Container for identity and ownership information of a resource. |
| `spec` | [`FlowSpecInput`](#flowspecinput) | ✔️ |  | Specifies the desired state of the flow. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/flow/v1alpha1/Flow.json)

### `FlowRun`
Defines a set of tasks to be executed in a sequence.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `$schema` | `string` | ✔️ | `type-uri` | Identifies this resource type. |
| `headers` | [`ResourceHeadersInput`](#resourceheadersinput) | ✔️ |  | Container for identity and ownership information of a resource. |
| `spec` | [`FlowRunSpecInput`](#flowrunspecinput) | ✔️ |  | Specifies the desired state of the flow run. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/flow/v1alpha1/FlowRun.json)

### `FlowRunActivationCause`
Cause of the flow run activation

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `activationTime` | `string` | ✔️ | [`date-time`](https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.7.3.1) | Time at which the trigger fired. |
| `initiator` | [`AccountHandle`](#accounthandle) |  |  | Account that initiated the run, if applicable. |
| `trigger` | [`FlowTrigger`](#flowtrigger) | ✔️ |  | Copy of the trigger configuration from the parent Flow that fired. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/flow/v1alpha1/FlowRunActivationCause.json)

### `FlowRunActivationCauses`
Condition capturing what caused this FlowRun to be scheduled. Set by the controller at creation time; never written by users. In case of a retry, the causes of the original run are preserved.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `activationCauses` | `array(`[`FlowRunActivationCause`](#flowrunactivationcause)`)` | ✔️ |  | Triggers that caused this run to be scheduled. |
| `lateActivationCauses` | `array(`[`FlowRunActivationCause`](#flowrunactivationcause)`)` |  |  | Additional triggers that fired while this run was already queued or executing. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/flow/v1alpha1/FlowRunActivationCauses.json)

### `FlowRunRetry`
Condition linking this FlowRun to the previous FlowRun it is retrying. Set by the controller; never written by users.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `retryOf` | [`ResourceHandle`](#resourcehandle) | ✔️ |  | Reference to the FlowRun this run is retrying. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/flow/v1alpha1/FlowRunRetry.json)

### `FlowRunSpec`
Defines a set of tasks to be executed in a sequence.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `target` | [`ResourceHandle`](#resourcehandle) |  |  | Defines the default target resources on which tasks will be performed. |
| `tasks` | `array(`[`TaskSpec`](#taskspec)`)` | ✔️ |  | List of tasks to run consecutively. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/flow/v1alpha1/FlowRunSpec.json)

### `FlowRunSpecInput`
Defines a set of tasks to be executed in a sequence.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `target` | [`ResourceRef`](#resourceref) |  |  | Defines the default target resources on which tasks will be performed. |
| `tasks` | `array(`[`TaskSpecInput`](#taskspecinput)`)` | ✔️ |  | List of tasks to run consecutively. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/flow/v1alpha1/FlowRunSpecInput.json)

### `FlowRunStatus`
Condition tracking the overall execution status of a FlowRun and its spawned tasks.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `status` | [`Value`](#value) | ✔️ |  | Overall execution status of the FlowRun. |
| `tasks` | `array(`[`TaskEntry`](#taskentry)`)` |  |  | Tasks spawned by this FlowRun, in execution order. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/flow/v1alpha1/FlowRunStatus.json)

### `FlowSpec`
Defines a sequence of tasks to be executed upon certain trigger conditions.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `target` | [`ResourceSelector`](#resourceselector) | ✔️ |  | Defines resources for which this flow will be instantiated. |
| `triggers` | `array(`[`FlowTrigger`](#flowtrigger)`)` | ✔️ |  | Conditions that cause this flow to execute. |
| `tasks` | `array(`[`TaskSpec`](#taskspec)`)` | ✔️ |  | List of tasks to run consecutively. |
| `retryPolicy` | [`RetryPolicy`](#retrypolicy) |  |  | Defines how a flow should react to failures. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/flow/v1alpha1/FlowSpec.json)

### `FlowSpecInput`
Defines a sequence of tasks to be executed upon certain trigger conditions.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `target` | [`ResourceSelector`](#resourceselector) | ✔️ |  | Defines resources for which this flow will be instantiated. |
| `triggers` | `array(`[`FlowTriggerInput`](#flowtriggerinput)`)` | ✔️ |  | Conditions that cause this flow to execute. |
| `tasks` | `array(`[`TaskSpecInput`](#taskspecinput)`)` | ✔️ |  | List of tasks to run consecutively. |
| `retryPolicy` | [`RetryPolicy`](#retrypolicy) |  |  | Defines how a flow should react to failures. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/flow/v1alpha1/FlowSpecInput.json)

### `FlowTrigger`
Condition that causes a flow to be executed.

| Union Type | Description |
| --- | --- |
| [`FlowTrigger::Manual`](#flowtriggermanual) | Triggers the flow via an API call or UI action. |
| [`FlowTrigger::Schedule`](#flowtriggerschedule) | Triggers the flow on a cron schedule. |
| [`FlowTrigger::Event`](#flowtriggerevent) | Triggers the flow when an event bus event matching one of the filters is observed. |
| [`FlowTrigger::Source`](#flowtriggersource) | Triggers the flow when a source receives new data, with optional batching controls. |
| [`FlowTrigger::Dataset`](#flowtriggerdataset) | Triggers the flow when matching datasets are updated. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/flow/v1alpha1/FlowTrigger.json)

### `FlowTrigger::Manual`
Triggers the flow via an API call or UI action.

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/flow/v1alpha1/FlowTrigger.json)

### `FlowTrigger::Schedule`
Triggers the flow on a cron schedule.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `cron` | `string` | ✔️ |  | Cron5 expression defining the schedule e.g. `@daily` or `*/30 * * * *`. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/flow/v1alpha1/FlowTrigger.json)

### `FlowTrigger::Event`
Triggers the flow when an event bus event matching one of the filters is observed.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `events` | [`EventFilter`](#eventfilter) | ✔️ |  | Filters the event by type and fields. |
| `cooldown` | `string` |  | `duration` | The trigger will fire upon first observed event. If another event arrives withing the `cooldown` interval the firing will be postponed until `cooldown` interval ends. I.e. trigger is guaranteed to fire, but may batch multiple events together into one flow run. |
| `cooldownMaxBatch` | `integer` |  | `uint64` | If an event is observed a `cooldownMaxBatch` number of times during the `cooldown` interval it will fire the trigger without waiting for cooldown to finish. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/flow/v1alpha1/FlowTrigger.json)

### `FlowTrigger::Source`
Triggers the flow when a source receives new data, with optional batching controls.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `source` | [`ResourceHandle`](#resourcehandle) | ✔️ |  | Reference to the source resource that drives this trigger. |
| `minRecordsToAwait` | `integer` |  | `uint64` | Minimum number of new records to accumulate before triggering. |
| `maxAwaitInterval` | `string` |  | `duration` | Maximum time to wait for `minRecordsToAwait` before triggering anyway e.g. `1h`. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/flow/v1alpha1/FlowTrigger.json)

### `FlowTrigger::Dataset`
Triggers the flow when matching datasets are updated.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `dataset` | [`DatasetSelector`](#datasetselector) | ✔️ |  | Selector that identifies which datasets can trigger this flow. |
| `events` | `array(string)` |  |  | Set of event bus event IDs that this trigger will react to |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/flow/v1alpha1/FlowTrigger.json)


### `FlowTriggerInput`
Condition that causes a flow to be executed.

| Union Type | Description |
| --- | --- |
| [`FlowTriggerInput::Manual`](#flowtriggerinputmanual) | Triggers the flow via an API call or UI action. |
| [`FlowTriggerInput::Schedule`](#flowtriggerinputschedule) | Triggers the flow on a cron schedule. |
| [`FlowTriggerInput::Event`](#flowtriggerinputevent) | Triggers the flow when an event bus event matching one of the filters is observed. |
| [`FlowTriggerInput::Source`](#flowtriggerinputsource) | Triggers the flow when a source receives new data, with optional batching controls. |
| [`FlowTriggerInput::Dataset`](#flowtriggerinputdataset) | Triggers the flow when matching datasets are updated. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/flow/v1alpha1/FlowTriggerInput.json)

### `FlowTriggerInput::Manual`
Triggers the flow via an API call or UI action.

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/flow/v1alpha1/FlowTriggerInput.json)

### `FlowTriggerInput::Schedule`
Triggers the flow on a cron schedule.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `cron` | `string` | ✔️ |  | Cron5 expression defining the schedule e.g. `@daily` or `*/30 * * * *`. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/flow/v1alpha1/FlowTriggerInput.json)

### `FlowTriggerInput::Event`
Triggers the flow when an event bus event matching one of the filters is observed.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `events` | [`EventFilter`](#eventfilter) | ✔️ |  | Filters the event by type and fields. |
| `cooldown` | `string` |  | `duration` | The trigger will fire upon first observed event. If another event arrives withing the `cooldown` interval the firing will be postponed until `cooldown` interval ends. I.e. trigger is guaranteed to fire, but may batch multiple events together into one flow run. |
| `cooldownMaxBatch` | `integer` |  | `uint64` | If an event is observed a `cooldownMaxBatch` number of times during the `cooldown` interval it will fire the trigger without waiting for cooldown to finish. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/flow/v1alpha1/FlowTriggerInput.json)

### `FlowTriggerInput::Source`
Triggers the flow when a source receives new data, with optional batching controls.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `source` | [`ResourceRef`](#resourceref) | ✔️ |  | Reference to the source resource that drives this trigger. |
| `minRecordsToAwait` | `integer` |  | `uint64` | Minimum number of new records to accumulate before triggering. |
| `maxAwaitInterval` | `string` |  | `duration` | Maximum time to wait for `minRecordsToAwait` before triggering anyway e.g. `1h`. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/flow/v1alpha1/FlowTriggerInput.json)

### `FlowTriggerInput::Dataset`
Triggers the flow when matching datasets are updated.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `dataset` | [`DatasetSelector`](#datasetselector) | ✔️ |  | Selector that identifies which datasets can trigger this flow. |
| `events` | `array(string)` |  |  | Set of event bus event IDs that this trigger will react to |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/flow/v1alpha1/FlowTriggerInput.json)


### `RetryBackoff`
Type of the backoff scaling.

| Enum Value |
| :---: |
| `Linear` |
| `Exponential` |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/flow/v1alpha1/RetryBackoff.json)

### `RetryPolicy`
Defines how a flow should react to failures.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `maxAttempts` | `integer` |  | `uint32` | Number of attempts before flow auto-scheduling will be disabled. |
| `minDelay` | `string` |  | `duration` | How long to wait until the first retry. |
| `backoff` | [`RetryBackoff`](#retrybackoff) |  |  | Type of the backoff scaling. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/flow/v1alpha1/RetryPolicy.json)

## Resource
### `LabelFilter`
Filters that work on resource labels and identity headers.

_Map of string keys to arbitrary values._

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/resource/v1alpha1/LabelFilter.json)

### `Resource`
Top-level container for canonical representation of a resource that specifies the type and version of the resource, carries identity, ownership, and status information.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `$schema` | `string` | ✔️ | `type-uri` | Identifies the controlling entity, a bounded context that this resource belongs to, and the version. Url should follow the pattern `{base-url}/{context}/{version}/{name}.json` e.g. `https://opendatafabric.org/schemas/dataset/v1/Dataset.json`. |
| `headers` | [`ResourceHeaders`](#resourceheaders) | ✔️ |  | Container for identity and ownership information of a resource. |
| `spec` | `object` | ✔️ | `fragment` | Specifies the desired state of a resource. |
| `status` | [`ResourceStatus`](#resourcestatus) | ✔️ |  | Resource lifecycle and reconciliation information. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/resource/v1alpha1/Resource.json)

### `ResourceAnnotations`
Annotations is an unstructured key value map stored with a resource that may be set by external tools to store and retrieve arbitrary metadata. Unlike labels, annotations are not indexed and cannot be queried by.

_Map of string keys to arbitrary values._

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/resource/v1alpha1/ResourceAnnotations.json)

### `ResourceConditions`
Container of feneric contditions that can be added by contollers to provide additional information about the state of a resource. Keys uniquely identify the condition and should be in the form of URL to a schema describing this condition, e.g. `https://opendatafabric.org/schemas/resource/ConditionReady.json`.

_Map of string keys to arbitrary values._

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/resource/v1alpha1/ResourceConditions.json)

### `ResourceHandle`
Link to another resolved resource.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `account` | [`AccountHandle`](#accounthandle) | ✔️ |  | Account that owns the target resource. |
| `type` | `string` | ✔️ | `type-uri` | Type URI of the target resource. |
| `id` | `string` | ✔️ | `resource-id` | ID of the resource within a node. |
| `did` | `string` |  | `did` | DID of the resource, if applicable. |
| `name` | `string` | ✔️ | `resource-name` | Name of a resource. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/resource/v1alpha1/ResourceHandle.json)

### `ResourceHeaders`
Container for identity and ownership information of a resource.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `id` | `string` | ✔️ | `resource-id` | Unique identifier of a resource within entire ODF node. Automatically assigned upon resource creation. |
| `name` | `string` | ✔️ | `resource-name` | Symbolic name of a resource that identifies it within a scope of an onwing account. |
| `account` | [`AccountHandle`](#accounthandle) | ✔️ |  | Link to the account that owns the resource. |
| `labels` | [`ResourceLabels`](#resourcelabels) | ✔️ |  | Map of string keys and values that can be used to organize, categorize, and query resources. |
| `annotations` | [`ResourceAnnotations`](#resourceannotations) | ✔️ |  | Annotations is a key value map stored with a resource that may be set by external tools to store and retrieve arbitrary metadata. Unlike labels, annotations are not indexed and cannot be queried by. |
| `ownerReferences` | `array(`[`ResourceHandle`](#resourcehandle)`)` |  |  | References to resources that created this resource. Used for lineage tracking and cascading cleanup. |
| `generation` | `integer` | ✔️ | `uint64` | A sequential number that changes every time the resource header and spec are updated. Does not increment on status changes, thus signifying changes to the desired state. Populated by the system. Starts with `1`. |
| `createdAt` | `string` | ✔️ | [`date-time`](https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.7.3.1) | Time when the resource was first applied and assigned an identity. |
| `updatedAt` | `string` | ✔️ | [`date-time`](https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.7.3.1) | Time when the resource was last updated, including header, spec, and status updates. |
| `deletedAt` | `string` |  | [`date-time`](https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.7.3.1) | Time when the resource was deleted. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/resource/v1alpha1/ResourceHeaders.json)

### `ResourceHeadersInput`
Container for identity and ownership information of a resource.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `id` | `string` |  | `resource-id` | Unique identifier of a resource within entire ODF node. Automatically assigned upon resource creation. |
| `name` | `string` | ✔️ | `resource-name` | Symbolic name of a resource that identifies it within a scope of an onwing account. |
| `account` | [`AccountRef`](#accountref) |  |  | Reference to the account that owns the resource. |
| `labels` | [`ResourceLabels`](#resourcelabels) |  |  | Map of string keys and values that can be used to organize, categorize, and query resources. |
| `annotations` | [`ResourceAnnotations`](#resourceannotations) |  |  | Annotations is a key value map stored with a resource that may be set by external tools to store and retrieve arbitrary metadata. Unlike labels, annotations are not indexed and cannot be queried by. |
| `ownerReferences` | `array(`[`ResourceRef`](#resourceref)`)` |  |  | References to resources that created this resource. Used for lineage tracking and cascading cleanup. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/resource/v1alpha1/ResourceHeadersInput.json)

### `ResourceInput`
Top-level container for user-authored representation of a resource that specifies the type and version of the resource and its desired state.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `$schema` | `string` | ✔️ | `type-uri` | Identifies the controlling entity, a bounded context that this resource belongs to, and the version. Url should follow the pattern `{base-url}/{context}/{version}/{name}.json` e.g. `https://opendatafabric.org/schemas/dataset/v1/Dataset.json`. |
| `headers` | [`ResourceHeadersInput`](#resourceheadersinput) | ✔️ |  | Container for identity and ownership information of a resource. |
| `spec` | `object` | ✔️ | `fragment` | Specifies the desired state of a resource. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/resource/v1alpha1/ResourceInput.json)

### `ResourceLabels`
Map of string keys and values that can be used to organize, categorize, and query resources.

_Map of string keys to arbitrary values._

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/resource/v1alpha1/ResourceLabels.json)

### `ResourcePhase`
Represents the reconciliation phase of a resource.

| Enum Value |
| :---: |
| `Pending` |
| `Reconciling` |
| `Ready` |
| `Degraded` |
| `Failed` |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/resource/v1alpha1/ResourcePhase.json)

### `ResourceRef`


| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `account` | [`AccountRef`](#accountref) |  |  | Reference to an account that owns the target resource. |
| `id` | `string` |  | `resource-id` | ID of the resource within a node. |
| `did` | `string` |  | `did` | DID of the resource. |
| `type` | `string` |  | `type-ref` | Short type name or full type URI of the target resource. |
| `name` | `string` |  | `resource-name` | Name of a resource. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/resource/v1alpha1/ResourceRef.json)

### `ResourceSelector`


| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `account` | [`AccountRef`](#accountref) |  |  | Reference to an account that owns the target resources. |
| `id` | `string` |  | `resource-id` | ID of the singular resource. |
| `did` | `string` |  | `did` | DID of the resource. |
| `type` | `string` |  | `type-ref` | Short type name of the target resource e.g. `SecretSet` or a full schema URI e.g. `https://opendatafabric.org/config/v1/SecretSet.json`. |
| `name` | `string` |  |  | Name pattern in SQL `LIKE` format. |
| `labels` | [`LabelFilter`](#labelfilter) |  |  | Filter by resource labels. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/resource/v1alpha1/ResourceSelector.json)

### `ResourceStatus`
Resource lifecycle and reconciliation information.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `phase` | [`ResourcePhase`](#resourcephase) | ✔️ |  | Represents the reconciliation phase of a resource as seen by the main resource controller. |
| `observedGeneration` | `integer` |  | `uint64` | Resource generation that was last seen by the main resource controller. |
| `observedAt` | `string` |  | [`date-time`](https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.7.3.1) | Time when the controller seen the resource state as defined in `observedGeneration`. |
| `reconciledGeneration` | `integer` |  | `uint64` | Resource generation that was last successfully reconciled by the main resource controller. |
| `reconciledAt` | `string` |  | [`date-time`](https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.7.3.1) | Time when the controller last reconciled the desired resource state as defined in `reconciledGeneration`. |
| `conditions` | [`ResourceConditions`](#resourceconditions) | ✔️ |  | Detailed conditions describing the state of the resource that are added by controllers. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/resource/v1alpha1/ResourceStatus.json)

## Sink
### `WebhookTarget`
Defines a webhook target endpoint that can receive event notifications and data.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `$schema` | `string` | ✔️ | `type-uri` | Identifies this resource type. |
| `headers` | [`ResourceHeadersInput`](#resourceheadersinput) | ✔️ |  | Container for identity and ownership information of a resource. |
| `spec` | [`WebhookTargetSpecInput`](#webhooktargetspecinput) | ✔️ |  | Specifies the desired state of the resource. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/sink/v1alpha1/WebhookTarget.json)

### `WebhookTargetSpec`
Defines a webhook target endpoint that can receive event notifications and data.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `url` | `string` | ✔️ | `uri` | Target url of the webhook. |
| `secret` | [`Secret`](#secret) |  |  | Shared secret used for HMAC signature of the request payload for authentication. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/sink/v1alpha1/WebhookTargetSpec.json)

### `WebhookTargetSpecInput`
Defines a webhook target endpoint that can receive event notifications and data.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `url` | `string` | ✔️ | `uri` | Target url of the webhook. |
| `secret` | [`Secret`](#secret) |  |  | Shared secret used for HMAC signature of the request payload for authentication. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/sink/v1alpha1/WebhookTargetSpecInput.json)

## Source
### `CompressionFormat`
Defines a compression algorithm.

| Enum Value |
| :---: |
| `Gzip` |
| `Zip` |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/source/v1alpha1/CompressionFormat.json)

### `EnvVar`
Defines an environment variable passed into some job.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `name` | `string` | ✔️ |  | Name of the variable. |
| `value` | `string` |  |  | Value of the variable. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/source/v1alpha1/EnvVar.json)

### `EventTimeSource`
Defines the external source of data.

| Union Type | Description |
| --- | --- |
| [`EventTimeSource::FromMetadata`](#eventtimesourcefrommetadata) | Extracts event time from the source's metadata. |
| [`EventTimeSource::FromPath`](#eventtimesourcefrompath) | Extracts event time from the path component of the source. |
| [`EventTimeSource::FromSystemTime`](#eventtimesourcefromsystemtime) | Assigns event time from the system time source. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/source/v1alpha1/EventTimeSource.json)

### `EventTimeSource::FromMetadata`
Extracts event time from the source's metadata.

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/source/v1alpha1/EventTimeSource.json)

### `EventTimeSource::FromSystemTime`
Assigns event time from the system time source.

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/source/v1alpha1/EventTimeSource.json)

### `EventTimeSource::FromPath`
Extracts event time from the path component of the source.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `pattern` | `string` | ✔️ | `regex` | Regular expression where first group contains the timestamp string. |
| `timestampFormat` | `string` |  |  | Format of the expected timestamp in java.text.SimpleDateFormat form. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/source/v1alpha1/EventTimeSource.json)


### `IngestParams`
Optional parameters to control ingestion behavior.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `targetSliceRecords` | `integer` |  | `uint64` | Target number of records to ingest per data slice. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/source/v1alpha1/IngestParams.json)

### `Ingress`
Defines the point where data enters the system.

| Union Type | Description |
| --- | --- |
| [`Ingress::Url`](#ingressurl) | Pulls data from one of the supported sources by its URL. |
| [`Ingress::FilesGlob`](#ingressfilesglob) | Uses glob operator to match files on the local file system. |
| [`Ingress::Container`](#ingresscontainer) | Runs the specified OCI container to fetch data from an arbitrary source. |
| [`Ingress::Mqtt`](#ingressmqtt) | Connects to an MQTT broker to fetch events from the specified topic. |
| [`Ingress::EvmLogs`](#ingressevmlogs) | Connects to an EVM (Ethereum) node to stream transaction logs. |
| [`Ingress::RestEndpoint`](#ingressrestendpoint) | Exposes a REST HTTP endpoint that accepts pushed data records. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/source/v1alpha1/Ingress.json)

### `Ingress::Url`
Pulls data from one of the supported sources by its URL.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `url` | `string` | ✔️ | `uri` | URL of the data source |
| `eventTime` | [`EventTimeSource`](#eventtimesource) |  |  | Describes how event time is extracted from the source metadata. |
| `cache` | [`SourceCaching`](#sourcecaching) |  |  | Describes the caching settings used for this source. |
| `headers` | `array(`[`RequestHeader`](#requestheader)`)` |  |  | Headers to pass during the request (e.g. HTTP Authorization) |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/source/v1alpha1/Ingress.json)

### `Ingress::FilesGlob`
Uses glob operator to match files on the local file system.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `path` | `string` | ✔️ |  | Path with a glob pattern. |
| `eventTime` | [`EventTimeSource`](#eventtimesource) |  |  | Describes how event time is extracted from the source metadata. |
| `cache` | [`SourceCaching`](#sourcecaching) |  |  | Describes the caching settings used for this source. |
| `order` | [`SourceOrdering`](#sourceordering) |  |  | Specifies how input files should be ordered before ingestion.<br/>Order is important as every file will be processed individually<br/>and will advance the dataset's watermark. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/source/v1alpha1/Ingress.json)

### `Ingress::Container`
Runs the specified OCI container to fetch data from an arbitrary source.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `image` | `string` | ✔️ |  | Image name and and an optional tag. |
| `command` | `array(string)` |  |  | Specifies the entrypoint. Not executed within a shell. The default OCI image's ENTRYPOINT is used if this is not provided. |
| `args` | `array(string)` |  |  | Arguments to the entrypoint. The OCI image's CMD is used if this is not provided. |
| `env` | `array(`[`EnvVar`](#envvar)`)` |  |  | Environment variables to propagate into or set in the container. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/source/v1alpha1/Ingress.json)

### `Ingress::Mqtt`
Connects to an MQTT broker to fetch events from the specified topic.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `host` | `string` | ✔️ |  | Hostname of the MQTT broker. |
| `port` | `integer` | ✔️ | `int32` | Port of the MQTT broker. |
| `username` | `string` |  |  | Username to use for auth with the broker. |
| `password` | `string` |  |  | Password to use for auth with the broker (can be templated). |
| `topics` | `array(`[`MqttTopicSubscription`](#mqtttopicsubscription)`)` | ✔️ |  | List of topic subscription parameters. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/source/v1alpha1/Ingress.json)

### `Ingress::RestEndpoint`
Exposes a REST HTTP endpoint that accepts pushed data records.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `buffer` | [`IngressBuffer`](#ingressbuffer) |  |  | Buffer configuration for holding records until they are ingested. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/source/v1alpha1/Ingress.json)

### `Ingress::EvmLogs`
Connects to an EVM (Ethereum) node to stream transaction logs.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `chainId` | `integer` |  | `uint64` | Identifier of the chain to scan logs from. This parameter may be used for RPC endpoint lookup as well as asserting that provided `nodeUrl` corresponds to the expected chain. |
| `nodeUrl` | `string` |  | `uri` | Url of the node. |
| `filter` | `string` |  |  | An SQL WHERE clause that can be used to pre-filter the logs before fetching them from the ETH node. |
| `signature` | `string` |  |  | Solidity log event signature to use for decoding. Using this field adds `event` to the output containing decoded log as JSON. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/source/v1alpha1/Ingress.json)


### `IngressBuffer`
Buffer configuration for holding pushed records until they are ingested.

| Union Type | Description |
| --- | --- |
| [`IngressBuffer::Memory`](#ingressbuffermemory) | An in-memory buffer. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/source/v1alpha1/IngressBuffer.json)

### `IngressBuffer::Memory`
An in-memory buffer.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `bufferSize` | `integer` |  | `uint64` | Maximum number of records to hold in the buffer. |
| `overflowPolicy` | `string` |  |  | Policy applied when the buffer is full. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/source/v1alpha1/IngressBuffer.json)


### `MergeStrategy`
Merge strategy determines how newly ingested data should be combined with the data that already exists in the dataset.

| Union Type | Description |
| --- | --- |
| [`MergeStrategy::Append`](#mergestrategyappend) | Append merge strategy. |
| [`MergeStrategy::Ledger`](#mergestrategyledger) | Ledger merge strategy. |
| [`MergeStrategy::Snapshot`](#mergestrategysnapshot) | Snapshot merge strategy. |
| [`MergeStrategy::ChangelogStream`](#mergestrategychangelogstream) | Changelog stream merge strategy. |
| [`MergeStrategy::UpsertStream`](#mergestrategyupsertstream) | Upsert stream merge strategy. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/source/v1alpha1/MergeStrategy.json)

### `MergeStrategy::Append`
Append merge strategy.

Under this strategy new data will be appended to the dataset in its entirety, without any deduplication.

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/source/v1alpha1/MergeStrategy.json)

### `MergeStrategy::ChangelogStream`
Changelog stream merge strategy.

This is the native stream format for ODF that accurately describes the evolution of all event records including appends, retractions, and corrections as per RFC-015. No pre-processing except for format validation is done.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `primaryKey` | `array(string)` | ✔️ |  | Names of the columns that uniquely identify the record throughout its lifetime |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/source/v1alpha1/MergeStrategy.json)

### `MergeStrategy::Ledger`
Ledger merge strategy.

This strategy should be used for data sources containing ledgers of events. Currently this strategy will only perform deduplication of events using user-specified primary key columns. This means that the source data can contain partially overlapping set of records and only those records that were not previously seen will be appended.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `primaryKey` | `array(string)` | ✔️ |  | Names of the columns that uniquely identify the record throughout its lifetime |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/source/v1alpha1/MergeStrategy.json)

### `MergeStrategy::Snapshot`
Snapshot merge strategy.

This strategy can be used for data state snapshots that are taken periodically and contain only the latest state of the observed entity or system. Over time such snapshots can have new rows added, and old rows either removed or modified.

This strategy transforms snapshot data into an append-only event stream where data already added is immutable. It does so by performing Change Data Capture - essentially diffing the current state of data against the reconstructed previous state and recording differences as retractions or corrections. The Operation Type "op" column will contain:
  - append (`+A`) when a row appears for the first time
  - retraction (`-D`) when row disappears
  - correction (`-C`, `+C`) when row data has changed, with `-C` event carrying the old value of the row and `+C` carrying the new value.

To correctly associate rows between old and new snapshots this strategy relies on user-specified primary key columns.

To identify whether a row has changed this strategy will compare all other columns one by one. If the data contains a column that is guaranteed to change whenever any of the data columns changes (for example a last modification timestamp, an incremental version, or a data hash), then it can be specified in `compareColumns` property to speed up the detection of modified rows.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `primaryKey` | `array(string)` | ✔️ |  | Names of the columns that uniquely identify the record throughout its lifetime. |
| `compareColumns` | `array(string)` |  |  | Names of the columns to compared to determine if a row has changed between two snapshots. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/source/v1alpha1/MergeStrategy.json)

### `MergeStrategy::UpsertStream`
Upsert stream merge strategy.

This strategy should be used for data sources containing ledgers of insert-or-update and delete events. Unlike ChangelogStream the insert-or-update events only carry the new values, so this strategy will use primary key to re-classify the events into an append or a correction from/to pair, looking up the previous values.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `primaryKey` | `array(string)` | ✔️ |  | Names of the columns that uniquely identify the record throughout its lifetime |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/source/v1alpha1/MergeStrategy.json)


### `MqttQos`
MQTT quality of service class.

| Enum Value |
| :---: |
| `AtMostOnce` |
| `AtLeastOnce` |
| `ExactlyOnce` |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/source/v1alpha1/MqttQos.json)

### `MqttTopicSubscription`
MQTT topic subscription parameters.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `path` | `string` | ✔️ |  | Name of the topic (may include patterns). |
| `qos` | [`MqttQos`](#mqttqos) |  |  | Quality of service class.<br/><br/>Default: `AtMostOnce` |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/source/v1alpha1/MqttTopicSubscription.json)

### `PrepStep`
Defines the steps to prepare raw data for ingestion.

| Union Type | Description |
| --- | --- |
| [`PrepStep::Decompress`](#prepstepdecompress) | Pulls data from one of the supported sources by its URL. |
| [`PrepStep::Pipe`](#prepsteppipe) | Executes external command to process the data using piped input/output. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/source/v1alpha1/PrepStep.json)

### `PrepStep::Decompress`
Pulls data from one of the supported sources by its URL.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `format` | [`CompressionFormat`](#compressionformat) | ✔️ |  | Name of a compression algorithm used on data. |
| `subPath` | `string` |  |  | Path to a data file within a multi-file archive. Can contain glob patterns. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/source/v1alpha1/PrepStep.json)

### `PrepStep::Pipe`
Executes external command to process the data using piped input/output.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `command` | `array(string)` | ✔️ |  | Command to execute and its arguments. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/source/v1alpha1/PrepStep.json)


### `ReadStep`
Defines how raw data should be read into the structured form.

| Union Type | Description |
| --- | --- |
| [`ReadStep::Csv`](#readstepcsv) | Reader for comma-separated files. |
| [`ReadStep::GeoJson`](#readstepgeojson) | Reader for GeoJSON files. It expects one `FeatureCollection` object in the root and will create a record per each `Feature` inside it extracting the properties into individual columns and leaving the feature geometry in its own column. |
| [`ReadStep::EsriShapefile`](#readstepesrishapefile) | Reader for ESRI Shapefile format. |
| [`ReadStep::Parquet`](#readstepparquet) | Reader for Apache Parquet format. |
| [`ReadStep::Json`](#readstepjson) | Reader for JSON files that contain an array of objects within them. |
| [`ReadStep::NdJson`](#readstepndjson) | Reader for files containing multiple newline-delimited JSON objects with the same schema. |
| [`ReadStep::NdGeoJson`](#readstepndgeojson) | Reader for Newline-delimited GeoJSON files. It is similar to `GeoJson` format but instead of `FeatureCollection` object in the root it expects every individual feature object to appear on its own line. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/source/v1alpha1/ReadStep.json)

### `ReadStep::Csv`
Reader for comma-separated files.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `ddlSchema` | `array(string)` |  |  | DEPRECATED: A DDL-formatted schema. Schema can be used to coerce values into more appropriate data types. |
| `separator` | `string` |  |  | Sets a single character as a separator for each field and value.<br/><br/>Default: `,` |
| `encoding` | `string` |  |  | Decodes the CSV files by the given encoding type.<br/><br/>Default: `utf8` |
| `quote` | `string` |  |  | Sets a single character used for escaping quoted values where the separator can be part of the value. Set an empty string to turn off quotations.<br/><br/>Default: `"` |
| `escape` | `string` |  |  | Sets a single character used for escaping quotes inside an already quoted value.<br/><br/>Default: `\` |
| `header` | `boolean` |  |  | Use the first line as names of columns. |
| `inferSchema` | `boolean` |  |  | Infers the input schema automatically from data. It requires one extra pass over the data. |
| `nullValue` | `string` |  |  | Sets the string representation of a null value. |
| `dateFormat` | `string` |  |  | Sets the string that indicates a date format. The `rfc3339` is the only required format, the other format strings are implementation-specific.<br/><br/>Default: `rfc3339` |
| `timestampFormat` | `string` |  |  | Sets the string that indicates a timestamp format. The `rfc3339` is the only required format, the other format strings are implementation-specific.<br/><br/>Default: `rfc3339` |
| `schema` | [`DataSchema`](#dataschema) |  |  | Schema used to coerce values into more appropriate data types. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/source/v1alpha1/ReadStep.json)

### `ReadStep::Json`
Reader for JSON files that contain an array of objects within them.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `subPath` | `string` |  |  | Path in the form of `a.b.c` to a sub-element of the root JSON object that is an array or objects. If not specified it is assumed that the root element is an array. |
| `ddlSchema` | `array(string)` |  |  | DEPRECATED: A DDL-formatted schema. Schema can be used to coerce values into more appropriate data types. |
| `dateFormat` | `string` |  |  | Sets the string that indicates a date format. The `rfc3339` is the only required format, the other format strings are implementation-specific.<br/><br/>Default: `rfc3339` |
| `encoding` | `string` |  |  | Allows to forcibly set one of standard basic or extended encodings.<br/><br/>Default: `utf8` |
| `timestampFormat` | `string` |  |  | Sets the string that indicates a timestamp format. The `rfc3339` is the only required format, the other format strings are implementation-specific.<br/><br/>Default: `rfc3339` |
| `schema` | [`DataSchema`](#dataschema) |  |  | Schema used to coerce values into more appropriate data types. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/source/v1alpha1/ReadStep.json)

### `ReadStep::NdJson`
Reader for files containing multiple newline-delimited JSON objects with the same schema.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `ddlSchema` | `array(string)` |  |  | DEPRECATED: A DDL-formatted schema. Schema can be used to coerce values into more appropriate data types. |
| `dateFormat` | `string` |  |  | Sets the string that indicates a date format. The `rfc3339` is the only required format, the other format strings are implementation-specific.<br/><br/>Default: `rfc3339` |
| `encoding` | `string` |  |  | Allows to forcibly set one of standard basic or extended encodings.<br/><br/>Default: `utf8` |
| `timestampFormat` | `string` |  |  | Sets the string that indicates a timestamp format. The `rfc3339` is the only required format, the other format strings are implementation-specific.<br/><br/>Default: `rfc3339` |
| `schema` | [`DataSchema`](#dataschema) |  |  | Schema used to coerce values into more appropriate data types. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/source/v1alpha1/ReadStep.json)

### `ReadStep::GeoJson`
Reader for GeoJSON files. It expects one `FeatureCollection` object in the root and will create a record per each `Feature` inside it extracting the properties into individual columns and leaving the feature geometry in its own column.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `ddlSchema` | `array(string)` |  |  | DEPRECATED: A DDL-formatted schema. Schema can be used to coerce values into more appropriate data types. |
| `schema` | [`DataSchema`](#dataschema) |  |  | Schema used to coerce values into more appropriate data types. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/source/v1alpha1/ReadStep.json)

### `ReadStep::NdGeoJson`
Reader for Newline-delimited GeoJSON files. It is similar to `GeoJson` format but instead of `FeatureCollection` object in the root it expects every individual feature object to appear on its own line.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `ddlSchema` | `array(string)` |  |  | DEPRECATED: A DDL-formatted schema. Schema can be used to coerce values into more appropriate data types. |
| `schema` | [`DataSchema`](#dataschema) |  |  | Schema used to coerce values into more appropriate data types. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/source/v1alpha1/ReadStep.json)

### `ReadStep::EsriShapefile`
Reader for ESRI Shapefile format.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `ddlSchema` | `array(string)` |  |  | DEPRECATED: A DDL-formatted schema. Schema can be used to coerce values into more appropriate data types. |
| `subPath` | `string` |  |  | If the ZIP archive contains multiple shapefiles use this field to specify a sub-path to the desired `.shp` file. Can contain glob patterns to act as a filter. |
| `schema` | [`DataSchema`](#dataschema) |  |  | Schema used to coerce values into more appropriate data types. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/source/v1alpha1/ReadStep.json)

### `ReadStep::Parquet`
Reader for Apache Parquet format.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `ddlSchema` | `array(string)` |  |  | DEPRECATED: A DDL-formatted schema. Schema can be used to coerce values into more appropriate data types. |
| `schema` | [`DataSchema`](#dataschema) |  |  | Schema used to coerce values into more appropriate data types. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/source/v1alpha1/ReadStep.json)


### `RequestHeader`
Defines a header (e.g. HTTP) to be passed into some request.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `name` | `string` | ✔️ |  | Name of the header. |
| `value` | `string` | ✔️ |  | Value of the header. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/source/v1alpha1/RequestHeader.json)

### `Source`
Defines an external source of data for ingestion.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `$schema` | `string` | ✔️ | `type-uri` | Identifies this resource type. |
| `headers` | [`ResourceHeadersInput`](#resourceheadersinput) | ✔️ |  | Container for identity and ownership information of a resource. |
| `spec` | [`SourceSpecInput`](#sourcespecinput) | ✔️ |  | Specifies the desired state of the resource. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/source/v1alpha1/Source.json)

### `SourceCaching`
Defines how external data should be cached.

| Union Type | Description |
| --- | --- |
| [`SourceCaching::Forever`](#sourcecachingforever) | After source was processed once it will never be ingested again. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/source/v1alpha1/SourceCaching.json)

### `SourceCaching::Forever`
After source was processed once it will never be ingested again.

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/source/v1alpha1/SourceCaching.json)


### `SourceOrdering`
Specifies how input files should be ordered before ingestion.

| Enum Value |
| :---: |
| `ByEventTime` |
| `ByName` |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/source/v1alpha1/SourceOrdering.json)

### `SourceSpec`
Specifies an external source of data for ingestion.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `config` | [`ValueRefs`](#valuerefs) |  |  | Brings the configuration values into the local `config` context. |
| `ingress` | [`Ingress`](#ingress) |  |  | Determines where data is sourced from. |
| `prepare` | `array(`[`PrepStep`](#prepstep)`)` |  |  | Defines how raw data is prepared before reading. |
| `read` | [`ReadStep`](#readstep) | ✔️ |  | Defines how data is read into structured format. |
| `preprocess` | [`Transform`](#transform) |  |  | Pre-processing query that shapes the data. |
| `merge` | [`MergeStrategy`](#mergestrategy) |  |  | Determines how newly-ingested data should be merged with existing history. |
| `vocab` | [`DatasetVocabulary`](#datasetvocabulary) |  |  | Defines the mapping of system fields to dataset column names. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/source/v1alpha1/SourceSpec.json)

### `SourceSpecInput`
Specifies an external source of data for ingestion.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `config` | [`ValueRefs`](#valuerefs) |  |  | Brings the configuration values into the local `config` context. |
| `ingress` | [`Ingress`](#ingress) |  |  | Determines where data is sourced from. |
| `prepare` | `array(`[`PrepStep`](#prepstep)`)` |  |  | Defines how raw data is prepared before reading. |
| `read` | [`ReadStep`](#readstep) | ✔️ |  | Defines how data is read into structured format. |
| `preprocess` | [`Transform`](#transform) |  |  | Pre-processing query that shapes the data. |
| `merge` | [`MergeStrategy`](#mergestrategy) |  |  | Determines how newly-ingested data should be merged with existing history. |
| `vocab` | [`DatasetVocabulary`](#datasetvocabulary) |  |  | Defines the mapping of system fields to dataset column names. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/source/v1alpha1/SourceSpecInput.json)

### `SourceState`
The state of the source the data was added from to allow fast resuming.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `sourceName` | `string` | ✔️ |  | Identifies the source that the state corresponds to. |
| `kind` | `string` | ✔️ |  | Identifies the type of the state. Standard types include: `odf/etag`, `odf/last-modified`. |
| `value` | `string` | ✔️ |  | Opaque value representing the state. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/source/v1alpha1/SourceState.json)

## Storage
### `AwsCredentials`
Access credentials for AWS or an AWS-compatible service.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `accessKey` | [`ValueHandle`](#valuehandle) |  |  | Reference to a secret containing the AWS access key ID. |
| `secretKey` | [`ValueHandle`](#valuehandle) |  |  | Reference to a secret containing the AWS secret access key. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/storage/v1alpha1/AwsCredentials.json)

### `AwsCredentialsInput`
Access credentials for AWS or an AWS-compatible service.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `accessKey` | [`ValueRef`](#valueref) |  |  | Reference to a secret containing the AWS access key ID. |
| `secretKey` | [`ValueRef`](#valueref) |  |  | Reference to a secret containing the AWS secret access key. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/storage/v1alpha1/AwsCredentialsInput.json)

### `PersistentVolume`
Defines a storage volume where data can be stored and its access credentials.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `$schema` | `string` | ✔️ | `type-uri` | Identifies this resource type. |
| `headers` | [`ResourceHeadersInput`](#resourceheadersinput) | ✔️ |  | Container for identity and ownership information of a resource. |
| `spec` | [`PersistentVolumeSpecInput`](#persistentvolumespecinput) | ✔️ |  | Specifies the desired state of the resource. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/storage/v1alpha1/PersistentVolume.json)

### `PersistentVolumeRef`


| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `account` | [`AccountRef`](#accountref) |  |  | Reference to an account that owns the `PersistentVolume`. |
| `id` | `string` |  | `resource-id` | ID of the resource. |
| `name` | `string` |  | `resource-name` | Name of the resource. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/storage/v1alpha1/PersistentVolumeRef.json)

### `PersistentVolumeSpec`
Defines a storage volume where data can be stored and its access credentials.

| Union Type | Description |
| --- | --- |
| [`PersistentVolumeSpec::S3`](#persistentvolumespecs3) | An Amazon S3 or S3-compatible object storage bucket. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/storage/v1alpha1/PersistentVolumeSpec.json)

### `PersistentVolumeSpec::S3`
An Amazon S3 or S3-compatible object storage bucket.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `endpoint` | `string` |  | `uri` | S3 endpoint URL. If omitted, defaults to AWS S3. Use for S3-compatible stores e.g. `https://s3.amazonaws.com`. |
| `region` | `string` |  |  | AWS region where the bucket is located e.g. `us-west-2`. |
| `bucket` | `string` | ✔️ |  | Name of the S3 bucket. |
| `prefix` | `string` |  |  | Optional path prefix within the bucket. |
| `capacity` | [`VolumeCapacity`](#volumecapacity) |  |  | Storage capacity allocation. |
| `credentials` | [`AwsCredentials`](#awscredentials) |  |  | Access credentials for the bucket. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/storage/v1alpha1/PersistentVolumeSpec.json)


### `PersistentVolumeSpecInput`
Defines a storage volume where data can be stored and its access credentials.

| Union Type | Description |
| --- | --- |
| [`PersistentVolumeSpecInput::S3`](#persistentvolumespecinputs3) | An Amazon S3 or S3-compatible object storage bucket. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/storage/v1alpha1/PersistentVolumeSpecInput.json)

### `PersistentVolumeSpecInput::S3`
An Amazon S3 or S3-compatible object storage bucket.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `endpoint` | `string` |  | `uri` | S3 endpoint URL. If omitted, defaults to AWS S3. Use for S3-compatible stores e.g. `https://s3.amazonaws.com`. |
| `region` | `string` |  |  | AWS region where the bucket is located e.g. `us-west-2`. |
| `bucket` | `string` | ✔️ |  | Name of the S3 bucket. |
| `prefix` | `string` |  |  | Optional path prefix within the bucket. |
| `capacity` | [`VolumeCapacity`](#volumecapacity) |  |  | Storage capacity allocation. |
| `credentials` | [`AwsCredentialsInput`](#awscredentialsinput) |  |  | Access credentials for the bucket. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/storage/v1alpha1/PersistentVolumeSpecInput.json)


### `VolumeCapacity`
Storage capacity allocation.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `storage` | `string` |  | `byte-size` | Maximum storage size e.g. `10Gi`. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/storage/v1alpha1/VolumeCapacity.json)

## Task
### `Task`
An individual work item to be executed.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `$schema` | `string` | ✔️ | `type-uri` | Identifies this resource type. |
| `headers` | [`ResourceHeadersInput`](#resourceheadersinput) | ✔️ |  | Container for identity and ownership information of a resource. |
| `spec` | [`TaskSpecInput`](#taskspecinput) |  |  | Specifies the desired state of the task. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/task/v1alpha1/Task.json)

### `TaskOutcome`
Result of the execution of a task.

| Union Type | Description |
| --- | --- |
| [`TaskOutcome::Success`](#taskoutcomesuccess) | Task completed successfully. |
| [`TaskOutcome::Failed`](#taskoutcomefailed) | Task failed. |
| [`TaskOutcome::NoOp`](#taskoutcomenoop) | Task completed with no work done (e.g. no new data to process). |
| [`TaskOutcome::Cancelled`](#taskoutcomecancelled) | Task was cancelled before completion. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/task/v1alpha1/TaskOutcome.json)

### `TaskOutcome::Success`
Task completed successfully.

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/task/v1alpha1/TaskOutcome.json)

### `TaskOutcome::Failed`
Task failed.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `message` | `string` | ✔️ |  | Human-readable description of the failure. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/task/v1alpha1/TaskOutcome.json)

### `TaskOutcome::NoOp`
Task completed with no work done (e.g. no new data to process).

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/task/v1alpha1/TaskOutcome.json)

### `TaskOutcome::Cancelled`
Task was cancelled before completion.

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/task/v1alpha1/TaskOutcome.json)


### `TaskPlan`
A self-contained logical execution plan of a task.

_Map of string keys to arbitrary values._

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/task/v1alpha1/TaskPlan.json)

### `TaskSpec`
An individual work item to be executed as part of a flow.

| Union Type | Description |
| --- | --- |
| [`TaskSpec::Ingest`](#taskspecingest) | Fetches data from a source and appends it to a dataset. |
| [`TaskSpec::Transform`](#taskspectransform) | Executes transformation of data defined in a derivative dataset. |
| [`TaskSpec::Compaction`](#taskspeccompaction) | Compacts data files in matching datasets to improve query performance. |
| [`TaskSpec::GarbageCollection`](#taskspecgarbagecollection) | Removes unreferenced data files from matching datasets. |
| [`TaskSpec::WebhookCall`](#taskspecwebhookcall) | Dispatches a certain payload to a specific `WebhookTarget`. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/task/v1alpha1/TaskSpec.json)

### `TaskSpec::Ingest`
Fetches data from a source and appends it to a dataset.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `name` | `string` |  |  | An alias for the task used to refer to it in flows and access the results |
| `source` | [`ResourceHandle`](#resourcehandle) | ✔️ |  | Reference to the source resource that defines how to fetch data. |
| `params` | [`IngestParams`](#ingestparams) |  |  | Optional parameters to control ingestion behavior. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/task/v1alpha1/TaskSpec.json)

### `TaskSpec::Transform`
Executes transformation of data defined in a derivative dataset.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `name` | `string` |  |  | An alias for the task used to refer to it in flows and access the results |
| `target` | [`DatasetHandle`](#datasethandle) |  |  | Reference to the derivative dataset that defines how to transform data. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/task/v1alpha1/TaskSpec.json)

### `TaskSpec::Compaction`
Compacts data files in matching datasets to improve query performance.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `name` | `string` |  |  | An alias for the task used to refer to it in flows and access the results |
| `params` | [`CompactionParams`](#compactionparams) |  |  | Optional parameters to control ingestion behavior. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/task/v1alpha1/TaskSpec.json)

### `TaskSpec::GarbageCollection`
Removes unreferenced data files from matching datasets.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `name` | `string` |  |  | An alias for the task used to refer to it in flows and access the results |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/task/v1alpha1/TaskSpec.json)

### `TaskSpec::WebhookCall`
Dispatches a certain payload to a specific `WebhookTarget`.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `name` | `string` |  |  | An alias for the task used to refer to it in flows and access the results |
| `target` | [`ResourceHandle`](#resourcehandle) | ✔️ |  | Reference to the `WebhookTarget`. |
| `payload` | `string` |  |  | The payload to send. May include templating. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/task/v1alpha1/TaskSpec.json)


### `TaskSpecInput`
An individual work item to be executed as part of a flow.

| Union Type | Description |
| --- | --- |
| [`TaskSpecInput::Ingest`](#taskspecinputingest) | Fetches data from a source and appends it to a dataset. |
| [`TaskSpecInput::Transform`](#taskspecinputtransform) | Executes transformation of data defined in a derivative dataset. |
| [`TaskSpecInput::Compaction`](#taskspecinputcompaction) | Compacts data files in matching datasets to improve query performance. |
| [`TaskSpecInput::GarbageCollection`](#taskspecinputgarbagecollection) | Removes unreferenced data files from matching datasets. |
| [`TaskSpecInput::WebhookCall`](#taskspecinputwebhookcall) | Dispatches a certain payload to a specific `WebhookTarget`. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/task/v1alpha1/TaskSpecInput.json)

### `TaskSpecInput::Ingest`
Fetches data from a source and appends it to a dataset.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `name` | `string` |  |  | An alias for the task used to refer to it in flows and access the results |
| `source` | [`ResourceRef`](#resourceref) | ✔️ |  | Reference to the source resource that defines how to fetch data. |
| `params` | [`IngestParams`](#ingestparams) |  |  | Optional parameters to control ingestion behavior. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/task/v1alpha1/TaskSpecInput.json)

### `TaskSpecInput::Transform`
Executes transformation of data defined in a derivative dataset.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `name` | `string` |  |  | An alias for the task used to refer to it in flows and access the results |
| `target` | [`DatasetRef`](#datasetref) |  |  | Reference to the derivative dataset that defines how to transform data. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/task/v1alpha1/TaskSpecInput.json)

### `TaskSpecInput::Compaction`
Compacts data files in matching datasets to improve query performance.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `name` | `string` |  |  | An alias for the task used to refer to it in flows and access the results |
| `params` | [`CompactionParams`](#compactionparams) |  |  | Optional parameters to control ingestion behavior. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/task/v1alpha1/TaskSpecInput.json)

### `TaskSpecInput::GarbageCollection`
Removes unreferenced data files from matching datasets.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `name` | `string` |  |  | An alias for the task used to refer to it in flows and access the results |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/task/v1alpha1/TaskSpecInput.json)

### `TaskSpecInput::WebhookCall`
Dispatches a certain payload to a specific `WebhookTarget`.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `name` | `string` |  |  | An alias for the task used to refer to it in flows and access the results |
| `target` | [`ResourceRef`](#resourceref) | ✔️ |  | Reference to the `WebhookTarget`. |
| `payload` | `string` |  |  | The payload to send. May include templating. |
| `retryPolicy` | [`RetryPolicy`](#retrypolicy) |  |  | Defines how a webhook should react to failures. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/task/v1alpha1/TaskSpecInput.json)


### `TaskStatus`
Execution phase of a task.

| Enum Value |
| :---: |
| `Pending` |
| `Planning` |
| `Ready` |
| `Running` |
| `Committing` |
| `Finished` |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://opendatafabric.org/schemas/task/v1alpha1/TaskStatus.json)

