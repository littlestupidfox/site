from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from datetime import datetime, date, time, timedelta
from app import db
from app.models import Employee, Booking, Article, StudioAnnouncement
from app.forms import BookingForm
from sqlalchemy import and_

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    employees = Employee.query.all()
    articles = Article.query.order_by(Article.created_at.desc()).limit(3).all()
    announcement = StudioAnnouncement.query.first()
    return render_template('index.html',
                         employees=employees,
                         articles=articles,
                         announcement=announcement)

@main_bp.route('/booking', methods=['GET', 'POST'])

def booking():
    form = BookingForm()
    announcement = StudioAnnouncement.query.first()
    
    # Фильтруем только будущие даты
    available_dates = [
        (date.date.strftime('%Y-%m-%d'), date.date.strftime('%d.%m.%Y'))
        for date in announcement.dates
        if date.date >= datetime.now()
    ]
    
    form.shooting_date.choices = available_dates
    
    if form.validate_on_submit():
        shooting_datetime = datetime.combine(
            form.shooting_date.data,
            datetime.strptime(form.shooting_time.data, '%H:%M').time()
        )
        
        existing_booking = Booking.query.filter(
            and_(
                Booking.shooting_date >= shooting_datetime,
                Booking.shooting_date < datetime.combine(
                    form.shooting_date.data,
                    (datetime.strptime(form.shooting_time.data, '%H:%M') + timedelta(hours=2)).time()
            )
        ).first())
        
        if existing_booking:
            flash('Это время уже занято')
            return redirect(url_for('main.booking'))
        
        booking = Booking(
            client_name=form.client_name.data,
            people_count=form.people_count.data,
            phone=form.phone.data,
            shooting_date=shooting_datetime
        )
        
        db.session.add(booking)
        db.session.commit()
        flash('Заявка принята!')
        return redirect(url_for('main.index'))
    
    today = date.today()
    bookings = Booking.query.filter(Booking.shooting_date >= datetime.combine(today, time(0, 0))).all()
    booked_slots = {booking.shooting_date.strftime('%Y-%m-%d %H:%M') for booking in bookings}
    
    
    return render_template('booking.html', form=form)
    
    
    #return render_template('booking.html', form=form, booked_slots=booked_slots)

@main_bp.route('/articles')
def articles():
    articles = Article.query.order_by(Article.created_at.desc()).all()
    return render_template('articles.html', articles=articles)

@main_bp.route('/article/<int:article_id>')
def article(article_id):
    article = Article.query.get_or_404(article_id)
    return render_template('article.html', article=article)