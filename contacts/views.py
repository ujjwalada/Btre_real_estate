from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.
from .models import Contact

from django.core.mail import send_mail


def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        # check same property enqiury happens or not
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contact = Contact.objects.all().filter(
                listing_id=listing_id, user_id=user_id)
            if has_contact:
                messages.error(
                    request, 'you have alredy made a query for this property ')
                return redirect('/listings/'+listing_id)

        contact = Contact(listing_id=listing_id, listing=listing, name=name,
                          email=email, phone=phone, message=message, user_id=user_id)

        contact.save()

        # email send
        send_mail(
            'Regarding Property Enquiry',
            'there is inquiry for ' + listing + '.plzz login to see more details ',
            'djangosmtp261@gmail.com',
            [realtor_email, 'gy8004623@gmail.com'],
            fail_silently=False

        )

        messages.success(
            request, 'Thank for Submitting we will contact yoy soon')

    return redirect('/listings/'+listing_id)
