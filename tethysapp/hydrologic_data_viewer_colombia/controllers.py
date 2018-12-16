from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tethys_sdk.gizmos import Button
from tethys_sdk.gizmos import *
from django.http import HttpResponse, JsonResponse
from hs_restclient import HydroShare, HydroShareAuthBasic

import requests
import json
import urllib2
import datetime as dt
import plotly.graph_objs as go
import csv
from csv import writer as csv_writer

@login_required()
def home(request):
    """
    Controller for the app home page.
    """
    save_button = Button(
        display_text='',
        name='save-button',
        icon='glyphicon glyphicon-floppy-disk',
        style='success',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Save'
        }
    )

    edit_button = Button(
        display_text='',
        name='edit-button',
        icon='glyphicon glyphicon-edit',
        style='warning',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Edit'
        }
    )

    remove_button = Button(
        display_text='',
        name='remove-button',
        icon='glyphicon glyphicon-remove',
        style='danger',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Remove'
        }
    )

    previous_button = Button(
        display_text='Previous',
        name='previous-button',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Previous'
        }
    )

    next_button = Button(
        display_text='Next',
        name='next-button',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Next'
        }
    )

    context = {
        'save_button': save_button,
        'edit_button': edit_button,
        'remove_button': remove_button,
        'previous_button': previous_button,
        'next_button': next_button
    }

    return render(request, 'hydrologic_data_viewer_colombia/home.html', context)

def hobs(request):
    """
    Controller for the app H observed page.
    """

    return render(request, 'hydrologic_data_viewer_colombia/hobs.html')

def hsen(request):
    """
    Controller for the app H sensor page.
    """

    return render(request, 'hydrologic_data_viewer_colombia/hsen.html')

def qobs(request):
    """
    Controller for the app Q observed page.
    """

    return render(request, 'hydrologic_data_viewer_colombia/qobs.html')

def qsen(request):
    """
    Controller for the app Q sensor page.
    """

    return render(request, 'hydrologic_data_viewer_colombia/qsen.html')

def about(request):
    """
    Controller for the app about page.
    """

    return render(request, 'hydrologic_data_viewer_colombia/about.html')


def get_realTimeObsDataH(request):
    """
    Get data from fews stations
    """

    get_data = request.GET

    try:
        codEstacion = get_data['stationcode']
        nomEstacion = get_data['stationname']

        url2 = 'http://fews.ideam.gov.co/colombia/jsonH/00' + codEstacion + 'Hobs.json'

        req2 = urllib2.Request(url2)
        opener2 = urllib2.build_opener()
        f2 = opener2.open(req2)
        data2 = json.loads(f2.read())

        obsWaterLevel = (data2.get('obs'))
        obsWaterLevel = (obsWaterLevel.get('data'))

        datesObsWaterLevel = [row[0] for row in obsWaterLevel]
        obsWaterLevel = [row[1] for row in obsWaterLevel]

        dates = []
        waterLevel = []

        for i in range(0, len(datesObsWaterLevel) - 1):
            year = int(datesObsWaterLevel[i][0:4])
            month = int(datesObsWaterLevel[i][5:7])
            day = int(datesObsWaterLevel[i][8:10])
            hh = int(datesObsWaterLevel[i][11:13])
            mm = int(datesObsWaterLevel[i][14:16])
            dates.append(dt.datetime(year, month, day, hh, mm))
            waterLevel.append(obsWaterLevel[i])

        datesObsWaterLevel = dates
        obsWaterLevel = waterLevel

        obs_WL = go.Scatter(
            x=datesObsWaterLevel,
            y=obsWaterLevel,
            name='Sensor'
        )

        layout = go.Layout(title='Real Time Observed Water Level',
                           xaxis=dict(
                               title='Dates', ),
                           yaxis=dict(
                               title='Water Level (m)',
                               autorange=True),
                           showlegend=False)

        chart_obj = PlotlyView(
            go.Figure(data=[obs_WL],
                      layout=layout)
        )

        context = {
            'gizmo_object': chart_obj,
        }

        return render(request, 'hydrologic_data_viewer_colombia/gizmo_ajax.html', context)

    except Exception as e:
        print str(e)
        return JsonResponse({'error': 'No  data found for the station.'})

