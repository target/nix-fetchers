# fetch-pypi-hash

Get the hash of the source tarball for a given PyPI package.

## Arguments

* `name`: The name of the package. Must be in the same form as on
  PyPI, despite some tooling being more flexible with cases. For
  example, `pillow` is an error while `Pillow` is correct.
* `version`: The version of the package. Must be in canonical form, as
  defined in [PEP 440][PEP-440].

[PEP-440]: https://www.python.org/dev/peps/pep-0440/

## Return value

### Success

* `sha256`: The SHA-256 hash of the source tarball.

### Failure

* `failure-type`: One of `"HTTP-status"` or `"JSON-parse"`.
* `code`: On an `HTTP-status` error, the non-200 HTTP status code.
* `message`: On a `JSON-parse` error, the error message from the
   parser.

Due to a quirk of the JSON parser in use, some errors due to valid
`JSON` without the expected schema manifest as `null` hashes.

Some errors currently manifest as an evaluation error.

More failure types may be added in the future.

## Notes

Successful results are cached in [XDG_CACHE_HOME], under
`nix-fetchers`.

A `3xx` `HTTP-status` error is a good indication of a non-canonical
package `name`. A `404` `HTTP-status` error is a good indication of a
missing package.

[XDG_CACHE_HOME]: https://specifications.freedesktop.org/basedir-spec/0.7/ar01s03.html
