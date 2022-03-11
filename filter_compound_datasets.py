import regex as re


with open('datasets/COCA_train_min3_no_doubles.txt', 'r') as infile:
    train_compounds = [line.strip('\n\r') for line in infile]

with open('datasets/COCA_dev_min3_no_doubles.txt', 'r') as infile:
    dev_compounds = [line.strip('\n\r') for line in infile]

with open('datasets/COCA_test_min3_no_doubles.txt', 'r') as infile:
    test_compounds = [line.strip('\n\r') for line in infile]


def remove_double_constituents(compound_list):
    return [compound for compound in compound_list if compound.split()[0] != compound.split()[1]]

def filter_out_nonwords(compound_list):
    repeated_char_reg = re.compile('(.)\1{2,}')
    digit_reg = re.compile('\d')

    filtered_compounds = []
    for compound in compound_list:
        mod, head = compound.split()

        #skip compound if mod or head contains any character repeated three or more times
        if repeated_char_reg.match(mod) or repeated_char_reg.match(head):
            continue
        #skip compound if mod or head contains a digit
        elif digit_reg.match(mod) or digit_reg.match(head):
            continue
        # skip compound if mod or head is shorter than three characters
        elif len(mod) < 3 or len(head) < 3:
            continue
        else:
            filtered_compounds.append(compound)
    return filtered_compounds

train_compounds = remove_double_constituents(train_compounds)
train_compounds = filter_out_nonwords(train_compounds)

dev_compounds = remove_double_constituents(dev_compounds)
dev_compounds = filter_out_nonwords(dev_compounds)

test_compounds = remove_double_constituents(test_compounds)
test_compounds = filter_out_nonwords(test_compounds)

with open('datasets/COCA_train_min3_no_doubles_filtered.txt', 'w') as outfile:
    for compound in train_compounds:
        outfile.write(f'{compound}\n')

with open('datasets/COCA_test_min3_no_doubles_filtered.txt', 'w') as outfile:
    for compound in test_compounds:
        outfile.write(f'{compound}\n')

with open('datasets/COCA_dev_min3_no_doubles_filtered.txt', 'w') as outfile:
    for compound in dev_compounds:
        outfile.write(f'{compound}\n')

