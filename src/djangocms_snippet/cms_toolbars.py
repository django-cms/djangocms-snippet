from cms.cms_toolbars import (
    ADMIN_MENU_IDENTIFIER,
    ADMINISTRATION_BREAK,
    SHORTCUTS_BREAK,
)
from cms.toolbar.items import Break
from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from cms.utils.urlutils import admin_reverse
from django.utils.encoding import force_str
from django.utils.translation import (
    gettext_lazy as _,
)


@toolbar_pool.register
class SnippetToolbar(CMSToolbar):
    name = _("Snippet")
    plural_name = _("Snippets")

    def populate(self):
        self.add_snippet_link_to_admin_menu()

    def add_snippet_link_to_admin_menu(self):
        admin_menu = self.toolbar.get_or_create_menu(ADMIN_MENU_IDENTIFIER)

        url = admin_reverse('djangocms_snippet_snippet_changelist')

        admin_menu.add_sideframe_item(
            _("Snippets"),
            url=url,
            position=self.get_insert_position(admin_menu, self.plural_name),
        )

    @classmethod
    def get_insert_position(cls, admin_menu, item_name):
        """
        Ensures that there is a SHORTCUTS_BREAK and returns a position for an
        alphabetical position against all items between SHORTCUTS_BREAK, and
        the ADMINISTRATION_BREAK.
        """
        start = admin_menu.find_first(Break, identifier=SHORTCUTS_BREAK)

        if not start:
            end = admin_menu.find_first(Break, identifier=ADMINISTRATION_BREAK)
            admin_menu.add_break(SHORTCUTS_BREAK, position=end.index)
            start = admin_menu.find_first(Break, identifier=SHORTCUTS_BREAK)
        end = admin_menu.find_first(Break, identifier=ADMINISTRATION_BREAK)

        items = admin_menu.get_items()[start.index + 1: end.index]
        for idx, item in enumerate(items):
            try:
                if force_str(item_name.lower()) < force_str(item.name.lower()):  # noqa: E501
                    return idx + start.index + 1
            except AttributeError:
                # Some item types do not have a 'name' attribute.
                pass
        return end.index
