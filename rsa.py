import random
import math

def is_prime(number):
    if number < 2:
        return False
    for i in range (2, number // 2 + 1):
        if number % i == 0:
            return False
    return True

def generate_prime(min_value, max_value):
    prime = random.randint(min_value, max_value)
    while not is_prime(prime):
        prime = random.randint(min_value, max_value)
    return prime

def mod_inverse(e, phi):
    for d in range(3, phi):
        if ((d * e) % phi) == 1:
            return d
    raise ValueError("mod_inverse does not exist")

def public_key(phi_n):
    
    e = random.randint(3, phi_n-1)

    while (math.gcd(e, phi_n)) != 1:
        e = random.randint(3, phi_n - 1)
    return e

def encode(m, e, n):

    m_encoded = [ord(c) for c in m]
    cypher = [pow(c, e, n) for c in m_encoded]

    return cypher

def decode(mc, d, n):

    me = [pow(c, d, n) for c in mc]
    m_decoded = "".join(chr(c) for c in me)

    return m_decoded

def encrypt_file(input_file, output_file, e, n):
    with open(input_file, 'r') as file:
        text = file.read()
    encrypted_data = encode(text, e, n)
    
    # Save encrypted data as space-separated integers
    with open(output_file, 'w') as file:
        file.write(" ".join(map(str, encrypted_data)))

def decrypt_file(input_file, output_file, d, n):
    with open(input_file, 'r') as file:
        encrypted_data = list(map(int, file.read().split()))
    decrypted_text = decode(encrypted_data, d, n)
    
    with open(output_file, 'w') as file:
        file.write(decrypted_text)

if __name__ == "__main__":
    
    p, q = generate_prime(1000, 5000), generate_prime(1000, 5000)

    while p == q:
        q = generate_prime(1000, 5000)

    n = p * q

    phi_n = (p-1) * (q - 1)

    e = public_key(phi_n)

    d = mod_inverse(e, phi_n)

    #print("Public Key: ", e)
    #print("Private Key: ", d)
    #print("n: ", n)
    #print("Phi of n: ", phi_n)
    #print("p: ", p)
    #print("q: ", q)

    input_file = input("Enter path to your file!\n")
    encrypted_file = "encrypted.txt"
    decrypted_file = "decrypted.txt"

    # Encrypt and save the file
    encrypt_file(input_file, encrypted_file, e, n)

    # Decrypt and save the file
    decrypt_file(encrypted_file, decrypted_file, d, n)