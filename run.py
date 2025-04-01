from app import create_app

app = create_app()

@app.route('/check-db')
def check_db():
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    return {
        'tables': inspector.get_table_names(),
        'admin_users': [u.username for u in AdminUser.query.all()]
    }

if __name__ == '__main__':
    app.run(debug=True)