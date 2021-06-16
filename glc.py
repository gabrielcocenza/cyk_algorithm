import os

def read_file(filename):
    filename = os.path.join(os.curdir, filename)
    with open(filename, 'r') as f:
        return f.read().splitlines()


def get_rules(rows):
    current_cyk = 1
    cyk_index = 1
    n_cyk = int(rows[0])
    rules = {}

    while current_cyk <= n_cyk:
        n_var, n_symbol, n_rule =  map(int, rows[cyk_index].split(' '))
        vars = rows[cyk_index + 1].split(' ')
        symbols = rows[cyk_index + 2].split(' ')
        assert len(vars) == n_var
        assert len(symbols) == n_symbol
        rules[current_cyk] = {}
        # print(rules)

        for i in range(cyk_index + 3, cyk_index + 3 + n_rule):
            left, right = rows[i].split(' => ')
            if len(right) > 1:
                if not rules[current_cyk].get(right):
                    rules[current_cyk][right] = set()
                rules[current_cyk][right].add(left)
            else:
                if not rules[current_cyk].get('terminals'):
                    rules[current_cyk]['terminals'] = {}
                if not rules[current_cyk]['terminals'].get(right):
                    rules[current_cyk]['terminals'][right] = []
                rules[current_cyk]['terminals'][right].append(left)
            # print(rules[current_cyk])



        # print()
        # print()
        cyk_index = cyk_index + 3 + n_rule
        current_cyk += 1
    
    return rules, n_cyk


def init_rules(vars):
    rules = {}
    for var in vars:
        rules[var] = {'terminals': [], 'non_terminals': []}

    return rules


def get_inputs(rows, n_cyk):
    inputs = {}
    current_cyk = 1
    cyk_index = 0

    while current_cyk <= n_cyk:
        inputs[current_cyk] = []
        n_inputs =  int(rows[cyk_index])
        for i in range(cyk_index + 1, cyk_index + n_inputs + 1):
            inputs[current_cyk].append(rows[i].replace(' ', ''))

        cyk_index = cyk_index + n_inputs + 1
        current_cyk += 1

    return inputs

def cyk_alg(rule, inputs):
    result = []

    for input in inputs:
        #cadeias de tamano 1
        if len(input) == 1:
            if input in list(rule['terminals'].keys()):
                result.append('1')
            else:
                result.append('0')

        else:
            table = [[set() for _ in range(len(input))] for i in range(len(input))]
            
            #subcadeias de tamanho 1
            for i in range(len(input)):
                table[i][i].update(rule['terminals'][input[i]])

            #subcadeias tamanho >= 2
            for l in range(2, len(input) + 1):
                # print(f'l = {l}')
                for i in range(0, len(input) - l + 1):
                    # print(f'i = {i}')
                    j = i + l -1
                    # print(f'j = {j}')
                    for k in range(i, j):
                        print(f'table[{i}][{k}]')
                        print(f'table[{k+1}][{j}]')
                        w = list(table[i][k])
                        x = list(table[k+1][j])
                        if len(w) > 0:
                            for elem_w in w:
                                for elem_x in x:
                                    a = f'{elem_w} {elem_x}'
                                    print(a)
                                    match = rule.get(f'{elem_w} {elem_x}')
                                    print(match)
                                    if match:
                                        table[i][j].update(match)
                        print(f'l = {l}, i = {i}, j = {j}, k = {k}')
                        pass


            if table[0][len(input) - 1]:
                result.append('1')
            else:
                result.append('0')
            print(input)
            for row in table:
                print(row)
            print()
            
    return result


def main():
    rows_grammar = read_file('teste-glc.txt')
    rows_input = read_file('teste-cadeias.txt')
    rules, n_cyk = get_rules(rows_grammar)
    inputs = get_inputs(rows_input, n_cyk)
    print(f'rules: {rules[1]}')
    print(f'inputs {inputs[1]}')
    result = cyk_alg(rules[1], inputs[1])
    print(f'final result: {result}')


if __name__ == "__main__":
    main()