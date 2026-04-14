from flask import Blueprint, jsonify
from agents import AGENTS_CONFIG
from crossmap import CROSSMAP

config_bp = Blueprint("config", __name__)

@config_bp.route('/config/agents', methods=['GET'])
def get_agents_config():
    """Return the specialist agents configuration as a list."""
    agents_list = []
    for agent_id, data in AGENTS_CONFIG.items():
        agents_list.append({
            "id": agent_id,
            "name": data["name"],
            "description": data["description"],
            "icon": data["icon"],
            "details": data["details"]
        })
    return jsonify(agents_list), 200

@config_bp.route('/config/crossmap', methods=['GET'])
def get_crossmap_config():
    """Return the full crossmap configuration."""
    return jsonify(CROSSMAP), 200
