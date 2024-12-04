# Route registration
from app.routes.match_routes import match_bp
from app.routes.player_routes import player_bp
from app.routes.auth_routes import login_bp, register_bp

def register_routes(app):
    app.register_blueprint(match_bp, url_prefix="/api/matches")
    app.register_blueprint(player_bp, url_prefix="/api/players")
    app.register_blueprint(login_bp, url_prefix="/api/login")
    app.register_blueprint(register_bp, url_prefix="/api/register")
