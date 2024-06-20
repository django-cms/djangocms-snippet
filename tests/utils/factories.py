import string

import factory
from cms.models import Placeholder
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from factory.fuzzy import FuzzyInteger, FuzzyText

from djangocms_snippet.models import Snippet, SnippetGrouper, SnippetPtr

try:
    from djangocms_versioning.models import Version
except ImportError:
    from tests.utils.models import Version


class UserFactory(factory.django.DjangoModelFactory):
    username = FuzzyText(length=12)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.LazyAttribute(lambda u: f"{u.first_name.lower()}.{u.last_name.lower()}@example.com")

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
    content_type = factory.LazyAttribute(lambda o: ContentType.objects.get_for_model(o.content))
    created_by = factory.SubFactory(UserFactory)

    class Meta:
        exclude = ("content",)
        abstract = True


class PlaceholderFactory(factory.django.DjangoModelFactory):
    default_width = FuzzyInteger(0, 25)
    slot = FuzzyText(length=2, chars=string.digits)
    # NOTE: When using this factory you will probably want to set
    # the source field manually

    class Meta:
        model = Placeholder


class SnippetGrouperFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SnippetGrouper


class AbstractSnippetFactory(factory.django.DjangoModelFactory):
    name = FuzzyText(length=12)
    slug = FuzzyText(length=12)
    snippet_grouper = factory.SubFactory(SnippetGrouperFactory)
    html = ""
    template = ""

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
    if hasattr(plugin.placeholder, "get_last_plugin_position"):
        # Placeholder is a CMS v4 Placeholder
        return (plugin.placeholder.get_last_plugin_position(language=plugin.language) or 0) + 1
    last_plugin_pos = (
        plugin.placeholder.cmsplugin_set.filter(
            parent=None,
            language=plugin.language,
        )
        .aggregate(models.Max("position"))
        .get("position__max")
    )
    offset = (last_plugin_pos or -1) + 1
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
