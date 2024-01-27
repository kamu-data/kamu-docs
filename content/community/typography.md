---
Title: Typography
description: Common UI elements used in documentation
weight: 1000
alwaysopen: false
categories: []
---

This section provides examples of all style elements available to documentation authors and the guidelines on using them.


## Code Blocks

Input:

<pre>
```js
const client = OdfClient::new("odf+https://localhost:8080");
```
</pre>

Result:

```js
const client = OdfClient::new("odf+https://localhost:8080");
```


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


## Tabs

Input:

```markdown
{{</*tabs
    tabTotal="3"
    tabID="1"
    tabName1="Tab 1"
    tabName2="Tab 2"
    tabName3="Tab 3"*/>}} 

{{</*tab tabNum="1"*/>}}
Tab 1 content as text
{{</*/tab*/>}}

{{</* tab tabNum="2"*/>}}
Tab 2 content
- as
- list
{{</*/tab*/>}}

{{</* tab tabNum="3"*/>}}
{{</*info*/>}}
Tab 3 content as rich elements
{{</*/info*/>}}
{{</*/tab*/>}}

{{</*/tabs*/>}}
```

Result:

{{<tabs tabTotal="3" tabID="1" tabName1="Tab 1" tabName2="Tab 2" tabName3="Tab 3">}}

{{<tab tabNum="1">}}
Tab 1 content as text
{{</tab>}}

{{<tab tabNum="2">}}
Tab 2 content
- as
- list
{{</tab>}}

{{<tab tabNum="3">}}
{{<info>}}
Tab 3 content as rich elements
{{</info>}}
{{</tab>}}

{{</tabs>}}


## Static Image

Input:

```markdown
{{</*image filename="/images/kamu_logo.svg" alt="Kamu logo" width="30%"*/>}}
```

Result:

{{<image filename="/images/kamu_logo.svg" alt="Kamu logo" width="30%">}}


## YouTube Video

Input:

```markdown
{{</*youtube hN_vpHYmwi0*/>}}
```

Result:

{{<youtube hN_vpHYmwi0>}}


## YouTube Playlist

Input:

```markdown
{{</*youtube-list PLV91cS45lwVG20Hicztbv7hsjN6x69MJk*/>}}
```

Result:

{{<youtube-list PLV91cS45lwVG20Hicztbv7hsjN6x69MJk>}}

## GOAT Diagrams

Input:

<pre>
```goat
      .               .                .               .--- 1          .-- 1     / 1
     / \              |                |           .---+            .-+         +
    /   \         .---+---.         .--+--.        |   '--- 2      |   '-- 2   / \ 2
   +     +        |       |        |       |    ---+            ---+          +
  / \   / \     .-+-.   .-+-.     .+.     .+.      |   .--- 3      |   .-- 3   \ / 3
 /   \ /   \    |   |   |   |    |   |   |   |     '---+            '-+         +
 1   2 3   4    1   2   3   4    1   2   3   4         '--- 4          '-- 4     \ 4
```
</pre>

Result:

```goat
      .               .                .               .--- 1          .-- 1     / 1
     / \              |                |           .---+            .-+         +
    /   \         .---+---.         .--+--.        |   '--- 2      |   '-- 2   / \ 2
   +     +        |       |        |       |    ---+            ---+          +
  / \   / \     .-+-.   .-+-.     .+.     .+.      |   .--- 3      |   .-- 3   \ / 3
 /   \ /   \    |   |   |   |    |   |   |   |     '---+            '-+         +
 1   2 3   4    1   2   3   4    1   2   3   4         '--- 4          '-- 4     \ 4
```

See more examples [here](https://gohugo.io/content-management/diagrams/).

## Mermaid Diagrams

Input:

<pre>
```mermaid
sequenceDiagram
    Alice ->> Bob: Hello Bob, how are you?
    Bob-->>John: How about you John?
    Bob--x Alice: I am good thanks!
    Bob-x John: I am good thanks!
    Note right of John: Bob thinks a long<br/>long time, so long<br/>that the text does<br/>not fit on a row.

    Bob-->Alice: Checking with John...
    Alice->John: Yes... John, how are you?

```
</pre>

Result:

```mermaid
sequenceDiagram
    Alice ->> Bob: Hello Bob, how are you?
    Bob-->>John: How about you John?
    Bob--x Alice: I am good thanks!
    Bob-x John: I am good thanks!
    Note right of John: Bob thinks a long<br/>long time, so long<br/>that the text does<br/>not fit on a row.

    Bob-->Alice: Checking with John...
    Alice->John: Yes... John, how are you?

```

See more examples [here](https://mermaid.js.org/syntax/examples.html).
