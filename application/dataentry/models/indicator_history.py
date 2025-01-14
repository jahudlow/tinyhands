import datetime
import os
import pytz

from django.db import models
from django.db.models import Q
from django.conf import settings
from django.contrib.postgres.fields import JSONField

from .border_station import BorderStation
from .country import Country

from dataentry.models import BorderStation, Form, FormCategory, IntercepteeCommon

class IndicatorHistory(models.Model):
    country = models.ForeignKey(Country)
    year = models.PositiveIntegerField('Year')
    month = models.PositiveIntegerField('Month')
    indicators = JSONField()
    
    @staticmethod
    def work_days (start_date, end_date):
        days_offset = [
                [0,1,2,3,4,4,4],
                [0,1,2,3,3,3,4],
                [0,1,2,2,2,3,4],
                [0,1,1,1,2,3,4],
                [0,0,0,1,2,3,4],
                [0,0,0,1,2,3,4],
                [0,0,1,2,3,4,4]
            ]
        
        if end_date <= start_date:
            return 0
        
        days = (end_date - start_date).days
        weeks = int(days/7)
        partial = days - weeks * 7
        work_days = weeks * 5 + days_offset[start_date.weekday()][partial]
        
        return work_days
    
    @staticmethod
    def add_result(result, name, value):
        if name in result:
            if value != '-':
                if result[name] != '-':
                    result[name] = result[name] + value
                else:
                    result[name] = value
        else:
            result[name] = value
    
    @staticmethod
    def calculate_indicators(start_date, end_date, country, check_photos=None, include_latest_date = False):
        if country.verification_start_year is None or country.verification_start_month is None:
            start_validation_date = None
        else:
            start_validation_date = datetime.date(country.verification_start_year,country.verification_start_month,1)
        station_list = BorderStation.objects.filter(operating_country=country)
        results = {}
        
        form_method = {
            'IRF':IndicatorHistory.calculate_irf_indicators,
            'CIF':IndicatorHistory.calculate_cif_indicators,
            'VDF':IndicatorHistory.calculate_vdf_indicators,
            }
        
        if check_photos is None:
            check_photos = IndicatorHistory.get_modified_photos(start_date, end_date)
               
        forms_processed = []
        class_cache = {
                'IRF':{},
                'CIF':{},
                'VDF':{}
                }
        
        storage_cache = {
                'IRF_People':{},
                }
        
        latest_date = None
        
        # general form information
        for form_type in ['IRF','CIF','VDF']:
            for station in station_list:
                form_class = IndicatorHistory.get_class(class_cache, form_type, station)
                if form_class is None or form_class in forms_processed:
                    # If there is no form for this station or we have already processed the form
                    # associated with this station, then skip to the next station
                    continue;
                
                query_set = form_class.objects.filter(station__in=station_list,
                                        logbook_submitted__gte=start_date, logbook_submitted__lte=end_date)
                form_method[form_type](results, query_set, start_date, end_date, class_cache, form_type)
                
                if form_type == 'IRF':
                    query_set = form_class.objects.filter(station__in=station_list,
                                        logbook_first_verification_date__gte=start_date,
                                        logbook_first_verification_date__lte=end_date)
                    IndicatorHistory.calculate_irf_first_verification(results, query_set, start_date, end_date)
                    
                    if start_validation_date is not None:
                        query_set = form_class.objects.filter(station__in=station_list,
                                                              logbook_submitted__gte=start_validation_date,
                                                              logbook_submitted__lte=end_date,
                                                              evidence_categorization__isnull=False).exclude(logbook_first_verification_date__lte=end_date)
                        IndicatorHistory.calculate_irf_backlog(results, query_set, 'v1')
                    
                    query_set = form_class.objects.filter(station__in=station_list,
                                        logbook_second_verification_date__gte=start_date,
                                        logbook_second_verification_date__lte=end_date)
                    IndicatorHistory.calculate_irf_second_verification(results, query_set, start_date, end_date)
                    
                    if start_validation_date is not None:
                        query_set = form_class.objects.filter(station__in=station_list,
                                                              logbook_first_verification_date__gte=start_validation_date,
                                                              logbook_first_verification_date__lte=end_date,
                                                              evidence_categorization__isnull=False).exclude(logbook_second_verification_date__lte=end_date)
                        IndicatorHistory.calculate_irf_backlog(results, query_set, 'v2')
                    
                    interceptee_storage = IndicatorHistory.get_card_storage(storage_cache, form_type, 'People', station)
                    if interceptee_storage is not None:
                        query_set = interceptee_storage.get_form_storage_class().objects.filter(interception_record__station__in=station_list, person__photo__in=check_photos.keys())
                        IndicatorHistory.process_photos(results, query_set, check_photos, start_date, end_date)
                    
                if include_latest_date:
                    query_set = form_class.objects.filter(station__in=station_list).exclude(logbook_submitted__isnull=True).order_by("-logbook_submitted")[:1]
                    if len(query_set) > 0:
                        if latest_date is None:
                            latest_date = query_set[0].logbook_submitted
                        elif latest_date < query_set[0].logbook_submitted:
                            latest_date = query_set[0].logbook_submitted
                    
                forms_processed.append(form_class)
        
        for prefix in ['irf','vdf', 'cif', 'photos', 'v1', 'v2']:
            IndicatorHistory.compute_lag(results, prefix)
            
            if prefix + 'Count' in results and prefix + 'OriginalFormCount' in results:
                if  results[prefix + 'Count'] > 0:
                    results[prefix + 'OriginalFormPercent'] = round(results[prefix + 'OriginalFormCount'] * 100 / results [prefix + 'Count'],2)
                else:
                    results[prefix + 'OriginalFormPercent'] = '-'
        
        if include_latest_date:
            if latest_date is None:
                results['latestDate'] = ''
            else:
                results['latestDate'] = str(latest_date)

        return results
    
    @staticmethod
    def date_in_range (the_date, start_date, end_date):
         if the_date is None:
             return False
         
         if start_date is not None and the_date < start_date:
             return False
         
         if end_date is not None and the_date > end_date:
             return False
         
         return True

    @staticmethod
    def get_class(class_cache, type, station):
        if station in class_cache[type]:
            the_class = class_cache[type][station]
        else:
            form = Form.current_form(type, station.id)
            if form is None:
                the_class = None
            else:
                the_class = form.storage.get_form_storage_class()

            class_cache[type][station] = the_class
        
        return the_class
    
    @staticmethod
    def get_card_storage(storage_cache, form_type, form_category_name, station):
        type = form_type + "_" + form_category_name
        if station in storage_cache[type]:
            the_storage = storage_cache[type][station]
        else:
            form = Form.current_form(form_type, station.id)
            form_categories = FormCategory.objects.filter(form=form, name=form_category_name)
            if len(form_categories) == 1 and form_categories[0].storage is not None:
                the_storage = form_categories[0].storage
            else:
                the_storage = None

            storage_cache[type][station] = the_storage
            
        return the_storage
    
    @staticmethod
    def compute_lag(results, prefix):
        if prefix + 'Count' in results and prefix + 'TotalLag' in results:
            count = results[prefix + 'Count']
            total = results[prefix + 'TotalLag']
            if count > 0:
                results[prefix + 'Lag'] =  round(total/count,2)
            else:
                results[prefix + 'Lag'] = '-'

    @staticmethod
    def calculate_irf_first_verification(results, query_set, start_date, end_date):
        lag_time = 0
        lag_count = 0
        victim_count = 0
        
        for irf in query_set:
            if IndicatorHistory.date_in_range(irf.logbook_submitted, None, None):
                lag_count += 1
                lag_time += IndicatorHistory.work_days(irf.logbook_submitted, irf.logbook_first_verification_date)
                victim_count += IntercepteeCommon.objects.filter(interception_record=irf, person__role='PVOT').count()
        
        IndicatorHistory.add_result(results, 'v1TotalLag', lag_time)
        IndicatorHistory.add_result(results, 'v1Count', lag_count)
        IndicatorHistory.add_result(results, 'v1VictimCount', victim_count)

    @staticmethod
    def calculate_irf_backlog(results, query_set, prefix):
        IndicatorHistory.add_result(results, prefix + 'Backlog', len(query_set))
    
    @staticmethod
    def calculate_irf_second_verification(results, query_set, start_date, end_date):
        lag_time = 0
        lag_count = 0
        victim_count = 0
        change_count = 0
        
        for irf in query_set:
            if IndicatorHistory.date_in_range(irf.logbook_first_verification_date, None, None):
                lag_count += 1
                lag_time += IndicatorHistory.work_days(irf.logbook_first_verification_date, irf.logbook_second_verification_date)
                victim_count += IntercepteeCommon.objects.filter(interception_record=irf, person__role='PVOT').count()
                if irf.logbook_first_verification != irf.logbook_second_verification:
                    change_count += 1
        
        IndicatorHistory.add_result(results, 'v2TotalLag', lag_time)
        IndicatorHistory.add_result(results, 'v2Count', lag_count)
        IndicatorHistory.add_result(results, 'v2VictimCount', victim_count)
        IndicatorHistory.add_result(results, 'v2ChangeCount', change_count)
     
    @staticmethod
    def calculate_form_indicators (results, query_set, form_type):
        storage_cache = {
                form_type + '_Attachments':{},
                }
        submitted_count = 0
        total_lag = 0
        interceptee_count = 0
        interceptee_photo_count = 0
        original_form_attached_count = 0
        
        for entry in query_set:
            submitted_count += 1
            
            if IndicatorHistory.date_in_range(entry.logbook_information_complete, None, None):
                start_date = entry.logbook_information_complete
            elif IndicatorHistory.date_in_range(entry.logbook_received, None, None):
                start_date = entry.logbook_received
            else:
                start_date = entry.date_time_entered_into_system.date()
            
            total_lag += IndicatorHistory.work_days(start_date, entry.logbook_submitted)
            storage = IndicatorHistory.get_card_storage(storage_cache, form_type, 'Attachments', entry.station)
            if storage is not None:
                orig_attachments = storage.get_form_storage_class().objects.filter(Q((storage.foreign_key_field_parent,entry)) & Q(('option','Original Form')))
                if len(orig_attachments) > 0:
                    original_form_attached_count += 1
            
        
        IndicatorHistory.add_result(results, form_type.lower() + 'Count', submitted_count)
        IndicatorHistory.add_result(results, form_type.lower() + 'TotalLag', total_lag)
        IndicatorHistory.add_result(results, form_type.lower() + 'OriginalFormCount', original_form_attached_count)
    
    @staticmethod
    def calculate_irf_indicators(results, query_set, start_date, end_date, class_cache, form_type):
        IndicatorHistory.calculate_form_indicators(results, query_set, form_type)
    
    @staticmethod
    def calculate_vdf_indicators(results, query_set, start_date, end_date, class_cache, form_type):
        IndicatorHistory.calculate_form_indicators(results, query_set, form_type)
    
    @staticmethod
    def calculate_cif_indicators(results, query_set, start_date, end_date, class_cache, form_type):
        IndicatorHistory.calculate_form_indicators(results, query_set, form_type)
    
    @staticmethod
    def get_modified_photos(start_date, end_date):
        # file dates are stored in UTC, but we want to filter based on the station's time zone
        # so start with a rough time range and then filter better after we determine the station's
        # time zone.
        one_day = datetime.timedelta(1)
        rough_start_date = start_date - one_day
        rough_end_date = end_date + one_day
        
        check_photos = {}
        for entry in os.scandir(settings.MEDIA_ROOT + '/interceptee_photos/'):
            stat_object = entry.stat ( )
            modification_time = datetime.datetime.fromtimestamp(stat_object.st_mtime)
            if modification_time.date() >= rough_start_date and modification_time.date() <= rough_end_date:
                check_photos['interceptee_photos/' + entry.name] = modification_time
                
        return check_photos
    
    @staticmethod
    def process_photos(results, query_set, check_photos, start_date, end_date):
        photos_uploaded = 0
        photo_lag_total = 0
        
        for interceptee in query_set:
            irf = interceptee.interception_record
            time_zone = pytz.timezone(irf.station.time_zone)
            modification_time = check_photos[interceptee.person.photo]
            local_date = modification_time.astimezone(time_zone).date()
            if local_date >= start_date and local_date <= end_date:
                photos_uploaded += 1
                if IndicatorHistory.date_in_range(irf.logbook_information_complete, None, None):
                    base_date = irf.logbook_information_complete
                elif IndicatorHistory.date_in_range(irf.logbook_received, None, None):
                    base_date = irf.logbook_received
                else:
                    base_date = irf.date_time_entered_into_system.astimezone(time_zone).date()
                
                photo_lag_total += IndicatorHistory.work_days(base_date, local_date)
            
        IndicatorHistory.add_result(results, 'photosCount', photos_uploaded)
        IndicatorHistory.add_result(results, 'photosTotalLag', photo_lag_total)
            
        