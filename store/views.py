from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.db.models import Count
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Category, Product
from .forms import ProductForm


# ==============================
# საერთო ლოგიკა სამივე სიის view-სთვის
# (კატეგორიების annotate ყველგან ერთნაირად სჭირდება)
# ==============================
class StoreContextMixin:
    def get_categories(self):
        return Category.objects.annotate(
            product_count=Count('products')
        ).filter(product_count__gt=0)



class ProductFilterMixin:
    def filter_queryset(self, queryset):
        request = self.request

        search = request.GET.get('q', '').strip()
        if search:
            queryset = queryset.filter(name__icontains=search)

        min_price = request.GET.get('min_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        max_price = request.GET.get('max_price')
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        if request.GET.get('discounted_only'):
            queryset = queryset.filter(is_discounted=True)

        category_id = request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        return queryset

    

    def sort_queryset(self, queryset):          
        sort = self.request.GET.get('sort', '')
        sort_options = {
            'price_asc': 'price',
            'price_desc': '-price',
            'name_asc': 'name',
            'name_desc': '-name',
            'newest': '-created_at',
        }
        order_by = sort_options.get(sort)
        if order_by:
            return queryset.order_by(order_by)
        return queryset
    

    def get_filter_context(self):
        request = self.request
        return {
            'search_query': request.GET.get('q', ''),
            'min_price': request.GET.get('min_price', ''),
            'max_price': request.GET.get('max_price', ''),
            'discounted_only': request.GET.get('discounted_only', ''),
            'current_sort': request.GET.get('sort', ' ')
        }


# ==============================
# ყველა პროდუქტი (home)
# ==============================
class ProductListView(StoreContextMixin, ProductFilterMixin, ListView):
    model = Product
    template_name = 'store/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        qs = Product.objects.all()
        qs = self.filter_queryset(qs)
        qs = self.sort_queryset(qs)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = self.get_categories()
        context['page_title'] = 'ყველა პროდუქტი'
        context.update(self.get_filter_context())

        category_id = self.request.GET.get('category')
        if category_id:
            context['selected_category'] = get_object_or_404(Category, id=category_id)

        return context


# ==============================
# კატეგორიის მიხედვით გაფილტრული პროდუქტები
# ==============================
class CategoryProductListView(StoreContextMixin, ProductFilterMixin, ListView):
    model = Product
    template_name = 'store/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['category_id'])
        qs = Product.objects.filter(category=self.category).order_by('price')
        return self.filter_queryset(qs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = self.get_categories()
        context['selected_category'] = self.category
        context['page_title'] = f'კატეგორია: {self.category.name}'
        context.update(self.get_filter_context())
        return context


# ==============================
# ფასდაკლებული პროდუქტები
# ==============================
class DiscountedProductListView(StoreContextMixin, ProductFilterMixin, ListView):
    model = Product
    template_name = 'store/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        qs = Product.objects.filter(is_discounted=True).order_by('price')
        return self.filter_queryset(qs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = self.get_categories()
        context['page_title'] = 'ფასდაკლებული პროდუქტები'
        context.update(self.get_filter_context())
        return context


# ==============================
# პროდუქტის დამატება (Create)
# ==============================
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'store/product_form.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'ახალი პროდუქტის დამატება'
        return context


# ==============================
# პროდუქტის განახლება (Update)
# ==============================
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'store/product_form.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'განახლება: {self.object.name}'
        return context


# ==============================
# პროდუქტის წაშლა (Delete)
# ==============================
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'store/product_confirm_delete.html'
    context_object_name = 'product'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'წაშლის დადასტურება'
        return context
