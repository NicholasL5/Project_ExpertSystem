class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class Stack:
    def __init__(self):
        self.top = None

    def is_empty(self):
        if self.top is None:
            return True
        return False

    def peek(self):
        return self.top.data

    def push(self, data):
        node = Node(data)
        node.next = self.top
        self.top = node

    def pop(self):
        if not self.is_empty():
            node = self.top
            self.top = self.top.next
            node.next = None
            return node.data
        return None

    def print(self):
        temp = self.top
        while temp is not None:
            print(temp.data, end=" ")
            temp = temp.next

        print()

    def get_top(self):
        return self.top


class Queue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def is_empty(self):
        if self.head is None:
            return True
        return False

    def peek(self):
        return self.head.data

    def get_head(self):
        return self.head

    def enQueue(self, data):
        node = Node(data)
        if self.is_empty():
            self.head = node
            self.tail = self.head
            self.head.next = self.tail
        else:
            self.tail.next = node
            self.tail = node
        self.size += 1

    def deQueue(self):
        if self.is_empty():
            return print("kosong")

        node = self.head
        self.head = self.head.next
        node.next = None

        self.size -= 1
        return node.data

    def get_size(self):
        return self.size

    def print(self):
        temp = self.head
        while temp is not self.tail:
            print(temp.data, end=" ")
            temp = temp.next
        print(temp.data)


def cek_operator(value):
    if value == "+" or value == "*" or value == "-" or value == "/":
        return True
    else:
        return False


def cek_string(value):
    counter = 0
    for i in value:
        if counter == 2:
            print("Invalid")
            return False
        if cek_operator(i):
            counter += 1
        else:
            counter = 0
    if counter == 2:
        print("Invalid")
        return False
    print("valid")
    return True


def to_prefix(stack: Stack):
    operand = Stack()
    operator = Stack()
    while not stack.is_empty():
        if not cek_operator(stack.peek()):
            operand.push(stack.pop())
        else:
            if operator.is_empty():
                operator.push(stack.pop())
            else:
                while not operator.is_empty() and priority(operator.peek()) > priority(stack.peek()):
                    operand.push(operator.pop())
                operator.push(stack.pop())

    while not operator.is_empty():
        operand.push(operator.pop())

    return operand


def calculate_prefix(stack: Stack):
    stack_balik = Stack()
    equ = ""
    hasil = Stack()
    opr = Stack()

    while not stack.is_empty():
        stack_balik.push(stack.pop())

    while not stack_balik.is_empty():
        if not cek_operator(stack_balik.peek()):
            hasil.push(stack_balik.pop())
        else:
            var1 = hasil.pop()
            var2 = hasil.pop()
            if var2 is None:
                temp = var1
            else:
                if stack_balik.peek() == "+":
                    temp = int(var1) + int(var2)
                elif stack_balik.peek() == "*":
                    temp = int(var1) * int(var2)
                elif stack_balik.peek() == "-":
                    temp = int(var1) - int(var2)
                elif stack_balik.peek() == "/":
                    temp = int(var1) / int(var2)
            stack_balik.pop()
            hasil.push(temp)
    return hasil.pop()


def copy_stack(stack: Stack):
    copy = Stack()
    temp_stack = Stack()
    temp = stack.get_top()

    while temp is not None:
        temp_stack.push(temp.data)
        temp = temp.next

    temp = temp_stack.get_top()
    while temp is not None:
        copy.push(temp.data)
        temp = temp.next
    return copy


def to_Queue(stack: Stack):
    new_stack = Stack()
    while not stack.is_empty():
        new_stack.push(stack.pop())
    return new_stack


def priority(value):
    if value == "+" or value == "-":
        return int(1)
    else:
        return int(2)


entry = True
hasil_stack = Stack()
stack_copy = Stack()
infix_Q = Queue()

while entry:
    # asumsi input 1 1, sama seperti memencet kalkulator dan di soal
    char = input("Masukkan input:")[0]
    if char.lower() == "e":
        entry = False
    else:
        # cek kalau input operator dan stack kosong maka tidak diinput
        if not (cek_operator(char) and hasil_stack.is_empty()):

            if hasil_stack.is_empty():
                hasil_stack.push(char)
            else:
                # cek kalau inputan terakhir kali angka dan inputan sekarang angka
                # maka jumlahkan angka 1,2 = 12
                if not cek_operator(hasil_stack.peek()) and not cek_operator(char):
                    if hasil_stack.peek() == "0":
                        hasil_stack.pop()
                        hasil_stack.push(char)
                    else:
                        temp = hasil_stack.pop()
                        temp = str(temp) + str(char)

                        hasil_stack.push(temp)
                elif not (cek_operator(hasil_stack.peek()) and cek_operator(char)):
                    hasil_stack.push(char)

            # hasil inputan akan dicopy 2 kali, tujuannya adalah yang 1 untuk diubah ke infix,
            # diubah ke infix karena output membutuhkan print secara prefix, sedangkan hasil inputan
            # berupa infix yang terbalik
            # yang 1 akan diubah ke prefix untuk menghitung hasil akhir kalkulator
            # hasil input tidak boleh dirubah karena nanti akan mempengaruhi yang lain

            print("ini hasil")
            hasil_stack.print()
            stack_copy = copy_stack(hasil_stack)
            stack_to_infix = copy_stack(hasil_stack)
            print("ini \copy")
            stack_copy.print()
            print("stack to infix")
            stack_to_infix.print()

            print("infix")
            infix = to_Queue(stack_to_infix)
            infix.print()
            # ubah ke prefix
            print("ini prefix")
            prefix = to_prefix(stack_copy)
            prefix.print()

            print("akhir output")
            hasil_akhir = calculate_prefix(prefix)
            print(hasil_akhir)