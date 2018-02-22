from src.provider import Provider
from .helpers.std import Std


class MangaOnlineToday(Provider, Std):
    __img_selector = '#sct_content img'

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{:0>3}-{}'.format(*idx)

    def get_chapter_index(self) -> str:
        idx = self.re.search(r'\.today/[^/]+/([^/]+)', self.get_current_chapter())
        idx = idx.group(1).split('.')
        return '{}-{}'.format(*self._idx_to_x2(idx))

    def get_main_content(self):
        return self.http_get('{}/{}/'.format(self.get_domain(), self.get_manga_name()))

    def get_manga_name(self) -> str:
        return self._get_name(r'\.today/([^/]+)')

    def get_chapters(self):
        return self._elements('ul.chp_lst a')

    def _pages_helper(self, options):
        images = []
        chapter = self.get_current_chapter()
        for n in range(1, int(options)):
            content = self.html_fromstring('{}{}/'.format(chapter, n * 2))
            img = content.cssselect(self.__img_selector)
            for i in img:
                images.append(i.get('src'))
        return images

    def get_files(self):
        images = []
        content = self.html_fromstring(self.get_current_chapter())
        img = content.cssselect(self.__img_selector)
        if img:
            images = [i.get('src') for i in img]

        options = len(content.cssselect('.cbo_wpm_pag')[0].cssselect('option')) / 2 + .5
        return images + self._pages_helper(options)

    def get_cover(self):
        pass  # TODO


main = MangaOnlineToday