def get_historicObsDataH(request):
    """
    Get data from hydroshare
    """

    get_data = request.GET

    try:
        codEstacion = get_data['stationcode']
        nomEstacion = get_data['stationname']
        resourceID = 'ceab9b8fccae452fac62d8d3ecbf8e78'

        auth = HydroShareAuthBasic(username='jorgessanchez7', password='Colombia03')
        hs = HydroShare(auth=auth)
        hs.setAccessRules(resourceID, public=True)

        url2 = 'https://www.hydroshare.org/resource/{0}/data/contents/H/obs/{1}_H_obs.csv'.format(resourceID,
                                                                                                  codEstacion)
        print(url2)

        response2 = urllib2.urlopen(url2)
        data = csv.reader(response2)
        data.next()

        dates = []
        data2 = []

        for row in data:
            date = row[0]
            date = dt.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            dates.append(date)
            value = row[1]
            data2.append(value)

        datesObsWaterLevel = dates
        obsWaterLevel = data2

        obs_WL = go.Scatter(
            x=datesObsWaterLevel,
            y=obsWaterLevel,
            name='Sensor'
        )

        layout = go.Layout(title='Historic Observed Water Level',
                           xaxis=dict(
                               title='Dates', ),
                           yaxis=dict(
                               title='Water Level (m)',
                               autorange=True),
                           showlegend=False)

        chart_obj = PlotlyView(
            go.Figure(data=[obs_WL],
                      layout=layout)
        )

        context = {
            'gizmo_object': chart_obj,
        }

        options = {"flag": "make_private"}
        result = hs.resource(resourceID).flag(options)

        return render(request, 'hydrologic_data_viewer_colombia/gizmo_ajax.html', context)

    except Exception as e:
        print str(e)
        return JsonResponse({'error': 'No  data found for the station.'})

def download_realTimeObsDataH(request):
    """
    Get data from fews stations
    """

    get_data = request.GET

    try:
        codEstacion = get_data['stationcode']
        nomEstacion = get_data['stationname']

        url2 = 'http://fews.ideam.gov.co/colombia/jsonH/00' + codEstacion + 'Hobs.json'

        req2 = urllib2.Request(url2)
        opener2 = urllib2.build_opener()
        f2 = opener2.open(req2)
        data2 = json.loads(f2.read())

        obsWaterLevel = (data2.get('obs'))
        obsWaterLevel = (obsWaterLevel.get('data'))

        datesObsWaterLevel = [row[0] for row in obsWaterLevel]
        obsWaterLevel = [row[1] for row in obsWaterLevel]

        dates = []
        waterLevel = []

        for i in range(0, len(datesObsWaterLevel) - 1):
            year = int(datesObsWaterLevel[i][0:4])
            month = int(datesObsWaterLevel[i][5:7])
            day = int(datesObsWaterLevel[i][8:10])
            hh = int(datesObsWaterLevel[i][11:13])
            mm = int(datesObsWaterLevel[i][14:16])
            dates.append(dt.datetime(year, month, day, hh, mm))
            waterLevel.append(obsWaterLevel[i])

        datesObsWaterLevel = dates
        obsWaterLevel = waterLevel

        pairs = [list(a) for a in zip(datesObsWaterLevel, obsWaterLevel)]

        response = HttpResponse(content_type='text/csv')

        response['Content-Disposition'] = 'attachment; filename=real_time_H_obs_{0}.csv'.format(codEstacion)

        writer = csv_writer(response)

        writer.writerow(['datetime', 'water level (m)'])

        for row_data in pairs:
            writer.writerow(row_data)

        return response

    except Exception as e:
        print str(e)
        return JsonResponse({'error': 'No  data found for the station.'})

