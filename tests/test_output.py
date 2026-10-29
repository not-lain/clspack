from clspack import pack
from external import Placeholder


def test_default_does_not_print(capsys):
    result = pack(Placeholder)
    assert isinstance(result, str)
    assert capsys.readouterr().out == ""


def test_print_output(capsys):
    result = pack(Placeholder, print_output=True)
    assert capsys.readouterr().out == result + "\n"


def test_output_file_str(tmp_path):
    path = tmp_path / "packed.py"
    result = pack(Placeholder, output_file=str(path))
    assert path.read_text(encoding="utf-8") == result + "\n"


def test_output_file_path(tmp_path):
    path = tmp_path / "packed.py"
    result = pack(Placeholder, output_file=path)
    assert path.read_text(encoding="utf-8") == result + "\n"


def test_print_and_save(tmp_path, capsys):
    path = tmp_path / "packed.py"
    result = pack(Placeholder, output_file=path, print_output=True)
    assert capsys.readouterr().out == result + "\n"
    assert path.read_text(encoding="utf-8") == result + "\n"


def test_default_does_not_create_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    pack(Placeholder)
    assert list(tmp_path.iterdir()) == []
