'''
Kei Imada
20181229

Converts from course description json to prereq visualizer json
'''

import re
import sys
import json
import argparse
from itertools import chain
import multiprocessing as multi


VERBOSE = False
creg = re.compile('[A-Z]{4} \d{3}[A-Z]*')  # compiled regex to match courses


def vprint(*args, **kwargs):
    ''' verbose printing '''
    if VERBOSE:
        print(*args, **kwargs)


def course_to_node(course):
    ''' maps course string to node string '''
    return ''.join(course.split())


def extract_node(cdict):
    ''' given course dict, map it to its node '''
    node = course_to_node(cdict['course'])
    return {'id': node, 'label': node}


def extract_edges(cdict):
    ''' given course dict, map it to its edges '''
    node = course_to_node(cdict['course'])
    in_edges = map(course_to_node, creg.findall(cdict['prereq']))
    return list(map(lambda s: {'from': s, 'to': node}, in_edges))


def convert_json(ijson, num_threads=None):
    ''' given list of dicts ijson, returns converted list of dicts '''
    pool = multi.Pool(num_threads)
    nodes = pool.map(extract_node, ijson)
    vprint('extracted', len(nodes), 'nodes')
    edges = list(chain.from_iterable(pool.map(extract_edges, ijson)))
    pool.close()
    return [nodes, edges]


def main():
    global VERBOSE
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=argparse.FileType('r'),
                        default=sys.stdin,
                        help='json file IFILE to convert',
                        metavar='IFILE')
    parser.add_argument('-o', '--out', type=argparse.FileType('w'),
                        default=sys.stdout,
                        help='Write converted data to OFILE',
                        metavar='OFILE')
    parser.add_argument('-t', '--threads', type=int, metavar='N',
                        help='Use N threads (default: number of cores)',
                        default=None)
    parser.add_argument('-v', '--verbose', help='Be verbose',
                        action='store_true', default=False)

    args = parser.parse_args()
    VERBOSE = args.verbose
    ojson = convert_json(json.load(args.file), num_threads=args.threads)
    json.dump(ojson, args.out)
    args.file.close()
    args.out.close()


if __name__ == '__main__':
    main()
