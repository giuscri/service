from main import parse_detected_front_text
import json

class TestParseDetectedFrontText:
    def test_empty_front_text(self):
        expected = {
            "municipality": None,
            "last_name": None,
            "first_name": None,
            "place_of_birth": None,
            "date_of_birth": None,
            "sex": None,
            "height": None,
            "nationality": None,
            "expiration_date": None,
            "issue_date": None,
        }

        actual = parse_detected_front_text("")
        assert json.dumps(actual, sort_keys=True) == json.dumps(expected, sort_keys=True)

    def test_front_text(self):
        detected_front_text = "REPUBBLICA ITALIANA\nCA3 1507DG\nMINISTERO DELUINTERNO\nCARTA DI IDENTITA 7IDENTITY CARD\nCOMUNE DI/ MUNICIPALITY\nMOLINO\nCOGNOME/SURNAME\nDOE\nJOHN\nLUOGO E DATA DI NASCITA\nPLACE AND DATE OF BIRTH\nBOLOGNA (BO) 03.05.1994\nSESSO\nSEX\nM\nSTATURA\nHEIGHT\n157\nCITTADINANZA\nNATIONALITY\nITA\nSCADENZA/EXPIRY\n03.05.2029\nEMISSIONE/ISSUING\n07.02.2019\nFIRMA DEL TITOLARE\nHOLDER'S SIGNATURE\n250845\n"
        expected = {
            "municipality": "MOLINO",
            "last_name": "DOE",
            "first_name": "JOHN",
            "place_of_birth": "BOLOGNA (BO)",
            "date_of_birth": "1994-05-03",
            "sex": "M",
            "height": "157",
            "nationality": "ITA",
            "expiration_date": "2029-05-03",
            "issue_date": "2019-02-07",
        }

        actual = parse_detected_front_text(detected_front_text)
        assert json.dumps(actual, sort_keys=True) == json.dumps(expected, sort_keys=True)

        detected_front_text = "REPUBBLICA ITALIANA\nCA31507DG\nMINISTERO DELL'INTERNO\nCARTA DI IDENTITA 7 IDENTITY CARD\nCOMUNE DI MUNICIPALITY\nMOLINO\nCOGNOME/SURNAME\nDOE\nNOME/NAME\nJOHN\nLUOGO E DATA DI NASCITA\nPLACE AND DATE OF BIRTH\nBOLOGNA (BO) 03.05.1994\nSESSO\nSEX\nSTATURA-\nHEI\nCITTADINANZA\nNATIONALITY\nTA\n157\nEMISSIONE ISSUING\n07.02.2019\nFIRMA DEL TITOLARE\nHOLDER'S SIGNATURE\nDENZA\n03.05.2029\n250845\n"
        expected = {
            "municipality": "MOLINO",
            "last_name": "DOE",
            "first_name": "JOHN",
            "place_of_birth": "BOLOGNA (BO)",
            "date_of_birth": "1994-05-03",
            "sex": None,
            "height": None,
            "nationality": "TA",
            "expiration_date": None,
            "issue_date": "2019-02-07",
        }

        actual = parse_detected_front_text(detected_front_text)
        assert json.dumps(actual, sort_keys=True) == json.dumps(expected, sort_keys=True)