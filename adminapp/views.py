from django.contrib.auth.decorators import user_passes_test
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, \
    DetailView

from adminapp.forms import ShopUserAdminEditForm, ProductCategoryForm, \
    ProductCreateForm
from adminapp.utils import AdminAccessMixin
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import Product, Category


# @user_passes_test(lambda u: u.is_superuser)
# def users(request):
#     context = {
#         'object_list': ShopUser.objects.all().order_by('-is_active')
#     }
#     return render(request, 'adminapp/users_list.html', context=context)

class UsersListView(AdminAccessMixin, ListView):
    model = ShopUser
    template_name = 'adminapp/users_list.html'

    def get_queryset(self):
        return ShopUser.objects.order_by('?')


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('adminapp:users'))
    else:
        user_form = ShopUserRegisterForm()
    context = {
        'form': user_form
    }
    return render(request, 'adminapp/user_form.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    current_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        user_form = ShopUserAdminEditForm(
            request.POST,
            request.FILES,
            instance=current_user
        )
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('adminapp:users'))
    else:
        user_form = ShopUserAdminEditForm(instance=current_user)
    context = {
        'form': user_form
    }
    return render(request, 'adminapp/user_form.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    current_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        current_user.is_active = False
        current_user.save()
        return HttpResponseRedirect(reverse('adminapp:users'))

    context = {
        'object': current_user,
    }

    return render(request, 'adminapp/user_delete.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    context = {
        'object_list': Category.objects.all()
    }
    return render(request, 'adminapp/categories_list.html', context=context)


# @user_passes_test(lambda u: u.is_superuser)
# def category_create(request):
#     if request.method == 'POST':
#         category_form = ProductCategoryForm(request.POST)
#         if category_form.is_valid():
#             category_form.save()
#             return HttpResponseRedirect(reverse('adminapp:categories'))
#     else:
#         category_form = ProductCategoryForm()
#     context = {
#         'form': category_form
#     }
#     return render(request, 'adminapp/category_form.html', context=context)

class CategoryCreate(AdminAccessMixin, CreateView):
    model = Category
    template_name = 'adminapp/category_form.html'
    # fields = '__all__'
    form_class = ProductCategoryForm
    success_url = reverse_lazy('adminapp:categories')


# @user_passes_test(lambda u: u.is_superuser)
# def category_update(request, pk):
#     category_item = get_object_or_404(Category, pk=pk)
#     if request.method == 'POST':
#         category_form = ProductCategoryForm(
#             request.POST,
#             instance=category_item
#         )
#         if category_form.is_valid():
#             category_form.save()
#             return HttpResponseRedirect(reverse('adminapp:categories'))
#     else:
#         category_form = ProductCategoryForm(instance=category_item)
#     context = {
#         'form': category_form
#     }
#     return render(request, 'adminapp/category_form.html', context=context)


class CategoryUpdate(AdminAccessMixin, UpdateView):
    model = Category
    template_name = 'adminapp/category_form.html'
    # fields = '__all__'
    form_class = ProductCategoryForm
    success_url = reverse_lazy('adminapp:categories')

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.product_set.update(price=F('price') * (
                        1-discount/100))
        return super().form_valid(form)


# @user_passes_test(lambda u: u.is_superuser)
# def category_delete(request, pk):
#     category_item = get_object_or_404(Category, pk=pk)
#     if request.method == 'POST':
#         category_item.is_active = False
#         category_item.save()
#         return HttpResponseRedirect(reverse('adminapp:categories'))
#
#     context = {
#         'object': category_item,
#     }
#
#     return render(request, 'adminapp/category_delete.html', context=context)

class DeleteCategory(AdminAccessMixin, DeleteView):
    model = Category
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('adminapp:categories')


@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    context = {
        'category_id': pk,
        'category_name': get_object_or_404(Category, pk=pk),
        'object_list': Product.objects.filter(category__pk=pk),
    }

    return render(request, 'adminapp/products_list.html', context=context)


# @user_passes_test(lambda u: u.is_superuser)
# def product_create(request, pk):
#     category_item = get_object_or_404(Product, pk)
#     if request.method == 'POST':
#         product_form = ProductCreateForm(request.POST, request.FILES)
#         if product_form.is_valid():
#             product_form.save()
#             return HttpResponseRedirect(
#                 reverse(
#                     'adminapp:products',
#                     kwargs={"pk": pk}
#                 )
#             )
#     else:
#         product_form = ProductCreateForm()
#
#     context = {
#         'category_id': pk,
#         'form': product_form
#     }
#     return render(request, 'adminapp/product_form.html', context=context)

class ProductCreate(AdminAccessMixin, CreateView):
    model = Product
    template_name = 'adminapp/product_form.html'
    form_class = ProductCreateForm

    def _get_category(self):
        category_id = self.kwargs.get('pk')
        return get_object_or_404(
            Category,
            pk=category_id
        )

    def get_success_url(self):
        return reverse(
            'adminapp:products',
            kwargs={"pk": self._get_category().pk}
        )

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['category_id'] = self._get_category().pk
        return context_data


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    product_item = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product_form = ProductCreateForm(
            request.POST,
            instance=product_item
        )
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('adminapp:categories'))
    else:
        product_form = ProductCreateForm(instance=product_item)
    context = {
        'form': product_form
    }
    return render(request, 'adminapp/category_form.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    product_item = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product_item.is_active = False
        product_item.save()
        return HttpResponseRedirect(reverse('adminapp:categories'))

    context = {
        'object': product_item,
    }

    return render(request, 'adminapp/product_delete.html', context=context)


# @user_passes_test(lambda u: u.is_superuser)
# def product_read(request, pk):
#     context = {
#         'object': get_object_or_404(Product, pk=pk),
#     }
#
#     return render(request, 'adminapp/product_detail.html', context=context)

class ProductDetail(AdminAccessMixin, DetailView):
    model = Product
    template_name = 'adminapp/product_detail.html'
