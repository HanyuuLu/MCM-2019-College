import os
path = '.\\'
if __name__ == '__main__':
    string = '# Inari\'s resource station\n '
    for (folder, subFolder, fileName) in os.walk(path):
        for i in fileName:
            string += '* [%s](%s)\n' % (i, os.path.join(folder, i))
    with open(os.path.join(path, 'readme.md'), 'w') as w:
        w.write(string)
    print(string)
