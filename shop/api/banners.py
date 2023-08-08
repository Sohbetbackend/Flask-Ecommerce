from flask import jsonify, request
from shop.products.models import Banner
from shop.api import bp


@bp.route('/banners/<int:id>', methods=['GET'])
def get_banner(id):
    return jsonify(Banner.query.get_or_404(id).to_dict())


@bp.route('/banners', methods=['GET'])
def get_banners():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Banner.to_collection_dict(Banner.query, page, per_page, 'api.get_categories')
    return jsonify(data)