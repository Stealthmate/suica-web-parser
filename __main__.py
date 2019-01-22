import os
import suica
import argparse
import json

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse suica history from www.mobilesuica.com')
    parser.add_argument('-u', '--username', type=str, dest='usr', default=os.environ.get('SUICA_USERNAME', None))
    parser.add_argument('-p', '--password', type=str, dest='pwd', default=os.environ.get('SUICA_PASSWORD', None))
    parser.add_argument('-o', '--output', type=str, dest='output', default=None, required=False)
    parser.add_argument('-d', '--driver', type=str, dest='driver', required=False, default=os.environ.get('SUICA_DRIVER', None))
    args = parser.parse_args()
    h = suica.parseHistory(args.usr, args.pwd, args.driver)
    if args.output:
        with open(args.output, mode='w', encoding='utf-8') as f:
            f.write(json.dumps(h, indent=2, separators=(',', ':'), ensure_ascii=False))
    else:
        print(h)
