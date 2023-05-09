from hashlib import sha256

password = 'hashtest'
salt = '22yLUkKC&c88'

string_bytes = bytes(f'{password}{salt}','utf-8')

m = sha256(string_bytes).hexdigest()
print(m)

