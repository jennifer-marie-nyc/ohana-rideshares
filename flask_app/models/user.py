from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app import bcrypt
from datetime import datetime, timedelta

class User:
    db = 'rideshares_schema'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']


    @staticmethod
    def create(form_data):
        query = """
            INSERT INTO users
            (first_name, last_name, email, password)
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """

        secure_user_data = {
            'first_name': form_data['first_name'],
            'last_name': form_data['last_name'],
            'email': form_data['email'],
            'password': bcrypt.generate_password_hash(form_data['password'])
        }

        user_id = connectToMySQL('rideshares_schema').query_db(query, secure_user_data)

        return user_id
    
    @classmethod
    def get_one_by_email(cls, email):
        query = """
                SELECT * FROM users
                WHERE email = %(email)s;
            """
        results = connectToMySQL(cls.db).query_db(query, email)
        
        this_user = cls(results[0])
    
        return this_user

    @classmethod
    def validate_user(cls, form_data):
        is_valid = True
        print("Validating form data...")

        # Validate first name
        if len(form_data['first_name'].strip()) == 0:
            flash('First name is required', 'registration')
            is_valid = False
        elif len(form_data['first_name'].strip()) < 2:
            flash('First name must be at least 2 characters.', 'registration')
            is_valid = False

        # Validate last name
        if len(form_data['last_name'].strip()) == 0:
            flash('Last name is required', 'registration')
            is_valid = False
        elif len(form_data['last_name'].strip()) < 2:
            flash('Last name must be at least 2 characters', 'registration')
            is_valid = False

        # Validate that email was entered
        if len(form_data['email'].strip()) == 0:
            flash('Email is required', 'registration')
            is_valid = False
        # If email entered, continue with other email validation checks
        else: 
            # Validate that email does not yet exist in DB
            query = """
                SELECT * FROM users
                WHERE email = %(email)s;
            """
            results = connectToMySQL(cls.db).query_db(query, form_data)

            if len(results) > 0:
                flash('User with this email already exists', 'registration')
                is_valid = False

            # Validate email format
            EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
            if not EMAIL_REGEX.match(form_data['email']):
                flash('Invalid email format', 'registration')
                is_valid = False

        # Validate that password was entered:
        if len(form_data['password'].strip()) == 0:
            flash('Password is required', 'registration')
            is_valid = False
        # If password was entered, continue with other password validation checks:
        else: 
            # Validate password confirmation
            if form_data['password'] != form_data['confirm-password']:
                flash('Passwords must match', 'registration')
                is_valid = False
            # Password must contain at least 8 characters, at least one uppercase letter, one lowercase letter, one number, and one special character
            PASSWORD_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_\-])[A-Za-z\d@$!%*?&_]{8,}$")
            if not PASSWORD_REGEX.match(form_data['password']):
                flash('Password must contain minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character', 'registration')
                is_valid = False

        return is_valid
    

    @classmethod
    def validate_login(cls, form_data):
        is_valid = True

        if not form_data['email']:
            flash('Email is required', 'login')
            is_valid = False

        if not form_data['password']:
            flash('Password is required', 'login')
            is_valid = False

        return is_valid

    @classmethod
    def login(cls, form_data):
        if not cls.validate_login(form_data):
            return False

        # Determine whether the email exists in the DB
        query = """
                SELECT * FROM users
                WHERE email = %(email)s;
            """
        results = connectToMySQL(cls.db).query_db(query, form_data)

        if len(results) < 1:
            flash('Invalid email/password', 'login')
            print('Email does not exist in db')
            return False
        
        # Determine whether the password provided matches the password in the DB
        if not bcrypt.check_password_hash(results[0]['password'], form_data['password']):
            flash('Invalid email/password', 'login')
            print('Password incorrect')
            return False
        
        # If login form passes validation checks, return a User object
        return cls(results[0])
    

    
