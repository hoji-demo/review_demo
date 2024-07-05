import socket
import hashlib

# Constants (public parameters)
PRIME_P = 23  # A large prime number
GENERATOR_G = 5   # A generator of the multiplicative group of integers modulo p

def verify_proof(commitment, challenge, response, public_key):
    """Verify the proof."""
    left_hand_side = pow(GENERATOR_G, response, PRIME_P)
    right_hand_side = (commitment * pow(public_key, challenge, PRIME_P)) % PRIME_P
    return left_hand_side == right_hand_side

def weak_generate_challenge(commitment):
    """Generate a challenge using a weak hashing scheme."""
    challenge_input = str(commitment).encode('utf-8')
    challenge = int(hashlib.sha256(challenge_input).hexdigest(), 16) % PRIME_P
    return challenge

def server_program():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 5000))
    server_socket.listen(1)
    print("Server is listening on port 5000...")
    
    conn, addr = server_socket.accept()
    print(f"Connection from {addr}")

    # Receive public key and commitment from client
    public_key = int(conn.recv(1024).decode())
    commitment = int(conn.recv(1024).decode())

    # Generate challenge
    challenge = weak_generate_challenge(commitment)
    conn.send(str(challenge).encode())

    # Receive response from client
    response = int(conn.recv(1024).decode())

    # Verify proof
    is_valid = verify_proof(commitment, challenge, response, public_key)
    verification_result = "Valid" if is_valid else "Invalid"
    print("Verification result:", verification_result)

    conn.send(verification_result.encode())
    conn.close()

if __name__ == '__main__':
    server_program()

