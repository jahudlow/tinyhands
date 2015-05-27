'use strict';

var c = require('../testConstants.json');

var irfPage = function() {
    var page = this;
    
    this.getToIRF = function(){
	    browser.get(c.webAddress + '/data-entry/irfs/search/');
        this.link = element(by.id("id_input_new_irf"));
        return this.link.click();
    };

    this.fillOutIRF = function(date) {
        var today = date || c.irfInterceptTime;
        browser.executeScript("arguments[0].style.visibility = 'hidden';", element(by.id("footer")).getWebElement()); // Hides the footer so the webdriver can click on stuff
        this.irf_number = element(by.id("id_irf_number")).sendKeys(c.irfNumber);
        this.location = element(by.id("id_location")).sendKeys(c.irfLocation);
        this.date_time_of_interception = element(by.id("id_date_time_of_interception")).sendKeys(today);
        this.staff_name = element(by.id("id_staff_name")).sendKeys(c.irfStaffName);
        this.drugged_or_drowsy = element(by.id("id_drugged_or_drowsy")).click();
        this.contact_noticed = element(by.id("id_contact_noticed")).click();

        this.which_contact_hotel_owner = element(by.id("id_which_contact_hotel_owner")).click();
        this.victSelect = element(by.cssContainingText('option', 'Victim')).click();
        this.intercepteesfname = element(by.id("id_interceptees-0-full_name")).sendKeys(c.irfInterceptFname);
        this.genderSelect = element(by.cssContainingText('option', 'F')).click();
        this.districtSelect = element(by.id("id_interceptees-0-district")).sendKeys(c.irfInterceptDistrict);
        this.vdcSelect = element(by.id("id_interceptees-0-vdc")).sendKeys(c.irfInterceptVdc);
        this.how_sure_was_trafficking = element(by.cssContainingText('option', 'Absolutely sure')).click();
        this.interception_type_india_trafficking = element(by.id("id_interception_type_india_trafficking")).click();
        this.call_subcommittee_chair = element(by.id("id_call_subcommittee_chair")).click();
        this.call_thn_to_cross_check = element(by.id("id_call_thn_to_cross_check")).click();
        this.name_came_up_before_1 = element(by.id("id_name_came_up_before_1")).click();
        this.name_came_up_before_value = element(by.id("id_name_came_up_before_value")).sendKeys(c.irfNameCameUpBeforeValue);
        this.scan_and_submit_same_day = element(by.id("id_scan_and_submit_same_day")).click();
        this.has_signature = element(by.id("id_has_signature")).click();
        browser.executeScript("arguments[0].style.visibility = '';", element(by.id("footer")).getWebElement()); // Hides the footer so the webdriver can click on stuff
        this.submit = element(by.id("submtButton")).click();

    };

    this.viewIRF = function() {
        this.vIRF = element(by.linkText('View')).click();
    };

    this.editIRF = function() {
        browser.executeScript("arguments[0].style.visibility = 'hidden';", element(by.id("footer")).getWebElement()); // Hides the footer so the webdriver can click on stuff
        this.eIRF = element(by.linkText('Edit')).click();
        this.irf_number = element(by.id("id_irf_number")).clear();
        this.irf_number = element(by.id("id_irf_number")).sendKeys(c.irfEditNumber);
        this.submit = element(by.id("submtButton")).click();
    };

    this.deleteIRF = function() {
        this.dIRF = element(by.linkText('Delete')).click();
        this.dIRFpopUp = element(by.linkText('Delete')).click();
    };
};

module.exports = new irfPage();