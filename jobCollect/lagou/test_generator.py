# 参考链接：https://www.bytelang.com/article/content/NQbmUaRIXyA=
# 简单来说，generator是一个能够返回迭代器对象的函数.
# 什么是迭代器？

# A simple generator function
def my_gen():
    n = 1
    print('This is printed first')
    # Generator function contains yield statements
    yield n

    n += 1
    print('This is printed second')
    yield n

    n += 1
    print('This is printed at last')
    yield n


# 使用my_gen()
# for i in range(0, 10):
#     print(my_gen().__next__())

'''
gen = my_gen()
for i in range(0,10):
    print(gen.__next__())
'''

# def rev_str(my_str):
#     length = len(my_str)
#     for i in range(length - 1,-1,-1):
#         yield my_str[i]
#
# for char in rev_str("hello"):
#     print(char)
#
#
#
# for i in range(4, -1, -1):
#     print(i)

# generator除了可以应用于string，还可以应用于其它类型的iterator，例如list，tuple等。

# python generator 表达式
# Initialize the list
my_list = [1, 3, 6, 10]

# # square each term using list comprehension
# # Output: [1, 9, 36, 100]
# tmp_list = [x ** 2 for x in my_list]
# print(tmp_list)
#
# # same thing can be done using generator expression
# # Output: <generator object <genexpr> at 0x0000000002EBDAF8>
# tmp_gen = (x ** 2 for x in my_list)
# print(type(tmp_gen))
# for item in tmp_gen:
#     print(type(item))
#
# def my_list_gen():
#     for x in my_list:
#         yield x ** 2
#
# tmp_gen = my_list_gen()
# for item in tmp_gen:
#     print(item)


# python里为什么要使用generator？
# class PowTwo:
#     def __init__(self, max=0):
#         self.max = max
#
#     def __iter__(self):
#         self.n = 0
#         return self
#
#     def __next__(self):
#         if self.n > self.max:
#             raise StopIteration
#
#         result = 2 ** self.n
#         self.n += 1
#         return result
#
#
# x = PowTwo(5)
# for n in x:
#     print(n)

# def PowTwoGen(max = 0):
#     n = 0
#     while n < max:
#         yield 2 ** n
#         n += 1
#
#
# for n in PowTwoGen(5):
#     print(n)


# def all_even():
#     n = 0
#     while True:
#         yield n
#         n += 2
#
#
# tmp_gen = all_even()
# while True:
#     print(tmp_gen.__next__())
#     break
#
# for i in range(0,1000):
#     print(tmp_gen.__next__())

#
# l=[1, 2, 3, 4, [5, 6]]
#
# def sum(l):
#     res = 0
#     for i in l:
#         if not isinstance(i, list):
#             print("here")
#             res+=i
#         else:
#             res+=sum(i)
#     return res
#
#
# def play(l):
#     res = []
#     for i in l:
#         if isinstance(i, list):
#             t = list(play(i))
#             for j in t:
#                 res.append(j)
#         else:
#             res.append(i)
#     return res
#
# print(play(l))

def quick_sort(parameter_list):

    if len(parameter_list) == 0:
        # print("error")
        return
    if len(parameter_list) == 1:
        # print(parameter_list[0])
        yield parameter_list[0]

    if parameter_list[0] < parameter_list[-1]:
        pivot = parameter_list[0]
        left = [i for i in parameter_list if i < pivot]
        right = [i for i in parameter_list if i > pivot]
        for item in quick_sort(left):
            yield item
        # quick_sort(left)      #recursion in Generator are limited
        yield pivot
        # quick_sort(right)
        for item in quick_sort(right):
            yield item

gen = quick_sort([5,6,34,6,2,8,16])
for i in gen:
    print(i)





