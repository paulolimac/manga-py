from src.provider import Provider
from .helpers.std import Std


class JurnaluRu(Provider, Std):

    def get_archive_name(self) -> str:
        name = self.get_manga_name()
        arc_name = self.re.search('/{0}/{0}([^/]+)'.format(name), self.get_current_chapter())
        if arc_name:
            pass
        return 'vol_{}'.format(self.get_chapter_index())

    def get_chapter_index(self) -> str:
        return str(self._storage['current_chapter'])

    def get_main_content(self):
        name = self._get_name(r'(online-reading/[^/]+/[^/]+)')
        url = self.html_fromstring(
            '{}/{}'.format(self.get_domain(), name),
            '.MagList .MagListLine > a',
            0
        ).get('href')
        return self.http_get(self.get_domain() + url)

    def get_manga_name(self) -> str:
        return self._get_name(r'/online-reading/[^/]+/([^/]+)')

    def get_chapters(self):
        name = self.re.search(r'(online-reading/[^/]+/[^/]+)', self.get_url())
        if not name:
            return []
        items = self.document_fromstring(self.get_storage_content(), 'select.magSelection option')
        url = '{}/{}/'.format(self.get_domain(), name.group(1))
        return [url + i.get('value') for i in items]

    @staticmethod
    def __get_file(parser):
        image = parser.cssselect('a[rel="shadowbox"]')
        return image[0].get('href')

    def get_files(self):
        chapter = self.get_current_chapter()
        page = self.html_fromstring(chapter, '.ForRead', 0)
        pages = page.cssselect('.navigation')[0].cssselect('select.M option + option')
        images = [self.__get_file(page)]
        for i in pages:
            uri = '{}/{}'.format(chapter, i.get('value'))
            parser = self.html_fromstring(uri, '.ForRead', 0)
            images.append(self.__get_file(parser))
        return images

    def get_cover(self):
        return self._cover_from_content('.ops > div > img')


main = JurnaluRu
