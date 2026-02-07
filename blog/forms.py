from django import forms


class RichTextWidget(forms.Textarea):
    class Media:
        css = {
            "all": (
                "https://cdn.jsdelivr.net/npm/quill@1.3.7/dist/quill.snow.css",
                "blog/admin.css",
            )
        }
        js = (
            "https://cdn.jsdelivr.net/npm/quill@1.3.7/dist/quill.min.js",
            "blog/admin.js",
        )

    def __init__(self, *args, **kwargs):
        attrs = kwargs.pop("attrs", {})
        attrs.setdefault("class", "")
        attrs["class"] = f"{attrs['class']} richtext".strip()
        super().__init__(attrs=attrs, *args, **kwargs)
