import socket
import random

# Constants (public parameters)
PRIME_P = 23  # A large prime number
GENERATOR_G = 5   # A generator of the multiplicative group of integers modulo p

def generate_public_key(secret):
    """Generate public key from secret."""
    return pow(GENERATOR_G, secret, PRIME_P)

def generate_commitment():
    """Generate a random commitment."""
    random_secret = random.randint(1, PRIME_P - 1)
    commitment = pow(GENERATOR_G, random_secret, PRIME_P)
    return random_secret, commitment

def generate_response(random_secret, challenge, prover_secret):
    """Generate response using the random secret, challenge, and prover's secret."""
    return (random_secret + challenge * prover_secret) % (PRIME_P - 1)

def client_program():
    prover_secret = 6  # Prover's secret (private key)
    public_key = generate_public_key(prover_secret)

    # Prover generates commitment
    random_secret, commitment = generate_commitment()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5000))

    # Send public key and commitment to server
    client_socket.send(str(public_key).encode())
    client_socket.send(str(commitment).encode())

    # Receive challenge from server
    challenge = int(client_socket.recv(1024).decode())

    # Generate response
    response = generate_response(random_secret, challenge, prover_secret)

    # Send response to server
    client_socket.send(str(response).encode())

    # Receive verification result from server
    verification_result = client_socket.recv(1024).decode()
    print("Verification result from server:", verification_result)

    client_socket.close()

if __name__ == '__main__':
    client_program()

