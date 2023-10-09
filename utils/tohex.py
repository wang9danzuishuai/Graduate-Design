hex_string = "11 22 33 44"
hex_data = bytearray.fromhex(hex_string)
print(hex_data)
print(len(hex_data))


def print_hex(bytes):
    l = [hex(int(i)) for i in bytes]
    print(" ".join(l))


print_hex(hex_data)


def print_bytes_hex(data):
    l = ['%02X' % i for i in data]
    print(" ".join(l))


def print_string_hex(data):
    l = ['%02X' % ord(i) for i in data]
    print(" ".join(l))


print_bytes_hex(hex_data)
arr = 'work'
print_string_hex(arr)