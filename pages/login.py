from flask import Blueprint, session, request, redirect
from .utils import sender
from settings import Config
from requests import get


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
            if not session.get("credentials") or not session.get("credentials")['logged_in']:
                return sender.render_template(
                    self,
                    "index.html",
                    navbar_active="login",
                    oauth=Config().get("OAuth"),
                    redirect_uri=request.args.get("redirect_uri", "/")
                )
            return redirect(request.args.get("redirect_uri", "/"), 302)

        # Replace # to ?
        @self.parent.route("/callback")
        def callback(*_, **__):
            return sender.render_template(self, "replace.html")

        @self.parent.route("/handle")
        def handle(*_, **__):
            token = request.args.get("access_token")

            if token:
                _data = get("https://content.googleapis.com/plus/v1/people/me",
                            headers={"Authorization": f"Bearer {token}"})

                if not _data:
                    return sender.render_template(self, "failed.html", reason="부정확한 로그인 정보입니다.")

                try:
                    _json = _data.json()
                    if "displayName" not in _json:
                        return sender.render_template(self, "failed.html", reason="로그인 정보를 찾을 수 없습니다.")

                    _display_name = _json['displayName']

                    session['credentials'] = {
                        "logged_in": True,
                        "token": token,
                        "display_name": _display_name
                    }
                    return sender.render_template(self, "success.html")
                except Exception as ex:
                    return sender.render_template(self, "failed.html", reason=repr(ex))

        @self.parent.route("/out")
        def logout(*_, **__):
            session.clear()
            return sender.render_template(
                self,
                "logout.html"
            )


def setup(engine):
    engine.register_blueprint(Root(engine).parent)