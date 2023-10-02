import csv
import datetime
from django.http import HttpResponse
from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Order, OrderItem


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    content_disposition = f'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not \
              field.many_to_many and not field.one_to_many]
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response
export_to_csv.short_description = 'Export to CSV'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


def order_payment(obj):
    url = obj.get_stripe_url()
    if obj.stripe_id:
        html = f'<a href="{url}" target="_blank">{obj.stripe_id}</a>'
        return mark_safe(html)
    return ''
order_payment.short_description = 'Stripe payment'

def order_detail(obj):
    url = reverse('orders:admin_order_detail', args=[obj.id])
    return mark_safe(f'<a href="{url}">View</a>')


def order_pdf(obj):
    url = reverse('orders:admin_order_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')
order_pdf.short_description = 'Invoice'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'sobrenome', 'email',
                    'endereco', 'CEP', 'cidade', 'pago',
                    'order_payment', 'criado_em', 'atualizado_em',
                    'order_detail', 'order_pdf']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]
    
    def nome(self, obj):
        return obj.first_name
    
    def sobrenome(self, obj):
        return obj.last_name
    
    def endereco(self, obj):
        return obj.address
    
    def CEP(self, obj):
        return obj.postal_code
    
    def cidade(self, obj):
        return obj.city
    
    def pago(self, obj):
        return "Pago" if obj.paid else "Não Pago"
    
    def criado_em(self, obj):
        return obj.created
    
    def atualizado_em(self, obj):
        return obj.updated
    
    def order_detail(self, obj):
        url = reverse('orders:admin_order_detail', args=[obj.id])
        return mark_safe(f'<a href="{url}">View</a>')
    order_detail.short_description = 'Order Detail'
    
    def order_pdf(self, obj):
        url = reverse('orders:admin_order_pdf', args=[obj.id])
        return mark_safe(f'<a href="{url}">PDF</a>')
    order_pdf.short_description = 'Invoice'
    
    def order_payment(self, obj):
        url = obj.get_stripe_url()
        if obj.stripe_id:
            html = f'<a href="{url}" target="_blank">{obj.stripe_id}</a>'
            return mark_safe(html)
        return ''
    order_payment.short_description = 'Stripe payment'
    
    # Custom labels for these new fields
    nome.short_description = "Nome"
    sobrenome.short_description = "Sobrenome"
    endereco.short_description = "Endereço"
    CEP.short_description = "CEP"
    cidade.short_description = "Cidade"
    pago.short_description = "Pago"
    criado_em.short_description = "Criado em"
    atualizado_em.short_description = "Atualizado em"


