import os
import json

from collections import defaultdict
from copy import deepcopy

from tqdm import tqdm

def load_data(file_path):
    data = []
    num = 0
    with open(file_path, 'r', encoding='utf-8') as f:
        sample = {}
        for line in f:
            if line.startswith('<question'):
                sample['question'] = line.strip().split('\t')[1].strip().lower()
            elif line.startswith('<triple'):
                s, p, o = line.replace('\n', '').split('\t')[1].split(' ||| ')
                sample['triple'] = s.lower(), p.replace(' ', ''), o.lower() #{'triple':('头实体','关系','尾实体')}
                assert len(sample['triple']) == 3, (line, sample['triple']) #验证失败的话，把括号里面的打出来
            elif line.startswith('==='):
                if sample['triple'][0] in sample['question']: #如果头实体在问题里，那么把这条数据放进data，否则num+1不放data
                    data.append(sample)
                else:
                    num += 1
                sample = {}
            else:
                pass
    print('num of failed sample: {}'.format(num))
    print('num of training sample: {}'.format(len(data)))
    return data #[{'question':'问题1','triple':('头实体','关系','尾实体'},{问题2}]

def load_knowledge(file_path='NLPCC2017-OpenDomainQA/knowledge/nlpcc-iccpol-2016.kbqa.kb'):
    s2p = defaultdict(list)
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            s, p, _ = [tmp.strip() for tmp in line.strip().split(' ||| ')]
            s = s.lower()
            p = p.replace(' ', '')
            s2p[s].append(p)
    return s2p #{'实体':['关系1', '关系2'...]}

if __name__ == "__main__":
    train_data = load_data('data/nlpcc-iccpol-2016.kbqa.training-data')
    s2p = load_knowledge()
    for item in tqdm(train_data):
        s, p, _ = item['triple']
        ps = deepcopy(s2p[s]) #[与实体s相关的所有关系]
        if p in ps:
            ps.remove(p)
        if len(ps) > 0:
            item['negative_predicates'] = ps #[负关系]
        else:
            for ss in s2p:
                if s in ss and p in s2p[ss]:
                    ps = deepcopy(s2p[ss])
                    ps.remove(p)
                    item['negative_predicates'] = ps
                    break

    with open('data/train.json', 'w', encoding='utf-8') as f:
        for sample in train_data:
            f.write(json.dumps(sample, ensure_ascii=False)+'\n')

    test_data = load_data('data/nlpcc-iccpol-2016.kbqa.testing-data')
    with open('data/dev.json', 'w', encoding='utf-8') as f:
        for sample in test_data:
            f.write(json.dumps(sample, ensure_ascii=False)+'\n')


