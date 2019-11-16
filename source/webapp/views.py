from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from webapp.forms import ProductReviewsForm
from webapp.models import Product, Review


class IndexView(ListView):
    model = Product
    template_name = 'index.html'


class ProductView(DetailView):
    model = Product
    template_name = 'product/detail.html'


class ProductCreateView(LoginRequiredMixin,CreateView):
    model = Product
    template_name = 'product/create.html'
    fields = ('name', 'category', 'photo', 'description')

    def get_success_url(self):
        return reverse('webapp:product_detail', kwargs={'pk': self.object.pk})


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'product/update.html'
    fields = ('name', 'category', 'photo', 'description')
    context_object_name = 'product'

    def get_success_url(self):
        return reverse('webapp:product_detail', kwargs={'pk': self.object.pk})




class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'product/delete.html'
    success_url = reverse_lazy('webapp:index')
    context_object_name = 'product'


class ReviewForProductCreateView(LoginRequiredMixin, CreateView):
    model = Review
    template_name = 'review/create.html'
    form_class = ProductReviewsForm

    def dispatch(self, request, *args, **kwargs):
        self.product = self.get_product()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = self.product.goods.create(
            author=self.request.user,
            **form.cleaned_data
        )
        return redirect('webapp:product_detail', pk=self.product.pk)

    def get_product(self):
        product_pk = self.kwargs.get('pk')
        return get_object_or_404(Product, pk=product_pk)



class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    template_name = 'review/update.html'
    fields = ('good', 'text', 'author', 'mark')
    context_object_name = 'review'

    def get_success_url(self):
        return reverse('webapp:product_detail', kwargs={'pk': self.object.good.pk})


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = 'review/delete.html'
    context_object_name = 'review'


    def get_success_url(self):
        return reverse('webapp:product_detail', kwargs={'pk': self.object.good.pk})