def download_historicObsDataH(request):
    """
    Get data from hydroshare
    """

    get_data = request.GET

    try:
        codEstacion = get_data['stationcode']
        nomEstacion = get_data['stationname']
        resourceID = 'ceab9b8fccae452fac62d8d3ecbf8e78'

        auth = HydroShareAuthBasic(username='jorgessanchez7', password='Colombia03')
        hs = HydroShare(auth=auth)
        hs.setAccessRules(resourceID, public=True)

        url2 = 'https://www.hydroshare.org/resource/{0}/data/contents/H/obs/{1}_H_obs.csv'.format(resourceID,
                                                                                                  codEstacion)
        print(url2)

        response2 = urllib2.urlopen(url2)
        data = csv.reader(response2)
        data.next()

        dates = []
        data2 = []

        for row in data:
            date = row[0]
            date = dt.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            dates.append(date)
            value = row[1]
            data2.append(value)

        datesObsWaterLevel = dates
        obsWaterLevel = data2

        pairs = [list(a) for a in zip(datesObsWaterLevel, obsWaterLevel)]

        response = HttpResponse(content_type='text/csv')

        response['Content-Disposition'] = 'attachment; filename=historic_H_obs_{0}.csv'.format(codEstacion)

        writer = csv_writer(response)

        writer.writerow(['datetime', 'water level (m)'])

        for row_data in pairs:
            writer.writerow(row_data)

        options = {"flag": "make_private"}
        result = hs.resource(resourceID).flag(options)

        return response

    except Exception as e:
        print str(e)
        return JsonResponse({'error': 'No  data found for the station.'})

def get_realTimeSensorDataH(request):
    """
    Get data from fews stations
    """

    get_data = request.GET
    
    try:
        codEstacion = get_data['stationcode']
        nomEstacion = get_data['stationname']

        url2 = 'http://fews.ideam.gov.co/colombia/jsonH/00' + codEstacion + 'Hobs.json'

        req2 = urllib2.Request(url2)
        opener2 = urllib2.build_opener()
        f2 = opener2.open(req2)
        data2 = json.loads(f2.read())

        sensorWaterLevel = (data2.get('sen'))
        sensorWaterLevel = (sensorWaterLevel.get('data'))

        datesSensorWaterLevel = [row[0] for row in sensorWaterLevel]
        sensorWaterLevel = [row[1] for row in sensorWaterLevel]

        dates = []
        waterLevel = []

        for i in range(0, len(datesSensorWaterLevel) - 1):
            year = int(datesSensorWaterLevel[i][0:4])
            month = int(datesSensorWaterLevel[i][5:7])
            day = int(datesSensorWaterLevel[i][8:10])
            hh = int(datesSensorWaterLevel[i][11:13])
            mm = int(datesSensorWaterLevel[i][14:16])
            dates.append(dt.datetime(year, month, day, hh, mm))
            waterLevel.append(sensorWaterLevel[i])

        datesSensorWaterLevel = dates
        sensorWaterLevel = waterLevel

        sensor_WL = go.Scatter(
            x=datesSensorWaterLevel,
            y=sensorWaterLevel,
            name='Sensor'
        )

        layout = go.Layout(title='Real Time Sensor Water Level',
                           xaxis=dict(
                               title='Dates', ),
                           yaxis=dict(
                               title='Water Level (m)',
                               autorange=True),
                           showlegend=False)

        chart_obj = PlotlyView(
            go.Figure(data=[sensor_WL],
                      layout=layout)
        )

        context = {
            'gizmo_object': chart_obj,
        }

        return render(request, 'hydrologic_data_viewer_colombia/gizmo_ajax.html', context)

    except Exception as e:
        print str(e)
        return JsonResponse({'error': 'No  data found for the station.'})

