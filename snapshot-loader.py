#!/usr/bin/env python3

import os, argparse
import tarfile, boto3

parser = argparse.ArgumentParser(description = 'DAOBet blockchain backup tool client')
parser.add_argument('-s','--last-load', action='store_true', help='Download latest snapshot')
parser.add_argument('-b','--last-num', action='store_true', help='Print latest snapshot block num')
args = parser.parse_args()

ENV_NAME = os.getenv('ENV_NAME', 'testnet')
DOWNLOAD_PATH = os.getenv('DOWNLOAD_PATH', '.')

DO_S3_REGION_NAME = os.getenv('DO_S3_REGION', 'fra1')
DO_S3_ENDPOINT_URL = os.getenv('DO_S3_URL', 'https://fra1.digitaloceanspaces.com')
DO_S3_ACCESS_KEY_ID = os.getenv('DO_S3_KEY_ID')
DO_S3_SECRET_ACCESS_KEY = os.getenv('DO_S3_KEY_SECRET')
DO_D3_SPACE = os.getenv('DO_S3_SPACE', 'daoblocks')

client = boto3.session.Session().client('s3',
    region_name=DO_S3_REGION_NAME,
    endpoint_url=DO_S3_ENDPOINT_URL,
    aws_access_key_id=DO_S3_ACCESS_KEY_ID,
    aws_secret_access_key=DO_S3_SECRET_ACCESS_KEY
)


def get_last_snapshot_name():
    result = client.list_objects_v2(
        Bucket=DO_D3_SPACE,
        Prefix=ENV_NAME,
        MaxKeys=1000
    )

    files = result['Contents']

    files.sort(key=lambda x:x['LastModified'])

    return files[-1]['Key']


def download_snapshot(name):
    client.download_file(
        Bucket=DO_D3_SPACE,
        Key=name,
        Filename=name
    )


def extract_file(name, new_name):
    tar = tarfile.open(name, 'r')
    member = tar.getmembers()[0]
    member.name = new_name
    tar.extract(member, DOWNLOAD_PATH)


def delete_tar(name):
    os.remove(name)


def block_num_from_name(name):
    items = name.split('-')
    return int(items[2])


def download_last_snapshot():
    name = get_last_snapshot_name()
    blk_num = block_num_from_name(name)

    new_name = 'snapshot-' + str(blk_num) + '.bin'

    download_snapshot(name)
    extract_file(name, new_name)
    delete_tar(name)

    print(os.path.realpath(DOWNLOAD_PATH + '/' + new_name), end='')


def print_last_blk_num():
    name = get_last_snapshot_name()
    blk_num = block_num_from_name(name)

    print(blk_num, end='')



def main():
    if args.last_load:
        download_last_snapshot()
        return
    if args.last_num:
        print_last_blk_num()
        return
    parser.print_help()

if __name__ == "__main__":
    main()
