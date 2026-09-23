# Data

Raw and processed data are not committed. To fetch the raw data, run from the project root:

```bash
python scripts/download_data.py
```

This saves `data/raw/uci_taiwan_default.xls` and checks it against the SHA-256 in `configs/uci_taiwan.toml`.

## Source

**Default of Credit Card Clients**, UCI Machine Learning Repository.
https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients
DOI: [10.24432/C55S3H](https://doi.org/10.24432/C55S3H)

30,000 credit card clients in Taiwan (April to September 2005), 23 explanatory variables and a binary target: default payment in the following month.

## Citation

Yeh, I.-C. and Lien, C.-H. (2009) 'The comparisons of data mining techniques for the predictive accuracy of probability of default of credit card clients', *Expert Systems with Applications*, 36(2), pp. 2473–2480.

## Licence

Creative Commons Attribution 4.0 International (CC BY 4.0).
