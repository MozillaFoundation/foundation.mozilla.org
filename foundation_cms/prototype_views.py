from django.shortcuts import render


def prototype_gallery(request):
    projects = [
        {
            "name": "Project 1",
            "image": "foundation_cms/_images/fallbacks/listing-page-1.png",
            "url": "#project-1",
        },
        {
            "name": "Project 2",
            "image": "foundation_cms/_images/fallbacks/listing-page-2.png",
            "url": "#project-2",
        },
        {
            "name": "Project 3",
            "image": "foundation_cms/_images/fallbacks/listing-page-3.png",
            "url": "#project-3",
        },
        {
            "name": "Project 4",
            "image": "foundation_cms/_images/fallbacks/listing-page-4.png",
            "url": "#project-4",
        },
        {
            "name": "Project 5",
            "image": "foundation_cms/_images/fallbacks/listing-page-5.png",
            "url": "#project-5",
        },
        {
            "name": "Project 6",
            "image": "foundation_cms/_images/fallbacks/listing-page-6.png",
            "url": "#project-6",
        },
    ]
    return render(request, "patterns/pages/prototype/gallery.html", {"projects": projects})
