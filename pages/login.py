from flask import Blueprint, current_app, session
from .utils import sender
from settings import Config


class Root:
    def is_debugging(self):
        return self.engine.debug

    def __init__(self, engine, path="./pages/login"):
        self.engine = engine

        self.parent = Blueprint(
            "Login",
            __name__,
            url_prefix="/login",
            template_folder=path
        )
        self.mobile_platform = ['android', 'iphone', 'blackberry']

        @self.parent.route("/<any(css, img, js, media):folder>/<path:filename>")
        def statics(folder, filename):
            print(f"{path}/", f"{folder}/{filename}")
            return sender.send_raw(f"{path}/", f"{folder}/{filename}")

        @self.parent.route('/')
        def root(*_, **__):
            return sender.render_template(
                self,
                "index.html",
                navbar_active="login",
                oauth=Config().get("OAuth")
            )

        @self.parent.route("/out")
        def logout(*_, **__):
            session.clear()
            return sender.render_template(
                self,
                "logout.html"
            )


def setup(engine):
    engine.register_blueprint(Root(engine).parent)