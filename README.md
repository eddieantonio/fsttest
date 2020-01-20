fsttest
=======

Test your Foma FSTs!

Install
-------

    $ pip install fsttest

Usage
-----

Write `test_*.toml` scripts in a folder called `tests/`, then run:

    $ fsttest


Documentation
-------------

 * [How to specify the FST under test](https://github.com/eddieantonio/fsttest/blob/development/docs/fst-under-test.md#how-to-specify-the-fst-under-test)

Tutorial
--------

In your FST project, create a folder called `tests/`:

    $ mkdir tests

Within this folder create a file called `test_{something}.toml` where
`{something}` is something specific to your FST. For example,
`test_phonology.toml`:

    $ touch tests/test_phonology.toml

Use the following template to create your test:

```toml
# tests/test_phonology.toml
[fst]
eval = "rewrite_rules.xfscript"
compose = ["TInsertion", "NiTDeletion", "Cleanup"]

[[tests]]
upper = "ni<ayaa<n"
expect = "dayaan"

[[tests]]
lower = "ki<tayaa<n"
expect = "kiayaan"
```

Then run the test!

    $ fsttest
    1/1 tests passed! ✨ 🍰 ✨


### Line-by-line

Let's breakdown this file, line-by-line.

```toml
[fst]
```

This defines the **FST under test** — that is, the FST we want to use to
transduce and test its output.

```toml
eval = "rewrite_rules.xfscript"
```

This says that our FST under test can be created by running
`rewrite_rules.xfscript` in Foma, creating an FST. As an example, let's
take the following `rewrite_rules.xfscript`:

```xfscript
# rewrite_rules.xfscript
define Vowel    a | e | i | o | u ;

define TInsertion [..] -> t || [n i | k i] "<" _ Vowel ;
define NiTDeletion n i "<" t -> d || _ Vowel ;
define Cleanup %< -> 0 ;
```

Yours will be different!

```toml
compose = ["TInsertion", "NiTDeletion"]
```

This line says that the **FST under test** is the result of _composing_
the `TInsertion` regex with the `NiTDeletion` regex. That is, the FST
puts its input into `TInsertion` and then passes the result to
`NiTDeletion`. The result of passing it through both FSTs is the result
we want to test.

```toml
[[tests]]
```

Next we define one or more test cases. Begin every test case with
`[[tests]]`: note the **two square brackets**!

```toml
upper = "ni<ayaa<n"
```

This test case feeds the string `ni<ayaa<n` into the upper side of the
FST. The upper side is conventionally the **analysis** side of the FST.

```toml
expect = "dayaan"
```

This says that we **expect** the lower side to be `dayaa<n`. That is,
this test case says that, given the analysis `ni<ayaa<n`, the FST should
produce `dayaa<n` among the possible **surface forms**.

```toml
[[tests]]
```

Next, we define another test case.

```toml
lower = "kitayaan"
```

In contrast to the previous test, we feed the input to the **lower**
side of the FST. In other words, we want to do a **lookup**.
Conventionally, this means we're providing a **surface form**, and
asking the FST to return an analysis.

```toml
expect = "ki<ayaa<n"
```

This means we're **expecting** the analysis of `ki<tayaa<n` when we give
the FST the wordform of `kitayaan`


License
=======

Written in 2020 by Eddie Antonio Santos <Eddie.Santos@nrc-cnrc.gc.ca>.

Licensed under the terms of the Mozilla Public License 2.0 (MPL-2.0).
