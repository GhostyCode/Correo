from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
from newsletters.models import NewsletterUser
from .forms import NewsletterUserSignUpForm
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage

def newsletter_signup(request):
    form = NewsletterUserSignUpForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        if NewsletterUser.objects.filter(email=instance.email).exists():
            messages.warning(request, 'Este correo ya existe.')

        else:
            instance.save()
            messages.success(request, 'Hemos enviado un correo electronico a su correo, abrelo para continuar con la subscripción')

            #CorreoElectronico
            subject="Libro de programación"
            from_email=settings.EMAIL_HOST_USER
            to_email=[instance.email]

            html_template='newsletter/welcome.html'
            html_message=render_to_string(html_template)
            message=EmailMessage(subject, html_message, from_email, to_email)
            message.content_subtype='html'
            message.send()

    context={
        'form':form,
    }
    return render(request, 'start_here.html',context)
        


def newsletter_unsubscribe(request):
    form = NewsletterUserSignUpForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        if NewsletterUser.objects.filter(email=instance.email).exists():
            NewsletterUser.objects.filter(email=instance.email).delete()
            messages.success(request, 'El correo ha sido eliminado')
        else:
            print('Email not found')
            messages.warning(request, 'Email not found')

    context = {
        'form':form,
    }

    return render(request, 'unsubscribe.html', context)