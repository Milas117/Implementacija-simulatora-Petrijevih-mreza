from petri_net import PetriNet

# configuration example
configuration = {
    'P': ['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7'],
    'T': ['t1', 't2', 't3', 't4', 't5'],
    'F': [('p1', 't1', 1), ('t1', 'p2', 1), ('p2', 't2', 1), ('t2', 'p3', 1),
          ('t2', 'p4', 1), ('p3', 't3', 1), ('p4', 't4', 1), ('t3', 'p5', 1),
          ('t4', 'p6', 1), ('p5', 't5', 1), ('p6', 't5', 1),('t5', 'p7', 1)],
    'M': [1, 0, 0, 0, 0, 0, 0]
}

# configuration 1 from the paper
w1, w2, w3 = 1, 1, 1
configuration1 = {
    'P': ['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7'],
    'T': ['t1', 't2', 't3', 't4', 't5'],
    'F': [('p1', 't1', 1), ('t1', 'p2', 1), ('p2', 't2', 1), ('t2', 'p3', w1),
          ('t2', 'p4', w2), ('p3', 't3', 1), ('p4', 't4', w3), ('t3', 'p5', 1),
          ('t4', 'p6', 1), ('p5', 't5', 1), ('p6', 't5', 1),('t5', 'p7', 1)],
    'M': [1, 0, 0, 0, 0, 0, 0]
}

# configuration 2 from the paper
w1, w2, w3, w4 = 2, 4, 3, 3
configuration2 = {
    'P': ['i', 'p1', 'p2', 'p3', 'p4', 'p5', 'o'],
    'T': ['fork', 'check_insurance', 'contact_garage', 'join', 'pay_damage',
          'send_letter'],
    'F': [('i', 'fork', 1), ('fork', 'p1', w1), ('fork', 'p2', w2),
          ('p1', 'check_insurance', 1), ('check_insurance', 'p3', 1),
          ('p2', 'contact_garage', 1), ('contact_garage', 'p4', 1),
          ('p3', 'join', 1), ('p4', 'join', 1), ('join', 'p5', w3),
          ('p5', 'pay_damage', 1), ('p5', 'send_letter', w4),
          ('pay_damage', 'o', 1), ('send_letter', 'o', 1)],
    'M': [6, 0, 1, 0, 1, 1, 0]
}





def main():
    pn = PetriNet.parse_configuration(configuration2)
    pn.run()

if __name__ == '__main__':
    main()
