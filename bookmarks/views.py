from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from .models import Tag, Bookmark


def index(request):
    try:
        search_words = request.POST['search']
        if not search_words:
            bookmarks = Bookmark.objects.filter(archived=False)
            return render(request, 'bookmarks/index.html', {'links': bookmarks, 'tags': Tag.objects.all(), 'title': 'Home'})

        search_word = search_words.split("tag")[0]
        bookmarks = Bookmark.objects.filter(Q(name__icontains=search_word) | Q(description__icontains=search_word))
    except KeyError:
        bookmarks = Bookmark.objects.filter(archived=False)

    if not bookmarks:
        return render(request, 'bookmarks/index.html', {'warning': 'No Bookmarks found!', 'tags': Tag.objects.all(), 'title': 'Home'})
    else:
        return render(request, 'bookmarks/index.html', {'links': bookmarks, 'tags': Tag.objects.all(), 'title': 'Home'})


def archive_bookmarks(request):
    bookmarks = Bookmark.objects.filter(archived=True)
    return render(request, 'bookmarks/index.html', {'links': bookmarks, 'tags': Tag.objects.all(), 'title': 'Archive'})


def archive_bookmark(request, bookmark_id):
    bookmark = Bookmark.objects.filter(pk=bookmark_id).first()
    bookmark.archived = True
    bookmark.save()

    bookmarks = Bookmark.objects.filter(archived=True)
    return render(request, 'bookmarks/index.html', {'links': bookmarks, 'tags': Tag.objects.all(), 'title': 'Archive'})


def tag(request, tag_id):
    tag = Tag.objects.get(pk=tag_id)
    bookmarks = Bookmark.objects.filter(tags=tag)

    if not bookmarks:
        return render(request, 'bookmarks/index.html', {'warning': 'No Bookmarks found!', 'tags': Tag.objects.all(), 'title': 'Home'})
    else:
        return render(request, 'bookmarks/index.html', {'links': bookmarks, 'tags': Tag.objects.all(), 'title': 'Home'})


def create(request):
    bookmarks = Bookmark.objects.filter(archived=False)

    try:
        name = request.POST['name']
        description = request.POST['description']
        link = request.POST['link']

        if name and description and link:
            bookmark = Bookmark.objects.create(name=name, description=description, link=link)

            for tag in Tag.objects.all():
                if f"checked-{tag.id}" in request.POST:
                    if request.POST['checked-' + str(tag.id)] == 'on':
                        bookmark.tags.add(tag.id)
            bookmark.save()

            return render(request, 'bookmarks/index.html',
                          {'links': bookmarks, 'tags': Tag.objects.all(),
                           'successtoast': 'Bookmark successfully created!', 'title': 'Home'})
    except KeyError:
        return render(request, 'bookmarks/index.html',
                      {'links': bookmarks, 'tags': Tag.objects.all(), 'successtoast': 'Error while validatingk', 'title': 'Home'})


def edit_bookmark(request, bookmark_id):
    bookmark = get_object_or_404(Bookmark)


def edit_tag(request, tag_id):
    pass


def delete_bookmark(request, bookmark_id):
    return_status = Bookmark.objects.filter(pk=bookmark_id).delete()

    bookmarks = Bookmark.objects.filter(archived=False)
    if return_status[0] == 0:
        return render(request, 'bookmarks/index.html',
                      {'links': bookmarks, 'tags': Tag.objects.all(), 'successtoast': 'Bookmark not found!', 'title': 'Home'})
    else:
        return render(request, 'bookmarks/index.html',
                      {'links': bookmarks, 'tags': Tag.objects.all(), 'title': 'Home'})
