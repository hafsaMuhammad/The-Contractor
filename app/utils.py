from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_order_email(order):
    subject = f"New Order #{order.id}"
    from_email = "TheContractor@test-xkjn41m6qv64z781.mlsender.net"
    to_email = ["hafsa.mohamed1999@gmail.com"]
    
    html_content = render_to_string("emails/order_created.html", {"order": order})

    email = EmailMultiAlternatives(subject, "", from_email, to_email)
    email.attach_alternative(html_content, "text/html")
    email.send()
