---
Title: Typography
description: Common UI elements used in documentation
weight: 1000
alwaysopen: false
categories: []
---

This section provides examples of all style elements available to documentation authors and the guidelines on using them.


## Links

We have special types of links to refer readers to:
- definitions of terms in the [Glossary]()
- schemas in the [Reference]()

Input:

<pre>
```
Raw data is stored in {{ </*term "slices" "data-slice"*/> }} that are linked from {{ </*schema "MetadataBlock"*/> }}s.
```
</pre>

Result:

```js
Raw data is stored in {{ <term "slices" "data-slice"> }} that are linked from {{ <schema "MetadataBlock"> }}s.
```

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

Result:

> [!tip]
> Tip block

> [!note]
> Note block

> [!info]
> Info block

> [!warning]
> Warning block

> [!danger]
> Danger block

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

```tpl
{{</* tabs "uniqueid" */>}}
    {{</* tab "MacOS" */>}}
        # MacOS

        This is tab **MacOS** content.

        Lorem markdownum insigne. Olympo signis Delphis! Retexi Nereius nova develat
        stringit, frustra Saturnius uteroque inter! Oculis non ritibus Telethusa
        protulit, sed sed aere valvis inhaesuro Pallas animam: qui _quid_, ignes.
        Miseratus fonte Ditis conubia.
    {{</* /tab */>}}
    {{</* tab "Linux" */>}}
        # Linux

        This is tab **Linux** content.

        Lorem markdownum insigne. Olympo signis Delphis! Retexi Nereius nova develat
        stringit, frustra Saturnius uteroque inter! Oculis non ritibus Telethusa
        protulit, sed sed aere valvis inhaesuro Pallas animam: qui _quid_, ignes.
        Miseratus fonte Ditis conubia.
    {{</* /tab */>}}
    {{</* tab "Windows" */>}}
        # Windows

        This is tab **Windows** content.

        Lorem markdownum insigne. Olympo signis Delphis! Retexi Nereius nova develat
        stringit, frustra Saturnius uteroque inter! Oculis non ritibus Telethusa
        protulit, sed sed aere valvis inhaesuro Pallas animam: qui _quid_, ignes.
        Miseratus fonte Ditis conubia.
    {{</* /tab */>}}
{{</* /tabs */>}}
```

Result:

{{<tabs "uniqueid">}}
{{<tab "MacOS">}}
# MacOS

This is tab **MacOS** content.

Lorem markdownum insigne. Olympo signis Delphis! Retexi Nereius nova develat
stringit, frustra Saturnius uteroque inter! Oculis non ritibus Telethusa
protulit, sed sed aere valvis inhaesuro Pallas animam: qui _quid_, ignes.
Miseratus fonte Ditis conubia.
{{< /tab >}}

{{<tab "Linux">}}

# Linux

This is tab **Linux** content.

Lorem markdownum insigne. Olympo signis Delphis! Retexi Nereius nova develat
stringit, frustra Saturnius uteroque inter! Oculis non ritibus Telethusa
protulit, sed sed aere valvis inhaesuro Pallas animam: qui _quid_, ignes.
Miseratus fonte Ditis conubia.
{{< /tab >}}

{{<tab "Windows">}}

# Windows

This is tab **Windows** content.

Lorem markdownum insigne. Olympo signis Delphis! Retexi Nereius nova develat
stringit, frustra Saturnius uteroque inter! Oculis non ritibus Telethusa
protulit, sed sed aere valvis inhaesuro Pallas animam: qui _quid_, ignes.
Miseratus fonte Ditis conubia.
{{</tab>}}
{{</tabs>}}


## Static Image

Input:

```markdown
{{</*image filename="/images/logo.svg" alt="Kamu logo" width="30%"*/>}}
```

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

```markdown
{{</*mermaid align="left"*/>}}
sequenceDiagram
    Alice ->> Bob: Hello Bob, how are you?
    Bob-->>John: How about you John?
    Bob--x Alice: I am good thanks!
    Bob-x John: I am good thanks!
    Note right of John: Bob thinks a long<br/>long time, so long<br/>that the text does<br/>not fit on a row.

    Bob-->Alice: Checking with John...
    Alice->John: Yes... John, how are you?
{{</* /mermaid */>}}
```

Result:


{{<mermaid align="left">}}
sequenceDiagram
    Alice ->> Bob: Hello Bob, how are you?
    Bob-->>John: How about you John?
    Bob--x Alice: I am good thanks!
    Bob-x John: I am good thanks!
    Note right of John: Bob thinks a long<br/>long time, so long<br/>that the text does<br/>not fit on a row.

    Bob-->Alice: Checking with John...
    Alice->John: Yes... John, how are you?
{{< /mermaid >}}

See more examples [here](https://mermaid.js.org/syntax/examples.html).
