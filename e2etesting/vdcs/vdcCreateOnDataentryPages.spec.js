var constants = require('../testConstants.json');
var loginPage = require('../accounts/loginPage.js');
var helper = require('./vdcCreateOnDataentryPages.js');

describe('TinyHands dataentry pages', function () {
    beforeEach(function () {
        return browser.ignoreSynchronization = true;
    });

    it('should have VDC create modal above any error tooltips on IRF pages', function () {
        loginPage.logout();
        loginPage.loginAsAdmin();
        helper.navigate('irfs');
        helper.submitIrfsWithErrors();
        helper.createNewVDC();
        expect(element(vdc tooltip error).click().toFail())
    });

    // TODO: -JS- Maybe just do it through here instead??
    it('should be able to create a new VDC through the vif:', function(){
        browser.get(constants.webAddress + '/data-entry/vifs/create/');
        this.victim_address_vdc = element(by.id("id_victim_address_vdc")).click();
        vdcAdminPage.createNewVDC();
        browser.sleep(500);
        vdcAdminPage.navigate();
        expect(element(by.css(".vdc_admin_name")).getText()).toBe(constants.vdcNewName);
        expect(element.all(by.css(".vdc_admin_district")).first().getText()).toEqual(constants.vdcNewDis);
        expect(element.all(by.css(".vdc_admin_cannonical")).first().getText()).toEqual(constants.vdcNewCan);
    });

//     it('should change the first VDCs information', function () {
//         vdcAdminPage.findItemsOnPage();
//         browser.sleep(500);
//
//         vdcAdminPage.firstVdcEditButton.click();
//         browser.sleep(500);
//
//         vdcAdminPage.changeValues();
//         browser.get(constants.webAddress);
//         vdcAdminPage.navigate();
//         browser.sleep(2000);
//         expect(element(by.css(".vdc_admin_name")).getText()).toBe(constants.vdcEditName);
//         expect(element.all(by.css(".vdc_admin_district")).first().getText()).toEqual(constants.vdcEditDis);
//         expect(element.all(by.css(".vdc_admin_cannonical")).first().getText()).toEqual(constants.vdcEditCan);
//         browser.sleep(500);
//     });
//
//     it('should be able to create a new VDC through the vif:', function(){
//         browser.get(constants.webAddress + '/data-entry/vifs/create/');
//         this.victim_address_vdc = element(by.id("id_victim_address_vdc")).click();
//         vdcAdminPage.createNewVDC();
//         browser.sleep(500);
//         vdcAdminPage.navigate();
//         expect(element(by.css(".vdc_admin_name")).getText()).toBe(constants.vdcNewName);
//         expect(element.all(by.css(".vdc_admin_district")).first().getText()).toEqual(constants.vdcNewDis);
//         expect(element.all(by.css(".vdc_admin_cannonical")).first().getText()).toEqual(constants.vdcNewCan);
//     });
//
});