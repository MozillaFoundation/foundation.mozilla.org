from django.shortcuts import render

PALETTE = [
    "#FF6B6B",
    "#4ECDC4",
    "#45B7D1",
    "#96CEB4",
    "#FFEAA7",
    "#DDA0DD",
    "#98D8C8",
    "#F7DC6F",
]


def prototype_gallery(request):
    projects = []
    for i in range(1, 25):
        if i <= 6:
            projects.append(
                {
                    "name": f"Project {i}",
                    "image": f"foundation_cms/_images/fallbacks/listing-page-{i}.png",
                    "bg_color": None,
                    "url": f"/project-{i}",
                }
            )
        else:
            projects.append(
                {
                    "name": f"Project {i}",
                    "image": None,
                    "bg_color": PALETTE[(i - 1) % len(PALETTE)],
                    "url": f"/project-{i}",
                }
            )
    return render(request, "patterns/pages/prototype/gallery.html", {"projects": projects})
