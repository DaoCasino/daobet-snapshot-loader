# DAOBet snapshot loader


## Deps
 - python3
 - boto3

## ENVS
 - `DO_S3_KEY_ID` - S3 key ID
 - `DO_S3_KEY_SECRET` - S3 secret key
 - `DOWNLOAD_PATH` - path to download directory

## How to run

### Download

```bash
./snapshot-loader.py --last-load
```

### Print last block num

```bash
./snapshot-loader.py --last-num
```
