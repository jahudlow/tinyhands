import StringIO

from braces.views import LoginRequiredMixin
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import View
from lxml import etree
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from templated_email import send_templated_mail
from z3c.rml import document

from accounts.mixins import PermissionsRequiredMixin
from budget.models import BorderStationBudgetCalculation, StaffSalary
from rest_api.authentication import HasPermission
from static_border_stations.models import Staff, CommitteeMember
from static_border_stations.serializers import StaffSerializer, CommitteeMemberSerializer


class MoneyDistribution(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, HasPermission]
    permissions_required = ['permission_budget_manage']

    def retrieve(self, request, pk):
        border_station = BorderStationBudgetCalculation.objects.get(pk=pk).border_station
        staff = border_station.staff_set.all().filter(receives_money_distribution_form=True)
        committee_members = border_station.committeemember_set.all().filter(receives_money_distribution_form=True).all()

        staff_serializer = StaffSerializer(staff, many=True)
        committee_members_serializer = CommitteeMemberSerializer(committee_members, many=True)

        pdf_url = settings.SITE_DOMAIN + reverse('MdfPdf', kwargs={"pk": pk})

        return Response({"staff_members": staff_serializer.data, "committee_members": committee_members_serializer.data, "pdf_url": pdf_url})

    def send_emails(self, request, pk):
        staff_ids = request.data['staff_ids']
        budget_calc_id = pk
        committee_ids = request.data['committee_ids']

        # send the emails
        for id in staff_ids:
            person = Staff.objects.get(pk=id)
            self.email_staff_and_committee_members(person, budget_calc_id, 'money_distribution_form')

        for id in committee_ids:
            person = CommitteeMember.objects.get(pk=id)
            self.email_staff_and_committee_members(person, budget_calc_id, 'money_distribution_form')

        return Response("Emails Sent!", status=200)

    def email_staff_and_committee_members(self, person, budget_calc_id, template, context={}):
        context['person'] = person
        context['budget_calc_id'] = budget_calc_id
        context['site'] = settings.SITE_DOMAIN
        send_templated_mail(
            template_name=template,
            from_email=settings.ADMIN_EMAIL_SENDER,
            recipient_list=[person.email],
            context=context
        )


class PDFView(View, LoginRequiredMixin, PermissionsRequiredMixin):
    permissions_required = ['permission_budget_manage']
    filename = 'report.pdf'
    template_name = ''

    def get_filename(self):
        return self.filename

    def get_context_data(self):
        return {}

    def dispatch(self, request, *args, **kwargs):
        if self.template_name == '':
            raise ImproperlyConfigured(
                "A template_name must be specified for the rml template.")

        # Use StringIO and not cStringIO because cStringIO can't accept unicode characters
        buf = StringIO.StringIO()
        rml = render_to_string(self.template_name, self.get_context_data())

        self.rml = render_to_string(self.template_name, self.get_context_data())

        buf.write(rml)
        buf.seek(0)
        root = etree.parse(buf).getroot()
        doc = document.Document(root)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = "filename=%s" % self.get_filename()
        response['X-Frame-Options'] = "*"

        doc.process(response)
        return response


class MoneyDistributionFormPDFView(PDFView, LoginRequiredMixin, PermissionsRequiredMixin):
    permissions_required = ['permission_budget_manage']
    template_name = 'budget/MoneyDistributionTemplate.rml'
    filename = 'Monthly-Money-Distribution-Form.pdf'

    def get_context_data(self):

        station = BorderStationBudgetCalculation.objects.get(pk=self.kwargs['pk'])
        staffSalaries = StaffSalary.objects.filter(budget_calc_sheet=self.kwargs['pk'])
        otherItems = station.otherbudgetitemcost_set.all()

        adminMeetings = station.administration_number_of_meetings_per_month * station.administration_number_of_meetings_per_month_multiplier

        return {
            'otherItems': otherItems,
            'name': station.border_station.station_name,
            'date': station.date_time_entered.date,
            'number': len(staffSalaries),
            'staffSalaries': staffSalaries,
            'salary_total': station.salary_total(),
            'travel_chair_bool': station.travel_chair_with_bike,
            'travel_chair': station.travel_chair_with_bike_amount,
            'travel_manager_bool': station.travel_manager_with_bike,
            'travel_manager': station.travel_manager_with_bike_amount,
            'travel_total': station.travel_total(),

            'communication_chair_bool': station.communication_chair,
            'communication_chair': station.communication_chair_amount,
            'communication_manager_bool': station.communication_manager,
            'communication_manager': station.communication_manager_amount,
            'communication_staff': station.communication_staff_total(),
            'communication_total': station.communication_total(),

            'admin_meetings': station.administration_number_of_meetings_per_month * station.administration_number_of_meetings_per_month_multiplier,
            'admin_total': station.administration_total(),

            'medical_total': station.medical_total(),

            'misc_total': station.miscellaneous_total(),

            'shelter_total': station.shelter_total(),

            'food_and_gas_intercepted_girls': station.food_and_gas_number_of_intercepted_girls_multiplier_before * station.food_and_gas_number_of_intercepted_girls * station.food_and_gas_number_of_intercepted_girls_multiplier_after,
            'food_and_gas_limbo_girls': station.food_and_gas_limbo_girls_multiplier * station.food_and_gas_number_of_limbo_girls * station.food_and_gas_number_of_days,
            'food_gas_total': station.food_and_gas_total(),

            'awareness_contact_cards_bool': station.awareness_contact_cards,
            'awareness_contact_cards': station.awareness_contact_cards_amount,
            'awareness_awareness_party_bool': station.awareness_awareness_party_boolean,
            'awareness_awareness_party': station.awareness_awareness_party,
            'awareness_sign_boards_bool': station.awareness_sign_boards_boolean,
            'awareness_sign_boards': station.awareness_sign_boards,
            'awareness_total': station.awareness_total(),

            'supplies_walkie_talkies_bool': station.supplies_walkie_talkies_boolean,
            'supplies_walkie_talkies': station.supplies_walkie_talkies_amount,
            'supplies_recorders_bool': station.supplies_recorders_boolean,
            'supplies_recorders': station.supplies_recorders_amount,
            'supplies_binoculars_bool': station.supplies_binoculars_boolean,
            'supplies_binoculars': station.supplies_binoculars_amount,
            'supplies_flashlights_bool': station.supplies_flashlights_boolean,
            'supplies_flashlights': station.supplies_flashlights_amount,
            'supplies_total': station.supplies_total,

            'monthly_total': station.station_total()
        }