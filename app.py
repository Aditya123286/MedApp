# app.py - COMPLETE FIXED VERSION WITH SESSION SUPPORT, SMTP EMAIL, ROLE-BASED PERMISSIONS AND API ENDPOINTS

from flask import Flask, app, render_template, g, session, request, jsonify, url_for
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, decode_token
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flasgger import Swagger
from datetime import datetime, timedelta
import os
import sys

# Ensure parent project directory is importable when running from either project root or `food/`
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
FOOD_ROOT = CURRENT_DIR
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
if FOOD_ROOT not in sys.path:
    sys.path.insert(0, FOOD_ROOT)

from dotenv import load_dotenv
from sqlalchemy import text
from middleware.domain import get_current_tenant, tenant_required

# 📧 NEW EMAIL IMPORTS
from flask_mail import Mail, Message
from celery import Celery
from itsdangerous import URLSafeTimedSerializer
import logging
from email_validator import validate_email, EmailNotValidError

# Database
from database import db, init_oracle_connection

# Models
from models.user import User
from models.medicine import Medicine
from models.suppliers import Supplier
from models.order import Order
from models.subscription import SubscriptionPlan, UserSubscription
from models.tenant import Tenant
from models.role import Role
from models.permission import Permission
from models.mail_message import MailMessage
from models.doctor import Doctor
from models.appointment import Appointment
from models.frontend import (
    FrontendBanner,
    FrontendFaq,
    FrontendSolution,
    FrontendFeature,
    FrontendFooter,
    FrontendSetting,
)

# Utils
from utils.helpers import create_response

load_dotenv()

# Blueprints
from routes.auth import auth_bp
from routes.medicines import medicine_bp
from routes.order import order_bp
from routes.dashboard import dashboard_bp
from routes.suppliers import suppliers_bp
from routes.about import about_bp
from routes.settings import settings_bp
from routes.report import report_bp
from routes.user import user_bp
from routes.search_result import search_result_bp 
from routes.main import main_bp
from routes.subscription import subscription_bp
from routes.feedback import feedback_bp
from routes.admin import admin_bp
from routes.super_admin import super_admin_bp
from routes.payment import payment_bp
from routes.frontend import frontend_bp
from routes.prescription import prescription_bp
from routes.support import support_bp
from routes.api_docs import api_docs_bp
from routes.appointment import appointments_bp

# Configuration
from configuration import config

# 📧 Initialize extensions
mail = Mail()
celery = Celery(__name__)

