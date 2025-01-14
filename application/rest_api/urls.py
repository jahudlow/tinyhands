from django.conf.urls import url

from dataentry.views import Address2ViewSet, Address1ViewSet, GeoCodeAddress1APIView, GeoCodeAddress2APIView, InterceptionRecordViewSet, VictimInterviewViewSet, IntercepteeViewSet, VictimInterviewDetailViewSet, PhotoExporter, IrfCsvExportView, VifCsvExportView, InterceptionAlertViewSet, PermissionViewSet, UserLocationPermissionViewSet
from dataentry.views import PersonViewSet, MasterPersonViewSet, PendingMatchViewSet
from dataentry.views import SiteSettingsViewSet, GoogleMapKeyViewSet
from dataentry.views import CountryViewSet
from dataentry.views import RegionViewSet
from dataentry.views import AuditViewSet, AuditSampleViewSet
from dataentry.views import IDManagementViewSet, TraffickerCheckViewSet, IrfFormViewSet, CifFormViewSet, VdfFormViewSet, GospelVerificationViewSet
from dataentry.views import FormViewSet, FormTypeViewSet
from dataentry.views import MonthlyReportFormViewSet
from dataentry.views import IndicatorsViewSet
from dataentry.views import BorderStationFormViewSet
from dataentry.views import StationStatisticsViewSet
from dataentry.views import LegalCaseFormViewSet
from dataentry.views import ClientDiagnosticViewSet
from help.views import VideoViewSet

list = {'get': 'list', 'post': 'create'}
detail = {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}