def get_historicSensorDataH(request):
    """
    Get data from hydroshare
    """

    get_data = request.GET

    try:
        codEstacion = get_data['stationcode']
        nomEstacion = get_data['stationname']
        resourceID = 'ceab9b8fccae452fac62d8d3ecbf8e78'

        auth = HydroShareAuthBasic(username='jorgessanchez7', password='Colombia03')
        hs = HydroShare(auth=auth)
        hs.setAccessRules(resourceID, public=True)

        url2 = 'https://www.hydroshare.org/resource/{0}/data/contents/H/sen/{1}_H_sen.csv'.format(resourceID, codEstacion)
        print(url2)

        response2 = urllib2.urlopen(url2)
        data = csv.reader(response2)
        data.next()

        dates = []
        data2 = []

        for row in data:
            date = row[0]
            date = dt.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            dates.append(date)
            value = row[1]
            data2.append(value)

        datesSensorWaterLevel = dates
        sensorWaterLevel = data2

        sensor_WL = go.Scatter(
            x=datesSensorWaterLevel,
            y=sensorWaterLevel,
            name='Sensor'
        )

        layout = go.Layout(title='Historic Sensor Water Level',
                           xaxis=dict(
                               title='Dates', ),
                           yaxis=dict(
                               title='Water Level (m)',
                               autorange=True),
                           showlegend=False)

        chart_obj = PlotlyView(
            go.Figure(data=[sensor_WL],
                      layout=layout)
        )

        context = {
            'gizmo_object': chart_obj,
        }

        options = {"flag": "make_private"}
        result = hs.resource(resourceID).flag(options)

        return render(request, 'hydrologic_data_viewer_colombia/gizmo_ajax.html', context)

    except Exception as e:
        print str(e)
        return JsonResponse({'error': 'No  data found for the station.'})

def download_realTimeSensorDataH(request):
    """
    Get data from fews stations
    """

    get_data = request.GET

    try:
        codEstacion = get_data['stationcode']
        nomEstacion = get_data['stationname']

        url2 = 'http://fews.ideam.gov.co/colombia/jsonH/00' + codEstacion + 'Hobs.json'

        req2 = urllib2.Request(url2)
        opener2 = urllib2.build_opener()
        f2 = opener2.open(req2)
        data2 = json.loads(f2.read())

        sensorWaterLevel = (data2.get('sen'))
        sensorWaterLevel = (sensorWaterLevel.get('data'))

        datesSensorWaterLevel = [row[0] for row in sensorWaterLevel]
        sensorWaterLevel = [row[1] for row in sensorWaterLevel]

        dates = []
        waterLevel = []

        for i in range(0, len(datesSensorWaterLevel) - 1):
            year = int(datesSensorWaterLevel[i][0:4])
            month = int(datesSensorWaterLevel[i][5:7])
            day = int(datesSensorWaterLevel[i][8:10])
            hh = int(datesSensorWaterLevel[i][11:13])
            mm = int(datesSensorWaterLevel[i][14:16])
            dates.append(dt.datetime(year, month, day, hh, mm))
            waterLevel.append(sensorWaterLevel[i])

        datesSensorWaterLevel = dates
        sensorWaterLevel = waterLevel

        pairs = [list(a) for a in zip(datesSensorWaterLevel, sensorWaterLevel)]

        response = HttpResponse(content_type='text/csv')

        response['Content-Disposition'] = 'attachment; filename=real_time_H_sen_{0}.csv'.format(codEstacion)

        writer = csv_writer(response)

        writer.writerow(['datetime', 'water level (m)'])

        for row_data in pairs:
            writer.writerow(row_data)

        return response

    except Exception as e:
        print str(e)
        return JsonResponse({'error': 'No  data found for the station.'})

