import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from catalog.forms import RenewBookForm
from django.views import generic
from .models import Book, Author, BookInstance, Genre
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from catalog.models import Author


# Create your views here:

@login_required
def index(request):
    #View function for home page of the site.

    #generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    #Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    #The 'all()' is implied by default
    num_authors = Author.objects.count()

    #Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    
    #This showcases how to search for filtered data
    num_adventure_genre = Genre.objects.filter(name__icontains='adventure').count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
        'num_adventure_genre': num_adventure_genre,
    }
    #Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

#@login_required
class BookListView(generic.ListView):
    # --------- THESE FUCNTIONS CAN BE USED INPLACE OF 'queryset' AND 'context_object_name' -----------
    #def get_queryset(self): 
    #    return Book.objects.filter(title__icontains='hunger')[:5] #Get 5 books containing the title 'hunger'

    #def get_context_data(self, **kwargs):
    #    # Call the base implementation first to get the context
    #    context = super(BookListView, self).get_context_data(**kwargs)
    #    # Create any data and add it to the context
    #    context['some_data'] = 'This is just some data'
    #    return context

    model = Book
    context_object_name = 'book_list' # your own name for the list as a template variable
    #queryset = Book.objects.filter(title__icontains='hunger')[:5] #Get 5 books containing the title 'hunger'
    template_name = 'books/my_arbitrary_template_name_list.html' #Specify your own template name/location
    paginate_by = 3

#@login_required
class BookDetailView(generic.DetailView):
    model = Book
    paginate_by = 3

##@login_required
class AuthorListView(generic.ListView):
    model = Author
    context_object_name = 'author_list'
    template_name = 'authors/my_arbitrary_template_name_list.html'
    paginate_by = 3

#@login_required
class AuthorDetailView(generic.DetailView):
    model = Author
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    paginate_by = 3


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    #Generic calss-based view listing books on loan to current user.
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class LibrarianLoanedBooksListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_librarian.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    #If this is a post request then process the form data
    if request.method == 'POST':

        #Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        #Check if the form is valid:
        if form.is_valid():
            #process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            return HttpResponseRedirect(reverse('all-borrowed-books'))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }


    return render(request, 'catalog/book_renew_librarian.html', context)


class AuthorCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'catalog.can_mark_returned'
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/06/2020'}

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.can_mark_returned'
    model = Author
    fields = '__all__' # Not recommended (potential security issue if more fields are added).

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'catalog.can_mark_returned'
    model = Author
    success_url = reverse_lazy('authors')

class BookCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'catalog.can_mark_returned'
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']
    #initial = {'language': 'English'}

class BookUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.can_mark_returned'
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']

class BookDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'catalog.can_mark_returned'
    model = Book
    success_url = reverse_lazy('books')