def create_app(config_name='default'):
    """Application factory function."""
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config[config_name])
    
    # ✅ CRITICAL FIX: Secret key for sessions
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # ✅ SESSION CONFIGURATION - COMPLETE FIX
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = True
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_COOKIE_NAME'] = 'medapp_session'
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SECURE'] = False  # True in production with HTTPS
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_PATH'] = '/'  # Important for cookie to work on all routes
    app.config['SESSION_REFRESH_EACH_REQUEST'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
    
    # 📧 Email Configuration
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
    app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', 'False').lower() == 'true'
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
    app.config['MAIL_MAX_EMAILS'] = int(os.getenv('MAIL_MAX_EMAILS', 10))
    
    # 📧 Celery Configuration
    app.config['CELERY_BROKER_URL'] = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    app.config['CELERY_RESULT_BACKEND'] = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    # 📧 Password Reset Settings
    app.config['PASSWORD_RESET_EXPIRY'] = 3600  # 1 hour in seconds
    app.config['COMPANY_NAME'] = os.getenv('COMPANY_NAME', 'MedApp Pharmacy')
    app.config['SUPPORT_EMAIL'] = os.getenv('SUPPORT_EMAIL', 'support@medapp.com')
    app.config['ADMIN_EMAIL'] = os.getenv('ADMIN_EMAIL', 'admin@medapp.com')

    # Initialize extensions
    CORS(app, origins=app.config.get('CORS_ORIGINS', '*'), supports_credentials=True)
    init_oracle_connection(app)
    JWTManager(app)
    
    # 📧 Initialize mail
    mail.init_app(app)
    
    # 📧 Configure Celery
    celery.conf.update(
        broker_url=app.config['CELERY_BROKER_URL'],
        result_backend=app.config['CELERY_RESULT_BACKEND'],
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='UTC',
        enable_utc=True,
        task_track_started=True,
        task_time_limit=30 * 60,  # 30 minutes
        task_soft_time_limit=60,   # 60 seconds
        worker_max_tasks_per_child=200
    )
    
    # Limiter - Completely disabled
    from flask_limiter import Limiter
    limiter = Limiter(key_func=get_remote_address, app=app, default_limits=[])
    limiter.enabled = False

    # Swagger  
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/swagger/"
    }
    Swagger(app, config=swagger_config)

    # API Prefix
    api_prefix = app.config.get('API_PREFIX', '/api/v1')

    # ✅ FIXED before_request with tenant safety and role loading
    @app.before_request
    def before_request():
        # Set tenant - YE LINE IMPORTANT HAI
        g.tenant = get_current_tenant()
        
        # EXTRA SAFETY - Ensure tenant is never None
        if g.tenant is None:
            print("[WARN] g.tenant is None, creating dummy tenant")
            class DummyTenant:
                def __init__(self):
                    self.id = 1
                    self.name = 'Default Tenant'
                    self.subdomain = 'default'
                    self.custom_domain = None
                    self.is_active = True
                    self.company_name = 'MedApp'
                    self.theme_color = '#2e5bff'
                
                def __getattr__(self, name):
                    # Safety: agar koi attribute nahi milta to default value return karo
                    if name == 'id':
                        return 1
                    elif name == 'name':
                        return 'Default'
                    elif name == 'subdomain':
                        return 'default'
                    else:
                        return None
            
            g.tenant = DummyTenant()
            print(f"[OK] Created dummy tenant with ID: {g.tenant.id}")
        
        # ✅ DEBUG SESSION - Add this for debugging
        if request.path != '/favicon.ico':
            print(f"\n[REQ] Request path: {request.path}")
            print(f"[REQ] Session ID: {session.sid if hasattr(session, 'sid') else 'No SID'}")
            print(f"[REQ] Session data: {dict(session)}")
        
        # Load user from session if available with role and permissions
        user_id = session.get('user_id')
        if user_id:
            try:
                print(f"[DEBUG] Loading user with ID: {user_id}")
                # ✅ FIXED: db.session.query() use karo, db.query() nahi
                user = db.session.query(User).options(
                    db.joinedload(User.role).joinedload(Role.permissions)
                ).get(user_id)
                
                if user and user.is_active:
                    g.user = user
                    g.role = user.role
                    g.permissions = {p.name for p in user.role.permissions} if user.role else set()
                    print(f"[OK] User loaded: {user.email} with role: {user.role_name}")
                else:
                    print(f"[ERROR] Invalid or inactive user")
                    session.clear()
                    g.user = None
                    g.role = None
                    g.permissions = set()
            except Exception as e:
                print(f"[ERROR] Error loading user: {e}")
                import traceback
                traceback.print_exc()
                g.user = None
                g.role = None
                g.permissions = set()
        else:
            if request.path != '/favicon.ico':
                print(f"[INFO] No user_id in session")
            g.user = None
            g.role = None
            g.permissions = set()

    # Register Blueprints - Including new admin and super_admin blueprints
    app.register_blueprint(auth_bp, url_prefix=f'{api_prefix}/auth')
    app.register_blueprint(medicine_bp, url_prefix=f'{api_prefix}/medicines')
    app.register_blueprint(order_bp, url_prefix=f'{api_prefix}/order')
    app.register_blueprint(dashboard_bp, url_prefix=f'{api_prefix}/dashboard')
    app.register_blueprint(suppliers_bp, url_prefix=f'{api_prefix}')
    app.register_blueprint(report_bp, url_prefix=f'{api_prefix}')
    app.register_blueprint(about_bp, url_prefix=f'{api_prefix}')
    app.register_blueprint(settings_bp, url_prefix=f'{api_prefix}/settings')
    app.register_blueprint(user_bp, url_prefix=f'{api_prefix}/user')
    app.register_blueprint(search_result_bp, url_prefix=f'{api_prefix}')
    app.register_blueprint(main_bp)
    app.register_blueprint(subscription_bp, url_prefix=f'{api_prefix}/subscription')
    app.register_blueprint(feedback_bp, url_prefix=f'{api_prefix}/feedback')
    app.register_blueprint(admin_bp, url_prefix=f'{api_prefix}/admin')
    app.register_blueprint(super_admin_bp, url_prefix=f'{api_prefix}/super-admin')
    app.register_blueprint(payment_bp, url_prefix=f'{api_prefix}/payment')
    app.register_blueprint(frontend_bp)
    app.register_blueprint(prescription_bp, url_prefix=f'{api_prefix}/prescription')
    app.register_blueprint(support_bp)
    app.register_blueprint(api_docs_bp)
    app.register_blueprint(appointments_bp, url_prefix=f'{api_prefix}/appointments')
    
    # ==================== 📧 EMAIL ROUTES ====================
    
    @app.route('/api/v1/email/send', methods=['POST'])
    def send_email():
        """Send a single email"""
        try:
            data = request.get_json()
            
            recipient = data.get('recipient')
            subject = data.get('subject')
            body = data.get('body')
            html_body = data.get('html_body')
            email_type = data.get('type', 'text')  # 'text' or 'html'
            
            if not all([recipient, subject, body]):
                return jsonify({'success': False, 'error': 'Missing required fields'}), 400
            
            # Validate email
            try:
                validate_email(recipient)
            except EmailNotValidError:
                return jsonify({'success': False, 'error': 'Invalid email address'}), 400
            
            msg = Message(
                subject=subject,
                recipients=[recipient],
                sender=app.config['MAIL_DEFAULT_SENDER']
            )
            
            if email_type == 'html' or html_body:
                msg.html = html_body or body
            else:
                msg.body = body
            
            mail.send(msg)
            
            return jsonify({
                'success': True, 
                'message': 'Email sent successfully',
                'recipient': recipient
            })
            
        except Exception as e:
            app.logger.error(f"Email send error: {str(e)}")
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @app.route('/api/v1/email/welcome/<email>', methods=['POST'])
    def send_welcome_email(email):
        """Send welcome email to new user"""
        try:
            # Get user from database
            user = User.query.filter_by(email=email).first()
            if not user:
                return jsonify({'success': False, 'error': 'User not found'}), 404
            
            # Render HTML template
            html_content = render_template(
                'email/welcome.html',
                user=user,
                company_name=app.config['COMPANY_NAME'],
                login_url=url_for('login_page', _external=True)
            )
            
            msg = Message(
                subject=f"Welcome to {app.config['COMPANY_NAME']}!",
                recipients=[email],
                html=html_content
            )
            
            mail.send(msg)
            
            return jsonify({
                'success': True,
                'message': 'Welcome email sent successfully'
            })
            
        except Exception as e:
            app.logger.error(f"Welcome email error: {str(e)}")
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @app.route('/api/v1/email/reset-password', methods=['POST'])
    def send_reset_password_email():
        """Send password reset email with secure token"""
        try:
            data = request.get_json()
            email = data.get('email')
            
            if not email:
                return jsonify({'success': False, 'error': 'Email required'}), 400
            
            user = User.query.filter_by(email=email).first()
            if not user:
                # Don't reveal if user exists or not (security)
                return jsonify({
                    'success': True, 
                    'message': 'If email exists, reset link will be sent'
                })
            
            # Generate secure token
            serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
            token = serializer.dumps(email, salt='password-reset-salt')
            
            reset_url = url_for('reset_password_page', token=token, _external=True)
            
            # Send email
            html_content = render_template(
                'email/reset_password.html',
                user=user,
                reset_url=reset_url,
                expiry_minutes=app.config['PASSWORD_RESET_EXPIRY'] // 60,
                company_name=app.config['COMPANY_NAME']
            )
            
            msg = Message(
                subject="Password Reset Request",
                recipients=[email],
                html=html_content
            )
            
            mail.send(msg)
            
            return jsonify({
                'success': True,
                'message': 'Password reset email sent'
            })
            
        except Exception as e:
            app.logger.error(f"Reset password email error: {str(e)}")
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @app.route('/reset-password/<token>')
    def reset_password_page(token):
        """Page to reset password with token"""
        try:
            serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
            email = serializer.loads(
                token,
                salt='password-reset-salt',
                max_age=app.config['PASSWORD_RESET_EXPIRY']
            )
            return render_template('reset_password.html', email=email, token=token)
        except:
            return render_template('reset_password_invalid.html'), 400
    
    @app.route('/api/v1/email/order-confirmation/<int:order_id>', methods=['POST'])
    def send_order_confirmation(order_id):
        """Send order confirmation email"""
        try:
            from models.order import Order
            from models.user import User
            
            order = Order.query.get(order_id)
            if not order:
                return jsonify({'success': False, 'error': 'Order not found'}), 404
            
            user = User.query.get(order.user_id)
            if not user:
                return jsonify({'success': False, 'error': 'User not found'}), 404
            
            html_content = render_template(
                'email/order_confirmation.html',
                order=order,
                user=user,
                company_name=app.config['COMPANY_NAME'],
                support_email=app.config['SUPPORT_EMAIL']
            )
            
            msg = Message(
                subject=f"Order Confirmation #{order.order_number}",
                recipients=[user.email],
                html=html_content
            )
            
            mail.send(msg)
            
            return jsonify({
                'success': True,
                'message': 'Order confirmation email sent'
            })
            
        except Exception as e:
            app.logger.error(f"Order confirmation email error: {str(e)}")
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @app.route('/api/v1/email/invoice/<int:order_id>', methods=['POST'])
    def send_invoice(order_id):
        """Send invoice email"""
        try:
            from models.order import Order
            from models.user import User
            
            order = Order.query.get(order_id)
            if not order:
                return jsonify({'success': False, 'error': 'Order not found'}), 404
            
            user = User.query.get(order.user_id)
            if not user:
                return jsonify({'success': False, 'error': 'User not found'}), 404
            
            html_content = render_template(
                'email/invoice.html',
                order=order,
                user=user,
                company_name=app.config['COMPANY_NAME'],
                company_address=os.getenv('COMPANY_ADDRESS', ''),
                date=datetime.now().strftime('%d %B, %Y')
            )
            
            msg = Message(
                subject=f"Invoice #{order.order_number}",
                recipients=[user.email],
                html=html_content
            )
            
            mail.send(msg)
            
            return jsonify({
                'success': True,
                'message': 'Invoice email sent'
            })
            
        except Exception as e:
            app.logger.error(f"Invoice email error: {str(e)}")
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @app.route('/api/v1/email/bulk', methods=['POST'])
    def send_bulk_email():
        """Send bulk emails (admin only)"""
        try:
            data = request.get_json()
            
            # Check if user is admin (from session)
            if not hasattr(g, 'user') or not g.user or not g.user.is_admin:
                return jsonify({'success': False, 'error': 'Unauthorized - Admin access required'}), 403
            
            recipients = data.get('recipients', [])
            subject = data.get('subject')
            body = data.get('body')
            html_body = data.get('html_body')
            
            if not recipients or not subject or not body:
                return jsonify({'success': False, 'error': 'Missing fields'}), 400
            
            if len(recipients) > 100:
                return jsonify({'success': False, 'error': 'Max 100 recipients allowed'}), 400
            
            # Send in batches
            batch_size = app.config['MAIL_MAX_EMAILS']
            successful = []
            failed = []
            
            with mail.connect() as conn:
                for i in range(0, len(recipients), batch_size):
                    batch = recipients[i:i+batch_size]
                    for recipient in batch:
                        try:
                            msg = Message(
                                subject=subject,
                                recipients=[recipient]
                            )
                            if html_body:
                                msg.html = html_body
                            else:
                                msg.body = body
                            conn.send(msg)
                            successful.append(recipient)
                        except Exception as e:
                            failed.append({'email': recipient, 'error': str(e)})
            
            return jsonify({
                'success': True,
                'message': f'Sent to {len(successful)} recipients',
                'successful': successful,
                'failed': failed
            })
            
        except Exception as e:
            app.logger.error(f"Bulk email error: {str(e)}")
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @app.route('/api/v1/email/test', methods=['GET'])
    def test_email():
        """Test email configuration"""
        try:
            msg = Message(
                subject="Test Email from MedApp",
                recipients=[app.config['ADMIN_EMAIL']],
                body=f"This is a test email sent at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            mail.send(msg)
            return jsonify({'success': True, 'message': 'Test email sent'})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    # ==================== API DOCS PAGE ====================
    
    @app.route('/')
    def home():
        """Home - Landing Page"""
        try:
            settings = FrontendSetting.query.first()
            footer = FrontendFooter.query.first()

            banners = (
                FrontendBanner.query.filter_by(status='active')
                .order_by(FrontendBanner.display_order.asc(), FrontendBanner.created_at.desc())
                .all()
            )
            features = (
                FrontendFeature.query.filter_by(is_enabled=True)
                .order_by(FrontendFeature.display_order.asc(), FrontendFeature.created_at.desc())
                .all()
            )
            solutions = (
                FrontendSolution.query.filter_by(is_active=True)
                .order_by(FrontendSolution.display_order.asc(), FrontendSolution.created_at.desc())
                .all()
            )
            faqs = (
                FrontendFaq.query.filter_by(is_active=True)
                .order_by(FrontendFaq.display_order.asc(), FrontendFaq.created_at.desc())
                .all()
            )
        except Exception as e:
            app.logger.error(f"Frontend manager data load failed: {str(e)}")
            settings = None
            footer = None
            banners = []
            features = []
            solutions = []
            faqs = []

        site_settings = settings.to_dict() if settings else {}
        footer_data = footer.to_dict() if footer else {}
        banner_data = [b.to_dict() for b in banners]
        feature_data = [f.to_dict() for f in features]
        solution_data = [s.to_dict() for s in solutions]
        faq_data = [f.to_dict() for f in faqs]

        hero_banner = banner_data[0] if banner_data else None

        return render_template(
            'index.html',
            site_settings=site_settings,
            footer_data=footer_data,
            hero_banner=hero_banner,
            banners=banner_data,
            frontend_features=feature_data,
            frontend_solutions=solution_data,
            frontend_faqs=faq_data,
        )
    
    @app.route('/api-docs')
    def api_docs():
        """API Documentation page"""
        return render_template('api_docs.html')
    
    # ==================== API ENDPOINTS LIST ROUTE ====================
    
    @app.route('/api/v1/endpoints')
    def get_endpoints():
        """Return all registered API endpoints"""
        endpoints = []
        for rule in app.url_map.iter_rules():
            if '/api/' in rule.rule and rule.rule != '/api/v1/endpoints':
                # Determine category from URL
                parts = rule.rule.split('/')
                category = 'other'
                if len(parts) > 3:
                    if parts[3] in ['auth', 'user', 'medicines', 'order', 'report', 'suppliers', 'feedback', 'subscription', 'payment', 'admin', 'super-admin']:
                        category = parts[3]
                    elif 'prescription' in rule.rule:
                        category = 'prescription'
                    elif 'email' in rule.rule:
                        category = 'email'
                
                # Get HTTP methods
                methods = list(rule.methods - {'HEAD', 'OPTIONS'})
                method = methods[0] if methods else 'GET'
                
                # Generate description
                description = f"API endpoint for {rule.rule}"
                
                endpoints.append({
                    'category': category,
                    'method': method,
                    'name': rule.rule,
                    'url': f"http://localhost:5000{rule.rule}",
                    'description': description
                })
        
        # Sort by category
        endpoints.sort(key=lambda x: (x['category'], x['name']))
        
        return jsonify({'success': True, 'endpoints': endpoints})
    
    # ==================== TENANT MANAGEMENT ROUTE ====================
    
    @app.route('/create-default-tenant')
    def create_default_tenant():
        """Create default tenant in database - FIXED for SQLite fallback"""
        try:
            # Check if tenant exists using model
            try:
                tenant = db.session.query(Tenant).filter_by(subdomain='default').first()
                if tenant:
                    return f"[OK] Default tenant already exists (ID: {tenant.id}, Name: {tenant.name})"
                
                # Create new tenant using model
                new_tenant = Tenant(
                    name='Default Tenant',
                    subdomain='default',
                    is_active=True
                )
                db.session.add(new_tenant)
                db.session.commit()
                
                return f"[OK] Default tenant created with ID: {new_tenant.id}"
                
            except Exception as model_error:
                print(f"[WARN] Model approach failed: {model_error}, trying raw SQL...")
                
                # Check if tenant exists using raw SQL (works in both Oracle and SQLite)
                result = db.session.execute(
                    text("SELECT COUNT(*) FROM tenants WHERE subdomain = 'default'")
                ).scalar()
                
                if result and result > 0:
                    return "[OK] Default tenant already exists"
                
                # Get next ID (works in both databases)
                try:
                    # Try Oracle sequence first
                    next_id = db.session.execute(text("SELECT tenants_seq.NEXTVAL FROM dual")).scalar()
                except:
                    # Fallback for SQLite - get max ID + 1
                    max_id = db.session.execute(text("SELECT MAX(id) FROM tenants")).scalar()
                    next_id = (max_id or 0) + 1
                
                # Use datetime.now() instead of SYSTIMESTAMP
                from datetime import datetime
                current_time = datetime.now()
                
                # Insert using raw SQL with database-agnostic timestamp
                db.session.execute(
                    text("""
                        INSERT INTO tenants (id, name, subdomain, is_active, created_at) 
                        VALUES (:id, :name, :subdomain, :is_active, :created_at)
                    """),
                    {
                        "id": next_id,
                        "name": "Default Tenant",
                        "subdomain": "default",
                        "is_active": 1,
                        "created_at": current_time
                    }
                )
                
                db.session.commit()
                
                return "[OK] Default tenant created successfully using raw SQL"
                
        except Exception as e:
            import traceback
            traceback.print_exc()
            return f"[ERROR] Error: {str(e)}"
    
    # ==================== ROLE MANAGEMENT ROUTES ====================
    
    @app.route('/seed-roles')
    def seed_roles():
        """Create default roles and permissions"""
        try:
            # Get current app context
            from flask import current_app
            
            # Use app context for database operations
            with current_app.app_context():
                from models.role import Role
                from models.permission import Permission
                from database import db
                from sqlalchemy import text
                
                # Check current roles
                roles = Role.query.all()
                print(f"Current roles: {[r.name for r in roles]}")
                
                # Create roles if missing
                Role.create_default_roles()
                
                # Create permissions
                Permission.create_default_permissions()
                
                # Assign permissions
                Permission.assign_permissions_to_roles()
                
                # Final check
                final_roles = Role.query.all()
                
                return jsonify({
                    'success': True,
                    'message': 'Roles seeded successfully',
                    'roles': [r.name for r in final_roles]
                })
                
        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @app.route('/seed-users')
    def seed_users():
        """Create users with proper roles"""
        try:
            from models.role import Role
            Role.create_default_roles()
            
            # Get roles
            super_admin_role = Role.query.filter_by(name='super_admin').first()
            admin_role = Role.query.filter_by(name='admin').first()
            user_role = Role.query.filter_by(name='user').first()
            supplier_role = Role.query.filter_by(name='supplier').first()
            doctor_role = Role.query.filter_by(name='doctor').first()
            
            users_created = []
            users_updated = []
            
            # Super Admin - Force update role
            super_admin = User.query.filter_by(email='superadmin@medapp.com').first()
            if not super_admin:
                super_admin = User(
                    user_id="SA001",
                    name="Aditya Prasad",
                    email="superadmin@medapp.com",
                    is_active=True,
                    role_id=super_admin_role.id if super_admin_role else None
                )
                super_admin.set_password("admin123")
                db.session.add(super_admin)
                users_created.append("SuperAdmin (super_admin)")
            else:
                # Force update role and reset password
                if super_admin_role:
                    super_admin.role_id = super_admin_role.id
                    super_admin.set_password("admin123")
                    users_updated.append("SuperAdmin updated")
            
            # Admin - Force update role
            admin = User.query.filter_by(email='admin@medapp.com').first()
            if not admin:
                admin = User(
                    user_id="U001",
                    name="Vishal Kumar",
                    email="admin@medapp.com",
                    is_active=True,
                    role_id=admin_role.id if admin_role else None
                )
                admin.set_password("admin123")
                db.session.add(admin)
                users_created.append("Admin (admin)")
            else:
                if admin_role:
                    admin.role_id = admin_role.id
                    admin.set_password("admin123")
                    users_updated.append("Admin updated")
            
            # Regular User
            user = User.query.filter_by(email='user@medapp.com').first()
            if not user:
                user = User(
                    user_id="U002",
                    name="Test User",
                    email="user@medapp.com",
                    is_active=True,
                    role_id=user_role.id if user_role else None
                )
                user.set_password("user123")
                db.session.add(user)
                users_created.append("TestUser (user)")
            
            # Supplier
            supplier = User.query.filter_by(email='supplier@medapp.com').first()
            if not supplier:
                supplier = User(
                    user_id="S001",
                    name="Test Supplier",
                    email="supplier@medapp.com",
                    is_active=True,
                    role_id=supplier_role.id if supplier_role else None
                )
                supplier.set_password("supplier123")
                db.session.add(supplier)
                users_created.append("Supplier (supplier)")
            else:
                if supplier_role:
                    supplier.role_id = supplier_role.id
                    users_updated.append("Supplier updated")

            # Doctor
            doctor_user = User.query.filter_by(email='doctor@medapp.com').first()
            if not doctor_user:
                doctor_user = User(
                    user_id="D001",
                    name="Dr. Priya Sharma",
                    email="doctor@medapp.com",
                    is_active=True,
                    role_id=doctor_role.id if doctor_role else None
                )
                doctor_user.set_password("doctor123")
                db.session.add(doctor_user)
                users_created.append("Doctor (doctor)")
            else:
                if doctor_role:
                    doctor_user.role_id = doctor_role.id
                    doctor_user.set_password("doctor123")
                    users_updated.append("Doctor updated")

            db.session.flush()

            if doctor_user and not Doctor.query.filter_by(user_id=doctor_user.id).first():
                db.session.add(Doctor(
                    user_id=doctor_user.id,
                    name=doctor_user.name,
                    email=doctor_user.email,
                    phone=doctor_user.phone,
                    specialization='General Physician',
                    qualification='MBBS',
                    experience_years=5,
                    consultation_fee=500,
                    is_available=True,
                    available_from='10:00',
                    available_to='18:00'
                ))
            
            if users_created or users_updated:
                db.session.commit()
                msg = []
                if users_created:
                    msg.append(f"Created: {', '.join(users_created)}")
                if users_updated:
                    msg.append(f"Updated: {', '.join(users_updated)}")
                return f"[OK] {' | '.join(msg)}"
            else:
                return "[OK] All users already exist"
        except Exception as e:
            db.session.rollback()
            return f"[ERROR] {str(e)}", 500
    
    @app.route('/check-permissions')
    def check_permissions():
        """Check current user's permissions - supports both session and token"""
        
        # Try session first (web)
        user_id = session.get('user_id')
        user = None
        
        if user_id:
            user = User.query.get(user_id)
        
        # If no session, try JWT token
        if not user:
            token = request.headers.get('Authorization', '').replace('Bearer ', '')
            if token:
                try:
                    decoded = decode_token(token)
                    email = decoded.get('sub')
                    if email:
                        user = User.query.filter_by(email=email).first()
                except Exception as e:
                    print(f"Token error: {e}")
        
        if not user:
            return jsonify({'success': False, 'message': 'Not logged in'}), 401
        
        permissions = []
        if user.role and user.role.permissions:
            permissions = [{'name': p.name, 'module': p.module, 'action': p.action} 
                          for p in user.role.permissions]
        
        return jsonify({
            'success': True,
            'user': {
                'name': user.name,
                'email': user.email,
                'role': user.role_name,
                'is_admin': user.is_admin,
                'is_super_admin': user.is_super_admin,
                'is_supplier': user.is_supplier,
                'is_doctor': getattr(user, 'is_doctor', False)
            },
            'permissions': permissions
        })
    
    # ==================== ORIGINAL ROUTES ====================
    
    @app.route('/health', methods=['GET'])
    def health_check():
        try:
            db.session.execute(text('SELECT 1 FROM dual'))
            db_status = "connected"
        except Exception as e:
            db_status = f"error: {str(e)}"

        return create_response(
            success=True,
            message="MedApp API is running",
            data={
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "database": db_status,
                "version": app.config.get('VERSION', '1.0')
            }
        ), 200

    @app.route('/login')
    def login_page():
        return render_template('login.html')

    # ==================== SEED ROUTE ====================
    @app.route('/seed')
    def seed():
        from models.role import Role
        Role.create_default_roles()
        
        users_created = []
        users_updated = []
        
        # Get roles
        super_admin_role = Role.query.filter_by(name='super_admin').first()
        admin_role = Role.query.filter_by(name='admin').first()
        user_role = Role.query.filter_by(name='user').first()
        supplier_role = Role.query.filter_by(name='supplier').first()
        doctor_role = Role.query.filter_by(name='doctor').first()
        
        # Create or update superadmin
        super_admin = User.query.filter_by(email='superadmin@medapp.com').first()
        if not super_admin:
            super_admin = User(
                user_id="SA001",
                name="Aditya Prasad",
                email="superadmin@medapp.com",
                is_active=True,
                role_id=super_admin_role.id if super_admin_role else None
            )
            super_admin.set_password("admin123")
            db.session.add(super_admin)
            users_created.append("SuperAdmin")
        else:
            if super_admin_role and super_admin.role_id != super_admin_role.id:
                super_admin.role_id = super_admin_role.id
                users_updated.append("SuperAdmin -> super_admin")
        
        # Create or update admin
        admin = User.query.filter_by(email='admin@medapp.com').first()
        if not admin:
            admin = User(
                user_id="U001",
                name="Vishal Kumar",
                email="admin@medapp.com",
                is_active=True,
                role_id=admin_role.id if admin_role else None
            )
            admin.set_password("admin123")
            db.session.add(admin)
            users_created.append("Admin")
        else:
            if admin_role and admin.role_id != admin_role.id:
                admin.role_id = admin_role.id
                users_updated.append("Admin -> admin")
        
        # Create or update user
        user = User.query.filter_by(email='user@medapp.com').first()
        if not user:
            user = User(
                user_id="U002",
                name="Test User",
                email="user@medapp.com",
                is_active=True,
                role_id=user_role.id if user_role else None
            )
            user.set_password("user123")
            db.session.add(user)
            users_created.append("User")
        else:
            if user_role and user.role_id != user_role.id:
                user.role_id = user_role.id
                users_updated.append("User -> user")

        # Create or update supplier
        supplier = User.query.filter_by(email='supplier@medapp.com').first()
        if not supplier:
            supplier = User(
                user_id="S001",
                name="Test Supplier",
                email="supplier@medapp.com",
                is_active=True,
                role_id=supplier_role.id if supplier_role else None
            )
            supplier.set_password("supplier123")
            db.session.add(supplier)
            users_created.append("Supplier")
        else:
            if supplier_role and supplier.role_id != supplier_role.id:
                supplier.role_id = supplier_role.id
                users_updated.append("Supplier -> supplier")

        # Create or update doctor
        doctor_user = User.query.filter_by(email='doctor@medapp.com').first()
        if not doctor_user:
            doctor_user = User(
                user_id="D001",
                name="Dr. Priya Sharma",
                email="doctor@medapp.com",
                is_active=True,
                role_id=doctor_role.id if doctor_role else None
            )
            doctor_user.set_password("doctor123")
            db.session.add(doctor_user)
            users_created.append("Doctor")
        else:
            if doctor_role and doctor_user.role_id != doctor_role.id:
                doctor_user.role_id = doctor_role.id
                users_updated.append("Doctor -> doctor")

        db.session.flush()

        if doctor_user and not Doctor.query.filter_by(user_id=doctor_user.id).first():
            db.session.add(Doctor(
                user_id=doctor_user.id,
                name=doctor_user.name,
                email=doctor_user.email,
                phone=doctor_user.phone,
                specialization='General Physician',
                qualification='MBBS',
                experience_years=5,
                consultation_fee=500,
                is_available=True,
                available_from='10:00',
                available_to='18:00'
            ))
        
        if users_created or users_updated:
            db.session.commit()
            msg = []
            if users_created:
                msg.append(f"Created: {', '.join(users_created)}")
            if users_updated:
                msg.append(f"Updated: {', '.join(users_updated)}")
            return f"[OK] {' | '.join(msg)}"
        else:
            return "[OK] All users already exist with correct roles"

    # Inject global Day/Night toggle script into all HTML pages.
    @app.after_request
    def inject_global_theme_toggle(response):
        try:
            content_type = (response.headers.get('Content-Type') or '').lower()
            if 'text/html' not in content_type:
                return response
            if response.direct_passthrough:
                return response

            html = response.get_data(as_text=True)
            marker = 'data-medapp-theme-toggle=\"1\"'
            if marker in html:
                return response

            script_tag = '<script src=\"/static/js/medapp-theme-toggle.js\" defer data-medapp-theme-toggle=\"1\"></script>'
            if '</body>' in html:
                html = html.replace('</body>', f'{script_tag}\n</body>', 1)
            else:
                html = f'{html}\n{script_tag}'

            response.set_data(html)
            response.headers['Content-Length'] = str(len(html.encode('utf-8')))
        except Exception as e:
            app.logger.warning(f'Global theme injection skipped: {e}')
        return response

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return create_response(success=False, message="Route not found", data=None), 404

    @app.errorhandler(500)
    def internal_error(error):
        return create_response(success=False, message="Internal server error", data=None), 500

    # Teardown session
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    return app

# ✅ Create app instance
app = create_app()

# 📧 Celery task for async email
@celery.task(name='send_async_email')
def send_async_email(recipient, subject, body, html_body=None):
    """Send email asynchronously with Celery"""
    with app.app_context():
        try:
            msg = Message(
                subject=subject,
                recipients=[recipient]
            )
            if html_body:
                msg.html = html_body
            else:
                msg.body = body
            mail.send(msg)
            return {'success': True, 'recipient': recipient}
        except Exception as e:
            app.logger.error(f"Async email error: {str(e)}")
            return {'success': False, 'error': str(e)}

# 📧 Celery task for scheduled email
@celery.task(name='send_scheduled_email')
def send_scheduled_email(recipient, subject, body, delay_seconds):
    """Send email after delay"""
    import time
    time.sleep(delay_seconds)
    return send_async_email(recipient, subject, body)

if __name__ == "__main__":
    # Use the same app instance
    with app.app_context():
        try:
            db.create_all()
            print("[OK] Database tables created/verified")
            
            # Test email configuration
            if app.config['MAIL_USERNAME'] and app.config['MAIL_PASSWORD']:
                print("[OK] Email configuration loaded")
            else:
                print("[WARN] Email credentials missing - check .env file")
                
        except Exception as e:
            print(f"[ERROR] Database error: {e}")

    print("\n" + "="*80)
    print("[INFO] REGISTERED ROUTES")
    print("="*80)
    for rule in app.url_map.iter_rules():
        methods = ','.join(sorted(rule.methods - {'HEAD', 'OPTIONS'}))
        print(f"{rule.endpoint:45s} [{methods:15s}] {rule.rule}")
    print("="*80 + "\n")
    print("[INFO] EMAIL ROUTES ADDED:")
    print("   POST   /api/v1/email/send                    - Send single email")
    print("   POST   /api/v1/email/welcome/<email>        - Send welcome email")
    print("   POST   /api/v1/email/reset-password         - Send password reset")
    print("   POST   /api/v1/email/order-confirmation/<id> - Order confirmation")
    print("   POST   /api/v1/email/invoice/<id>           - Send invoice")
    print("   POST   /api/v1/email/bulk                    - Bulk email (admin)")
    print("   GET    /api/v1/email/test                    - Test configuration")
    print("\n[INFO] ROLE ROUTES ADDED:")
    print("   GET    /seed-roles                           - Seed roles & permissions")
    print("   GET    /check-permissions                    - Check user permissions")
    print("\n[INFO] API ENDPOINTS ROUTE ADDED:")
    print("   GET    /api/v1/endpoints                     - List all API endpoints")
    print("="*80)

    app.run(debug=True, host="0.0.0.0", port=5000)  