def download_historicSensorDataH(request):
    """
    Get data from hydroshare
    """

    get_data = request.GET

    try:
        codEstacion = get_data['stationcode']
        nomEstacion = get_data['stationname']
        resourceID = 'ceab9b8fccae452fac62d8d3ecbf8e78'

        auth = HydroShareAuthBasic(username='jorgessanchez7', password='Colombia03')
        hs = HydroShare(auth=auth)
        hs.setAccessRules(resourceID, public=True)

        url2 = 'https://www.hydroshare.org/resource/{0}/data/contents/H/sen/{1}_H_sen.csv'.format(resourceID,
                                                                                                  codEstacion)
        print(url2)

        response2 = urllib2.urlopen(url2)
        data = csv.reader(response2)
        data.next()

        dates = []
        data2 = []

        for row in data:
            date = row[0]
            date = dt.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            dates.append(date)
            value = row[1]
            data2.append(value)

        datesSensorWaterLevel = dates
        sensorWaterLevel = data2

        pairs = [list(a) for a in zip(datesSensorWaterLevel, sensorWaterLevel)]

        response = HttpResponse(content_type='text/csv')

        response['Content-Disposition'] = 'attachment; filename=historic_H_sen_{0}.csv'.format(codEstacion)

        writer = csv_writer(response)

        writer.writerow(['datetime', 'water level (m)'])

        for row_data in pairs:
            writer.writerow(row_data)

        options = {"flag": "make_private"}
        result = hs.resource(resourceID).flag(options)

        return response

    except Exception as e:
        print str(e)
        return JsonResponse({'error': 'No  data found for the station.'})

def get_realTimeObsDataQ(request):
    """
    Get data from fews stations
    """

    get_data = request.GET

    try:
        codEstacion = get_data['stationcode']
        nomEstacion = get_data['stationname']

        url2 = 'http://fews.ideam.gov.co/colombia/jsonQ/00' + codEstacion + 'Qobs.json'

        req2 = urllib2.Request(url2)
        opener2 = urllib2.build_opener()
        f2 = opener2.open(req2)
        data2 = json.loads(f2.read())

        obsDischarge = (data2.get('obs'))
        obsDischarge = (obsDischarge.get('data'))

        datesObsDischarge = [row[0] for row in obsDischarge]
        obsDischarge = [row[1] for row in obsDischarge]

        dates = []
        Discharge = []

        for i in range(0, len(datesObsDischarge) - 1):
            year = int(datesObsDischarge[i][0:4])
            month = int(datesObsDischarge[i][5:7])
            day = int(datesObsDischarge[i][8:10])
            hh = int(datesObsDischarge[i][11:13])
            mm = int(datesObsDischarge[i][14:16])
            dates.append(dt.datetime(year, month, day, hh, mm))
            Discharge.append(obsDischarge[i])

        datesObsDischarge = dates
        obsDischarge = Discharge

        obs_Q = go.Scatter(
            x=datesObsDischarge,
            y=obsDischarge,
            name='Sensor'
        )

        layout = go.Layout(title='Real Time Observed Discharge',
                           xaxis=dict(
                               title='Dates', ),
                           yaxis=dict(
                               title='Discharge (m<sup>3</sup>/s)',
                               autorange=True),
                           showlegend=False)

        chart_obj = PlotlyView(
            go.Figure(data=[obs_Q],
                      layout=layout)
        )

        context = {
            'gizmo_object': chart_obj,
        }

        return render(request, 'hydrologic_data_viewer_colombia/gizmo_ajax.html', context)

    except Exception as e:
        print str(e)
        return JsonResponse({'error': 'No  data found for the station.'})

