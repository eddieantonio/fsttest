How to specify the FST under test
=================================

`fsttest` can help you test either **Foma** saved FSTs (`*.fomabin`
files) or defined rules in an **XFST script** (`.xfscript` file).


Loading an FST from a pre-compile Fomabin
-----------------------------------------

In your `test_*.toml` file, use this as your `[fst]` section:

```toml
[fst]
fomabin = "path/to/fst.fomabin"
```

Replace `path/to/fst.fomabin` with the path to your fomabin.

### Example

Suppose I have the following folder structure:

    .
    ├── michif.fomabin
    └── tests
        └── test_verbs.toml

I want to test `michif.fomabin` in `test_verbs.toml` Then let this be
the start of `test_verbs.toml`:

```toml
[fst]
fomabin = "michif.fomabin"
```



Loading an FST from an XFST script
----------------------------------

In your `test_*.toml` file, use this as the start of your `[fst]` section:

```toml
[fst]
eval = "path/to/script.xfscript"
regex = "DefinedRuleInTheXFScript"
```
