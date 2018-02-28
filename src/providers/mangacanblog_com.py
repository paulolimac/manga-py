from urllib.parse import unquote_plus

from src.provider import Provider
from .helpers.std import Std


class MangaCanBlogCom(Provider, Std):
    _home_link = None

    def get_archive_name(self) -> str:
        ch = self.chapter
        idx = self.re.search(r'/.+/.+?(?:-indonesia-)(.+)\.html', ch)
        if not idx:
            idx = self.re.search(r'/.+/(.+)\.html', ch)
        idx = idx.group(1)
        if idx.find('-terbaru') > 0:
            idx = idx[:idx.find('-terbaru')]
        return 'vol_{:0>3}-{}'.format(
            self._chapter_index(),
            idx
        )

    def get_chapter_index(self) -> str:
        return str(self._chapter_index())

    def get_main_content(self):
        return self.http_get(self._home_link)

    @staticmethod
    def _clear_name(a):
        name = a[0].text_content()
        name = unquote_plus(name.split('|')[0].strip())
        if name.find(' Indonesia') > 0:
            name = name[:name.find(' Indonesia')]
        return name

    def get_manga_name(self) -> str:
        url = self.get_url()
        selector = '.navbar a[href*=".html"]'
        content = self.http_get(url)
        a = self.document_fromstring(content)
        is_chapter = a.cssselect(selector)
        if len(is_chapter) < 1:
            selector = '#latestchapters h1'
            a = a.cssselect(selector)
            self._home_link = url
        else:
            a = is_chapter
            self._home_link = a[0].get('href')
        return self._clear_name(a)

    def get_chapters(self):
        items = self._elements('a.chaptersrec')
        result = []
        for i in items:
            url = i.get('href')
            _ = url.find('-terbaru-1')
            if _:
                url = url[:_] + '-terbaru.html'
            result.append(url)
        return result

    def get_files(self):
        content = self.http_get(self.chapter)
        items = self._elements('#imgholder .picture', content)
        return [i.get('src') for i in items]

    def get_cover(self) -> str:
        # return self._cover_from_content('.cover img')
        pass


main = MangaCanBlogCom
