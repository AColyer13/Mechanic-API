from flask import Blueprint, request, jsonify
from application.extensions import limiter, cache
from application.models import Order, User
from application import db

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/orders', methods=['POST'])
@limiter.limit("20 per hour")  # Rate limit: only 20 orders per hour per client
def create_order():
    # Rate limiting is crucial here to prevent order spam and ensure
    # legitimate use of the ordering system. Prevents overwhelming mechanics
    # with fake or duplicate orders
    data = request.get_json()
    new_order = Order(
        user_id=data['user_id'],
        mechanic_id=data['mechanic_id'],
        service_type=data['service_type'],
        status='pending'
    )
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'message': 'Order created', 'order_id': new_order.id}), 201

@orders_bp.route('/orders/<int:order_id>', methods=['GET'])
@cache.cached(timeout=180)  # Cache individual orders for 3 minutes
def get_order(order_id):
    # Caching individual order details improves performance when
    # order details are accessed multiple times (customer checks, mechanic updates)
    order = Order.query.get_or_404(order_id)
    return jsonify({
        'id': order.id,
        'user_id': order.user_id,
        'mechanic_id': order.mechanic_id,
        'service_type': order.service_type,
        'status': order.status
    }), 200