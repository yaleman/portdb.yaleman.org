from portdb.generator import render_port, render_section


def test_render_port_uses_zola_front_matter_and_content() -> None:
    rendered = render_port("tcp", 443, "TLS traffic", "_Name:_ https")

    assert 'path = "tcp/443"' in rendered
    assert 'template = "port.html"' in rendered
    assert "TLS traffic\n\n## IANA Data\n\n_Name:_ https" in rendered


def test_render_section_preserves_legacy_category_url() -> None:
    rendered = render_section("udp")

    assert 'aliases = ["/category/udp.html"]' in rendered
    assert "paginate_by = 100" in rendered
