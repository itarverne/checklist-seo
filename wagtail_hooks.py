from wagtail.core import hooks
from django.utils.html import format_html
from django.templatetags.static import static




@hooks.register("insert_editor_js")
def editor_js():
    return format_html(
        '<script src="{}"></script><script src="{}"></script>',
        static("js/helper.js"),
        static("js/seoSidePannel.js")
    )


@hooks.register("insert_editor_css")
def editor_css():
    return format_html(
        '<link rel="stylesheet" href="{}" type="text/css">',
        static("css/seo.css")
    )
