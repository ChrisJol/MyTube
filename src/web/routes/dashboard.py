from flask import Blueprint, send_from_directory, current_app, jsonify
import os
from pathlib import Path

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def index():
    """Serve Vue SPA index.html or fallback"""
    try:
        return send_from_directory(current_app.static_folder, 'index.html')
    except FileNotFoundError:
        return jsonify({
            'error': 'Frontend not built',
            'message': 'Run "cd frontend && npm run build" to build the Vue application',
            'frontend_path': current_app.static_folder
        }), 404

@dashboard_bp.route('/<path:path>')
def serve_vue_app(path):
    """Serve Vue SPA for all routes (SPA routing)"""
    # Check if it's a static asset first
    if path.startswith('assets/'):
        try:
            return send_from_directory(current_app.static_folder, path)
        except FileNotFoundError:
            return jsonify({'error': f'Asset not found: {path}'}), 404

    # For all other routes, serve the Vue SPA
    try:
        return send_from_directory(current_app.static_folder, 'index.html')
    except FileNotFoundError:
        return jsonify({
            'error': 'Frontend not built',
            'message': 'Run "cd frontend && npm run build" to build the Vue application'
        }), 404