def get_historicObsDataQ(request):
    """
    Get data from hydroshare
    """

    get_data = request.GET

    try:
        codEstacion = get_data['stationcode']
        nomEstacion = get_data['stationname']
        resourceID = 'ceab9b8fccae452fac62d8d3ecbf8e78'

        auth = HydroShareAuthBasic(username='jorgessanchez7', password='Colombia03')
        hs = HydroShare(auth=auth)
        hs.setAccessRules(resourceID, public=True)

        url2 = 'https://www.hydroshare.org/resource/{0}/data/contents/Q/obs/{1}_Q_obs.csv'.format(resourceID,
                                                                                                  codEstacion)
        print(url2)

        response2 = urllib2.urlopen(url2)
        data = csv.reader(response2)
        data.next()

        dates = []
        data2 = []

        for row in data:
            date = row[0]
            date = dt.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            dates.append(date)
            value = row[1]
            data2.append(value)

        datesObsDischarge = dates
        obsDischarge = data2

        obs_Q = go.Scatter(
            x=datesObsDischarge,
            y=obsDischarge,
            name='Sensor'
        )

        layout = go.Layout(title='Historic Observed Discharge',
                           xaxis=dict(
                               title='Dates', ),
                           yaxis=dict(
                               title='Discharge (m<sup>3</sup>/s)',
                               autorange=True),
                           showlegend=False)

        chart_obj = PlotlyView(
            go.Figure(data=[obs_Q],
                      layout=layout)
        )

        context = {
            'gizmo_object': chart_obj,
        }

        options = {"flag": "make_private"}
        result = hs.resource(resourceID).flag(options)

        return render(request, 'hydrologic_data_viewer_colombia/gizmo_ajax.html', context)

    except Exception as e:
        print str(e)
        return JsonResponse({'error': 'No  data found for the station.'})

def download_realTimeObsDataQ(request):
    """
    Get data from fews stations
    """

    get_data = request.GET

    try:
        codEstacion = get_data['stationcode']
        nomEstacion = get_data['stationname']

        url2 = 'http://fews.ideam.gov.co/colombia/jsonQ/00' + codEstacion + 'Qobs.json'

        req2 = urllib2.Request(url2)
        opener2 = urllib2.build_opener()
        f2 = opener2.open(req2)
        data2 = json.loads(f2.read())

        obsDischarge = (data2.get('obs'))
        obsDischarge = (obsDischarge.get('data'))

        datesObsDischarge = [row[0] for row in obsDischarge]
        obsDischarge = [row[1] for row in obsDischarge]

        dates = []
        Discharge = []

        for i in range(0, len(datesObsDischarge) - 1):
            year = int(datesObsDischarge[i][0:4])
            month = int(datesObsDischarge[i][5:7])
            day = int(datesObsDischarge[i][8:10])
            hh = int(datesObsDischarge[i][11:13])
            mm = int(datesObsDischarge[i][14:16])
            dates.append(dt.datetime(year, month, day, hh, mm))
            Discharge.append(obsDischarge[i])

        datesObsDischarge = dates
        obsDischarge = Discharge

        pairs = [list(a) for a in zip(datesObsDischarge, obsDischarge)]

        response = HttpResponse(content_type='text/csv')

        response['Content-Disposition'] = 'attachment; filename=real_time_Q_obs_{0}.csv'.format(codEstacion)

        writer = csv_writer(response)

        writer.writerow(['datetime', 'discharge (m3/s)'])

        for row_data in pairs:
            writer.writerow(row_data)

        return response

    except Exception as e:
        print str(e)
        return JsonResponse({'error': 'No  data found for the station.'})

def download_historicObsDataQ(request):
    """
    Get data from hydroshare
    """

    get_data = request.GET

    try:
        codEstacion = get_data['stationcode']
        nomEstacion = get_data['stationname']
        resourceID = 'ceab9b8fccae452fac62d8d3ecbf8e78'

        auth = HydroShareAuthBasic(username='jorgessanchez7', password='Colombia03')
        hs = HydroShare(auth=auth)
        hs.setAccessRules(resourceID, public=True)

        url2 = 'https://www.hydroshare.org/resource/{0}/data/contents/Q/obs/{1}_Q_obs.csv'.format(resourceID,
                                                                                                  codEstacion)
        print(url2)

        response2 = urllib2.urlopen(url2)
        data = csv.reader(response2)
        data.next()

        dates = []
        data2 = []

        for row in data:
            date = row[0]
            date = dt.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            dates.append(date)
            value = row[1]
            data2.append(value)

        datesObsDischarge = dates
        obsDischarge = data2

        pairs = [list(a) for a in zip(datesObsDischarge, obsDischarge)]

        response = HttpResponse(content_type='text/csv')

        response['Content-Disposition'] = 'attachment; filename=historic_Q_obs_{0}.csv'.format(codEstacion)

        writer = csv_writer(response)

        writer.writerow(['datetime', 'discharge (m3/s)'])

        for row_data in pairs:
            writer.writerow(row_data)

        options = {"flag": "make_private"}
        result = hs.resource(resourceID).flag(options)

        return response

    except Exception as e:
        print str(e)
        return JsonResponse({'error': 'No  data found for the station.'})

