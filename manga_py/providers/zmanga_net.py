from manga_py.provider import Provider
from .helpers.std import Std


class ZMangaNet(Provider, Std):

    def get_archive_name(self) -> str:
        return self.normal_arc_name(self.get_chapter_index())

    def get_chapter_index(self) -> str:
        re = self.re.compile(r'capitulo-(\d+(?:-\d+)?)')
        return re.search(self.chapter).group(1)

    def get_main_content(self):
        return self._get_content('{}/manga-online/{}/')

    def get_manga_name(self) -> str:
        re = r'\.\w+(?:/manga-online)?/([^/]+?)(?:-capitulo[^/]+)?/'
        return self._get_name(re)

    def get_chapters(self):
        return self._elements('.mangabox_line > a')

    def get_files(self):
        items = self.html_fromstring(self.chapter, 'meta[property="og:image:secure_url"]')
        return [i.get('content') for i in items]

    def get_cover(self) -> str:
        # return self._cover_from_content('.cover img')
        pass

    def book_meta(self) -> dict:
        pass


main = ZMangaNet
