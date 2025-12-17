"""Crud functions for event table"""

from datetime import datetime

from flask import Blueprint

from app.db import execute_query

bp = Blueprint("events", __name__)


def create_event(description: str, date: datetime):
    """Creates new event row in the database

    Args:
        description (str): Description of the event
        date (datetime): Date of the event

    Returns:
        insert_id (int): Insert id given by database
    """
    query = "INSERT INTO Event (description, eventDate) VALUES (?, ?)"
    result = execute_query(query, (description, date))
    insert_id = result["insertId"]
    return insert_id


def get_event(event_id):
    """_summary_

    Args:
        event_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    query = "SELECT * FROM Event WHERE eventId = ?"
    result = execute_query(query, event_id)
    event = result[0]
    return event


def get_events():
    """AI is creating summary for get_events

    Returns:
        [type]: [description]
    """
    query = "SELECT * FROM Event"
    events = execute_query(query)
    return events


def update_event(event_id: int, description: str, date: str):
    """_summary_

    Args:
        event_id (int): _description_
        description (str): _description_
        date (str): _description_
    """
    query = "UPDATE Event SET description = ?, eventDate = ? WHERE eventId = ?"
    execute_query(query, (description, date, event_id))


def delete_event(event_id: int):
    pass


from app.events import routes
