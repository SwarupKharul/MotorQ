from django.http import JsonResponse
from django.shortcuts import render
from .models import event_type, attendee, waiting_list
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
import datetime
import json


@api_view(["POST"])
def register(request):
    body_unicode = request.body.decode("utf-8")
    form_data = json.loads(body_unicode)
    # form_data = body["content"]
    print(form_data)
    if form_data:
        name = form_data.get("name")
        email = form_data.get("email")
        phone = form_data.get("phone")
        event = form_data.get("event")
        event_object = event_type.objects.get(name=event)

        try:
            attendee_object = attendee.objects.get(email=email)
        except attendee.DoesNotExist:
            attendee_object = attendee.objects.create(
                name=name, email=email, phone=phone
            )

        # check if the attendee is already in the database
        # attendee_object = attendee.objects.get_object_or_404(email=email)

        # check if the event is full and in_time is greater than current time

        print(
            datetime.datetime.strptime(
                str(event_object.date) + " " + str(event_object.in_time),
                "%Y-%m-%d %H:%M:%S",
            )
        )
        print(datetime.datetime.now())
        if (
            event_object.availability > 0
            # convert both in_time and current time to datetime objects
            and datetime.datetime.strptime(
                str(event_object.date) + " " + str(event_object.in_time),
                "%Y-%m-%d %H:%M:%S",
            )
            > datetime.datetime.now()
        ):

            # if attendee has already registered for the event, return error
            if attendee_object.registered_events.filter(name=event):
                return JsonResponse(
                    {
                        "status": "fail",
                        "message": "You are already registered for this event",
                    }
                )
            attendee_object.registered_events.add(event_object)
            event_object.availability -= 1
            event_object.save()
            return JsonResponse(
                {
                    "status": "success",
                    "message": "You have successfully registered for the event",
                }
            )
        # Put the attendee in the waiting list if the event is full
        elif event_object.availability == 0:
            waiting_object = waiting_list.objects.create(
                name=name, email=email, phone=phone
            )
            waiting_object.registered_events.add(event_object)
            waiting_object.save()
            return JsonResponse(
                {
                    "status": "success",
                    "message": "You are in the waiting list for the event",
                }
            )

        else:
            return JsonResponse({"status": "fail", "message": "The event is over"})


@api_view(["DELETE"])
def cancel(request):
    body_unicode = request.body.decode("utf-8")
    form_data = json.loads(body_unicode)
    # form_data = body["content"]
    print(form_data)
    if form_data:
        name = form_data.get("name")
        email = form_data.get("email")
        phone = form_data.get("phone")
        event = form_data.get("event")
        event_object = event_type.objects.get(name=event)

        # check if the attendee is already in the database
        attendee_object = attendee.objects.get(email=email)

        # if attendee has already registered for the event, and the out_time is greater than current time, cancel the event
        if attendee_object.registered_events.filter(
            name=event
        ) and datetime.datetime.now() < datetime.datetime.strptime(
            str(event_object.date) + " " + str(event_object.out_time),
            "%Y-%m-%d %H:%M:%S",
        ):
            print(attendee_object.registered_events.count())
            attendee_object.registered_events.remove(event_object)
            print(attendee_object.registered_events.count())
            attendee_object.save()
            event_object.availability += 1
            event_object.save()
            return JsonResponse(
                {
                    "status": "success",
                    "message": "You have successfully cancelled the event",
                }
            )
        else:
            return JsonResponse(
                {
                    "status": "fail",
                    "message": "You are not registered for this event",
                }
            )


def get_all_attendees(request):
    # return all attendees and their registered events
    attendees = []
    for a in attendee.objects.all():
        attendees.append(
            {
                "name": a.name,
                "email": a.email,
                "phone": a.phone,
                "registered_events": list(a.registered_events.values()),
            }
        )

    return JsonResponse({"attendees": attendees})


def get_all_events(request):
    # return all attendees with thier registered events
    event_types = event_type.objects.all().values()
    return JsonResponse({"event_types": list(event_types)})


def get_waiting_list(request):
    # return all attendees in the waiting list
    waiting_lists = []
    for a in waiting_list.objects.all():
        waiting_lists.append(
            {
                "name": a.name,
                "email": a.email,
                "phone": a.phone,
                "registered_events": list(a.registered_events.values()),
            }
        )

    return JsonResponse({"waiting_list": waiting_lists})
