from sys import stdin

from re import compile

from optparse import OptionParser

def print_constant(constant, value):
    print "%s = GLenum(0x%.4X)" % (constant, value)
    
if __name__ == '__main__':
    parser = OptionParser(usage="%prog [options]")
    parser.add_option('-c', '--cull', dest='cull', action='append',
                      default=['APPLE', 'SGIX', 'ATI', 'NV', 'EXT', 'ARB'],
                      help="Define a preference for constant suffixes, from least preferred to most.")

    options, args = parser.parse_args()

    suffix_regex = compile("^([A-Za-z0-9_]+)_(%s)$" % '|'.join(options.cull))

    constants = {}
    for line in stdin:
        exec(line, {}, constants)

    values = {}
    for constant, value in constants.iteritems():
        try:
            values[value].append(constant)
        except KeyError:
            values[value] = [constant]

    def compare_suffixes(a, b):
        try:
            a = options.cull.index(a)
        except ValueError:
            return -1

        try:
            b = options.cull.index(b)
        except ValueError:
            return 1

        return b - a

    print "from gltypes import GLenum"
    print
#    for constant, value in constants.iteritems():
#        print_constant(constant, value)

    #getting lazy TODO culling ARB EXT etc
    for value, constants in values.iteritems():
        duplicates = {}
        for constant in constants:
            m = suffix_regex.match(constant)
            if not m:
                root = constant
                suffix = None
            else:
                root, suffix = m.groups([1, 2])
                #print root, suffix
            
            try:
                duplicates[root].append((constant, suffix))
            except KeyError:
                duplicates[root] = [(constant, suffix)]
        
        for root, suffixes in duplicates.iteritems():
            suffixes.sort(cmp=compare_suffixes, key=lambda x: x[1]) 

            print_constant(suffixes[0][0], value)