urlpatterns = [
    # Data Entry App
        # Addresses
        url(r'^address1/$', Address1ViewSet.as_view(list), name='Address1'),
        url(r'^address1/all/$', Address1ViewSet.as_view({'get': 'list_all'}), name='Address1all'),
        url(r'^address1/(?P<pk>\d+)/$', Address1ViewSet.as_view(detail), name='Address1detail'),
        url(r'^address1/(?P<pk>\d+)/related-items/$', Address1ViewSet.as_view({'get': 'related_items'}), name='Address1RelatedItems'),
        url(r'^address1/(?P<pk>\d+)/swap-with/(?P<pk2>\d+)/$', Address1ViewSet.as_view({'delete': 'swap_addresses'}), name='Address1RelatedItemsSwap'),

        url(r'^address2/$', Address2ViewSet.as_view(list), name='Address2'),
        url(r'^address2/(?P<pk>\d+)/$', Address2ViewSet.as_view(detail), name='Address2detail'),
        url(r'^address2/(?P<pk>\d+)/related-items/$', Address2ViewSet.as_view({'get': 'related_items'}), name='Address2RelatedItems'),
        url(r'^address2/(?P<pk>\d+)/swap-with/(?P<pk2>\d+)/$', Address2ViewSet.as_view({'delete': 'swap_addresses'}), name='Address2RelatedItemsSwap'),

        url(r'^address1/fuzzy/$', GeoCodeAddress1APIView.as_view(), name="Address1FuzzySearch"),
        url(r'^address2/fuzzy/$', GeoCodeAddress2APIView.as_view(), name="Address2FuzzySearch"),

        # IRFs
        url(r'^irf/$', InterceptionRecordViewSet.as_view(list), name="InterceptionRecord"),
        url(r'^irf/(?P<pk>\d+)/$', InterceptionRecordViewSet.as_view(detail), name="InterceptionRecordDetail"),
        url(r'^irf/export/$', IrfCsvExportView.as_view(), name="InterceptionRecordCsvExport"),

        # Interceptee
        url(r'^interceptee/$', IntercepteeViewSet.as_view(list), name="Interceptee"),
        url(r'^interceptee/(?P<pk>\d+)/$', IntercepteeViewSet.as_view(detail), name="IntercepteeDetail"),

        #SiteSettings
        url(r'^site-settings/$', SiteSettingsViewSet.as_view({'get': 'retrieve_custom'}), name="SiteSettings"),
        url(r'^site-settings/(?P<pk>\d+)/$', SiteSettingsViewSet.as_view({'put': 'update'}), name="SiteSettingsUpdate"),
        url(r'^site-settings/google_map_key/$', GoogleMapKeyViewSet.as_view({'get': 'retrieve_google_map_key'}), name="GoogleMapKey"),

        # VIFs
        url(r'^vif/$', VictimInterviewViewSet.as_view(list), name="VictimInterview"),
        url(r'^vif/(?P<pk>\d+)/$', VictimInterviewDetailViewSet.as_view(detail), name="VictimInterviewDetail"),
        url(r'^vif/export/$', VifCsvExportView.as_view(), name="VictimInterviewCsvExport"),

        #IRFBatch
        url(r'^photos/(?P<start_date>(\d+)-(\d+)-\d+)/(?P<end_date>\d+-\d+-\d+)/$', PhotoExporter.as_view({'get': 'export_photos'}), name="PhotoExporter"),
        url(r'^photos/(?P<start_date>(\d+)-(\d+)-\d+)/(?P<end_date>\d+-\d+-\d+)/count/$', PhotoExporter.as_view({'get': 'count_photos_in_date_range'}), name="PhotoExporterCount"),

        #Persons
        url(r'^person/$', PersonViewSet.as_view({'get': 'list'}), name="Person"),
        url(r'^person/associated/(?P<station_id>\d+)/(?P<form_number>\w+)/$', PersonViewSet.as_view({'get': 'associated_persons'}), name="AssociatedPersons"),
        
         url(r'^master-person/$', MasterPersonViewSet.as_view({'get': 'list'}), name="MasterPerson"),
         url(r'^master-person/(?P<pk>\d+)/$', MasterPersonViewSet.as_view(detail), name='MasterPersonDetail'),
         url(r'^master-person/type/(?P<type_name>[^/]+)/$', MasterPersonViewSet.as_view({'get':'retrieve_type'}), name='MasterPersonType'),
         url(r'^master-person/pv-relations/(?P<id>\d+)/$', MasterPersonViewSet.as_view({'get':'retrieve_pv_relations'}), name='MasterPersonRelations'),
         url(r'^master-person/remove/(?P<id>\d+)/(?P<person_id>\d+)/$', MasterPersonViewSet.as_view({'put':'remove_person'}), name='MasterPersonRemove'),
         url(r'^master-person/match/(?P<id>\d+)/(?P<type_id>\d+)/$', MasterPersonViewSet.as_view({'get':'retrieve_matches'}), name='MasterPersonMatch'),
         url(r'^master-person/update-match/(?P<id>\d+)/$', MasterPersonViewSet.as_view({'put':'update_match'}), name='MasterPersonUpdateMatch'),
         url(r'^master-person/create-match/$', MasterPersonViewSet.as_view({'put':'create_match'}), name='MasterPersonCreateMatch'),
         url(r'^master-person/merge/(?P<id1>\d+)/(?P<id2>\d+)/$', MasterPersonViewSet.as_view({'put':'merge_master_persons'}), name='MasterPersonMerge'),
         url(r'^pending-match/$', PendingMatchViewSet.as_view({'get': 'list'}), name='PendingMatch'),

        #KnownPersons
        url(r'^idmgmt/$', IDManagementViewSet.as_view({'get': 'list'}), name="IDManagement"),
        url(r'^idmgmt/fuzzy/$', TraffickerCheckViewSet.as_view({'get':'fuzzy_match'}), name="IDManagementFuzzy"),
        url(r'^idmgmt/phone/$', TraffickerCheckViewSet.as_view({'get':'partial_phone'}), name="IDManagementPhone"),
        url(r'^idmgmt/aperson/$', IDManagementViewSet.as_view({'get':'get_person'}), name="IDManagementPerson"),
        url(r'^idmgmt/forms/$', IDManagementViewSet.as_view({'get':'person_forms'}), name="IDManagementForms"),
        url(r'^idmgmt/group/$', IDManagementViewSet.as_view({'get':'alias_group'}), name="IDManagementGroup"),
        url(r'^idmgmt/(?P<pk>\d+)/addgroup/(?P<pk2>\d+)/$', IDManagementViewSet.as_view({'put':'add_alias_group'}), name="IDManagementAdd"),
        url(r'^idmgmt/(?P<pk>\d+)/removegroup/$', IDManagementViewSet.as_view({'put':'remove_alias_group'}), name="IDManagementRemove"),

        url(r'^region/$', RegionViewSet.as_view(list), name='Region'),
        #Countries
        url(r'^country/$', CountryViewSet.as_view(list), name='Country'),
        url(r'^country/(?P<pk>\d+)/$', CountryViewSet.as_view(detail), name='Countrydetail'),
        
       url(r'^intercept-alerts/$', InterceptionAlertViewSet.as_view({'get':'list'}), name='InterceptionAlert'), 
       
       url(r'^permission/$', PermissionViewSet.as_view({'get':'list'}), name='Permission'),
       url(r'^user_permission_list/$', UserLocationPermissionViewSet.as_view({'get':'user_permission_list'}), name='UserLocationPermissionList'),
       url(r'^user_permission/(?P<pk>\d+)/$', UserLocationPermissionViewSet.as_view({'get':'user_permissions', 'put':'update_permissions'}), name='UserLocationPermission'),
       url(r'^user_permission/countries/(?P<pk>\d+)/$', UserLocationPermissionViewSet.as_view({'get':'user_countries'}), name='UserPermissionCountries'),
       url(r'^user_permission/countries/current-user/$', UserLocationPermissionViewSet.as_view({'get':'user_countries_current_user'}), name='UserPermissionCountriesCurrent'),
        url(r'^user_permission/stations/(?P<pk>\d+)/$', UserLocationPermissionViewSet.as_view({'get':'user_stations'}), name='UserPermissionStations'),
        
        url(r'^irfNew/$', IrfFormViewSet.as_view(list), name='irfNew'),
        url(r'^irfNew/(?P<station_id>\d+)/(?P<pk>\d+)', IrfFormViewSet.as_view({'get': 'my_retrieve', 'put': 'update', 'delete': 'destroy'}), name='irfNewDetail'),
        url(r'^irfNew/blank/(?P<station_id>\d+)', IrfFormViewSet.as_view({'get': 'retrieve_blank_form'}), name='irfNewBlank'),
        url(r'^irfNew/tally/$', IrfFormViewSet.as_view({'get': 'tally'}), name='irfNewTally'),
        url(r'^irfNew/six-month-tally/$', IrfFormViewSet.as_view({'get': 'six_month_tally'}), name='sixMonthTally'),
        
        
        url(r'^forms/$', FormViewSet.as_view({'get':'list'}), name='forns'),
        url(r'^forms/config/(?P<form_name>\w+)/$', FormViewSet.as_view({'get':'form_config'}), name='formConfig'),
        url(r'^forms/types/$', FormTypeViewSet.as_view({'get':'list'}), name='fornTypes'),
        url(r'^forms/(?P<station_id>\d+)/station_forms/$', FormViewSet.as_view({'put':'set_forms'}), name='setForms'),
        url(r'^forms/related/(?P<station_id>\d+)/(?P<form_number>[^/]+)/$', FormViewSet.as_view({'get':'related_forms'}), name='relatedForms'),
        url(r'^forms/countries/(?P<form_id>\d+)/$', FormViewSet.as_view({'get':'get_form_countries'}), name='formCountries'),
        url(r'^forms/versions/(?P<form_id>\d+)/(?P<country_id>\d+)/$', FormViewSet.as_view({'get':'get_form_versions'}), name='formVersions'),
        
        
        url(r'^cif/$', CifFormViewSet.as_view(list), name='cif'),
        url(r'^cif/(?P<station_id>\d+)/(?P<pk>\d+)', CifFormViewSet.as_view({'get': 'my_retrieve', 'put': 'update', 'delete': 'destroy'}), name='cifDetail'),
        url(r'^cif/blank/(?P<station_id>\d+)', CifFormViewSet.as_view({'get': 'retrieve_blank_form'}), name='cifBlank'),
        
        url(r'^vdf/$', VdfFormViewSet.as_view(list), name='vdf'),
        url(r'^vdf/(?P<station_id>\d+)/(?P<pk>\d+)', VdfFormViewSet.as_view({'get': 'my_retrieve', 'put': 'update', 'delete': 'destroy'}), name='vdfDetail'),
        url(r'^vdf/blank/(?P<station_id>\d+)', VdfFormViewSet.as_view({'get': 'retrieve_blank_form'}), name='vdfBlank'),
        url(r'^gospel-verification/$', GospelVerificationViewSet.as_view({'get': 'list'}), name='gospelVerificationList'),
        url(r'^gospel-verification/(?P<station_id>\d+)/(?P<pk>\d+)/$', GospelVerificationViewSet.as_view({'get': 'my_retrieve', 'put': 'update'}), name='gospelVerificationDetail'),
        url(r'^gospel-vdf-update/(?P<pk>\d+)/$', GospelVerificationViewSet.as_view({'put': 'update_vdf_gospel'}), name='gospelVdfUpdate'),
        url(r'^gospel-verification/vdf-number/(?P<station_id>\d+)/(?P<form_number>[^/]+)/$', GospelVerificationViewSet.as_view({'get': 'retrieve_by_form_number'}), name='gospelVerificationFormNumber'),
        
        url(r'^monthly_report/$', MonthlyReportFormViewSet.as_view(list), name='monthlyReport'),
        url(r'^monthly_report/(?P<station_id>\d+)/(?P<pk>\d+)', MonthlyReportFormViewSet.as_view({'get': 'my_retrieve', 'put': 'update', 'delete': 'destroy'}), name='monthlyReportDetail'),
        url(r'^monthly_report/blank/(?P<station_id>\d+)', MonthlyReportFormViewSet.as_view({'get': 'retrieve_blank_form'}), name='monthlyReportBlank'),
        url(r'^monthly_report/summary/(?P<country_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/$', MonthlyReportFormViewSet.as_view({'get': 'summary'}), name='monthlyReportSummary'),
        
        url(r'^indicators/(?P<country_id>\d+)$', IndicatorsViewSet.as_view({'get': 'calculate_indicators'}), name='indicators'),
        url(r'^collection_indicators/(?P<country_id>\d+)/$', IndicatorsViewSet.as_view({'get': 'get_collection_indicators'}), name='collectionIndicators'),
        
        url(r'help/video/$', VideoViewSet.as_view({'get':'list'}), name='helpVideo'),
        
        url(r'^border_station/$', BorderStationFormViewSet.as_view({'post': 'create'}), name="borderStation"),
        url(r'^border_station/(?P<pk>\d+)/$', BorderStationFormViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name="borderStationForm"),
        url(r'^border_station/blank/', BorderStationFormViewSet.as_view({'get': 'retrieve_blank'}), name='borderStationBlank'),
        url(r'^border_station/category/', BorderStationFormViewSet.as_view({'get': 'get_project_categories'}), name='borderStationCategory'),
        
        url(r'^operations-dashboard/(?P<country_id>\d+)/$', StationStatisticsViewSet.as_view({'get': 'retrieve_dashboard'}), name='retrieveDashboard'),
        url(r'^station-data/country/(?P<country_id>\d+)/(?P<year_month>\d+)/$', StationStatisticsViewSet.as_view({'get': 'retrieve_country_data'}), name='retrieveCountryOperations'),
        url(r'^station-data/country/$', StationStatisticsViewSet.as_view({'put': 'update_station_data'}), name='setCountryOperations'),
        url(r'^location-staff/(?P<station_id>\d+)/(?P<year_month>\d+)/$', StationStatisticsViewSet.as_view({'get': 'retrieve_location_staff'}), name='retrieveLocationStaff'),
        url(r'^location-staff/$', StationStatisticsViewSet.as_view({'put': 'update_location_staff'}), name='setLocationStaff'),
        url(r'^location-statistics/(?P<station_id>\d+)/(?P<year_month>\d+)/$', StationStatisticsViewSet.as_view({'get': 'retrieve_location_statistics'}), name='retrieveLocationStatistics'),
        url(r'^location-statistics/$', StationStatisticsViewSet.as_view({'put': 'update_location_statistics'}), name='setLocationStatistics'),
        url(r'^exchange-rate/(?P<country_id>\d+)/(?P<year_month>\d+)/$', StationStatisticsViewSet.as_view({'get': 'get_exchange_rate'}), name='getExchangeRate'),
        url(r'^exchange-rate/$', StationStatisticsViewSet.as_view({'put': 'update_exchange_rate'}), name='updateExchangeRate'),
        
        #Audits
        url(r'^audit/$', AuditViewSet.as_view(list), name='Audit'),
        url(r'^audit/(?P<pk>\d+)/$', AuditViewSet.as_view(detail), name='Auditdetail'),
        url(r'^audit/sample-size/$', AuditViewSet.as_view({'get':'sample_size'}), name='Auditdetail'),
        url(r'^audit-notes/(?P<pk>\d+)/$', AuditViewSet.as_view({'put':'update_notes'}), name='AuditNotes'),
        url(r'^audit-sample/$', AuditSampleViewSet.as_view(list), name='Audit'),
        url(r'^audit-sample/(?P<pk>\d+)/$', AuditSampleViewSet.as_view(detail), name='Auditdetail'),

        url(r'^legal-case/$', LegalCaseFormViewSet.as_view(list), name='legalCase'),
        url(r'^legal-case/(?P<station_id>\d+)/(?P<pk>\d+)', LegalCaseFormViewSet.as_view({'get': 'my_retrieve', 'put': 'update', 'delete': 'destroy'}), name='legalCaseDetail'),
        url(r'^legal-case/blank/(?P<station_id>\d+)', LegalCaseFormViewSet.as_view({'get': 'retrieve_blank_form'}), name='legalCaseBlank'),
        
         url(r'^diagnostic/$', ClientDiagnosticViewSet.as_view(list), name='Diagnostic'),
]
