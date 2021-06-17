from category.models import Category
# utiliser les context processors pour rendre le contenu accessible partout

def menu_links(request):
    links = Category.objects.all()
    return dict(links =links)