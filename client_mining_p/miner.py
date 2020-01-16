import hashlib
import requests
from time import time

import sys
import json


def proof_of_work(block):
    """
    Simple Proof of Work Algorithm
    Stringify the block and look for a proof.
    Loop through possibilities, checking each one against `valid_proof`
    in an effort to find a number that is a valid proof
    :return: A valid proof for the provided block
    """
    # TODO
    block_string = json.dumps(block)
    proof = 0
    while valid_proof(block_string, proof) is False:
        proof += 1
    return proof


def valid_proof(block_string, proof):
    """
    Validates the Proof:  Does hash(block_string, proof) contain 3
    leading zeroes?  Return true if the proof is valid
    :param block_string: <string> The stringified block to use to
    check in combination with `proof`
    :param proof: <int?> The value that when combined with the
    stringified previous block results in a hash that has the
    correct number of leading zeroes.
    :return: True if the resulting hash is a valid proof, False otherwise
    """
    # TODO
    guess = f"{block_string}{proof}".encode()
    guess_hash = hashlib.sha256(guess).hexdigest()

    return guess_hash[:3] == "000"
    # return True or False


if __name__ == '__main__':
    # What is the server address? IE `python3 miner.py https://server.com/api/`
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    # Load ID
    f = open("my_id.txt", "r")
    id = f.readline()
    print("ID is", id)
    f.close()

    # Load coins
    f = open('my_id.txt', 'r')
    content = f.readlines()
    if 'Lambda' in str(content):
      lambda_coin = int(content[-1])
    else:
      lambda_coin = 0
    print('content', content, lambda_coin)
    f.close

    # Run forever until interrupted
    while True:
        start = time()
        r = requests.get(url=node + "/last_block")
        # Handle non-json response
        try:
            data = r.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(r)
            break

        # TODO: Get the block from `data` and use it to look for a new proof
        last_block = data['last_block']
        new_proof = proof_of_work(last_block)

        # When found, POST it to the server {"proof": new_proof, "id": id}
        post_data = {"proof": new_proof, "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()

        # TODO: If the server responds with a 'message' 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
        if 'New Block Forged' in data['message']:
          end = data['new_block']['timestamp']
          timeTaken = end - start
          lambda_coin += 1
          a = open('my_id.txt', 'a')
          a.write(f'Lambda coin as of {str(end)} \n {lambda_coin} \n')
          a.close
          print(f'Plus 1 lambda coins in {timeTaken} secs \n You now have {lambda_coin} coins')
        else:
          print(data['message'])
        breakpoint()
