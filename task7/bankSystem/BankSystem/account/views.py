# from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
# from django.shortcuts import render
# from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# from .models import BankAccount
#
# class BankAccountListView(LoginRequiredMixin, ListView):
#     model = BankAccount
#     template_name = 'account/bankaccount_list.html'
#     context_object_name = 'bankaccounts'
#     ordering = ['account_number']
# class BankAccountDetailView(LoginRequiredMixin, DetailView):
#     model = BankAccount
#     template_name = 'account/bankaccount_detail.html'
#     context_object_name = 'bankaccount'
# class BankAccountCreateView(LoginRequiredMixin, CreateView):
#     model = BankAccount
#     fields = ['account_number', 'balance']
#
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)
# class BankAccountUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
#     model = BankAccount
#     fields = ['account_number', 'balance']
#
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)
# class BankAccountDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
#     model = BankAccount
#     success_url = '/account/'