import mysql.connector

def detect_price_errors():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='votre_mot_de_passe',
        database='prices'
    )
    c = conn.cursor()
    c.execute('SELECT * FROM products')
    rows = c.fetchall()
    conn.close()

    anomalies = []
    for row in rows:
        link, title, price, timestamp = row
        # Exemple de détection d'anomalies : prix inférieur à 5.00
        if price < 5.00:
            anomalies.append({
                'link': link,
                'title': title,
                'price': price,
                'timestamp': timestamp
            })

    # Afficher les anomalies détectées
    if anomalies:
        print("Anomalies détectées:")
        for anomaly in anomalies:
            print(anomaly)
    else:
        print("Aucune anomalie détectée.")

if __name__ == "__main__":
    detect_price_errors()
