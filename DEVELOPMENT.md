## Testing
```bash
pytest --cov=badger --cov-report=term-missing
```

## Releasing to pypi
```bash
python setup.py bdist_wheel
gpg --detach-sign -a dist/<the newly created wheel>
twine upload dist/<new whl> dist/<new whl.asc>
```