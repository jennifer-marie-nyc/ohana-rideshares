from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User
from datetime import datetime
from pprint import pprint

class Rideshare:
    db = 'rideshares_schema'
    def __init__(self, data):
        self.id = data['id']
        self.destination = data['destination']
        self.pickup_loc = data['pickup_loc']
        self.date = data['date']
        self.details = data['details']
        self.rider_id = data['rider_id']
        self.rider = None
        self.driver = None

    @staticmethod
    def create(form_data):
        query = """
            INSERT INTO rideshares
            (destination, pickup_loc, date, details, rider_id)
            VALUES
            (%(destination)s, %(pickup_loc)s, %(date)s, %(details)s, %(rider_id)s);
        """

        rideshare_id = connectToMySQL('rideshares_schema').query_db(query, form_data)

        return rideshare_id
    
    @classmethod
    def get_all(cls):
        query = """
            SELECT rideshares.id, destination, pickup_loc, date, details, rider_id, driver_id, u1.first_name AS rider_first_name, u2.first_name AS driver_first_name
            FROM rideshares
            JOIN users AS u1 on rideshares.rider_id = u1.id
            LEFT JOIN users AS u2 on rideshares.driver_id = u2.id;
        """

        results = connectToMySQL(cls.db).query_db(query)
        pprint(results)
        all_rideshares = []

        for row in results:
            rideshare = cls(row)

            # Add rider object
            rider_data = {
                'id': row['rider_id'],
                'first_name': row['rider_first_name'],
            }
            rider_obj = User(rider_data)
            rideshare.rider = rider_obj

            # Add driver object if driver assigned
            if row['driver_id']:
                driver_data = {
                    'id': row['driver_id'],
                    'first_name': row['driver_first_name']
                }
                driver_obj =  User(driver_data)
                rideshare.driver = driver_obj

            all_rideshares.append(rideshare)

        return all_rideshares
    
    @classmethod
    def get_one_by_id_with_rider_and_driver(cls, rideshare_id):
        query = """
            SELECT rideshares.id, destination, pickup_loc, date, details, rider_id, driver_id, u1.first_name AS rider_first_name, u2.first_name AS driver_first_name
            FROM rideshares
            JOIN users AS u1 on rideshares.rider_id = u1.id
            LEFT JOIN users AS u2 on rideshares.driver_id = u2.id
            WHERE rideshares.id = %(id)s;
        """

        data = {
            'id': rideshare_id
        }

        results = connectToMySQL(cls.db).query_db(query, data)
        one_dict = results[0]

        rideshare = cls(one_dict)

        # Add rider object
        rider_data = {
                'id': one_dict['rider_id'],
                'first_name': one_dict['rider_first_name']
            }
        rider_obj = User(rider_data)
        rideshare.rider = rider_obj

        # Add driver object if driver assigned
        if one_dict['driver_id']:
            driver_data = {
                'id': one_dict['driver_id'],
                'first_name': one_dict['driver_first_name']
            }
            driver_obj =  User(driver_data)
            rideshare.driver = driver_obj
        
        return rideshare

    @staticmethod
    def update_rideshare(form_data):
        query = """
            UPDATE rideshares
            SET
            pickup_loc = %(pickup_loc)s,
            details = %(details)s
            WHERE id = %(rideshare_id)s
        """
        connectToMySQL('rideshares_schema').query_db(query, form_data)


    @staticmethod
    def update_driver(rideshare_id, driver_id):
        query = """
            UPDATE rideshares
            SET
            driver_id = %(driver_id)s
            WHERE id = %(rideshare_id)s;
        """
        data = {
            'driver_id': driver_id,
            'rideshare_id': rideshare_id
        }
        connectToMySQL('rideshares_schema').query_db(query, data)

    @staticmethod
    def delete(rideshare_id):
        query = """
            DELETE FROM rideshares
            WHERE id = %(id)s;
        """
        data = {
            'id': rideshare_id
        }

        connectToMySQL('rideshares_schema').query_db(query, data)

    @classmethod
    def validate_rideshare(cls, form_data):
        is_valid = True

        # Validate destination
        if len(form_data['destination'].strip()) == 0:
            flash('Destination is required')
            is_valid = False
        elif len(form_data['destination'].strip()) < 3:
            flash('Destination must be at least 3 characters.')
            is_valid = False

        # Validate pickup location
        if len(form_data['pickup_loc'].strip()) == 0:
            flash('Pickup location is required')
            is_valid = False
        elif len(form_data['pickup_loc'].strip()) < 3:
            flash('Pickup location must be at least 3 characters.')
            is_valid = False

        # Validate rideshare date
        if len(form_data['date'].strip()) == 0:
            flash('Rideshare date is required')
            is_valid = False
        # If date entered, validate that date is not in the past
        else:
            rideshare_date = datetime.strptime(form_data['date'], '%Y-%m-%d').date()
            today = datetime.today().date()
            if rideshare_date < today:
                flash('Rideshare date cannot be in the past')
                is_valid = False

        # Validate details
        if len(form_data['details'].strip()) == 0:
            flash('Details field is required')
        elif len(form_data['details'].strip()) < 10:
            flash('Details must be at least 10 characters.')
            is_valid = False

        return is_valid

    @staticmethod
    def validate_rideshare_edit(form_data):
        is_valid = True

        # Validate pickup location
        if len(form_data['pickup_loc'].strip()) == 0:
            flash('Pickup location is required')
            is_valid = False
        elif len(form_data['pickup_loc'].strip()) < 3:
            flash('Pickup location must be at least 3 characters.')
            is_valid = False

        # Validate details
        if len(form_data['details'].strip()) == 0:
            flash('Details field is required')
        elif len(form_data['details'].strip()) < 10:
            flash('Details must be at least 10 characters.')
            is_valid = False

        return is_valid