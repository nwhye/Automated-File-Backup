from project import write_config, write_json, copy_folder_to_directory, perform_backup
import pytest


def test_write_config(tmp_path, monkeypatch):
    # exit on invalid schedule type
    source = tmp_path / "source"
    source.mkdir()
    dest = tmp_path / "dest"
    dest.mkdir()

    answers = iter([str(source), str(dest), "weekly"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    with pytest.raises(SystemExit):
        write_config()


def test_write_json(tmp_path, monkeypatch):
    # create JSON if it does not exist
    db_file = tmp_path / "backup_log.json"
    monkeypatch.setattr("project.DB_FILE", str(db_file))
    write_json("/src", "/dest", "Success")
    assert db_file.exists()


def test_copy_folder_to_directory():
    # check that folder and inside files copied to the dest
    source = tmp_path / "source"
    source.mkdir()
    dest = tmp_path / "dest"
    dest.mkdir()

    monkeypatch.setattr("project.DB_FILE", str(tmp_path / "backup_log.json"))

    copy_folder_to_directory(str(source), str(dest))

    today = str(__import__("datetime").date.today())
    assert (dest / today).exists()


def test_perform_backup(tmp_path, monkeypatch, capsys):
    # after completion function print message
    source = tmp_path / "source"
    source.mkdir()
    dest = tmp_path / "dest"
    dest.mkdir()

    db_file = tmp_path / "backup_log.json"
    monkeypatch.setattr("project.DB_FILE", str(db_file))

    perform_backup(str(source), str(dest))

    captured = capsys.readouterr()
    assert "Backup routine finished" in captured.out