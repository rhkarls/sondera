# -*- coding: utf-8 -*-
"""
Parameters and related for the various APIs

"""
from enum import Enum


class ParametersHydroObs(Enum):
    """
    Numbers match API integer parameter ids

    """
    Discharge = 1  # Vattenföring, dygn


class ParametersMetObs(Enum):
    """ Numbers match API integer parameter ids
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
    PrecipitationTypeAt06And18 = 17  # Nederbörd, 2 gånger/dygn, kl 06 och 18
    PrecipitationTypeDayAt06 = 18  # Nederbörd, 1 gång/dygn, kl 06
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
    LevelBelowWellTop = 'grundvattenniva_cm_u._roroverkant'
    LevelAboveSeaLevel = 'grundvattenniva_m_o.h.'
    LevelBelowGroundSurface = 'grundvattenniva_m_under_markyta'


class SGULanCodes(Enum):
    Blekinge = '10'
    Dalarna = '20'
    Gotland = '09'
    Gavleborg = '21'
    Halland = '13'
    Jamtland = '23'
    Jonkoping = '06'
    Kalmar = '08'
    Kronoberg = '07'
    Norrbotten = '25'
    Skane = '12'
    Stockholm = '01'
    Sodermanland = '04'
    Uppsala = '03'
    Varmland = '17'
    Vasterbotten = '24'
    Vasternorrland = '22'
    Vastmanland = '19'
    VastraGotaland = '14'
    Orebro = '18'
    Ostergotland = '05'


# Patterns to more safely find start of CSV data from SMHI MetObs, and for parsing date and time
# TODO timestamp_type might not be needed
# move else where, own file
# TODO str_pattern doesnt have to be unique, just to find the line in each csv str
#       Only a few (2-3?) different formats
# get str pattern by looking up data:
# https://opendata-download-metobs.smhi.se/api/version/latest/parameter/3.json
# then click on a station corrected-archive

smhi_parameter_patterns = {
    ParametersMetObs.TemperatureAirHour: {'str_pattern': 'Datum;Tid (UTC);Lufttemperatur',
                                          'use_cols': [0, 1, 2, 3],
                                          'timestamp_type': 'date_time'},
    ParametersMetObs.TemperatureAirDay: {
        'str_pattern': 'Från Datum Tid (UTC);Till Datum Tid (UTC);Representativt dygn',
        'use_cols': [2, 3, 4],
        'timestamp_type': 'ref'},
    ParametersMetObs.WindDirection: {
        'str_pattern': 'Datum;Tid (UTC);Vindriktning',
        'use_cols': [0, 1, 2, 3],
        'timestamp_type': 'date_time'},
    ParametersMetObs.WindSpeed: {'str_pattern': 'Datum;Tid (UTC);Vindhastighet',
                                 'use_cols': [0, 1, 2, 3],
                                 'timestamp_type': 'date_time'},
    ParametersMetObs.PrecipitationDayAt06: {
        'str_pattern': 'Från Datum Tid (UTC);Till Datum Tid (UTC);Representativt dygn',
        'use_cols': [2, 3, 4],
        'timestamp_type': 'ref'},
    ParametersMetObs.RelativeHumidity: {
        'str_pattern': 'Datum;Tid (UTC);Relativ Luftfuktighet',
        'use_cols': [0, 1, 2, 3],
        'timestamp_type': 'date_time'},
    ParametersMetObs.PrecipitationHour: {
        'str_pattern': 'Datum;Tid (UTC);Nederbördsmängd',
        'use_cols': [0, 1, 2, 3],
        'timestamp_type': 'date_time'},
    ParametersMetObs.SnowDepth: {'str_pattern': 'Datum;Tid (UTC);Snödjup',
                                 'use_cols': [0, 1, 2, 3],
                                 'timestamp_type': 'date_time'},
    ParametersMetObs.PressureAir: {
        'str_pattern': 'Datum;Tid (UTC);Lufttryck',
        'use_cols': [0, 1, 2, 3],
        'timestamp_type': 'date_time'},
    ParametersMetObs.SunshineDuration: {
        'str_pattern': 'Datum;Tid (UTC);Solskenstid',
        'use_cols': [0, 1, 2, 3],
        'timestamp_type': 'date_time'},
    ParametersMetObs.RadiationGlobal: {
        'str_pattern': 'Datum;Tid (UTC);Global Irradians',
        'use_cols': [0, 1, 2, 3],
        'timestamp_type': 'date_time'},
    ParametersMetObs.Visibility: {
        'str_pattern': 'Datum;Tid (UTC);Sikt',
        'use_cols': [0, 1, 2, 3],
        'timestamp_type': 'date_time'},
    ParametersMetObs.CurrentWeather: {
        'str_pattern': 'Datum;Tid (UTC);Rådande väder',
        'use_cols': [0, 1, 2, 3],
        'timestamp_type': 'date_time'},
    ParametersMetObs.Precipitation15min: {
        'str_pattern': 'Datum;Tid (UTC);Nederbördsmängd',
        'use_cols': [0, 1, 2, 3],
        'timestamp_type': 'date_time'},
    ParametersMetObs.PrecipitationIntensityMax15min: {
        'str_pattern': 'Datum;Tid (UTC);Nederbördsintensitet',
        'use_cols': [0, 1, 2, 3],
        'timestamp_type': 'date_time'},
    ParametersMetObs.Cloudiness: {
        'str_pattern': 'Datum;Tid (UTC);Total molnmängd',
        'use_cols': [0, 1, 2, 3],
        'timestamp_type': 'date_time'},
    ParametersMetObs.PrecipitationTypeAt06And18: {
        'str_pattern': 'Datum;Tid (UTC);Nederbörd',
        'use_cols': [0, 1, 2, 3],
        'timestamp_type': 'date_time'},
    ParametersMetObs.PrecipitationTypeDayAt06: {
        'str_pattern': 'Från Datum Tid (UTC);Till Datum Tid (UTC);Representativt dygn;Nederbörd',
        'use_cols': [2, 3, 4],
        'timestamp_type': 'ref'},
    ParametersMetObs.TemperatureAirMin: {
        'str_pattern': 'Från Datum Tid (UTC);Till Datum Tid (UTC);Representativt dygn;Lufttemperatur',
        'use_cols': [2, 3, 4],
        'timestamp_type': 'ref'},
    ParametersMetObs.TemperatureAirMax: {
        'str_pattern': 'Från Datum Tid (UTC);Till Datum Tid (UTC);Representativt dygn;Lufttemperatur',
        'use_cols': [2, 3, 4],
        'timestamp_type': 'ref'},
    ParametersMetObs.GroundConditions: {'str_pattern': 'Datum;Tid (UTC);Markens tillstånd',
                                        'use_cols': [0, 1, 2, 3],
                                        'timestamp_type': 'date_time'},

    ParametersHydroObs.Discharge: {'str_pattern': 'Datum (svensk sommartid);Vattenföring',
                                   'use_cols': [0, 1, 2],
                                   'timestamp_type': 'date'}}  # NOTE ONLY HYDROOBS CAN HAVE DATE ATM, CHANGE IN CODE NEEDED IF OTHER HAVE IT TOO


# SMHI:
# Rådande väder
# Moln mängd

smhi_groundcondition_codes = {0: 'Torr (utan sprickor eller nämnvärd mängd stoft eller lös sand)',
                              1: 'Fuktig',
                              2: 'Våt (större eller mindre vattensamlingar förekommer)',
                              3: 'Översvämmad',
                              4: 'Frusen',
                              5: 'Täckt av glattis',
                              6: 'Täckt av löst torrt stoft eller lös torr sand – som inte helt täcker markytan',
                              7: 'Täckt av löst torrt stoft eller lös torr sand – i ett tunt lager som helt täcker markytan',
                              8: 'Täckt av löst torrt stoft eller lös torr sand – i ett måttligt eller tjockt lager som helt täcker markytan',
                              9: 'Extremt torr med sprickor',
                              10: 'Huvudsakligen täckt av is',
                              11: 'Delvis eller helt täckt av packad eller våt snö – till mindre än hälften',
                              12: 'Delvis eller helt täckt av packad eller våt snö – till minst hälften men ej helt',
                              13: 'Delvis eller helt täckt av packad eller våt snö – helt och i ett jämnt lager',
                              14: 'Delvis eller helt täckt av packad eller våt snö – helt och i ett ojämnt lager',
                              15: 'Delvis eller helt täckt av lös och torr snö – till mindre än hälften',
                              16: 'Delvis eller helt täckt av lös och torr snö – till minst hälften men ej helt',
                              17: 'Delvis eller helt täckt av lös och torr snö – helt och i ett jämnt lager',
                              18: 'Delvis eller helt täckt av lös och torr snö – helt och i ett ojämnt lager',
                              19: 'Helt täckt av snö med höga drivor'}
