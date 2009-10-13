from sys import stdin

from re import compile

from optparse import OptionParser

def print_constant(constant, value):
    print "%s = GLenum(0x%.4X)" % (constant, value)

def read_header(file):
    constant = compile('#define\s+(GL_[A-Z0-9_x]+)\s+(0x[0-9A-Fa-f]+|[0-9]+L?)')

    constants = {}
    for line in file:
        m = constant.search(line)
        if m:
            name, value = m.groups([1, 2])
            constants[name] = value

    return constants

def parse_values(constants):
    transformed_constants = {}

    for name, value in constants.iteritems():
        transformed_constants[name] = eval(value)
    return transformed_constants

def select(constants, selection):
    transformed_constants = {}

    selected = compile('^(GL_)?(%s)(_[A-Z]+)?$' % '|'.join(selection)) # results in some false positives
                                                                       # can remedy with list of vendor names
    for name, value in constants.iteritems():
        if selected.match(name):
            transformed_constants[name] = value

    return transformed_constants

def remove_prefix(constants):
    transformed_constants = {}

    prefix = compile('^GL_(.*)$')

    for name, value in constants.iteritems():
        m = prefix.match(name)

        if m:
            name = m.group(1)

        transformed_constants[name] = value

    return transformed_constants

def remove_duplicates(constants, cull_list):
    suffix_regex = compile("^([A-Za-z0-9_]+)_(%s)$" % '|'.join(cull_list))

    def compare_suffixes(a, b):
        try:
            a = cull_list.index(a)
        except ValueError:
            return -1

        try:
            b = cull_list.index(b)
        except ValueError:
            return 1

        return b - a

    values = {}
    for constant, value in constants.iteritems():
        try:
            values[value].append(constant)
        except KeyError:
            values[value] = [constant]

    transformed_constants = {}
    for value, constants in values.iteritems():
        duplicates = {}
        for constant in constants:
            m = suffix_regex.match(constant)
            if not m:
                root = constant
                suffix = None
            else:
                root, suffix = m.groups([1, 2])
            
            try:
                duplicates[root].append((constant, suffix))
            except KeyError:
                duplicates[root] = [(constant, suffix)]
        
        for root, suffixes in duplicates.iteritems():
            suffixes.sort(cmp=compare_suffixes, key=lambda x: x[1]) 

            transformed_constants[suffixes[0][0]] = value

    return transformed_constants
    
if __name__ == '__main__':
    parser = OptionParser(usage="%prog [options]")
    parser.add_option('--clear-cull', dest='cull', action='store_const', const=list(),
                      help="There is a predefined list of suffixes to cull, this clears them.")
    parser.add_option('-c', '--cull', dest='cull', action='append',
                      default=['APPLE', 'SGIX', 'ATI', 'NV', 'EXT', 'ARB'],
                      help="Define a preference for constant suffixes, from least preferred to most.")
    parser.add_option('-s', '--select', dest='select', action='append',
                      default=[],
                      help="Select which constants you want to retrieve")

    options, args = parser.parse_args()

    constants = read_header(stdin)
    if options.select:
        constants = select(constants, options.select)
    constants = remove_prefix(constants) # remove GL_ from constant names
    constants = parse_values(constants)  # transform strings into integers for constant values

    constants = remove_duplicates(constants, options.cull)

    print "from gltypes import GLenum"
    print
    for constant, value in constants.iteritems():
        print_constant(constant, value)
