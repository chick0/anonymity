from io import BytesIO
from random import choice
from secrets import token_hex

from flask import Blueprint
from flask import send_file
from captcha.image import ImageCaptcha

from app import redis
from app.ip import get_ip_hash

bp = Blueprint(
    name="captcha",
    import_name="captcha",
    url_prefix="/captcha"
)


@bp.get("/<string:uuid>")
def generate(uuid: str):
    image = ImageCaptcha()
    token = token_hex(3)
    token = token[:choice([4, 4, 4, 4, 5, 5, 5])]

    stream = BytesIO()
    image.generate_image(token).save(stream, format="JPEG")
    stream.seek(0)

    redis.set(
        name=f"{get_ip_hash()}:{uuid}",
        value=token, ex=3600
    )

    return send_file(
        stream,
        mimetype="image/jpeg",
    )
