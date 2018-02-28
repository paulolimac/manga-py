from src.provider import Provider
from .helpers.std import Std


class WMangaRu(Provider, Std):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index()
        return 'vol_{:0>3}-{}'.format(*idx)

    def get_chapter_index(self) -> str:
        selector = r'/manga_chapter/[^/]+/(\d+)/(\d+)'
        idx = self.re.search(selector, self.chapter).groups()
        return '{}-{}'.format(*idx)

    def get_main_content(self):
        return self._get_content('{}/starter/manga_byid/{}')

    def get_manga_name(self) -> str:
        return self._get_name('/starter/manga_[^/]+/([^/]+)')

    def get_chapters(self):
        return self._elements('td div div div td > a')[::-1]

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        return self._images_helper(parser, 'td a.gallery', 'href')

    def get_cover(self):
        pass  # FIXME HOME


main = WMangaRu
