
class Node(object):
    def __init__(self, name=None, value=None):
        self.name = name
        self.value = value
        self.lchild = None
        self.rchild = None

    def __repr__(self):
        return str([self.name, self.value, self.rchild, self.lchild])

class HuffmanTree(object):
    def __init__(self, char_Weights):
        self.Leaf = [Node(name, value) for name, value in char_Weights.items()]
        while len(self.Leaf) != 1:
            self.Leaf.sort(key=lambda node: node.value, reverse=True)
            n = Node(value=(self.Leaf[-1].value + self.Leaf[-2].value))
            n.lchild = self.Leaf.pop(-1)
            n.rchild = self.Leaf.pop(-1)
            self.Leaf.append(n)
        self.root = self.Leaf[0]
        self.Buffer = list(range(1000))
        self.done_tree = {}

    def __Hu_generate(self, tree, length):
        node = tree
        if (not node):
            return
        elif node.name:
            for i in range(length):
                self.done_tree[node.name] = ''
            for i in range(length):
                self.done_tree[node.name] += str(self.Buffer[i])                
            return

        self.Buffer[length] = 0
        self.__Hu_generate(node.lchild, length + 1)
        self.Buffer[length] = 1
        self.__Hu_generate(node.rchild, length + 1)
    def get_code(self):
        self.__Hu_generate(self.root, 0)
        return self.done_tree

class Archivator():
    letter_array = []
    parsed_symbols = {}

    def __init__(self, input_file):
        self.input_file = input_file

    def __get_array_from_file(self):
        try:
            with open(self.input_file, 'r', encoding='UTF-8') as file:
                for char in file.read():
                    self.letter_array.append(char)
        except FileNotFoundError:
            print('такого файла не существует')
            quit()
    
    def __parse_array_to_dict(self):
        for char in self.letter_array:
            if char in self.parsed_symbols:
                self.parsed_symbols[char] = self.parsed_symbols[char] + 1
            else:
                self.parsed_symbols[char] = 1
        self.parsed_symbols = {key: value for key, value in sorted(self.parsed_symbols.items(), key=lambda item: item[1], reverse=True)}


    def archive(self):
        self.__get_array_from_file()
        self.__parse_array_to_dict()
        create_tree = HuffmanTree(self.parsed_symbols)
        alphabet = create_tree.get_code()

        with open(self.input_file.removesuffix('.txt') + '.bin', 'wb') as bin_file:
            for char in self.letter_array:
                bin_file.write(alphabet.get(char).encode())
            bin_file.write(b'\n')
            for key, value in alphabet.items():
                if key == '\n':
                    key = r'\n'
                text = '{0}={1},'.format(key, value).encode()
                bin_file.write(text)
    

    def __recover_alphabet(self, text):
        text = text.split(',')
        recoverd_text = {}
        
        for word in text:
            wordkv = word.split('=')
            
            if len(wordkv) == 1:
                pass
            else:
                recoverd_text[wordkv[0]] = wordkv[1]
        return recoverd_text        

    def __get_key(self, val, alphabet):
        for key, value in alphabet.items():
            if val == value:
                return key

        return "key doesn't exist"

    def unzip(self):
        try:
            with open(self.input_file, 'rb') as bin_file:
                out = bin_file.readlines()
        except FileNotFoundError:
            print('такого файла не существует')
            quit()

        alphabet = self.__recover_alphabet(out[1].decode())
        code = out[0].decode()

        alphabet_values = list(alphabet.values())
        ptr = 0
        endptr = 1
        counter = 0

        text = ''

        while endptr < len(code):
            if counter == len(alphabet_values):
                counter = 0
                endptr += 1
            if code[ptr:endptr] == alphabet_values[counter]:
                key = self.__get_key(code[ptr:endptr], alphabet)
                if key == r'\n':
                    key = '\n'
                text += key
                ptr = endptr
                endptr += 1

            counter += 1

        with open(self.input_file.removesuffix('.bin') + '_new' + '.txt', 'w', encoding='UTF-8') as file:
            file.write(text)
        

if __name__ == '__main__':
    try:
        selection = int(input('архивировать 1, разархивировать 0: '))
        file = input('напишите путь до файла: ')
    except ValueError:
        print('Ввести нужно только одну цифру')
        quit()
    
    if selection == 1:
        A = Archivator(file)
        A.archive()
        print('архивация успешна')

    elif selection == 0:
        A = Archivator(file)
        A.unzip()
        print('разархивация успешна')
    else:
        print('не правильно введена цифра')
