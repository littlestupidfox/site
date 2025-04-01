from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Booking, Article, Employee, StudioAnnouncement
from app.forms import ArticleForm, EmployeeForm, AnnouncementForm
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/')
@login_required
def admin_dashboard():
    return render_template('admin/admin_base.html')



@admin_bp.route('/orders')
@login_required
def manage_orders():
    status_filter = request.args.get('status', 'all')
    
    if status_filter == 'all':
        bookings = Booking.query.order_by(Booking.shooting_date.desc()).all()
    else:
        bookings = Booking.query.filter_by(status=status_filter).order_by(Booking.shooting_date.desc()).all()
    
    return render_template('admin/admin_orders.html', bookings=bookings, status_filter=status_filter)

@admin_bp.route('/order/edit/<int:order_id>', methods=['GET', 'POST'])
@login_required
def edit_order(order_id):
    booking = Booking.query.get_or_404(order_id)
    if request.method == 'POST':
        booking.status = request.form.get('status')
        db.session.commit()
        flash('Статус заказа обновлен', 'success')
        return redirect(url_for('admin.manage_orders'))
    return render_template('admin/edit_order.html', booking=booking)

@admin_bp.route('/order/delete/<int:order_id>', methods=['POST'])
@login_required
def delete_order(order_id):
    booking = Booking.query.get_or_404(order_id)
    db.session.delete(booking)
    db.session.commit()
    flash('Заказ удален', 'success')
    return redirect(url_for('admin.manage_orders'))

@admin_bp.route('/posts')
@login_required
def manage_posts():
    articles = Article.query.order_by(Article.created_at.desc()).all()
    return render_template('admin/admin_posts.html', articles=articles)

@admin_bp.route('/post/add', methods=['GET', 'POST'])
@login_required
def create_post():
    form = ArticleForm()
    if form.validate_on_submit():
        article = Article(
            title=form.title.data,
            content=form.content.data,
            image=form.image.data
        )
        db.session.add(article)
        db.session.commit()
        flash('Статья успешно создана', 'success')
        return redirect(url_for('admin.manage_posts'))
    return render_template('admin/add_post.html', form=form)

@admin_bp.route('/post/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    article = Article.query.get_or_404(post_id)
    form = ArticleForm(obj=article)
    if form.validate_on_submit():
        form.populate_obj(article)
        db.session.commit()
        flash('Статья обновлена', 'success')
        return redirect(url_for('admin.manage_posts'))
    return render_template('admin/edit_post.html', form=form, article=article)

@admin_bp.route('/post/delete/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    article = Article.query.get_or_404(post_id)
    db.session.delete(article)
    db.session.commit()
    flash('Статья удалена', 'success')
    return redirect(url_for('admin.manage_posts'))

@admin_bp.route('/employees')
@login_required
def manage_employees():
    employees = Employee.query.all()
    return render_template('admin/admin_employees.html', employees=employees)

@admin_bp.route('/employee/add', methods=['GET', 'POST'])
@login_required
def add_employee():
    form = EmployeeForm()
    if form.validate_on_submit():
        employee = Employee(
            full_name=form.full_name.data,
            position=form.position.data,
            photo=form.photo.data,
            bio=form.bio.data
        )
        db.session.add(employee)
        db.session.commit()
        flash('Сотрудник успешно добавлен', 'success')
        return redirect(url_for('admin.manage_employees'))
    return render_template('admin/add_employee.html', form=form)

@admin_bp.route('/employee/edit/<int:employee_id>', methods=['GET', 'POST'])
@login_required
def edit_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    form = EmployeeForm(obj=employee)
    if form.validate_on_submit():
        form.populate_obj(employee)
        db.session.commit()
        flash('Данные сотрудника обновлены', 'success')
        return redirect(url_for('admin.manage_employees'))
    return render_template('admin/edit_employee.html', form=form, employee=employee)

@admin_bp.route('/employee/delete/<int:employee_id>', methods=['POST'])
@login_required
def delete_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    db.session.delete(employee)
    db.session.commit()
    flash('Сотрудник удален', 'success')
    return redirect(url_for('admin.manage_employees'))

@admin_bp.route('/announcement', methods=['GET', 'POST'])
@login_required
def manage_announcement():
    announcement = StudioAnnouncement.query.first()
    form = AnnouncementForm(obj=announcement) if announcement else AnnouncementForm()
    
    if form.validate_on_submit():
        if announcement:
            form.populate_obj(announcement)
        else:
            announcement = StudioAnnouncement(
                title=form.title.data,
                description=form.description.data,
                button_text=form.button_text.data
            )
            db.session.add(announcement)
        db.session.commit()
        flash('Анонс обновлен', 'success')
        return redirect(url_for('admin.manage_announcement'))
    
    return render_template('admin/manage_announcement.html', form=form)