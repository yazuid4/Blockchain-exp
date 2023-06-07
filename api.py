from flask import Flask, jsonify, request, make_response
from uuid import uuid4

from Blockchain import Blockchain

app = Flask(__name__)

node_id = str(uuid4()).replace('-', '')

blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    # calculate PoW:
    proof = blockchain.proof_of_work(last_proof)
    # reward: new transaction
    blockchain.new_transaction(**{
        'sender': '0',
        'recipient': node_id,
        'amount': 1
    })
    # new block:
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'index': block['index'],
        'transactions': block['transactions']
    }
    return {
        'status': 200,
        'message': 'new block forged',
        'result': response
    }


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    params = request.get_json()
    if len({'sender', 'recipient', 'amount'}.
                   intersection(set(params.keys()))) == 3:
        # add new transaction
        blockchain.new_transaction(
            params['sender'],
            params['recipient'],
            params['amount']
        )
        return jsonify({'status': 201,
                        'message': 'transaction added successfully'
                        })
    else:
        return jsonify({'status': 400,
                        'message': 'missing values!'
                        })


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        "chain": blockchain.chain,
        "length": len(blockchain.chain)
    }
    return make_response({
        'status': 200,
        'result': response
    })


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
