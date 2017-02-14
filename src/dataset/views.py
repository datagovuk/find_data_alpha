import math

from django.http import Http404
from django.shortcuts import render

from .search import search_query, search_single_dataset

from stats.models import StatRecord

def view_dataset(request, slug):
    dataset = search_single_dataset(slug)
    if not dataset:
        raise Http404()

    StatRecord.record_now(
        dataset['organisation']['id'],
        dataset['id'],
        dataset['title'],
        'view'
    )

    return render(request, 'dataset/view.html', {'dataset': dataset})


def search(request):
    query = request.GET.get('q')

    page = 1
    try:
        page = int(request.GET.get('page'))
    except:
        page = 1

    page_size = 20
    datasets, total = search_query(query, offset=(page * page_size) - page_size, limit=page_size)
    page_count = math.ceil(float(total) / page_size)

    if query:
        StatRecord.record_bulk_now(
            [d['organisation']['id'] for d in datasets],
            [d['id'] for d in datasets],
            [d['title'] for d in datasets],
            'search'
        )

    return render(request, 'dataset/search.html', {
        'datasets': datasets,
        'total': total,
        'page_count': page_count,
        'page_range':  range(1, page_count+1),
        'current_page': page,
        'q': query or ""
    })


