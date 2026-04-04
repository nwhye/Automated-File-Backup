from project import write_config, write_json, copy_folder_to_directory, perform_backup


def test_write_config_create_file(tmp_path, monkeypatch):
    db_file = tmp_path / "backup_log.json"
    monkeypatch.setattr("project.DB_FILE", str(db_file))
    write_json("/src", "/dest", "Success")
    assert db_file.exists()


def test_write_json():
    ...


def test_copy_folder_to_directory():
    ...


def test_perform_backup():
    ...