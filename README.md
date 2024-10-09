## XMLparser: Parse speeches of German plenary sessions (Bundestag)

### Usage:

```bash
python3 execute.py > output.csv
sed -i '/<redner id="[^:]*:/d' output.csv
```
