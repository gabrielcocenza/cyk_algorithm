# Gabriel Angelo Sgarbi Cocenza nºUSP: 6448118

import os

def read_file(filename):
    filename = os.path.join(os.curdir, filename)
    with open(filename, 'r') as f:
        return f.read().splitlines()


def write_output_file(results) -> None:
    with open("out-status.txt", "w") as f:
        for result in results:
            f.write(" ".join(result))


def get_rules(rows):
    current_cyk = 1
    cyk_index = 1
    n_cyk = int(rows[0])
    rules = {}

    while current_cyk <= n_cyk:
        n_var, n_symbol, n_rule =  map(int, rows[cyk_index].split(' '))
        vars = rows[cyk_index + 1].split(' ')
        symbols = rows[cyk_index + 2].split(' ')
        s0 = vars[0]
        assert len(vars) == n_var
        assert len(symbols) == n_symbol
        rules[current_cyk] = {'s0': s0}

        for i in range(cyk_index + 3, cyk_index + 3 + n_rule):
            left, right = rows[i].replace(' ', '').split('=>')
            if len(right) > 1:
                if not rules[current_cyk].get(right):
                    rules[current_cyk][right] = set()
                rules[current_cyk][right].add(left)
            else:
                if not rules[current_cyk].get('initial'):
                    rules[current_cyk]['initial'] = []
                
                if left == s0:
                    rules[current_cyk]['initial'].append(right) 
                
                if not rules[current_cyk].get('terminals'):
                    rules[current_cyk]['terminals'] = {}
                
                if not rules[current_cyk]['terminals'].get(right):
                    rules[current_cyk]['terminals'][right] = []
                rules[current_cyk]['terminals'][right].append(left)

        cyk_index = cyk_index + 3 + n_rule
        current_cyk += 1
    
    return rules, n_cyk


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
            if input in rule['initial']:
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
                for i in range(0, len(input) - l + 1):
                    j = i + l -1
                    for k in range(i, j):
                        w = list(table[i][k])
                        x = list(table[k+1][j])
                        if len(w) > 0:
                            for elem_w in w:
                                for elem_x in x:
                                    a = f'{elem_w} {elem_x}'
                                    match = rule.get(f'{elem_w}{elem_x}')
                                    if match:
                                        table[i][j].update(match)

            #Se 𝑆0∈𝑀(1,𝑛), aceite; senão, rejeite
            if rule['s0'] in table[0][len(input) - 1]:
                result.append('1')
            else:
                result.append('0')

    return result


def main():
    results = []
    rows_grammar = read_file('inp-glc.txt')
    rows_input = read_file('inp-cadeias.txt')
    rules, n_cyk = get_rules(rows_grammar)
    inputs = get_inputs(rows_input, n_cyk)
    for key in rules.keys():
        results.append(cyk_alg(rules[key], inputs[key]) + ["\n"])
    
    write_output_file(results)


if __name__ == "__main__":
    main()