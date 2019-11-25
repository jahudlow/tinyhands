from django.core.management.base import BaseCommand
import httplib2
from oauth2client.client import GoogleCredentials
from apiclient import discovery
import traceback

from export_import.google_sheet_basic import GoogleSheetBasic

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            
            credentials =  GoogleCredentials.get_application_default()
            credentials = credentials.create_scoped(GoogleSheetBasic.scope)
            http = credentials.authorize(httplib2.Http())      
        except:
            print ('Unable to get credentials: ', traceback.format_exc())
            return
            
        drive_service = discovery.build('drive', 'v3', http=http)
        results = drive_service.files().list().execute()
        items = results.get('files', [])
        if items:
            for item in items:
                print (item['name'])
        else:
            print ('No Files found')