from flask import Blueprint, current_app
from .utils import sender


class Root:
    def is_debugging(self):
        return self.engine.debug

    def __init__(self, engine, path="./pages/create"):
        self.engine = engine

        self.parent = Blueprint(
            "Create",
            __name__,
            url_prefix="/create",
            template_folder=path
        )
        self.mobile_platform = ['android', 'iphone', 'blackberry']

        @self.parent.route('/')
        def root(*_, **__):
            return sender.render_template(
                self,
                "index.html",
                navbar_active="create"
            )

        @self.parent.route("/<any(css, img, js, media):folder>/<path:filename>")
        def statics(folder, filename):
            print(f"{path}/", f"{folder}/{filename}")
            return sender.send_raw(f"{path}/", f"{folder}/{filename}")


def setup(engine):
    engine.register_blueprint(Root(engine).parent)