def get_realTimeSensorDataQ(request):
    """
    Get data from fews stations
    """

    get_data = request.GET

    try:
        codEstacion = get_data['stationcode']
        nomEstacion = get_data['stationname']

        url2 = 'http://fews.ideam.gov.co/colombia/jsonQ/00' + codEstacion + 'Qobs.json'

        req2 = urllib2.Request(url2)
        opener2 = urllib2.build_opener()
        f2 = opener2.open(req2)
        data2 = json.loads(f2.read())

        sensorDischarge = (data2.get('sen'))
        sensorDischarge = (sensorDischarge.get('data'))

        datesSensorDischarge = [row[0] for row in sensorDischarge]
        sensorDischarge = [row[1] for row in sensorDischarge]

        dates = []
        Discharge = []

        for i in range(0, len(datesSensorDischarge) - 1):
            year = int(datesSensorDischarge[i][0:4])
            month = int(datesSensorDischarge[i][5:7])
            day = int(datesSensorDischarge[i][8:10])
            hh = int(datesSensorDischarge[i][11:13])
            mm = int(datesSensorDischarge[i][14:16])
            dates.append(dt.datetime(year, month, day, hh, mm))
            Discharge.append(sensorDischarge[i])

        datesSensorDischarge = dates
        sensorDischarge = Discharge

        sensor_Q = go.Scatter(
            x=datesSensorDischarge,
            y=sensorDischarge,
            name='Sensor'
        )

        layout = go.Layout(title='Real Time Sensor Discharge',
                           xaxis=dict(
                               title='Dates', ),
                           yaxis=dict(
                               title='Discharge (m<sup>3</sup>/s)',
                               autorange=True),
                           showlegend=False)

        chart_obj = PlotlyView(
            go.Figure(data=[sensor_Q],
                      layout=layout)
        )

        context = {
            'gizmo_object': chart_obj,
        }

        return render(request, 'hydrologic_data_viewer_colombia/gizmo_ajax.html', context)

    except Exception as e:
        print str(e)
        return JsonResponse({'error': 'No  data found for the station.'})

def get_historicSensorDataQ(request):
    """
    Get data from hydroshare
    """

    get_data = request.GET

    try:
        codEstacion = get_data['stationcode']
        nomEstacion = get_data['stationname']
        resourceID = 'ceab9b8fccae452fac62d8d3ecbf8e78'

        auth = HydroShareAuthBasic(username='jorgessanchez7', password='Colombia03')
        hs = HydroShare(auth=auth)
        hs.setAccessRules(resourceID, public=True)

        url2 = 'https://www.hydroshare.org/resource/{0}/data/contents/Q/sen/{1}_Q_sen.csv'.format(resourceID,
                                                                                                  codEstacion)
        print(url2)

        response2 = urllib2.urlopen(url2)
        data = csv.reader(response2)
        data.next()

        dates = []
        data2 = []

        for row in data:
            date = row[0]
            date = dt.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            dates.append(date)
            value = row[1]
            data2.append(value)

        datesSensorDischarge = dates
        sensorDischarge = data2

        sensor_Q = go.Scatter(
            x=datesSensorDischarge,
            y=sensorDischarge,
            name='Sensor'
        )

        layout = go.Layout(title='Historic Sensor Discharge',
                           xaxis=dict(
                               title='Dates', ),
                           yaxis=dict(
                               title='Discharge (m<sup>3</sup>/s)',
                               autorange=True),
                           showlegend=False)

        chart_obj = PlotlyView(
            go.Figure(data=[sensor_Q],
                      layout=layout)
        )

        context = {
            'gizmo_object': chart_obj,
        }

        options = {"flag": "make_private"}
        result = hs.resource(resourceID).flag(options)

        return render(request, 'hydrologic_data_viewer_colombia/gizmo_ajax.html', context)

    except Exception as e:
        print str(e)
        return JsonResponse({'error': 'No  data found for the station.'})

