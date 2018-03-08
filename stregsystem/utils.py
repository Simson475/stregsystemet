import datetime
import smtplib

import pytz
from django.db.models import Count, F, Q
from django.utils import timezone


def make_active_productlist_query(queryset):
    now = timezone.now()
    # Create a query for the set of products that MIGHT be active. Might
    # because they can be out of stock. Which we compute later
    active_candidates = (
        queryset
        .filter(
            Q(active=True)
            & (Q(deactivate_date=None) | Q(deactivate_date__gte=now)))
    )
    # This query selects all the candidates that are out of stock.
    candidates_out_of_stock = (
        active_candidates
        .filter(sale__timestamp__gt=F("start_date"))
        .annotate(c=Count("sale__id"))
        .filter(c__gte=F("quantity"))
        .values("id")
    )
    # We can now create a query that selects all the candidates which are not
    # out of stock.
    return (
        active_candidates
        .exclude(
            Q(start_date__isnull=False)
            & Q(id__in=candidates_out_of_stock)))


def make_inactive_productlist_query(queryset):
    now = timezone.now()
    # Create a query of things are definitively inactive. Some of the ones
    # filtered here might be out of stock, but we include that later.
    inactive_candidates = (
        queryset
        .exclude(
            Q(active=True)
            & (Q(deactivate_date=None) | Q(deactivate_date__gte=now)))
        .values("id")
    )
    inactive_out_of_stock = (
        queryset
        .filter(sale__timestamp__gt=F("start_date"))
        .annotate(c=Count("sale__id"))
        .filter(c__gte=F("quantity"))
        .values("id")
    )
    return (
        queryset
        .filter(
            Q(id__in=inactive_candidates)
            | Q(id__in=inactive_out_of_stock))
    )


def make_room_specific_query(room):
    return (
        Q(rooms__id=room) | Q(rooms=None)
    )


def date_to_midnight(date):
    """
    Converts a datetime.date to a datetime of the same date at midnight.

    :param date: date to convert
    :return: the date as a timezone aware datetime at midnight
    """
    return timezone.make_aware(timezone.datetime(date.year, date.month, date.day, 0, 0))


def send_payment_mail(member, amount):
    msg = f"Hey {member.firstname} we've added {amount} to your streg-account: '{member.username}'"
    try:
       smtpObj = smtplib.SMTP('localhost')
       smtpObj.sendmail('FIT@fklub.dk', member.email, msg)
    except:
       pass

