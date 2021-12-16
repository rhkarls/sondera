# -*- coding: utf-8 -*-
"""
Parameters and related for the different APIs

"""
from enum import Enum


class ParametersHydroObs(Enum):
    """
    Numbers match API parameters

    """
    Discharge = 1  # Vattenföring, dygn

class ParametersMetObs(Enum):
    """ Numbers match API parameters
    For values that are coded:
    https://opendata.smhi.se/apidocs/metobs/codes.html
    """
    TemperatureAirHour = 1  # Lufttemperatur, momentanvärde, 1 gång/tim
    TemperatureAirDay = 2  # Lufttemperatur, medelvärde 1 dygn, 1 gång/dygn, kl 00
    WindDirection = 3  # Vindriktning, medelvärde 10 min, 1 gång/tim
    WindSpeed = 4  # Vindhastighet, medelvärde 10 min, 1 gång/tim
    PrecipitationDayAt06 = 5  # Nederbördsmängd, summa 1 dygn, 1 gång/dygn, kl 06
    RelativeHumidity = 6  # Relativ Luftfuktighet, momentanvärde, 1 gång/tim
    PrecipitationHour = 7  # Nederbördsmängd, summa 1 timme, 1 gång/tim
    SnowDepth = 8  # Snödjup, momentanvärde, 1 gång/dygn, kl 06
    PressureAir = 9  # Lufttryck reducerat havsytans nivå, vid havsytans nivå, momentanvärde, 1 gång/tim
    SunshineDuration = 10  # Solskenstid, summa 1 timme, 1 gång/tim
    RadiationGlobal = 11  # Global Irradians (svenska stationer), medelvärde 1 timme, 1 gång/tim
    Visibility = 12  # Sikt, momentanvärde, 1 gång/tim
    CurrentWeather = 13  # Rådande väder, momentanvärde, 1 gång/tim resp 8 gånger/dygn
    Precipitation15min = 14  # Nederbördsmängd, summa 15 min, 4 gånger/tim
    PrecipitationIntensityMax15min = 15  # Nederbördsintensitet, max under 15 min, 4 gånger/tim
    Cloudiness = 16  # Total molnmängd, momentanvärde, 1 gång/tim
    PrecipitationAt06At18 = 17  # Nederbörd, 2 gånger/dygn, kl 06 och 18
    PrecipitationDayAt18 = 18  # Nederbörd, 1 gång/dygn, kl 18
    TemperatureAirMin = 19  # Lufttemperatur, min, 1 gång per dygn
    TemperatureAirMax = 20  # Lufttemperatur, max, 1 gång per dygn
    WindSpeedGust = 21  # Byvind, max, 1 gång/tim
    TemperatureAirMeanMonth = 22  # Lufttemperatur, medel, 1 gång per månad
    PrecipitationMonth = 23  # Nederbördsmängd, summa, 1 gång per månad
    RadiationLongwave = 24  # Långvågs-Irradians, Långvågsstrålning, medel 1 timme, varje timme
    WindSpeedMax = 25  # Max av MedelVindhastighet, maximum av medelvärde 10 min, under 3 timmar, 1 gång/tim
    TemperatureAirMinAt06At18 = 26  # Lufttemperatur, min, 2 gånger per dygn, kl 06 och 18
    TemperatureAirMaxAt06At18 = 27  # Lufttemperatur, max, 2 gånger per dygn, kl 06 och 18
    CloudBaseLayer1 = 28  # Molnbas, lägsta molnlager, momentanvärde, 1 gång/tim
    CloudinessLayer1 = 29  # Molnmängd, lägsta molnlager, momentanvärde, 1 gång/tim
    CloudBaseLayer2 = 30  # Molnbas, andra molnlager, momentanvärde, 1 gång/tim
    CloudinessLayer2 = 31  # Molnmängd, andra molnlager, momentanvärde, 1 gång/tim
    CloudBaseLayer3 = 32  # Molnbas, tredje molnlager, momentanvärde, 1 gång/tim
    CloudinessLayer3 = 33  # Molnmängd, tredje molnlager, momentanvärde, 1 gång/tim
    CloudBaseLayer4 = 34  # Molnbas, fjärde molnlager, momentanvärde, 1 gång/tim
    CloudinessLayer4 = 35  # Molnmängd, fjärde molnlager, momentanvärde, 1 gång/tim
    CloudBaseLayerLowest = 36  # Molnbas, lägsta molnbas, momentanvärde, 1 gång/tim
    CloudBaseLayerLowestMin = 37  # Molnbas, lägsta molnbas, min under 15 min, 1 gång/tim
    PrecipitationIntensityMaxMean15min = 38  # Nederbördsintensitet, max av medel under 15 min, 4 gånger/tim
    TemperatureDewPoint = 39  # Daggpunktstemperatur, momentanvärde, 1 gång/tim
    GroundConditions = 40  # Markens tillstånd, momentanvärde, 1 gång/dygn, kl 06


class ParametersGWLevels(Enum):
    LevelBelowWellTop = 1  # grundvattenniva_cm_u._roroverkant
    LevelAboveSeaLevel = 2  # grundvattenniva_m_o.h.
    LevelBelowGroundSurface = 3  # grundvattenniva_m_under_markyta


# Patterns to more safely find start of CSV data from SMHI MetObs, and for parsing date and time
# TODO timestamp_type might not be needed
parameter_patterns = {
    ParametersMetObs.TemperatureAirHour: {'str_pattern': 'Datum;Tid (UTC);Lufttemperatur',
                                          'use_cols': [0, 1, 2, 3],
                                          'timestamp_type': 'date_time'},
    ParametersMetObs.TemperatureAirDay: {'str_pattern': 'Från Datum Tid (UTC);Till Datum Tid (UTC)',
                                         'use_cols': [2, 3, 4],
                                         'timestamp_type': 'ref'},
    ParametersHydroObs.Discharge: {'str_pattern': 'Datum (svensk sommartid);Vattenföring',
                                   'use_cols': [0, 1, 2],
                                   'timestamp_type': 'date'}} # NOTE ONLY HYDROOBS CAN HAVE DATE ATM, CHANGE IN CODE NEEDED IF OTHER HAVE IT TOO
