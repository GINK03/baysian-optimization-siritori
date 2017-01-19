# coding: utf-8
import re
import math
import os
import sys
import glob
import random
import re
import pickle 

KATAKANA = """アイウエオ
カキクケコ
ガギグゲゴ
サシスセソ
ザジズゼゾ
タチツテト
ダヂズデド
ナニヌネノ
ハヒフヘホ
バビブベボ
パピプペポ
マミムメモ
ラリルレロ
ヤユヨ
ャュョ
ワオン
"""
def conv_rules_gen():
    inputs = KATAKANA.split('\n')
    title = inputs[0]
    convs = []
    for es in inputs:
        if es == "ヤユヨ" or es == "ワオン" or es == "ャュョ":
          print( list(map(lambda x: (x[0] + 'ー', x[0] + x[1]), list(zip(es, "アウオ")) ) )  )
          convs.append( list(map(lambda x: (x[0] + 'ー', x[0] + x[1]), \
                list(zip(es, "アウオ")) ) \
          ))
        else:
          convs.append( list(map(lambda x: (x[0] + 'ー', x[0] + x[1]), \
                list(zip(es, title)) ) \
          ))
    return sum(convs, [])

conv_rules = conv_rules_gen()

class Noun(object):
    def __init__(self):
        self.name = ""
        self.orig = ""
        self.yomi = ""
        self.head = ""
        self.tail = ""
        self.head_tail = ""

chain = []
bases = []
nlist = []
for name in glob.glob('./*'):
  allkana = list(map(lambda x:x, KATAKANA.replace('\n', '') ) )
  if 'Noun' not in name and 'noun' not in name : continue
  for line in open(name).read().split('\n'):
    if line == '' : continue
    tp = line.split(',')
    orig = tp[0]
    yomi = tp[-2]
    for rep in [('ァ','ア'), ('ィ','イ'), ('ゥ','ウ'), ('ェ','エ'), ('ォ','オ'), ('ャ', 'ヤ'), ('ュ', 'ユ'), ('ョ', 'ヨ'), ('ッ', 'ツ'), ('ヅ', 'ツ'), ('ヱ', 'エ')]:
      yomi = yomi.replace(rep[0], rep[1])
    for rule in conv_rules:
      yomi = yomi.replace(rule[0], rule[1])
     
    head = yomi[0]
    tail = yomi[-1]
    #print(name, orig, yomi, head, tail)
    n = Noun()
    n.name = name
    n.orig = orig
    n.yomi = yomi
    n.tail = tail
    n.head = head
    n.head_tail = head + tail
    if n.head not in allkana or n.tail not in allkana:
        continue
    if n.tail == 'ン':
        nlist.append(n)
    else:
        bases.append(n)

if '--stat' in sys.argv:
  def statistics():
    eachhead = {}
    for b in bases:
        if eachhead.get(b.head) is None: eachhead[b.head] = 0
        eachhead[b.head] += 1
    for t, n in eachhead.items():
        #print("head", t, n)
        pass
    
    eachtail = {}
    for b in bases:
        if eachtail.get(b.tail) is None: eachtail[b.tail] = 0
        eachtail[b.tail] += 1
    for t, n in eachtail.items():
        #print("tail", t, n)
        pass

    for k in eachhead.keys():
        if eachtail.get(k) is not None:
            print("k", k, "h", eachhead[k], "t", eachtail[k])
  statistics()
  sys.exit()

def insert_op():
    for be in range(len(bases)):
        try:
            bases[be]
        except IndexError as e:
            print('finished max len ', len(chain) )
            sys.exit()
        if bases[be].tail == "ン" : 
            #print(bases[be].yomi)
            continue
        if bases[be].head != bases[be].tail: continue
        #print(base.orig, base.head_tail, base.yomi)
        for ce in range(len(chain) - 2): 
            #print( chain[ce].tail + chain[ce+1].head, bases[be].tail, bases[be].head_tail, bases[be].yomi)
            if chain[ce].tail + chain[ce+1].head == bases[be].head_tail:
                chain.insert(ce+1, bases[be])
                _ = bases.pop(be)
                print( 'iter', be, len(chain), len(bases), chain[ce].yomi, chain[ce+1].yomi, chain[ce+2].yomi )
if '--insert_op' in sys.argv:
    chain = pickle.loads(open('./chain.pkl', 'rb').read())
    bases = pickle.loads(open('./bases.pkl', 'rb').read())
    nlist = pickle.loads(open('./nlist.pkl', 'rb').read())
    insert_op()

def search(tail):
    ps = list(map(float, sys.argv[1:]))
    not_found = True
    if random.random() > 0.98:
        random.shuffle(bases)
    for e, _ in enumerate(bases):
        #if tail == n.head and "ン" != n.tail and n.tail not in ['ル']:
        n = bases[e]
        if tail == n.head and "ン" != n.tail:
            if 'ル' == n.tail and random.random() < 1.: continue
            if 'ヂ' == n.tail and random.random() < 1.: continue
            if 'ワ' == n.tail and random.random() < 1.: continue
            if 'ラ' == n.tail and random.random() < ps[7]: continue
            if 'ウ' == n.tail and random.random() < ps[6]: continue
            if 'ゲ' == n.tail and random.random() < ps[5]: continue
            if 'ズ' == n.tail and random.random() < ps[4]: continue
            if 'マ' == n.tail and random.random() < ps[3]: continue
            if 'リ' == n.tail and random.random() < ps[2]: continue
            if 'ケ' == n.tail and random.random() < ps[1]: continue
            if 'エ' == n.tail and random.random() < ps[0]: continue
            not_found = False
            break
    if not_found == False:
      t = bases.pop(e)
      return t
    print('最後の文字は、', chain[-1].orig, chain[-1].yomi)
    _ = bases.pop(e)
    point = str(len(chain))
    open('./chain.' + point + '.pkl', 'wb').write(pickle.dumps(chain))
    open('./bases.' + point + '.pkl', 'wb').write(pickle.dumps(bases))
    open('./nlist.' + point + '.pkl', 'wb').write(pickle.dumps(nlist))
    sys.exit(0)

def main():
    seed = bases.pop( random.randint(1, len(bases)) )
    chain.append(seed)
    print(1, seed.orig, seed.yomi, seed.tail, seed.head)

    for i in range(300000):
        tail = chain[-1].tail
        t = search(tail)
        chain.append(t)
        print(len(chain), len(bases), t.orig, t.yomi)

if __name__ == '__main__':
    random.shuffle(bases)
    main()
