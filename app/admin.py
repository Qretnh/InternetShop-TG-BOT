import logging

from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import render, redirect
from .forms import MailingForm
from .models import Categories, Orders, Products, Subcategories, Users, FAQ
from app.tasks import send_mailing_task


@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id',)  # Убрали mailing_action из list_display
    actions = ['send_mailing']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('send-mailing/', self.admin_site.admin_view(self.send_mailing_view), name='send_mailing'),
        ]
        return custom_urls + urls

    def send_mailing_view(self, request):
        if request.method == 'POST':
            form = MailingForm(request.POST)
            if form.is_valid():
                message = form.cleaned_data['message']
                buttons = form.cleaned_data['buttons'] or None

                # Получаем выбранных пользователей из сессии
                user_ids = request.session.get('mailing_user_ids', [])
                logging.info(user_ids)
                for user_id in user_ids:
                    send_mailing_task.delay(user_id, message, buttons)

                self.message_user(request, "Рассылка успешно отправлена.")
                return redirect('..')  # Возвращаемся на страницу списка пользователей
        else:
            form = MailingForm()

        context = {
            'form': form,
            'opts': self.model._meta,
            'app_label': self.model._meta.app_label,
        }
        return render(request, 'admin/mailing_form.html', context)

    def send_mailing(self, request, queryset):
        user_ids = list(queryset.values_list('id', flat=True))
        logging.info(user_ids)
        request.session['mailing_user_ids'] = user_ids

        # Перенаправляем на страницу с формой
        return redirect('admin:send_mailing')

    send_mailing.short_description = "Отправить рассылку через Telegram"

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        # Добавляем кастомную кнопку сверху
        extra_context['show_mailing_button'] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('category',)


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    fields = ('phone_number', 'email', 'items', 'price', 'complete', 'address', 'time')  # Отображаемые поля
    list_display = ('phone_number', 'email', 'items', 'price', 'complete', 'address', 'time')
    list_editable = ('complete',)
    search_fields = ('phone_number', 'email')
    ordering = ('id',)


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'subcategory', 'name', 'price', 'description', 'photo_id')


@admin.register(Subcategories)
class SubcategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')


@admin.register(FAQ)
class SubcategoriesAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')
