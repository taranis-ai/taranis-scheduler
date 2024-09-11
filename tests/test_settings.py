def test_flask_secret_key(app):
    with app.app_context():
        secret_key = app.config.get("SECRET_KEY", None)
        assert secret_key == "test_key"
