exec: fetch-pypi-hash:
{ name, version, filename ? "${name}-${version}.tar.gz" }: exec [
  "${fetch-pypi-hash}/bin/fetch-pypi-hash" name version filename
]
