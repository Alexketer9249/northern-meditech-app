from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, RFQSubmission
from .serializers import ProductSerializer, RFQSerializer
from django.db.models import Q

# PDF & EMAIL IMPORTS
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from xhtml2pdf import pisa
from django.utils import timezone
import io  # <--- Essential for handling PDF in memory

@api_view(['GET'])
def get_products(request):
    # (This function stays exactly the same)
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    products = Product.objects.all()

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(model_number__icontains=search_query)
        )
    if category_filter:
        products = products.filter(category__name__iexact=category_filter)

    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def submit_rfq(request):
    data = request.data
    
    # 1. Save Lead to Database
    submission = RFQSubmission.objects.create(
        institution=data.get('institution', 'Web Visitor'),
        contact_person=data.get('contact_person', 'Pending'),
        email=data.get('email', 'visitor@lead.com'),
        phone=data.get('phone', 'N/A'),
        details=data.get('details', 'Generated Quote')
    )

    # 2. Get Products & Calculate Total
    product_ids = data.get('product_ids', [])
    products = Product.objects.filter(id__in=product_ids)
    total = sum([getattr(p, 'price', 0) for p in products])

    # 3. Prepare PDF Data
    context = {
        'date': timezone.now().strftime("%d %b, %Y"),
        'quote_id': f"QT-{submission.id:04d}",
        'customer_name': submission.institution,
        'customer_email': submission.email,
        'customer_phone': submission.phone,
        'items': products,
        'total_amount': f"{total:,.2f}"
    }

    # 4. Generate PDF in Memory (The Secret Sauce)
    html_string = render_to_string('quotation.html', context)
    pdf_file = io.BytesIO()
    pisa_status = pisa.CreatePDF(html_string, dest=pdf_file)
    
    if pisa_status.err:
        return Response({"error": "PDF Generation Failed"}, status=500)

    # 5. Create the Email
    subject = f"Your Quotation from Northern Meditech (Ref: QT-{submission.id:04d})"
    body = f"""
    Dear {submission.contact_person},

    Thank you for your interest in Northern Meditech.
    Please find attached the quotation for your requested medical equipment.

    Total Amount: KES {total:,.2f}

    Regards,
    Sales Team
    """

    email = EmailMessage(
        subject,
        body,
        settings.EMAIL_HOST_USER, # From
        [submission.email]        # To (The customer)
    )

    # 6. Attach the PDF
    email.attach(f"Quotation_{submission.id}.pdf", pdf_file.getvalue(), 'application/pdf')

    # 7. Send!
    email.send()

    return Response({"message": "Quotation sent to your email!"}, status=200)