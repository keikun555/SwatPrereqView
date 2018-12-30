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
from functools import lru_cache
from collections import defaultdict


VERBOSE = False
# compiled regex to match courses
creg = re.compile('[A-Z]{4} \d{3}[A-Z]*(?: [A-Z]+)?')
node_cnt = defaultdict(int)  # counts how many times the node came up


def vprint(*args, **kwargs):
    ''' verbose printing '''
    if VERBOSE:
        print(*args, **kwargs)


@lru_cache(maxsize=None)
def course_to_node(course):
    ''' maps course string to node string '''
    return ''.join(course.split())


def extract_dept(cdict):
    ''' given course dict, map it to its department '''
    return cdict['department']


def extract_node(cdict):
    ''' given course dict, map it to its node '''
    node_label = course_to_node(cdict['course'])
    node_id = node_label + str(node_cnt[node_label])
    node_cnt[node_label] += 1
    prereqs = creg.findall(cdict['prereq'])
    return {
        'id': node_id,
        'label': node_label,
        'desc': str(cdict['text'][len(cdict['course'])+2:]),
        'font': {'size': 30},
        'shape': 'box',
        'dept': cdict['course'].split()[0],
        'prereqs': list(filter(None, map(course_to_node, prereqs)))
    }


def extract_edges(node):
    ''' given node dict, map it to its list of edges '''
    edge_list = []
    for prereq in node['prereqs']:
        depts = list(set([prereq[:4], node['dept']]))
        edges = [{
            'from': prereq+str(i),
            'to': node['id'],
            'arrows': 'to',
            'depts': depts
            } for i in range(node_cnt[prereq]+1)]
        edge_list += edges
    return edge_list


def convert_json(ijson, num_threads=None):
    ''' given list of dicts ijson, returns converted list of dicts '''
    pool = multi.Pool(processes=num_threads)
    depts = list(set(pool.map(extract_dept, ijson)))
    nodes = list(map(extract_node, ijson))
    vprint('extracted', len(nodes), 'nodes')
    edges = list(chain.from_iterable(pool.map(extract_edges, nodes)))
    vprint('extracted', len(edges), 'edges')
    pool.close()
    return [depts, nodes, edges]


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
