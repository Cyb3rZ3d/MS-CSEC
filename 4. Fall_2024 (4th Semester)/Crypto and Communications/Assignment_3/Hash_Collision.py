# Hash_Collision.py
"""
Ruben Valdez
Crypto_SecureCommunications
Prof. Dr. Robert Jones
Assignment-2
"""

import hashlib

# Function to test for collision between two similar inputs
def test_for_collision():
    # Original text
    input1 = "Decrypt me, I am secret!!!".encode()
    # Slightly modified text
    input2 = "Decrypt me, I am secret!!! ".encode()  # Extra space at the end

    # Generate MD5 hashes for both inputs
    md5_hash1 = hashlib.md5(input1).hexdigest()
    md5_hash2 = hashlib.md5(input2).hexdigest()

    # Print the inputs and their MD5 hashes
    print(f"Input 1: '{input1.decode()}' \nMD5 Hash: {md5_hash1}\n")
    print(f"Input 2: '{input2.decode()}' \nMD5 Hash: {md5_hash2}\n")

    # Check if they match
    if md5_hash1 == md5_hash2:
        print("COLLISION FOUND: Both inputs produce the same MD5 hash!")
        return True
    else:
        print("NO COLLISION: The MD5 hashes are different.\n")
        return False

# Main function to run the collision test 50 times
def main():
    collision_found = False
    total_runs = 50

    for attempt in range(total_runs):
        print(f"Run {attempt + 1}/{total_runs}")
        if test_for_collision():
            collision_found = True
            break

    if not collision_found:
        print(f"\nNo collision was found after {total_runs} attempts.\n")
        
        print(f"End of Program \n")
        

# Run the main function
if __name__ == "__main__":
    main()
