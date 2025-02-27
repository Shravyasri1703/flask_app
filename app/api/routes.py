from flask import jsonify, request
from ariadne import graphql_sync
from ariadne.explorer import ExplorerGraphiQL

from app.api.schema import create_schema

# Create GraphQL schema
schema = create_schema()

# Create Explorer instance
explorer_html = ExplorerGraphiQL(
    title="GraphQL API Explorer"
).html(None)


def init_app(app):
    """Initialize API routes"""
    
    # GraphQL endpoint
    @app.route("/graphql", methods=["GET"])
    def graphql_explorer():
        # Serve GraphiQL explorer on GET request
        return explorer_html
    
    @app.route("/graphql", methods=["POST"])
    def graphql_server():
        # Process GraphQL queries on POST request
        data = request.get_json()
        success, result = graphql_sync(
            schema,
            data,
            context_value={"request": request},
            debug=app.debug
        )
        status_code = 200 if success else 400
        return jsonify(result), status_code
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({'status': 'ok'})