CATEGORIES = {
    '0': 'MANUELLE KATEGORISIERUNG',
    '1.1': 'Nettogehalt',
    '1.2': 'Selbststaendige Taetigkeiten',
    '1.3': 'Dividenden & Zinsen',
    '1.4': 'Kursgewinne',
    '1.5': 'Vermietung',
    '1.6': 'Verkauf',
    '1.7': 'Steuererstattung',
    '1.8': 'Zuschuesse',
    '2.1': 'Miete',
    '2.2': 'Nebenkosten',
    '2.3': 'Internetanschluss',
    '3.1': 'Haftpflicht',
    '4.1': 'Schuldtilgung',
    '4.2': 'Kontofuehrungsgebuehren',
    '5.1': 'Regionales Abo OPNV',
    '5.2': 'Bahncard',
    '6.1': 'Mitgliedsbeitraege',
    '6.2': 'Saisonkarten',
    '7.1': 'Kursbeitraege',
    '8.1': 'Mobilfunk',
    '8.2': 'Cloud Speicher',
    '8.3': 'Spotify',
    '9.1': 'Haushaltsgeraete',
    '9.2': 'Einrichtungsgegenstaende',
    '9.3': 'Handwerkskosten',
    '10.1': 'Lebensmittel',
    '10.2': 'Mode',
    '10.3': 'Elektronik',
    '10.4': 'Musikinstrumente',
    '10.5': 'Sport',
    '10.6': 'Mittagstisch Arbeit',
    '10.7': 'Gekaufte Speisen',
    '10.8': 'Gesundheit',
    '10.9': 'Körperpflege',
    '11.1': 'Kursverluste',
    '11.2': 'Schuldtilgung',
    '12.1': 'Mobilitaet ohne Ausfluege und Urlaube',
    '13.1': 'Musikschule', '13.2': 'Buecher',
    '13.3': 'Kursgebuehren',
    '14.1': 'Ausgehen',
    '14.2': 'Ausfluege',
    '14.3': 'Urlaub',
    '14.4': 'Wellness',
    '15.1': 'Unzurechenbare Barzahlungen',
    '15.2': 'Versandkosten',
    '15.3': 'Geschenke',
    '15.4': 'Spenden',
    '15.5': 'Geldstrafen'
}

def pretty_print_categories():
    s = ''
    family = 0
    for k, v in CATEGORIES.items():
        number = float(k)
        number = int(number)

        if family == number:
            s = s + k + ": " + v + "\t"
        else:
            print(s)
            s = k + ": " + v + "\t"
            family = number

    print(s)
