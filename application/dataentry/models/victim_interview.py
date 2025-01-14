from django.db import models

from .addresses import Address1, Address2
from .person import Person
from .border_station import BorderStation


class VictimInterview(models.Model):

    class Meta:
        ordering = ['-date_time_last_updated']

    GENDER_CHOICES = [('M', 'm'), ('F', 'f')]

    vif_number = models.CharField('VIF #', max_length=20, unique=True)
    date = models.DateField('Date')

    date_time_entered_into_system = models.DateTimeField(auto_now_add=True)
    date_time_last_updated = models.DateTimeField(auto_now=True)

    number_of_victims = models.PositiveIntegerField('# of victims', null=True, blank=True)
    number_of_traffickers = models.PositiveIntegerField('# of traffickers', null=True, blank=True)

    location = models.CharField(max_length=255, blank=True)
    interviewer = models.CharField(max_length=255)

    statement_read_before_beginning = models.BooleanField('Check the box if form is signed', default=False)
    permission_to_use_photograph = models.BooleanField('Check the box if form is signed', default=False)

    # 1. Victim & Family Information

    victim = models.ForeignKey(Person, null=True, blank=True)

    victim_address_ward = models.CharField('Ward #', max_length=255, blank=True)

    victim_height = models.PositiveIntegerField('Height(ft)', null=True, blank=True)
    victim_weight = models.PositiveIntegerField('Weight(kg)', null=True, blank=True)

    victim_caste_magar = models.BooleanField('Magar', default=False)
    victim_caste_jaisi = models.BooleanField('Jaisi', default=False)
    victim_caste_thakuri = models.BooleanField('Thakuri', default=False)
    victim_caste_brahmin = models.BooleanField('Brahmin', default=False)
    victim_caste_chhetri = models.BooleanField('Chhetri', default=False)
    victim_caste_newar = models.BooleanField('Newar', default=False)
    victim_caste_tamang = models.BooleanField('Tamang', default=False)
    victim_caste_mongolian = models.BooleanField('Mongolian', default=False)
    victim_caste_muslim = models.BooleanField('Muslim', default=False)
    victim_caste_madeshi_terai = models.BooleanField('Madeshi / Terai Ethnic Group', default=False)
    victim_caste_dalit = models.BooleanField('Dalit / under-priviledged', default=False)
    victim_caste_other = models.BooleanField('Other', default=False)
    victim_caste_other_value = models.CharField(max_length=255, blank=True)

    victim_occupation_unemployed = models.BooleanField('Unemployed', default=False)
    victim_occupation_farmer = models.BooleanField('Farmer', default=False)
    victim_occupation_wage_laborer = models.BooleanField('Wage-laborer', default=False)
    victim_occupation_business_owner = models.BooleanField('Business Owner', default=False)
    victim_occupation_migrant_worker = models.BooleanField('Migrant Worker', default=False)
    victim_occupation_tailoring = models.BooleanField('Tailoring', default=False)
    victim_occupation_housewife = models.BooleanField('Housewife', default=False)
    victim_occupation_animal_husbandry = models.BooleanField('Animal Husbandry', default=False)
    victim_occupation_domestic_work = models.BooleanField('Domestic Work', default=False)
    victim_occupation_shopkeeper = models.BooleanField('Shopkeeper', default=False)
    victim_occupation_hotel = models.BooleanField('Hotel', default=False)
    victim_occupation_factory = models.BooleanField('Factory', default=False)
    victim_occupation_other = models.BooleanField('Other', default=False)
    victim_occupation_other_value = models.CharField(max_length=255, blank=True)

    victim_marital_status_single = models.BooleanField('Single', default=False)
    victim_marital_status_married = models.BooleanField('Married', default=False)
    victim_marital_status_widow = models.BooleanField('Widow', default=False)
    victim_marital_status_divorced = models.BooleanField('Divorced', default=False)
    victim_marital_status_husband_has_other_wives = models.BooleanField('Husband has other wives', default=False)
    victim_marital_status_abandoned_by_husband = models.BooleanField('Abandoned by husband', default=False)

    victim_lives_with_own_parents = models.BooleanField('Own Parent(s)', default=False)
    victim_lives_with_husband = models.BooleanField('Husband', default=False)
    victim_lives_with_husbands_family = models.BooleanField('Husband\'s family', default=False)
    victim_lives_with_friends = models.BooleanField('Friends', default=False)
    victim_lives_with_alone = models.BooleanField('Alone', default=False)
    victim_lives_with_other_relative = models.BooleanField('Other Relative', default=False)
    victim_lives_with_other = models.BooleanField('Other', default=False)
    victim_lives_with_other_value = models.CharField(max_length=255, blank=True)

    victim_num_in_family = models.IntegerField('How many people are in your (own) family?', null=True, blank=True)

    victim_primary_guardian_own_parents = models.BooleanField('Own Parent(s)', default=False)
    victim_primary_guardian_husband = models.BooleanField('Husband', default=False)
    victim_primary_guardian_other_relative = models.BooleanField('Other Relative', default=False)
    victim_primary_guardian_non_relative = models.BooleanField('Non-relative', default=False)
    victim_primary_guardian_no_one = models.BooleanField('No one (I have no guardian)', default=False)

    victim_guardian_address1 = models.ForeignKey(Address1, null=True, on_delete=models.CASCADE)
    victim_guardian_address2 = models.ForeignKey(Address2, null=True, on_delete=models.CASCADE)
    victim_guardian_address_ward = models.CharField('Ward #', max_length=255, blank=True)
    victim_guardian_phone = models.CharField('Phone #', max_length=255, blank=True)

    victim_parents_marital_status_single = models.BooleanField('Single', default=False)
    victim_parents_marital_status_married = models.BooleanField('Married', default=False)
    victim_parents_marital_status_widow = models.BooleanField('Widow', default=False)
    victim_parents_marital_status_father_has_other_wives = models.BooleanField('My father has other wives', default=False)
    victim_parents_marital_separated = models.BooleanField('Separated (Legally married)', default=False)
    victim_parents_marital_divorced = models.BooleanField('Divorced', default=False)

    victim_education_level_none = models.BooleanField('None', default=False)
    victim_education_level_informal = models.BooleanField('Only informal (adult)', default=False)
    victim_education_level_primary = models.BooleanField('Primary only', default=False)
    victim_education_level_grade_4_8 = models.BooleanField('Grade 4-8', default=False)
    victim_education_level_grade_9_10 = models.BooleanField('Grade 9-10', default=False)
    victim_education_level_slc = models.BooleanField('SLC', default=False)
    victim_education_level_11_12 = models.BooleanField('11-12', default=False)
    victim_education_level_bachelors = models.BooleanField('Bachelors', default=False)
    victim_education_level_masters = models.BooleanField('Masters', default=False)

    victim_is_literate = models.NullBooleanField('Is the victim literate?', null=True)

    # 2. Migration Plans
    migration_plans_education = models.BooleanField('Education', default=False)
    migration_plans_travel_tour = models.BooleanField('Travel / Tour', default=False)
    migration_plans_shopping = models.BooleanField('Shopping', default=False)
    migration_plans_eloping = models.BooleanField('Eloping', default=False)
    migration_plans_arranged_marriage = models.BooleanField('Arranged Marriage', default=False)
    migration_plans_meet_own_family = models.BooleanField('Meet your own family', default=False)
    migration_plans_visit_brokers_home = models.BooleanField('Visit broker\'s home', default=False)
    migration_plans_medical_treatment = models.BooleanField('Medical treatment', default=False)
    migration_plans_job_broker_didnt_say = models.BooleanField('Job - Broker did not say what job', default=False)
    migration_plans_job_baby_care = models.BooleanField('Job - Baby Care', default=False)
    migration_plans_job_factory = models.BooleanField('Job - Factory', default=False)
    migration_plans_job_hotel = models.BooleanField('Job - Hotel', default=False)
    migration_plans_job_shop = models.BooleanField('Job - Shop', default=False)
    migration_plans_job_laborer = models.BooleanField('Job - Laborer', default=False)
    migration_plans_job_brothel = models.BooleanField('Job - Brothel', default=False)
    migration_plans_job_household = models.BooleanField('Job - Household', default=False)
    migration_plans_job_other = models.BooleanField('Job - Other', default=False)
    migration_plans_other = models.BooleanField('Other', default=False)
    migration_plans_job_other_value = models.CharField(max_length=255, blank=True)
    migration_plans_other_value = models.CharField(max_length=255, blank=True)

    primary_motivation_support_myself = models.BooleanField('Support myself', default=False)
    primary_motivation_support_family = models.BooleanField('Support family', default=False)
    primary_motivation_personal_debt = models.BooleanField('Personal Debt', default=False)
    primary_motivation_family_debt = models.BooleanField('Family Debt', default=False)
    primary_motivation_love_marriage = models.BooleanField('Love / Marriage', default=False)
    primary_motivation_bad_home_marriage = models.BooleanField('Bad home / marriage', default=False)
    primary_motivation_get_education = models.BooleanField('Get an education', default=False)
    primary_motivation_tour_travel = models.BooleanField('Tour / Travel', default=False)
    primary_motivation_didnt_know = models.BooleanField('Didn\'t know I was going abroad', default=False)
    primary_motivation_other = models.BooleanField('Other', default=False)
    primary_motivation_other_value = models.CharField(max_length=255, blank=True)

    victim_where_going_region_india = models.NullBooleanField('India', null=True)
    victim_where_going_region_gulf = models.NullBooleanField('Gulf / Other', null=True)

    victim_where_going_india_delhi = models.NullBooleanField('Delhi', null=True)
    victim_where_going_india_mumbai = models.NullBooleanField('Mumbai', null=True)
    victim_where_going_india_surat = models.NullBooleanField('Surat', null=True)
    victim_where_going_india_rajastan = models.NullBooleanField('Rajastan', null=True)
    victim_where_going_india_kolkata = models.NullBooleanField('Kolkata', null=True)
    victim_where_going_india_pune = models.NullBooleanField('Pune', null=True)
    victim_where_going_india_jaipur = models.NullBooleanField('Jaipur', null=True)
    victim_where_going_india_bihar = models.NullBooleanField('Bihar', null=True)
    victim_where_going_india_didnt_know = models.NullBooleanField('Did Not Know', null=True)
    victim_where_going_india_other = models.NullBooleanField('Other', null=True)
    victim_where_going_india_other_value = models.CharField(max_length=255, blank=True)

    victim_where_going_gulf_lebanon = models.NullBooleanField('Lebanon', null=True)
    victim_where_going_gulf_dubai = models.NullBooleanField('Dubai', null=True)
    victim_where_going_gulf_malaysia = models.NullBooleanField('Malaysia', null=True)
    victim_where_going_gulf_oman = models.NullBooleanField('Oman', null=True)
    victim_where_going_gulf_saudi_arabia = models.NullBooleanField('Saudi Arabia', null=True)
    victim_where_going_gulf_kuwait = models.NullBooleanField('Kuwait', null=True)
    victim_where_going_gulf_qatar = models.NullBooleanField('Qatar', null=True)
    victim_where_going_gulf_didnt_know = models.NullBooleanField('Did Not Know', null=True)
    victim_where_going_gulf_other = models.NullBooleanField('Other', null=True)
    victim_where_going_gulf_other_value = models.CharField(max_length=255, blank=True)

    manpower_involved = models.NullBooleanField('Was a manpower involved?', null=True)
    victim_recruited_in_village = models.BooleanField('Did someone recruit you in your village and persuade you to abroad?', default="False")

    brokers_relation_to_victim_own_dad = models.BooleanField('Own dad', default=False)
    brokers_relation_to_victim_own_mom = models.BooleanField('Own mom', default=False)
    brokers_relation_to_victim_own_uncle = models.BooleanField('Own uncle', default=False)
    brokers_relation_to_victim_own_aunt = models.BooleanField('Own aunt', default=False)
    brokers_relation_to_victim_own_bro = models.BooleanField('Own bro', default=False)
    brokers_relation_to_victim_own_sister = models.BooleanField('Own sister', default=False)
    brokers_relation_to_victim_own_other_relative = models.BooleanField('Other relative', default=False)
    brokers_relation_to_victim_friend = models.BooleanField('Friend', default=False)
    brokers_relation_to_victim_agent = models.BooleanField('Agent', default=False).set_weight(2)
    brokers_relation_to_victim_husband = models.BooleanField('Husband', default=False)
    brokers_relation_to_victim_boyfriend = models.BooleanField('Boyfriend', default=False)
    brokers_relation_to_victim_neighbor = models.BooleanField('Neighbor', default=False)
    brokers_relation_to_victim_recently_met = models.BooleanField('Recently met', default=False)
    brokers_relation_to_victim_contractor = models.BooleanField('Contractor', default=False)
    brokers_relation_to_victim_other = models.BooleanField('Other', default=False)
    brokers_relation_to_victim_other_value = models.CharField(max_length=255, blank=True)

    victim_married_to_broker_years = models.PositiveIntegerField('Years', null=True, blank=True)
    victim_married_to_broker_months = models.PositiveIntegerField('Months', null=True, blank=True)

    victim_how_met_broker_from_community = models.BooleanField('Broker is from my community', default=False)
    victim_how_met_broker_at_work = models.BooleanField('At work', default=False)
    victim_how_met_broker_at_school = models.BooleanField('At school', default=False)
    victim_how_met_broker_job_advertisement = models.BooleanField('Job advertisement', default=False)
    victim_how_met_broker_he_approached_me = models.BooleanField('He approached me', default=False)
    victim_how_met_broker_through_friends = models.BooleanField('Through friends', default=False)
    victim_how_met_broker_through_family = models.BooleanField('Through family', default=False)
    victim_how_met_broker_at_wedding = models.BooleanField('At Wedding', default=False)
    victim_how_met_broker_in_a_vehicle = models.BooleanField('In a Vehicle', default=False)
    victim_how_met_broker_in_a_hospital = models.BooleanField('In a Hospital', default=False)
    victim_how_met_broker_went_myself = models.BooleanField('Went to him myself', default=False)
    victim_how_met_broker_called_my_mobile = models.BooleanField('Called my mobile', default=False)
    victim_how_met_broker_other = models.BooleanField('Other', default=False)
    victim_how_met_broker_other_value = models.CharField(max_length=255, blank=True)

    victim_how_met_broker_mobile_explanation = models.TextField(blank=True)

    victim_how_long_known_broker_years = models.PositiveIntegerField('Years', null=True, blank=True)
    victim_how_long_known_broker_months = models.PositiveIntegerField('Months', null=True, blank=True)

    victim_how_expense_was_paid_paid_myself = models.BooleanField('I paid the expenses myself', default=False)
    victim_how_expense_was_paid_broker_paid_all = models.BooleanField('The broker paid all the expenses', default=False)
    victim_how_expense_was_paid_gave_money_to_broker = models.BooleanField('I gave a sum of money to the broker', default=False)
    victim_how_expense_was_paid_broker_gave_loan = models.BooleanField('The broker paid the expenses and I have to pay him back', default=False)
    victim_how_expense_was_paid_amount = models.DecimalField('Amount', max_digits=10, decimal_places=2, null=True, blank=True)

    broker_works_in_job_location_no = models.BooleanField('No', default=False)
    broker_works_in_job_location_yes = models.BooleanField('Yes', default=False)
    broker_works_in_job_location_dont_know = models.BooleanField('Don\'t Know', default=False)

    amount_victim_would_earn = models.DecimalField('Amount', max_digits=10, decimal_places=2, null=True, blank=True)

    number_broker_made_similar_promises_to = models.PositiveIntegerField(null=True, blank=True)

    # Section 4

    victim_first_time_crossing_border = models.NullBooleanField(null=True)

    victim_primary_means_of_travel_tourist_bus = models.BooleanField('Tourist Bus', default=False)
    victim_primary_means_of_travel_motorbike = models.BooleanField('Motorbike', default=False)
    victim_primary_means_of_travel_private_car = models.BooleanField('Private Car', default=False)
    victim_primary_means_of_travel_local_bus = models.BooleanField('Local Bus', default=False)
    victim_primary_means_of_travel_microbus = models.BooleanField('Microbus', default=False)
    victim_primary_means_of_travel_plane = models.BooleanField('Plane', default=False)
    victim_primary_means_of_travel_other = models.BooleanField('Other', default=False)
    victim_primary_means_of_travel_other_value = models.CharField(max_length=255, blank=True)

    victim_stayed_somewhere_between = models.BooleanField(default=False)

    victim_how_long_stayed_between_days = models.PositiveIntegerField('Days', null=True, blank=True)
    victim_how_long_stayed_between_start_date = models.DateField('Start Date', null=True, blank=True)

    victim_was_hidden = models.NullBooleanField(null=True)
    victim_was_hidden_explanation = models.TextField(blank=True)

    victim_was_free_to_go_out = models.NullBooleanField(null=True)
    victim_was_free_to_go_out_explanation = models.TextField(blank=True)

    how_many_others_in_situation = models.PositiveIntegerField(null=True, blank=True)

    others_in_situation_age_of_youngest = models.PositiveIntegerField(null=True, blank=True)

    passport_made_no_passport_made = models.BooleanField('No passport made', default=False)
    passport_made_real_passport_made = models.BooleanField('Real passport made', default=False)
    passport_made_passport_included_false_name = models.BooleanField('Passport included a false name', default=False).set_weight(3)
    passport_made_passport_included_other_false_info = models.BooleanField('Passport included other false info', default=False).set_weight(3)
    passport_made_passport_was_fake = models.BooleanField('Passport was fake', default=False).set_weight(5)

    victim_passport_with_broker = models.NullBooleanField(null=True)

    abuse_happened_sexual_harassment = models.BooleanField('Sexual Harassment', default=False).set_weight(5)
    abuse_happened_sexual_abuse = models.BooleanField('Sexual Abuse', default=False).set_weight(9)
    abuse_happened_physical_abuse = models.BooleanField('Physical Abuse', default=False).set_weight(5)
    abuse_happened_threats = models.BooleanField('Threats', default=False).set_weight(4)
    abuse_happened_denied_proper_food = models.BooleanField('Denied Proper Food', default=False).set_weight(4)
    abuse_happened_forced_to_take_drugs = models.BooleanField('Forced to take Drugs', default=False).set_weight(9)
    abuse_happened_by_whom = models.TextField('By whom?', blank=True)
    abuse_happened_explanation = models.TextField('Explain', blank=True)

    victim_traveled_with_broker_companion_yes = models.BooleanField('Yes', default=False)
    victim_traveled_with_broker_companion_no = models.BooleanField('No', default=False)
    victim_traveled_with_broker_companion_broker_took_me_to_border = models.BooleanField('Broker took me to border', default=False)

    companion_with_when_intercepted = models.NullBooleanField(null=True)
    planning_to_meet_companion_later = models.NullBooleanField(null=True)

    money_changed_hands_broker_companion_no = models.BooleanField('No', default=False)
    money_changed_hands_broker_companion_dont_know = models.BooleanField('Don\'t know', default=False)
    money_changed_hands_broker_companion_broker_gave_money = models.BooleanField('Broker gave money to the companion', default=False).set_weight(3)
    money_changed_hands_broker_companion_companion_gave_money = models.BooleanField('Companion gave money to the broker', default=False).set_weight(3)

    # 5. Destination & India Contact

    meeting_at_border_yes = models.BooleanField('Yes', default=False)
    meeting_at_border_no = models.BooleanField('No', default=False)
    meeting_at_border_meeting_broker = models.BooleanField('Meeting Broker', default=False)
    meeting_at_border_meeting_companion = models.BooleanField('Meeting Companion', default=False)

    victim_knew_details_about_destination = models.BooleanField(default=False)

    other_involved_person_in_india = models.NullBooleanField(null=True)
    other_involved_husband_trafficker = models.NullBooleanField(null=True)
    other_involved_someone_met_along_the_way = models.NullBooleanField(null=True)
    other_involved_someone_involved_in_trafficking = models.NullBooleanField(null=True)
    other_involved_place_involved_in_trafficking = models.NullBooleanField(null=True)
    victim_has_worked_in_sex_industry = models.NullBooleanField(null=True)
    victim_place_worked_involved_sending_girls_overseas = models.NullBooleanField(null=True)

    # 6. Awareness & Assessment

    awareness_before_interception_had_heard_not_how_bad = models.BooleanField('Had heard, but never knew how bad it was until I was intercepted by TH', default=False)
    awareness_before_interception_knew_how_bad_not_happening_to_her = models.BooleanField('Knew how bad it was, but didn\'t think that was happening to her', default=False)
    awareness_before_interception_never_heard = models.BooleanField('Had never heard about it', default=False)

    attitude_towards_tiny_hands_thankful = models.BooleanField('Yes, thankful to TH for saving her', default=False)
    attitude_towards_tiny_hands_blames = models.BooleanField('No, blames Tiny Hands for stopping her', default=False)
    attitude_towards_tiny_hands_doesnt_know = models.BooleanField('Doesn\'t Know', default=False)

    victim_heard_gospel_no = models.BooleanField('No, I have never heard', default=False)
    victim_heard_gospel_heard_name_only = models.BooleanField('Has heard the name only', default=False)
    victim_heard_gospel_heard_but_never_believed = models.BooleanField('Had heard the gospel but never believed', default=False)
    victim_heard_gospel_already_believer = models.BooleanField('Was already a believer', default=False)

    victim_beliefs_now_doesnt_believe = models.BooleanField('Doesn\'t believe in Jesus', default=False)
    victim_beliefs_now_believes_no_church = models.BooleanField('Believes in Jesus, but doesn\'t plan to go to church', default=False)
    victim_beliefs_now_believes_and_church = models.BooleanField('Believes in Jesus and plans to go to church', default=False)

    RATING_CHOICES = [(i, i) for i in range(1, 11)]
    tiny_hands_rating_border_staff = models.PositiveIntegerField('Border Staff polite and respectful', choices=RATING_CHOICES, null=True, blank=True)
    tiny_hands_rating_shelter_staff = models.PositiveIntegerField('Shelter Staff polite and respectful', choices=RATING_CHOICES, null=True, blank=True)
    tiny_hands_rating_trafficking_awareness = models.PositiveIntegerField('Trafficking Awareness', choices=RATING_CHOICES, null=True, blank=True)
    tiny_hands_rating_shelter_accommodations = models.PositiveIntegerField('Shelter Accommodations', choices=RATING_CHOICES, null=True, blank=True)

    how_can_we_serve_you_better = models.TextField(blank=True)

    # Section 7

    guardian_knew_was_travelling_to_india = models.NullBooleanField(null=True)
    family_pressured_victim = models.NullBooleanField(null=True)
    family_will_try_sending_again = models.NullBooleanField(null=True)
    victim_feels_safe_at_home = models.NullBooleanField(null=True)
    victim_wants_to_go_home = models.NullBooleanField(null=True)

    victim_home_had_sexual_abuse_never = models.BooleanField('Never', default=False)
    victim_home_had_sexual_abuse_rarely = models.BooleanField('Rarely / Minor', default=False)
    victim_home_had_sexual_abuse_frequently = models.BooleanField('Frequent / Severe', default=False)

    victim_home_had_physical_abuse_never = models.BooleanField('Never', default=False)
    victim_home_had_physical_abuse_rarely = models.BooleanField('Rarely / Minor', default=False)
    victim_home_had_physical_abuse_frequently = models.BooleanField('Frequent / Severe', default=False)

    victim_home_had_emotional_abuse_never = models.BooleanField('Never', default=False)
    victim_home_had_emotional_abuse_rarely = models.BooleanField('Rarely / Minor', default=False)
    victim_home_had_emotional_abuse_frequently = models.BooleanField('Frequent / Severe', default=False)

    victim_guardian_drinks_alcohol_never = models.BooleanField('Never', default=False)
    victim_guardian_drinks_alcohol_occasionally = models.BooleanField('Occasionally', default=False)
    victim_guardian_drinks_alcohol_all_the_time = models.BooleanField('All the time', default=False)

    victim_guardian_uses_drugs_never = models.BooleanField('Never', default=False)
    victim_guardian_uses_drugs_occasionally = models.BooleanField('Occasionally', default=False)
    victim_guardian_uses_drugs_all_the_time = models.BooleanField('All the time', default=False)

    victim_family_economic_situation_no_basic_needs = models.BooleanField('Unable to meet basic needs', default=False)
    victim_family_economic_situation_difficult_basic_needs = models.BooleanField('Able to meet only basic needs, but it is very difficult', default=False)
    victim_family_economic_situation_comfortable_basic_needs = models.BooleanField('Comfortably meet basic needs, and can afford to buy some non-essential goods/services', default=False)
    victim_family_economic_situation_wealthy = models.BooleanField('Wealthy', default=False)

    victim_had_suicidal_thoughts = models.NullBooleanField(null=True)

    reported_total_situational_alarms = models.PositiveIntegerField(blank=True, null=True)

    border_station = models.ForeignKey(BorderStation, models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.vif_number

    def victim_address1_as_string(self):
        rtn = ''
        try:
            rtn = self.victim_address1
        finally:
            return rtn

    def victim_address2_as_string(self):
        rtn = ''
        try:
            rtn = self.victim_address2
        finally:
            return rtn

    def victim_guardian_address1_as_string(self):
        rtn = ''
        try:
            rtn = self.victim_guardian_address1
        finally:
            return rtn

    def victim_guardian_address2_as_string(self):
        rtn = ''
        try:
            rtn = self.victim_guardian_address2
        finally:
            return rtn

    def calculate_strength_of_case_points(self):
            total = 0
            for field in self._meta.fields:
                if type(field) == models.BooleanField:
                    value = getattr(self, field.name)
                    if value is True:
                        if hasattr(field, 'weight'):
                            total += field.weight
            if self.victim_how_expense_was_paid_broker_gave_loan > 0:
                total += (2 + (self.victim_how_expense_was_paid_broker_gave_loan//20000))
            if self.number_broker_made_similar_promises_to and self.victim_how_expense_was_paid_amount > 0:
                total += int(self.victim_how_expense_was_paid_amount)
            if self.how_many_others_in_situation > 0:
                total += self.how_many_others_in_situation
            if self.others_in_situation_age_of_youngest > 0:
                total += (20 - self.others_in_situation_age_of_youngest)
            if self.victim_was_hidden:
                total += 5
            if not self.victim_was_free_to_go_out:
                total += 5
            if not self.companion_with_when_intercepted:
                total += 3
            if self.victim_place_worked_involved_sending_girls_overseas:
                total += 7
            return total

    def get_calculated_situational_alarms(self):
        total = 0
        if self.family_pressured_victim is True:
            total += 1
        if self.family_will_try_sending_again is True:
            total += 3
        if self.victim_feels_safe_at_home is False:
            total += 4
        if self.victim_wants_to_go_home is False:
            total += 4
        if self.victim_home_had_sexual_abuse_rarely is True:
            total += 4
        if self.victim_home_had_sexual_abuse_frequently is True:
            total += 10
        if self.victim_home_had_physical_abuse_frequently is True:
            total += 6
        if self.victim_home_had_emotional_abuse_frequently is True:
            total += 2
        if self.victim_guardian_drinks_alcohol_all_the_time is True:
            total += 1
        if self.victim_guardian_uses_drugs_occasionally is True:
            total += 2
        if self.victim_guardian_uses_drugs_all_the_time is True:
            total += 6
        if self.victim_family_economic_situation_no_basic_needs is True:
            total += 7
        if self.victim_had_suicidal_thoughts is True:
            total += 7
        return total

    legal_action_against_traffickers_no = models.BooleanField('No', default=False)
    legal_action_against_traffickers_fir_filed = models.BooleanField('FIR filed against', default=False)
    legal_action_against_traffickers_dofe_complaint = models.BooleanField('DoFE complaint against', default=False)
    legal_action_fir_against_value = models.CharField(max_length=255, blank=True)
    legal_action_dofe_against_value = models.CharField(max_length=255, blank=True)

    reason_no_legal_no_trafficking_suspected = models.BooleanField('No trafficking suspected', default=False)
    reason_no_legal_police_not_enough_info = models.BooleanField('Police say not enough information', default=False)
    reason_no_legal_trafficker_is_own_people = models.BooleanField('Trafficker is victim\'s own people', default=False)
    reason_no_legal_she_was_going_herself = models.BooleanField('She was going herself', default=False)
    reason_no_legal_trafficker_ran_away = models.BooleanField('Trafficker ran away', default=False)
    reason_no_legal_victim_afraid_of_reputation = models.BooleanField('Victim afraid of reputation', default=False)
    reason_no_legal_victim_afraid_for_safety = models.BooleanField('Victim afraid for her safety', default=False)
    reason_no_legal_family_afraid_of_reputation = models.BooleanField('Family afraid of reputation', default=False)
    reason_no_legal_family_afraid_for_safety = models.BooleanField('Family afraid for her safety', default=False)
    reason_no_legal_police_bribed = models.BooleanField('Police bribed by trafficker', default=False)
    reason_no_legal_victim_family_bribed = models.BooleanField('Victim / family bribed by trafficker', default=False)
    reason_no_legal_interference_by_powerful_people = models.BooleanField('Interference by powerful people', default=False)
    reason_no_legal_other = models.BooleanField('Other', default=False)
    reason_no_legal_interference_value = models.CharField(max_length=255, blank=True)
    reason_no_legal_other_value = models.CharField(max_length=255, blank=True)

    def get_reason_for_no(self):
        if self.reason_no_legal_no_trafficking_suspected:
            return 'no trafficking suspected'
        if self.reason_no_legal_police_not_enough_info:
            return 'police say not enough information'
        if self.reason_no_legal_trafficker_is_own_people:
            return 'trafficker is victim\'s own people'
        if self.reason_no_legal_she_was_going_herself:
            return 'she was going herself'
        if self.reason_no_legal_trafficker_ran_away:
            return 'trafficker ran away'
        if self.reason_no_legal_victim_afraid_of_reputation:
            return 'victim afraid of reputation'
        if self.reason_no_legal_victim_afraid_for_safety:
            return 'victim afraid for her safety'
        if self.reason_no_legal_family_afraid_of_reputation:
            return 'family afraid of reputation'
        if self.reason_no_legal_family_afraid_for_safety:
            return 'family afraid for her safety'
        if self.reason_no_legal_police_bribed:
            return 'police bribed by trafficker'
        if self.reason_no_legal_victim_family_bribed:
            return 'victim / family bribed by trafficker'
        if self.reason_no_legal_interference_by_powerful_people:
            return self.reason_no_legal_interference_value
        if self.reason_no_legal_other:
            return self.reason_no_legal_other_value
        return "nothing"

    interviewer_recommendation_send_home = models.BooleanField('Plan to send the girl home to stay with her guardians', default=False)
    interviewer_recommendation_send_to_other_relatives = models.BooleanField('Plan to send the girl to stay with other relatives', default=False)
    interviewer_recommendation_find_other_place = models.BooleanField('Tiny Hands needs to help her find another place to go', default=False)

    other_people_and_places_involved = models.NullBooleanField(null=True)

    has_signature = models.BooleanField('Scanned form has signature', default=False)

    case_notes = models.TextField('Case Notes', blank=True)

    scanned_form = models.FileField('Attach scanned copy of form (pdf or image)', upload_to='scanned_vif_forms', default='', blank=True)
