import requests
import argparse
import re


def create_arg_parser():
    parser = argparse.ArgumentParser(description='Extract subdomains from crt.sh.')
    parser.add_argument('domains', nargs='+')
    return parser

def request_crt(domain):
    url = f'https://crt.sh/?q={domain}'
    resp = requests.get(url)
    return resp

def process_body(body):
    domains = set()
    # in some cells threre are multiple domains separated by <BR>
    cells = re.findall(r'<TD>([^<].*)</TD>', body)
    for cell in cells:
        cell = cell.split('<BR>')
        for domain in cell:
            # exclude wildcard domains
            if '*' not in domain:
                domains.add(domain)
    return sorted(domains)

def get_subdomains(domains):
    subdomains = set()
    for domain in domains:
        resp = request_crt(domain)
        subdomains |= set(process_body(resp.text))
    return subdomains


if __name__ == '__main__':
    args = create_arg_parser().parse_args()
    domains = args.domains

    subdomains = get_subdomains(domains)
    print('\n'.join(subdomains))