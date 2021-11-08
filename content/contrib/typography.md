---
Title: Typography
description: Common UI elements used in documentation
weight: 1000
alwaysopen: false
categories: []
---

## Media

### Static Image

Input:

```markdown
{{</*image filename="/images/kamu_logo.svg" alt="Kamu logo" width="30%"*/>}}
```

Result:

{{<image filename="/images/kamu_logo.svg" alt="Kamu logo" width="30%">}}

## Tables

Input:

```markdown
| Name | Description |
| ---- | :---------: |
| Foo  |    Test     |
| Bar  |    Test     |
```

Result:

| Name | Description |
| ---- | :---------: |
| Foo  |    Test     |
| Bar  |    Test     |


## Text Blocks

Input:

```markdown
{{</*tip*/>}}
Tip block
{{</*/tip*/>}}

{{</*note*/>}}
Note block
{{</*/note*/>}}

{{</*info*/>}}
Info block
{{</*/info*/>}}

{{</*warning*/>}}
Warning block
{{</*/warning*/>}}

{{</*danger*/>}}
Danger block
{{</*/danger*/>}}
```

Result:

{{<tip>}}
Tip block
{{</tip>}}

{{<note>}}
Note block
{{</note>}}

{{<info>}}
Info block
{{</info>}}

{{<warning>}}
Warning block
{{</warning>}}

{{<danger>}}
Danger block
{{</danger>}}