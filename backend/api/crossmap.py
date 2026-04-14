from flask import Blueprint, request, jsonify, Response
from crossmap import get_crossmap, get_families, get_stats, generate_sankey_csv

crossmap_bp = Blueprint("crossmap", __name__)

@crossmap_bp.route('', methods=['GET'])
def crossmap():
    """Return NIST 800-53 cross-mapping to ISO 27001, CSF 2.0, ISO 27005."""
    family = request.args.get('family')
    nist_id = request.args.get('nist_id')
    framework = request.args.get('framework')
    data = get_crossmap(family=family, nist_id=nist_id, framework=framework)
    return jsonify({"mappings": data, "count": len(data)}), 200

@crossmap_bp.route('/families', methods=['GET'])
def crossmap_families():
    return jsonify({"families": get_families()}), 200

@crossmap_bp.route('/stats', methods=['GET'])
def crossmap_stats():
    return jsonify(get_stats()), 200

@crossmap_bp.route('/sankey', methods=['GET'])
def crossmap_sankey():
    csv_data = generate_sankey_csv()
    return Response(
        csv_data,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=nist_crossmap_sankey.csv'},
    )
