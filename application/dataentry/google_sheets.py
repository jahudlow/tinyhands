from oauth2client.client import GoogleCredentials
from gdata.gauth import OAuth2TokenFromCredentials
from gdata.spreadsheets.client import SpreadsheetsClient
from gdata.spreadsheets.client import ListQuery
from gdata.spreadsheets.data import ListEntry
from multiprocessing import Queue
from threading import Thread

import re
import os
import traceback
import smtplib
import string


from models import (InterceptionRecord, VictimInterview)
from csv_io import get_irf_export_rows
from django.conf import settings
from csv_io import get_vif_export_rows


    

class GoogleSheetClientThread (Thread):

    scope=( "https://www.googleapis.com/auth/drive",
            "https://spreadsheets.google.com/feeds",
            "https://docs.google.com/feeds"
        )
    
    work_queue = None
    
    queue_enabled = None
    token = None
    client = None
    spreadsheet_key = None
    
    def get_token(self):
        if os.path.isfile("google_cred.json"):
            self.have_credentials = True
            credentials = GoogleCredentials.from_stream("google_cred.json")
            credentials = credentials.create_scoped(self.scope)
            self.token = OAuth2TokenFromCredentials(credentials)
        else:
            self.have_credentials = False
            print "No credentials file for google spreadsheet.  No update to google spreadsheets will be attempted."
    
    def get_client(self):
        self.client = SpreadsheetsClient()
        self.client = self.token.authorize(self.client)
    
    def find_spreadsheet_by_name(self, name):
        spreadsheets = self.client.get_spreadsheets()
        for spreadsheet in spreadsheets.entry:
            if (name == spreadsheet.title.text):
                return spreadsheet.id.text.rsplit('/',1)[1]
    
        print "Spreadsheet with the name " + name + " not found"
        return None
    
    def find_worksheet_by_name(self, name):
        if self.spreadsheet_key is not None:
            worksheets = self.client.get_worksheets(self.spreadsheet_key);
            for worksheet in worksheets.entry:
                if (name == worksheet.title.text):
                    return worksheet.id.text.rsplit('/',1)[1]
    
        print "Worksheet with the name " + name + " not found"
        return None
    
    def spreadsheet_header_from_export_header(self, hdr):
        hdr = hdr.lower()
        hdr = re.sub("[^a-z0-9\.\-]*","", hdr)
        hdr = re.sub("^[0-9\.\-]*","", hdr)
        return hdr
    
    def reinitialize(self): 
        self.token = None   
        self.get_token()
        if self.token is not None:
            self.get_client()
            self.spreadsheet_key = self.find_spreadsheet_by_name(settings.SPREADSHEET_NAME)
            self.irf_worksheet_key = self.find_worksheet_by_name(settings.IRF_WORKSHEET_NAME)
            self.vif_worksheet_key = self.find_worksheet_by_name(settings.VIF_WORKSHEET_NAME)
        else:
            print "Unable to get token"
        
    def __init__(self):
        Thread.__init__(self)
        self.reinitialize()
        if self.have_credentials:
            self.work_queue = Queue()
            self.start()
        
    def run(self):
        while True:
            work = self.work_queue.get()
            print "in run " + work[0] + ", " + work[1]
            try:
                if work[0] == 'IRF':
                    self.internal_update_irf(work[1])
                elif work[0] == 'VIF':
                    self.internal_update_vif(work[1])
                else:
                    print "Unknown work type " + work[0]
            except:
                print "Failed to process " + work[0] + " " + work[1] + " on attempt " + str(work[2])
                self.reinitialize();
                work[2] = work[2] + 1
                if work[2] < 2:
                    print "GoogleSheetClientThread.run Failed to process " + work[0] + " " + work[1] + " on attempt " + str(work[2]) + " - retrying"
                    self.work_queue.put(work);
                else:
                    print "GoogleSheetClientThread.run Failed to process " + work[0] + " " + work[1] + " on attempt " + str(work[2]) + " - giving up" 
                    self.send_exception_mail(traceback.format_exc())
    
    def build_list_entry(self, header_row, data_row):
        list_entry = ListEntry()
        for col_idx in range(0, len(data_row)):
            col_header = self.spreadsheet_header_from_export_header(header_row[col_idx])
            list_entry.set_value(col_header, str(data_row[col_idx]))
            
        return list_entry
    
        
    def update_sheet (self, worksheet_key, new_rows):
        if (len(new_rows) < 2):
            return
        
        key_name = self.spreadsheet_header_from_export_header(new_rows[0][0])
        key_value = str(new_rows[1][0])
        #print key_name + "==" + key_value
        
        feed = self.client.get_list_feed(self.spreadsheet_key, worksheet_key, query=ListQuery(sq=key_name + "==" + key_value))
        for idx in range(len(feed.entry)-1, -1, -1):
            self.client.delete(feed.entry[idx])
        
        for row_idx in range(1, len(new_rows)):
            list_entry = self.build_list_entry(new_rows[0], new_rows[row_idx])
            self.client.add_list_entry(list_entry, self.spreadsheet_key, worksheet_key)          
            
    def update_irf(self, the_irf_number):
        #print "in update_irf " + the_irf_number
        if self.have_credentials:
            work = ['IRF', the_irf_number, 0]
            self.work_queue.put(work)
        
    def update_vif(self, the_vif_number):
        #print "in update_vif " + the_vif_number
        if self.have_credentials:
            work = ['VIF', the_vif_number, 0]
            self.work_queue.put(work)
        
    def internal_update_irf(self, the_irf_number):
        #print "in internal_update_irf " + the_irf_number
        irf = InterceptionRecord.objects.get(irf_number = the_irf_number)
        if irf is None:
            print "Could not find IRF " + the_irf_number
            return
        irfs = [irf]
        new_rows = get_irf_export_rows(irfs)
        self.update_sheet(self.irf_worksheet_key, new_rows)
        
    def internal_update_vif(self, the_vif_number):
        #print "in internal_update_vif " + the_vif_number
        vif = VictimInterview.objects.get(vif_number = the_vif_number)
        if vif is None:
            print "Could not find VIF " + the_vif_number
            return
        vifs = [vif]
        new_rows = get_vif_export_rows(vifs)
        self.update_sheet(self.vif_worksheet_key, new_rows)
        
    def send_exception_mail(self, exception_text):
        try:
            to = []
            for idx in range(0,len(settings.ADMINS)):
                to.append(settings.ADMINS[idx][1])
            
            if len(to) < 1:
                # There are no admins defined
                return
                
            frm = settings.DEFAULT_FROM_EMAIL
            body = string.join((
                    "From: %s" % frm,
                    "To: %s" % ", ".join(to),
                    "Subject: %s" % "Exception sending updates to Google Sheets",
                    "",
                    exception_text
                    ), "\r\n")
            print body
            server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.sendmail(frm, to, body)
            server.quit()
        except:
            traceback.print_exc()
        
google_sheet_client = GoogleSheetClientThread()