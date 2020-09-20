import random
import uuid

from book.models import Book

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

import requests

import tqdm


class Command(BaseCommand):

    def handle(self, *args, **options):
        url = 'https://htmlstream.com/preview/unify-v2.6/assets/img-temp/400x270/img{}.jpg'
        queryset = Book.objects.all()

        pics = []
        for num in range(1, 29):
            url_get = url.format(num)
            response = requests.get(url_get, verify=False)
            response.raise_for_status()
            pics.append(response.content)

        for book in tqdm.tqdm(queryset.iterator(), total=queryset.count()):
            name = str(uuid.uuid4()) + '.jpg'
            book.cover.save(name, ContentFile(random.choice(pics)), save=True)
