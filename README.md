# advent-of-code2017

## Stack

Stack is used to manage our project dependencies as well as to fetch GHC.

### Setup

Install Stack: 

    curl -sSL https://get.haskellstack.org/ | sh

Install GHC:

    stack setup

Make sure `~/.local/bin/` is on your $PATH.

More info here: https://docs.haskellstack.org/en/stable/README/

### Install some common utils

The following commands are used by editor plugins and are pretty useful.

    stack install stylish-haskell
    stack install hlint

### Editor Configuration

#### VS Code

I personally really like intero as it plays really nice with stack and
has support in most major editors. For now I'll show vs code but there
should be intero plugins for everything.

Install the following plugins:

    * haskell-linter
    * stylish-haskell
    * hoogle-vscode
    * haskero


### REPL

Get a REPL:

    stack ghci

Once inside a REPL you can load your module (after code changes):

    :load Problem01

Get type information:

    :t map

NOTE: In the REPL to define a new top level declaration you must do it like:

```haskell
let foo = 3
```

### Build & Run

    stack build
    stack exec advent-of-code2017

### Automatic Build

    stack build --file-watch

### hpack

HPack is a new way of specifying dependencies that is a bit simpler than
using cabal files which is the old build tool. 
Stack will auto generate a cabal file from `package.yaml`, so there is no need to edit
it at all. New dependencies can be added to the `package.yaml` file. If stack can't resolve them
then they can be specified in `stack.yaml`.
