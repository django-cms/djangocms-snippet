import string

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site

from cms import constants
from cms.models import Page, PageContent, PageUrl, Placeholder, TreeNode

import factory
from factory.fuzzy import FuzzyChoice, FuzzyInteger, FuzzyText

from djangocms_versioning.models import Version

from djangocms_snippet.models import (
    Snippet,
    SnippetGrouper,
    SnippetPtr
)


class PlaceholderFactory(factory.django.DjangoModelFactory):
    default_width = FuzzyInteger(0, 25)
    slot = FuzzyText(length=2, chars=string.digits)
    # NOTE: When using this factory you will probably want to set
    # the source field manually

    class Meta:
        model = Placeholder


class UserFactory(factory.django.DjangoModelFactory):
    username = FuzzyText(length=12)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.LazyAttribute(
        lambda u: "%s.%s@example.com" % (u.first_name.lower(), u.last_name.lower())
    )

    class Meta:
        model = User

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with our custom call."""
        manager = cls._get_manager(model_class)
        # The default would use ``manager.create(*args, **kwargs)``
        return manager.create_user(*args, **kwargs)


class AbstractVersionFactory(factory.django.DjangoModelFactory):
    object_id = factory.SelfAttribute("content.id")
    content_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.content)
    )
    created_by = factory.SubFactory(UserFactory)

    class Meta:
        exclude = ["content"]
        abstract = True


class TreeNodeFactory(factory.django.DjangoModelFactory):
    site = factory.fuzzy.FuzzyChoice(Site.objects.all())
    depth = 0
    # NOTE: Generating path this way is probably not a good way of
    # doing it, but seems to work for our present tests which only
    # really need a tree node to exist and not throw unique constraint
    # errors on this field. If the data in this model starts mattering
    # in our tests then something more will need to be done here.
    path = FuzzyText(length=8, chars=string.digits)

    class Meta:
        model = TreeNode


class PageFactory(factory.django.DjangoModelFactory):
    node = factory.SubFactory(TreeNodeFactory)

    class Meta:
        model = Page


class PageContentFactory(factory.django.DjangoModelFactory):
    page = factory.SubFactory(PageFactory)
    language = FuzzyChoice(["en", "fr", "it"])
    title = FuzzyText(length=12)
    page_title = FuzzyText(length=12)
    menu_title = FuzzyText(length=12)
    meta_description = FuzzyText(length=12)
    redirect = FuzzyText(length=12)
    created_by = FuzzyText(length=12)
    changed_by = FuzzyText(length=12)
    in_navigation = FuzzyChoice([True, False])
    soft_root = FuzzyChoice([True, False])
    limit_visibility_in_menu = constants.VISIBILITY_USERS
    template = 'page.html'
    xframe_options = FuzzyInteger(0, 25)

    class Meta:
        model = PageContent


class PageVersionFactory(AbstractVersionFactory):
    content = factory.SubFactory(PageContentFactory)

    class Meta:
        model = Version


class PageContentWithVersionFactory(PageContentFactory):
    @factory.post_generation
    def version(self, create, extracted, **kwargs):
        # NOTE: Use this method as below to define version attributes:
        # PageContentWithVersionFactory(version__label='label1')
        if not create:
            # Simple build, do nothing.
            return
        PageVersionFactory(content=self, **kwargs)


class SnippetGrouperFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = SnippetGrouper


class AbstractSnippetFactory(factory.django.DjangoModelFactory):
    name = FuzzyText(length=12)
    slug = FuzzyText(length=12)
    snippet_grouper = factory.SubFactory(SnippetGrouperFactory)

    class Meta:
        abstract = True


class SnippetFactory(AbstractSnippetFactory):
    class Meta:
        model = Snippet


class SnippetVersionFactory(AbstractVersionFactory):
    content = factory.SubFactory(SnippetFactory)

    class Meta:
        model = Version


class SnippetWithVersionFactory(AbstractSnippetFactory):
    @factory.post_generation
    def version(self, create, extracted, **kwargs):
        # NOTE: Use this method as below to define version attributes:
        # PageContentWithVersionFactory(version__label='label1')
        if not create:
            # Simple build, do nothing.
            return
        SnippetVersionFactory(content=self, **kwargs)

    class Meta:
        model = Snippet


def get_plugin_position(plugin):
    """Helper function to correctly calculate the plugin position.
    Use this in plugin factory classes
    """
    offset = plugin.placeholder.get_last_plugin_position(plugin.language) or 0
    return offset + 1


def get_plugin_language(plugin):
    """Helper function to get the language from a plugin's relationships.
    Use this in plugin factory classes
    """
    if plugin.placeholder.source:
        return plugin.placeholder.source.language


class SnippetPluginFactory(factory.django.DjangoModelFactory):
    plugin_type = "SnippetPlugin"
    parent = None
    snippet_grouper = factory.SubFactory(SnippetGrouperFactory)
    placeholder = factory.SubFactory(PlaceholderFactory)
    position = factory.LazyAttribute(get_plugin_position)
    language = factory.LazyAttribute(get_plugin_language)

    class Meta:
        model = SnippetPtr
