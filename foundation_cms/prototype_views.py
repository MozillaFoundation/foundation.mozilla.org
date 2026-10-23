"""
Temporary previews of redesign components that don't have a page type to live
on yet. Delete each view once a real page renders its component.
"""

from django.shortcuts import render


def meteor_hero_preview(request):
    """
    Previews the Meteor hero for review.
    """
    # TODO: Remove this view, its URL, template and tests once the Our Work page
    # type (TP1-4395) renders the Meteor hero.
    return render(
        request,
        "patterns/pages/prototype/meteor_hero.html",
        {
            "headline": "Better technology won't build itself. We back the people building it.",
            "target_id": "meteor-hero-preview-content",
        },
    )


def galaxy_hero_preview(request):
    """Preview Galaxy independently until homepage assembly (TP1-4385)."""
    backgrounds = ("Gray", "Orange", "Yellow", "Blue")
    background = request.GET.get("background", "Gray")
    return render(
        request,
        "patterns/pages/prototype/galaxy_hero.html",
        {
            "headline": "Mozilla Foundation expands\nwho shapes technology",
            "second_headline": "Because the future should be\nin the hands of many.",
            "background": background if background in backgrounds else "Gray",
            "target_id": "galaxy-hero-preview-content",
        },
    )
