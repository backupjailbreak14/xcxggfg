from datetime import datetime
from flask import abort, redirect, render_template, request, url_for
from app.events import bp, create_event, get_event, get_events, update_event, execute_query


@bp.route('/aanmelden', methods=['GET', 'POST'])
def aanmelden():
    """Handle horeca (restaurant) registration and insert data into the database."""
    if request.method == 'POST':
        bedrijfsnaam = request.form['Bnaam']
        email = request.form['email']
        wachtwoord = request.form['Pass']
        locatie = request.form['locatie']

        # Insert registration data into the database
        query = 'INSERT INTO aanmeld_horeca (bedrijfsnaam, email, wachtwoord, locatie) VALUES (?, ?, ?, ?)'
        execute_query(query, (bedrijfsnaam, email, wachtwoord, locatie))

        return redirect(url_for("events.start"))
    return render_template('/aanmelden.html')


@bp.route('/start', methods=['POST', 'GET'])
def start():
    """Handle login for horeca users and validate email and password."""
    if request.method == 'POST':
        email = request.form['email']
        wachtwoord = request.form['Pass']  

        # SQL query: find a row where email and password match
        query = 'SELECT * FROM aanmeld_horeca WHERE email = ? AND wachtwoord = ?'

        # Execute the query and store it in result
        # If a match exists, it will login
        result = execute_query(query, (email, wachtwoord))    

        if result:
            return redirect(url_for('events.voedselbox_hor'))
        else:
            return render_template('/start.html', error='Onjuist email/wachtwoord')
                                    
    return render_template('/start.html') 


@bp.route('/voedselbox_hor', methods=['POST', 'GET'])
def voedselbox_hor():
    """Handle creation of food boxes by horeca users."""
    if request.method == 'POST':

        # Retrieve fields from the form
        boxnaam = request.form['Vnaam']
        beschrijving = request.form["beschrijving"]
        prijs = request.form["prijs"]
        tijdstip = request.form['tijd']
        datum = request.form['datum']

        # Retrieve checkboxes: 1 = true, 0 = false (for database storage)
        halal = 1 if 'hal_label' in request.form else 0
        gluten = 1 if 'glu_label' in request.form else 0
        vegan = 1 if 'vegan_label' in request.form else 0
        vega = 1 if 'vegar_label' in request.form else 0

        # Query to save the food box in the database
        query = 'INSERT INTO voedselbox_hor(boxnaam, beschrijving, prijs, halal, gluten, vegan, vega, tijdstip, datum) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'

        # Execute the query and store the values in the database
        execute_query(query, (boxnaam, beschrijving, prijs, halal, gluten, vegan, vega, tijdstip, datum))

    return render_template('/voedselbox_hor.html')


@bp.route('/registratie_klant', methods=['POST', 'GET'])
def registratie():
    """Handle registration of a customer and insert data into the database."""
    if request.method == 'POST':
        naam = request.form['Pnaam']
        email = request.form['email']
        wachtwoord = request.form['Wwoord']

        # Insert customer registration data into database
        query = 'INSERT INTO aanmeld_klant (naam, email, wachtwoord) VALUES (?, ?, ?)'
        execute_query(query, (naam, email, wachtwoord))

        return redirect(url_for('events.inlog_klant'))
    
    return render_template('/registratie_klant.html')


@bp.route('/inlog_klant', methods=['POST', 'GET'])
def inlog_klant():
    """Handle customer login and validate email and password."""
    if request.method == 'POST':
        email = request.form['email']
        wachtwoord = request.form['Wwoord']

        # Query to check if customer exists with given email and password
        query = 'SELECT * FROM aanmeld_klant WHERE email = ? AND wachtwoord = ?'
        result = execute_query(query, (email, wachtwoord))

        if result:
            return redirect(url_for('events.voedselbox_klant'))
        else:
            return render_template('/inlog_klant.html', error='Onjuist email/wachtwoord')
 
    return render_template('/inlog_klant.html')


@bp.route('/voedselbox_klant')
def voedselbox_klant():
    """Retrieve all available (not reserved) food boxes for customers."""
    # Query to get available boxes (not reserved = 0)
    query = 'SELECT * FROM voedselbox_hor WHERE gereserveerd = 0 ORDER BY ID'
    
    # Execute query and store results in variable 'boxen'
    boxen = execute_query(query)

    # Render the customer page with the list of available boxes
    return render_template('/voedselbox_klant.html', boxen=boxen)


@bp.route('/reserveer/<int:id>', methods=['POST', 'GET'])
def reserveer(id):
    """Reserve a food box based on its ID and render confirmation page and also removes it from dashboard."""
    # Retrieve the box from the database by ID from the URL
    query = 'SELECT * FROM voedselbox_hor WHERE ID = ?'
    box = execute_query(query, (id,))[0]

    # Update the box as reserved (only boxes with gereserveerd = 0 are visible)
    update_query = 'UPDATE voedselbox_hor SET gereserveerd = 1 WHERE ID = ?'

    # Execute the update query
    execute_query(update_query, (id,))

    # Render the confirmation page with box details
    return render_template('reservering_gelukt.html', box=box)


@bp.route('/reserveringen_hor')
def reserveringen_hor():
    """Retrieve all reserved boxes for horeca users."""
    query = 'SELECT * FROM voedselbox_hor WHERE gereserveerd = 1 ORDER BY ID'

    reserveringen = execute_query(query)

    return render_template('reserveringen_hor_v2.html', reserveringen=reserveringen)


@bp.route('/afhandel_reservering/<int:id>')
def afhandel_reservering(id):
    """Delete a reserved food box based on its ID When the horeca user clicks on  Markeer als afg. ."""
    query = "DELETE FROM voedselbox_hor WHERE ID = ?"
    execute_query(query, (id,))

    return redirect(url_for('events.reserveringen_hor'))