def download_realTimeSensorDataQ(request):
    """
    Get data from fews stations
    """

    get_data = request.GET

    try:
        codEstacion = get_data['stationcode']
        nomEstacion = get_data['stationname']

        url2 = 'http://fews.ideam.gov.co/colombia/jsonQ/00' + codEstacion + 'Qobs.json'

        req2 = urllib2.Request(url2)
        opener2 = urllib2.build_opener()
        f2 = opener2.open(req2)
        data2 = json.loads(f2.read())

        sensorDischarge = (data2.get('sen'))
        sensorDischarge = (sensorDischarge.get('data'))

        datesSensorDischarge = [row[0] for row in sensorDischarge]
        sensorDischarge = [row[1] for row in sensorDischarge]

        dates = []
        Discharge = []

        for i in range(0, len(datesSensorDischarge) - 1):
            year = int(datesSensorDischarge[i][0:4])
            month = int(datesSensorDischarge[i][5:7])
            day = int(datesSensorDischarge[i][8:10])
            hh = int(datesSensorDischarge[i][11:13])
            mm = int(datesSensorDischarge[i][14:16])
            dates.append(dt.datetime(year, month, day, hh, mm))
            Discharge.append(sensorDischarge[i])

        datesSensorDischarge = dates
        sensorDischarge = Discharge

        pairs = [list(a) for a in zip(datesSensorDischarge, sensorDischarge)]

        response = HttpResponse(content_type='text/csv')

        response['Content-Disposition'] = 'attachment; filename=real_time_Q_sen_{0}.csv'.format(codEstacion)

        writer = csv_writer(response)

        writer.writerow(['datetime', 'discharge (m3/s)'])

        for row_data in pairs:
            writer.writerow(row_data)

        return response

    except Exception as e:
        print str(e)
        return JsonResponse({'error': 'No  data found for the station.'})

def download_historicSensorDataQ(request):
    """
    Get data from hydroshare
    """

    get_data = request.GET

    try:
        codEstacion = get_data['stationcode']
        nomEstacion = get_data['stationname']
        resourceID = 'ceab9b8fccae452fac62d8d3ecbf8e78'

        auth = HydroShareAuthBasic(username='jorgessanchez7', password='Colombia03')
        hs = HydroShare(auth=auth)
        hs.setAccessRules(resourceID, public=True)

        url2 = 'https://www.hydroshare.org/resource/{0}/data/contents/Q/sen/{1}_Q_sen.csv'.format(resourceID,
                                                                                                  codEstacion)
        print(url2)

        response2 = urllib2.urlopen(url2)
        data = csv.reader(response2)
        data.next()

        dates = []
        data2 = []

        for row in data:
            date = row[0]
            date = dt.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            dates.append(date)
            value = row[1]
            data2.append(value)

        datesSensorDischarge = dates
        sensorDischarge = data2

        pairs = [list(a) for a in zip(datesSensorDischarge, sensorDischarge)]

        response = HttpResponse(content_type='text/csv')

        response['Content-Disposition'] = 'attachment; filename=historic_Q_sen_{0}.csv'.format(codEstacion)

        writer = csv_writer(response)

        writer.writerow(['datetime', 'discharge (m3/s)'])

        for row_data in pairs:
            writer.writerow(row_data)

        options = {"flag": "make_private"}
        result = hs.resource(resourceID).flag(options)

        return response

    except Exception as e:
        print str(e)
        return JsonResponse({'error': 'No  data found for the station.'})

