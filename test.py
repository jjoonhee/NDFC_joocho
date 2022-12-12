


tmp = [123,456]

if tmp is True:
    print("1")
else:
    print("0")

def tmp_func():
    k = 1
    return k

#print(bool(tmp))

print(bool(tmp_func()))

if bool(tmp_func()) is True:
    print("123")

#if bool(tmp_func()) is True:
#    print("123")
#else:
#    print("456")
#
#if tmp is False:
#    print("False")
#elif tmp is True:
#    print("True")
#else:
#    print("3rd")