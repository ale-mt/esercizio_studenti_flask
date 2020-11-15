from flask import flash, redirect, url_for, Blueprint
from flask_security import login_required, logout_user

logout_bp = Blueprint('logout', __name__)


@logout_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out!', 'warning')
    return redirect(url_for('login.login'))

