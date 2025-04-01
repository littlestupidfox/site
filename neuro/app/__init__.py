from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from config import Config
from sqlalchemy import inspect  # Добавляем новый импорт

db = SQLAlchemy()
login_manager = LoginManager()
bootstrap = Bootstrap()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Инициализация расширений
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    bootstrap.init_app(app)

    # Регистрация blueprints
    from app.routes import main_bp
    from app.auth import auth_bp
    from app.admin import admin_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Создание таблиц и данных
    with app.app_context():
        # Удалите эти строки после первого успешного запуска
        db.drop_all()
        db.create_all()
        
        from app.models import AdminUser, Employee, StudioAnnouncement
        from app.admin_credentials import ADMIN_CREDENTIALS
        
        # Проверка существования таблицы (новый способ)
        inspector = inspect(db.engine)
        table_names = inspector.get_table_names()
        
        if 'admin_user' in table_names:
            # Создаем администраторов
            for username, password in ADMIN_CREDENTIALS.items():
                if not AdminUser.query.filter_by(username=username).first():
                    user = AdminUser(username=username)
                    user.set_password(password)
                    db.session.add(user)
            
            # Создаем стандартный анонс
            if not StudioAnnouncement.query.first():
                db.session.add(StudioAnnouncement(
                    title="NEON ФОТОСЕССИИ",
                    description="Забронируйте уникальную фотосессию",
                    button_text="ЗАБРОНИРОВАТЬ"
                ))
            
            # Создаем сотрудников
            if not Employee.query.first():
                db.session.add_all([
                    Employee(
                        full_name="Анна Светлова",
                        position="Фотограф",
                        photo="employee1.jpg",
                        bio="Опыт 7 лет"
                    ),
                    Employee(
                        full_name="Иван Петров",
                        position="Визажист",
                        photo="employee2.jpg",
                        bio="Специалист по макияжу"
                    )
                ])
            
            db.session.commit()
        else:
            print("Ошибка: Таблица admin_user не была создана!")

    return app