import mysql.connector as mysql
from dotenv import load_dotenv
from typing import Union
import os

load_dotenv()

MYSQL_HOST = os.environ.get("MYSQL_HOST")
MYSQL_PORT = os.environ.get("MYSQL_PORT")
MYSQL_USER = os.environ.get("MYSQL_USER")
MYSQL_PASS = os.environ.get("MYSQL_PASS")
MYSQL_NAME = os.environ.get("MYSQL_NAME")


def get_connection():
    db = mysql.connect(host=MYSQL_HOST, port=MYSQL_PORT,
                       user=MYSQL_USER, password=MYSQL_PASS, database=MYSQL_NAME, autocommit=True,  charset="utf8mb4",
                       collation="utf8mb4_unicode_ci")
    cursor = db.cursor()
    return db, cursor


def setup_database():
    db, cursor = get_connection()
    profileTable = """
        CREATE TABLE IF NOT EXISTS personal_profile(
            id INT PRIMARY KEY AUTO_INCREMENT,
            username VARCHAR(255),
            platform enum("tiktok", "youtube", "instagram")
        );
    """
    videosTable = """
        CREATE TABLE IF NOT EXISTS videos(
            id BIGINT PRIMARY KEY,
            username VARCHAR(255) not null,
            description VARCHAR(4000),
            song VARCHAR(255),
            url VARCHAR(4000) not null,
            uploaded BOOl,
            downloaded BOOL,
            profile_id INT not null,
            FOREIGN KEY (profile_id) REFERENCES personal_profile(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_unicode_ci;
    """

    queryList = [profileTable, videosTable]

    for query in queryList:
        cursor.execute(query)

    db.close()


def update_video(videoId: int, username: str, description: str, song: Union[str, None], url: str, profile: str):
    db, cursor = get_connection()

    if check_if_video_already_exist(videoId, cursor):
        updateQuery = """
        INSERT INTO videos (id, username, description, song, url, uploaded, downloaded, profile_id) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, (SELECT id from personal_profile where username = %s));
        """

        cursor.execute(updateQuery, (videoId, username,
                                     description, song, url, 0, 0, profile))
        db.close()


def check_if_video_already_exist(videoId: int, cursor) -> bool:
    query = "SELECT * FROM videos WHERE id = %s"

    # Execute the query with the videoId as parameter
    cursor.execute(query, (videoId,))

    # Fetch the result
    result = cursor.fetchone()
    if result is None:
        return True


def check_if_video_downloaded(videoId: int, cursor) -> bool:
    """
    Args:
        videoDict (int): _description_

    Returns:
        bool: True if the video has already been downloaded, False otherwise 
    """
    checkQuery = "SELECT downloaded from videos where id = %s"
    cursor.execute(checkQuery, (videoId,))
    result = cursor.fetchone()[0]

    if result == 1:
        return True

    return False


def check_if_profile_already_exist(profile: str, platform: str, cursor) -> bool:
    checkQuery = "SELECT id from personal_profile where username = %s and platform = %s"
    cursor.execute(checkQuery, (profile, platform))
    result = cursor.fetchone()

    if result is None:
        return False

    return True


def get_videos(profile: str) -> list[set]:
    db, cursor = get_connection()

    getQuery = """SELECT id, description, song FROM videos where uploaded = 0 AND downloaded = 1 AND profile_id = (SELECT id from personal_profile where username = %s)
    """
    cursor.execute(getQuery, (profile,))
    results = cursor.fetchall()
    db.close()
    return results


def update_downloaded_video(videoId: int, cursor) -> None:
    checkQuery = "UPDATE videos set downloaded = 1 where id = %s"
    cursor.execute(checkQuery, (videoId,))


def update_uploaded_video(videoId: int) -> None:
    db, cursor = get_connection()
    checkQuery = "UPDATE videos set uploaded = 1 where id = %s"
    cursor.execute(checkQuery, (videoId,))
    db.close()


def get_remaining_videos(profile: str) -> list[set]:
    raise NotImplementedError


def get_profiles() -> list[set]:
    db, cursor = get_connection()
    cursor.execute("SELECT * from personal_profile")
    results = cursor.fetchall()
    db.close()
    return results


def db_add_profile(profile: str, platform: str) -> bool:
    """return true if it creates the account"""
    db, cursor = get_connection()

    if not check_if_profile_already_exist(profile, platform, cursor):
        addProfileQuery = "INSERT INTO personal_profile(username, platform) VALUES(%s, %s)"
        cursor.execute(addProfileQuery, (profile, platform))
        db.close()
        return True

    else:
        db.close()
        return False


def db_delete_profile(profileId: int) -> None:
    """return true if it creates the account"""
    db, cursor = get_connection()

    addProfileQuery = "DELETE FROM personal_profile where id = %s"
    cursor.execute(addProfileQuery, (profileId,))
    db.close()
    return True
