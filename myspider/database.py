import mysql.connector
from mysql.connector import Error


def create_connection():
    """Crée une connexion à la base de données MySQL"""
    conn = None
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='votre_mot_de_passe',
            database='prices'
        )
        print("Connexion réussie à la base de données MySQL")
    except Error as e:
        print(f"Erreur lors de la connexion à la base de données: {e}")
    return conn


def create_table(conn):
    """Crée la table products si elle n'existe pas"""
    try:
        c = conn.cursor()
        c.execute('''
            create table products(
                link varchar(255) not null primary key,
                title varchar(255) null,
                price float null,
                timestamp timestamp null
            )
        ''')
        conn.commit()
        print("Table 'products' créée avec succès")
    except Error as e:
        print(f"Erreur lors de la création de la table: {e}")


def insert_product(link, title, price, timestamp):
    """Insère un produit dans la table"""
    conn = create_connection()
    if conn:
        try:
            c = conn.cursor()
            c.execute('''
                INSERT INTO products (link, title, price, timestamp)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    title = VALUES(title),
                    price = VALUES(price),
                    timestamp = VALUES(timestamp)
            ''', (link, title, price, timestamp))
            conn.commit()
            print(f"Produit inséré/ mis à jour: {title} à {price}")
        except Error as e:
            print(f"Erreur lors de l'insertion du produit: {e}")
        finally:
            conn.close()


def check_table_exists(conn):
    """Vérifie si la table 'products' existe"""
    try:
        c = conn.cursor()
        c.execute("SHOW TABLES LIKE 'products';")
        result = c.fetchone()
        if result:
            print("Table 'products' existe.")
            return True
        else:
            print("Table 'products' n'existe pas.")
            return False
    except Error as e:
        print(f"Erreur lors de la vérification de la table: {e}")
        return False


def setup_database():
    """Configure la base de données et vérifie la présence de la table"""
    conn = create_connection()
    if conn:
        if not check_table_exists(conn):
            create_table(conn)
        conn.close()


if __name__ == "__main__":
    setup_database()
