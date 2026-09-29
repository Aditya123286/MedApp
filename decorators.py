from functools import wraps
from flask import session, redirect, url_for, g
from models.user import User

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        
        if not user_id:
            return redirect(url_for('auth.login'))
        
        user = User.query.get(user_id)
        if not user:
            session.clear()
            return redirect(url_for('auth.login'))
        
        g.user = user
        return f(*args, **kwargs)
    
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        
        if not user_id:
            return redirect(url_for('auth.login'))
        
        user = User.query.get(user_id)
        if not user:
            session.clear()
            return redirect(url_for('auth.login'))
        
        if user.role not in ['admin', 'super_admin']:
            return redirect(url_for('dashboard.dashboard_web'))
        
        g.user = user
        return f(*args, **kwargs)
    
    return decorated_function
