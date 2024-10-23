from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User

class Message:
    db = 'rideshares_schema'
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.users_id = data['users_id']
        self.rideshares_id = data['rideshares_id']
        self.sender = None


    @staticmethod
    def create(form_data):
        query = """
            INSERT INTO messages
            (content, users_id, rideshares_id)
            VALUES
            (%(content)s, %(users_id)s, %(rideshares_id)s);
        """

        data = {
            'content': form_data['content'],
            'users_id': form_data['user_id'],
            'rideshares_id': form_data['rideshare_id']
        }

        message_id = connectToMySQL('rideshares_schema').query_db(query, data)

        return message_id
    

    @classmethod
    def get_all(cls):
        query = """
            SELECT * FROM MESSAGES
            JOIN users
            ON messages.users_id = users.id
        """

        results = connectToMySQL('rideshares_schema').query_db(query)

        all_messages = []

        for row in results:
            message = cls(row)

            # Add sender object
            sender_data = {
                'id': row['users.id'],
                'first_name': row['first_name']
            }
            sender_obj = User(sender_data)
            message.sender = sender_obj

            all_messages.append(message)

        return all_messages


    @staticmethod
    def delete(form_data):
        query = """
            DELETE FROM comments
            WHERE id = %(comment_id)s;
        """
        connectToMySQL('coding_dojo_wall_schema').query_db(query, form_data)