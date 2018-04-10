nix-fetchers
==============

A set of morally pure fetching builtins for [Nix].

[Nix]: https://nixos.org/nix

Prerequisites
--------------

While the fetchers provided here are *morally* pure (that is, they
always yield the same output for a given input), they rely on
operations (such as network access) that `Nix` by itself can't allow.
As such, they all rely on the special `exec` builtin. In vanilla
`Nix`, this builtin is only available when the
`allow-unsafe-native-code-during-evaluation` configuration setting is
`true`. This allows *any* `Nix` evaluation to run arbitrary code as
the user, though, so the [nix-plugins] project includes the
[extraBuiltins] plugin to make `exec` available only in specific
user-controlled circumstances. See the [extraBuiltins] documentation
for more details.

[nix-plugins]: https://github.com/shlevy/nix-plugins
[extraBuiltins]: https://github.com/shlevy/nix-plugins#extra-builtins

Project structure
------------------

Due to their privileged nature and their expected use as being
(lazily) referenced for every `Nix` evaluation (in the `extraBuiltins`
model), the fetchers are organized a bit unusually for `Nix` projects.

Each fetcher has a subdirectory in this repo. The subdirectory
contains at least two `Nix` expressions:

* `build.nix`: This is a "normal" `Nix` expression like you might find
  in [nixpkgs]. It is callable via the normal `callPackage` mechanism
  and returns a derivation containing the program that will actually
  be run by the fetcher.
* `run.nix`: This expression takes two arguments. The first is the
  `exec` builtin itself, the second is a package or path that includes
  the program built by `build.nix`. The result of applying the
  function in `run.nix` is usually another function corresponding to
  the fetcher interface itself, documented in the fetcher's
  `README.md`.

Note that the second argument to `run.nix` may just be the result of
`callPackage build.nix {}`, or it may for example be a `buildEnv`
containing at least that result.

This design allows the user to opt-in only to the plugins they need
and avoid having their `extra-builtins.nix` (which is included in
every evaluation) require a reference to or evaluation of a full
`nixpkgs` set. See [make-extra-builtins] for a recommended workflow
for this.

[nixpkgs]: https://nixos.org/nixpkgs
[make-extra-builtins]: #make-extra-builtins

make-extra-builtins
---------------------

This repo contains [make-extra-builtins.nix], defining a function to
generate `extra-builtins.nix` from a set of fetchers. After being
imported with `callPackage`, `make-extra-builtins` takes a set of
directories with the same structure as the fetchers in this project
and returns a derivation yielding `extra-builtins.nix` in a directory
suitable for including in a top-level `extra-builtins.nix` or serving
as it directly. For example, if you only wanted fetchers
`fetch-monotone` and `fetch-bitkeeper`, you could do something like:

```nix
let
  pkgs = import <nixpkgs> {};
  make-extra-builtins =
    pkgs.callPackage <nix-fetchers/make-extra-builtins.nix> {};
in make-extra-builtins {
  fetchers.fetch-monotone = <nix-fetchers/fetch-monotone>;
  fetchers.fetch-bitkeeper = <nix-fetchers/fetch-bitkeeper>;
}
```

Which will generate an `extra-builtins.nix` like:

```nix
{ exec, ... }: let
  fetcher-programs = builtins.storePath /nix/store/g13qx40xakg4zaz1bprx0ix5j8mlidlj-fetcher-programs;
in {
  fetch-monotone = import /nix/store/v6z4bc0mzzw1b9sqc2yhn2n11fbj6nqs-run.nix exec fetcher-programs;
  fetch-bitkeeper = import /nix/store/0hkg88a9z08jaipcp4rn6xm62f74i22n-run.nix exec fetcher-programs;
}
```

which has no dependency on `nixpkgs`.

There is a top-level `all-fetchers.nix` that can be imported and
passed as `fetchers` to `make-extra-builtins` if you wish to simply
include all of the fetchers defined here.

[make-extra-builtins.nix]: ./make-extra-builtins.nix 

Testing
--------

The test suite can be run with the [run] script in the [test]
directory. Note that the test suite relies on network connectivity
(naturally), so it cannot be run within a `Nix` build itself.

[run]: ./test/run
[test]: ./test
