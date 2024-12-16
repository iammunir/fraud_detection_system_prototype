from flask import Flask, request, jsonify
from app.celery_app import celery_app
from app.tasks import preprocess_transaction
from app.validators import validate_transaction
from app.models import Transaction, engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
Session = sessionmaker(bind=engine)

@app.route('/process_transactions', methods=['POST'])
def process_transactions():
    transactions = request.json
    
    # Validate all transactions
    validation_errors = {}
    for transaction in transactions:
        errors = validate_transaction(transaction)
        if errors:
            validation_errors[transaction['id']] = errors

    if validation_errors:
        return jsonify({'errors': validation_errors}), 400

    # Process valid transactions
    try:
        task = preprocess_transaction.delay(transactions)
        return jsonify({'message': 'transactions are on queue to process', 'task_id': task.id}), 202
    except Exception as e:
        return jsonify({'errors': str(e)}), 500

@app.route('/status_task/<task_id>', methods=['GET'])
def get_task_status(task_id):
    task_result = celery_app.AsyncResult(task_id)
    return jsonify({
        'task_id': task_id,
        'status': task_result.status,
        'result': task_result.result
    })

@app.route('/status_transaction/<transaction_id>', methods=['GET'])
def get_transaction_status(transaction_id):
    session = Session()
    try:
        transaction = session.query(Transaction).filter_by(trans_num=transaction_id).first()
        if not transaction:
            return jsonify({'error': 'Transaction not found'}), 404
        
        return jsonify(transaction.to_dict()), 200
    finally:
        session.close()
