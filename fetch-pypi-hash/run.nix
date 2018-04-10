exec: fetch-pypi-hash: { name, version }: exec [
  "${fetch-pypi-hash}/bin/fetch-pypi-hash" name version
]
