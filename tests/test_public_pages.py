import pytest


@pytest.mark.parametrize("path", ["/", "/impressum.html", "/datenschutz.html"])
def test_public_pages_return_200(client, path):
    response = client.get(path)

    assert response.status_code == 200


@pytest.mark.parametrize(
    "path",
    [
        "/static/style.css",
        "/static/logo.png",
        "/static/assets/favicons/favicon-32x32.png",
        "/static/assets/logo/logo-master.svg",
        "/static/assets/hero/airpods-reunion-hero.mp4",
        "/static/assets/airpods/products/web/airpods-pro-2-with-case-front.png",
    ],
)
def test_representative_static_assets_return_200(client, path):
    response = client.get(path)

    assert response.status_code == 200
