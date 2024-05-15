from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomerForm, DocumentForm
from .models import CustomerModel, CustomerDocumentModel
from .utils import extract_text_from_document
import json

def create_customer(request):
    if request.method == 'POST':
        customer_form = CustomerForm(request.POST)
        if customer_form.is_valid():
            customer = customer_form.save(commit=False)
            customer.created_by = request.user
            customer.save()
            messages.success(request, 'Customer information saved successfully.')
            return redirect('upload_document', customer_id=customer.id)
        else:
            messages.error(request, 'Failed to save customer information. Please check the form.')
    else:
        customer_form = CustomerForm()

    return render(request, 'create_customer.html', {'customer_form': customer_form})

def upload_document(request, customer_id):
    customer = CustomerModel.objects.get(id=customer_id)

    if request.method == 'POST':
        document_form = DocumentForm(request.POST, request.FILES)
        if document_form.is_valid():
            document = document_form.save(commit=False)
            document.customer = customer
            document.save()

            extracted_data = extract_text_from_document(document.attached_file.path)
            document.extracted_json = json.dumps(extracted_data)
            document.save()

            # Compare extracted data with customer data
            form_data = {
                'Name': f"{customer.first_name} {customer.surname}",
            }

            if 'Name' in extracted_data:
                extracted_name = extracted_data['Name'].upper()
                form_name = form_data['Name'].upper()
                print(extracted_name, form_name, "EeE")

                if extracted_name == form_name:
                    messages.success(request, 'Customer and document verified successfully.')
                else:
                    messages.error(request, 'Document data does not match customer data.')
                    return render(request, 'upload_document.html', {'document_form': document_form, 'customer': customer})
            else:
                messages.error(request, 'Failed to extract name from document.')

            return redirect('list_customers')
        else:
            messages.error(request, 'Failed to upload document. Please try again.')
    else:
        document_form = DocumentForm()

    return render(request, 'upload_document.html', {'document_form': document_form, 'customer': customer})


def list_customers(request):
    customers = CustomerModel.objects.all()
    return render(request, 'list_customers.html', {'customers': customers})
