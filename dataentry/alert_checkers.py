from accounts.models import Alert


class VIFAlertChecker(object):
    def __init__(self, form, inlines):
        self.vif = form
        self.inlines = inlines

    def check_them(self):
        self.fir_and_dofe_against()
        self.ten_or_more_case_points()

    def fir_and_dofe_against(self):
        """
        - Any time a VIF is submitted with the box checked for "FIR filed against __" or for "DoFE complaint against __" on question 8.1. E-mail should
        include VIF number, which type of case has been filed and the name of the person it has been filed against.
        """
        fir = self.vif.cleaned_data.get("legal_action_against_traffickers_fir_filed")
        fir_value = self.vif.cleaned_data.get("legal_action_fir_against_value")
        dofe = self.vif.cleaned_data.get("legal_action_against_traffickers_dofe_complaint")
        dofe_value = self.vif.cleaned_data.get("legal_action_dofe_against_value")
        points = self.vif.instance.calculate_strength_of_case_points()

        if (fir and fir_value != '') and (dofe and dofe_value != ''):
            Alert.alert_objects.send_alert("fir and dofe against", context={"vif": self.vif.instance, "both": True, "points": points, "fir_value": fir_value, "dofe_value": dofe_value})
        if fir and fir_value != '':
            Alert.alert_objects.send_alert("fir and dofe against", context={"vif": self.vif.instance, "fir": True, "fir_value": fir_value, "points": points})
        if dofe and dofe_value != '':
            Alert.alert_objects.send_alert("fir and dofe against", context={"vif": self.vif.instance, "dofe": True, "points": points, "dofe_value": dofe_value})

    def ten_or_more_case_points(self):
        """
        Any time there are 10 or more Strength of Case points. E-mail should include VIF number, the number of SoC
        points and whether or not a legal case has been filed.
        """
        fir = self.vif.cleaned_data.get("legal_action_against_traffickers_fir_filed")
        dofe = self.vif.cleaned_data.get("legal_action_against_traffickers_dofe_complaint")
        reason_for_no = self.vif.instance.get_reason_for_no()
        points = self.vif.instance.calculate_strength_of_case_points()

        if self.vif.instance.calculate_strength_of_case_points() > 10:
            Alert.alert_objects.send_alert("strength of case", context={"vif": self.vif.instance, "points": points, "fir": fir, "dofe": dofe, "reason_for_no": reason_for_no})
        pass


class IRFAlertChecker(object):
    def __init__(self, form, inlines):
        self.irf = form
        self.interceptees = inlines[0]
        self.IRF_data = form.cleaned_data

    def check_them(self):
        self.identified_trafficker()
        self.trafficker_name_match()

    def trafficker_name_match(self):
        """
        - Any time there is a trafficker name match from a separate interception. E-mail should include form number that
        was submitted, form number that the match came from, and the name and all personal identifiers from both forms.
        """
        pass

    def identified_trafficker(self):
        """
        Email Alerts to Investigators:
            Any time there is photo of a trafficker on the IRF and the response to question 9.7 is a 4 or a 5
            OR any time there is a photo of a trafficker and the Red Flag points calculated by the computer is 400 or
            higher. E-mail should include IRF number, traffickers name, photo, and the reason for the alert.
        """
        trafficker_list = []
        for person in self.interceptees:
            if person.cleaned_data.get("kind") == 't' and person.cleaned_data.get('photo') not in [None, '']:
                trafficker_list.append(person.instance)

        trafficker_in_custody = self.IRF_data.get("trafficker_taken_into_custody")
        trafficker_name = ''


        taken_into_custody = 0
        if self.IRF_data.get("trafficker_taken_into_custody")=='':
            taken_into_custody = self.IRF_data.get("trafficker_taken_into_custody")
        if trafficker_in_custody is not None and taken_into_custody < len([there for there in self.interceptees.cleaned_data if there]):
            trafficker_name = self.interceptees.cleaned_data[int(self.IRF_data.get("trafficker_taken_into_custody")) - 1].get("full_name")

        red_flags = self.irf.instance.calculate_total_red_flags()
        certainty_points = self.IRF_data.get('how_sure_was_trafficking')
        if len(trafficker_list) > 0:
            if (certainty_points >= 4) and (red_flags >= 400):
                Alert.alert_objects.send_alert("Identified Trafficker", context={"irf": self.irf.instance, "trafficker_list": trafficker_list, "both": True,
                                                                                 "trafficker_in_custody": trafficker_name, "red_flags": red_flags,
                                                                                 "certainty_points": certainty_points})
                return
            if certainty_points >= 4:
                Alert.alert_objects.send_alert("Identified Trafficker", context={"irf": self.irf.instance, "trafficker_list": trafficker_list, "how_sure": True,
                                                                                 "trafficker_in_custody": trafficker_name,
                                                                                 "certainty_points": certainty_points})
            if red_flags >= 400:
                Alert.alert_objects.send_alert("Identified Trafficker", context={"irf": self.irf.instance, "trafficker_list": trafficker_list, "flags": True,
                                                                                 "trafficker_in_custody": trafficker_name, "red_flags": red_flags})