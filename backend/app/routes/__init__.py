# Route registration
from app.routes.match_routes import match_bp
from app.routes.player_routes import player_bp

def register_routes(app):
    app.register_blueprint(match_bp, url_prefix="/api")
    app.register_blueprint(player_bp, url_prefix="/api")