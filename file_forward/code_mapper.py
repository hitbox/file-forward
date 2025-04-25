import csv

class CodeMapper:
    """
    Convert IATA to ICAO and vice verse.
    """

    def __init__(self, *, iata_to_icao=None, icao_to_iata=None):
        if (
            (iata_to_icao is None and icao_to_iata is None)
            or
            (iata_to_icao is not None and icao_to_iata is not None)
        ):
            raise ValueError(
                'Must provide exactly one of "iata_to_icao" or "icao_to_iata".')

        if iata_to_icao:
            icao_to_iata = {val: key for key, val in iata_to_icao.items()}
        else:
            iata_to_icao = {val: key for key, val in icao_to_iata.items()}

        self.iata_to_icao = iata_to_icao
        self.icao_to_iata = icao_to_iata

    @classmethod
    def from_csv(cls, filename, iata_fieldname, icao_fieldname):
        """
        Load conversions from CSV file.
        """
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            iata_to_icao = {row[iata_fieldname]: row[icao_fieldname] for row in reader}

        return cls(iata_to_icao=iata_to_icao)

    def iata(self, icao):
        return self.icao_to_iata[icao]

    def icao(self, iata):
        return self.iata_to_icao[iata]
