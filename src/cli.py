import asyncio
import json
from TikTokApi import TikTokApi
import asyncio
import sys
import os
from pyrogram import Client
from const import *
from upload import upload_video
from db import *
import pyfiglet
from simple_term_menu import TerminalMenu
from time import sleep


def show_banner():
    banner = pyfiglet.Figlet(font="big")
    text = f"Tiktok Dumper"
    render = banner.renderText(text=text)
    cls()
    print(f"{GREEN}{render}{RESET}\n{GREEN}Version: {RED}1.0.0\n")


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def setup():

    # Create dirs
    if not os.path.isdir(COOKIES_PATH):
        os.mkdir(COOKIES_PATH)

    if not os.path.isdir(VIDEOS_PATH):
        os.mkdir(VIDEOS_PATH)

    if not os.path.isdir(TELEGRAM_SESSIONS_PATH):
        os.mkdir(TELEGRAM_SESSIONS_PATH)


async def create_session(profile: str):
    """Create a new session, save the cookies and return it"""
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens="ms_token", num_sessions=1, sleep_after=5)
        session = api._get_session()
        cookie = await api.get_session_cookies(session[1])
        with open(file=f"cookies/{profile}.json", mode="w", encoding="utf-8") as file:
            json.dump(obj=cookie, fp=file, indent=4)

        return session


def get_cookie(profile: str):
    """Read the session file and returns the cookies"""
    # TODO with new account it gives "FileNotFoundError"

    with open(file=f"cookies/{profile}.json", mode="r", encoding="utf-8") as file:
        cookie = json.loads(file.read())
    return cookie


async def dump_channel_videos(profile: str, profileDump: str, videosCount: int):

    cookie = get_cookie(profile)
    ms_token = cookie["msToken"]
    videoUrls = []

    # TODO Add the proxy usage while scraping videos from tiktok
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=10, cookies=[cookie])
        try:
            async for video in api.user(username=profileDump).videos(count=videosCount):
                username = video.author.username
                videoId = video.id
                description = video.as_dict['desc']
                song = video.sound.as_dict['music']['title']
                if song == "original sound":
                    song = None

                url = f"https://www.tiktok.com/@{username}/video/{videoId}"

                videoDict = {
                    "videoId": videoId,
                    "url": url,
                }

                update_video(videoId, username, description,
                             song, url, profile)

                videoUrls.append(videoDict)
        except KeyError:
            print(f"{GREEN}The user {RED}{profileDump}{GREEN} was not found!")
            await asyncio.sleep(5)
            return

        await api.close_sessions()
        return await telegram_download(videoUrls)


# Telegram

async def telegram_download(videoUrls: list):
    """Connect, get the videos without the watermark and then delete them from the chat"""
    db, cursor = get_connection()
    print(f"{GREEN}Videos found: {len(videoUrls)}{RESET}")
    async with Client("telegram_session/bot") as client:
        for index, videoDict in enumerate(videoUrls):
            index += 1
            videoId = videoDict['videoId']
            url = videoDict['url']

            if not check_if_video_downloaded(videoId, cursor):
                initialMessage = await client.send_message("tikwatermark_remover_bot", url)
                initialMessageId = initialMessage.id + 2
                await asyncio.sleep(SLEEP_BETWEEN_SCRAPE_TELEGRAM_VIDEO)

                reponseMessage = await client.get_messages("tikwatermark_remover_bot", initialMessageId)
                await client.download_media(reponseMessage, file_name=f"videos/{videoId}.mp4")
                update_downloaded_video(videoId, cursor)
                print(
                    f"{GREEN}Video {RED}{videoId} {GREEN}downloaded{RESET} - {index}/{len(videoUrls)}")
            else:
                print(
                    f"{GREEN}Video {RED}{videoId} {GREEN}already downloaded{RESET} - {index}/{len(videoUrls)}")
    db.close()
    print(f"{GREEN}Process ended correctly!{RESET}")
    await asyncio.sleep(10)
    show_banner()


def main_menu():
    show_banner()
    main_menu_title = f"Choose an option:\nPress Q or Esc to quit. \n"
    main_menu_items = ["Add profile", "Delete profile",
                       "Download videos", "Upload Videos", "Exit"]
    main_menu_exit = False

    main_menu = TerminalMenu(
        menu_entries=main_menu_items,
        title=main_menu_title,
        menu_cursor=MENU_CURSOR,
        menu_cursor_style=MENU_CURSOR_STYLE,
        menu_highlight_style=MENU_HIGHLIGHT_STYLE,
        cycle_cursor=True,
        clear_screen=False
    )

    while not main_menu_exit:
        main_sel = main_menu.show()

        if main_sel == 0:
            add_profile()
        elif main_sel == 1:
            delete_profile()
        elif main_sel == 2:
            download_video()
        elif main_sel == 3:
            upload()
        elif main_sel == 4 or main_sel == None:
            main_menu_exit = True
            sys.exit(0)


def show_profiles(profiles, profilesOptions):
    for profile in profiles:
        option = f"{profile[1]} - {profile[2]}"
        profilesOptions.append(option)

    profileTitle = f"Choose one profile:\nPress Q or Esc to quit. \n"
    profilesMenu = TerminalMenu(
        menu_entries=profilesOptions,
        title=profileTitle,
        menu_cursor=MENU_CURSOR,
        menu_cursor_style=MENU_CURSOR_STYLE,
        menu_highlight_style=MENU_HIGHLIGHT_STYLE,
        cycle_cursor=True,
        show_multi_select_hint=True,
        clear_screen=False,
    )

    profilesIndex = profilesMenu.show()
    return profilesIndex


def add_profile():
    addProfileTitle = f"Choose the platform:\nPress Q or Esc to quit."
    platformOptions = ["tiktok", "youtube", "instagram"]
    platformMenu = TerminalMenu(
        menu_entries=platformOptions,
        title=addProfileTitle,
        menu_cursor=MENU_CURSOR,
        menu_cursor_style=MENU_CURSOR_STYLE,
        menu_highlight_style=MENU_HIGHLIGHT_STYLE,
        cycle_cursor=True,
        show_multi_select_hint=True,
        clear_screen=False,
    )

    username = input(f"{GREEN}Enter your username: {RESET}")
    platformIndex = platformMenu.show()
    if platformIndex is None:
        return

    platform = platformOptions[platformIndex]
    cls()
    show_banner()
    print(
        f"{GREEN}Username: {RED}{username} {RESET}- {GREEN}Platform {RED}{platform}{RESET}")

    if db_add_profile(username, platform):
        print(f"{GREEN}Profile added correctly\nRemember to add the cookies file for this profile in '{COOKIES_PATH}', and rename the file with the username -> '<username>.txt'{RESET}")
        sleep(10)
        cls()
        show_banner()
    else:
        print(f"{RED}Something went wrong...{RESET}")
        sleep(2)
        cls()
        show_banner()


def delete_profile():
    profilesOptions = []
    profiles = get_profiles()

    for profile in profiles:
        option = f"{profile[1]} - {profile[2]}"
        profilesOptions.append(option)

    deleteProfileTitle = f"Choose one or more profile to delete:\nPress Q or Esc to quit. \n"
    deleteProfileMenu = TerminalMenu(
        menu_entries=profilesOptions,
        title=deleteProfileTitle,
        menu_cursor=MENU_CURSOR,
        menu_cursor_style=MENU_CURSOR_STYLE,
        menu_highlight_style=MENU_HIGHLIGHT_STYLE,
        multi_select=True,
        cycle_cursor=True,
        show_multi_select_hint=True,
        clear_screen=False,
    )

    deleteProfileIndex = deleteProfileMenu.show()

    if deleteProfileIndex is None:
        return

    for index in deleteProfileIndex:
        profileId = profiles[index][0]
        username = profiles[index][1]
        db_delete_profile(profileId)
        print(f"{GREEN}Profile {RED}{username}{GREEN} eliminated correctly{RESET}")
        sleep(3)
        show_banner()


def download_video():
    profilesOptions = []
    profiles = get_profiles()

    profilesIndex = show_profiles(profiles, profilesOptions)

    if profilesIndex is None:
        return

    profile = profiles[profilesIndex][1]

    profileDump = input(
        f"{GREEN}Enter the username of the channel u want to dump: {RESET}")

    if len(profileDump) < 3:
        print(f"{RED}The username is not valid, try again...{RESET}")
        sleep(2)
        return

    try:
        videosCount = int(input(
            f"{GREEN}Enter the number of videos to dump (does not change much, even with count = 1 it will download at least 10): {RESET}"))
    except ValueError:
        print(f"{RED}Enter a valid number next time, try again...{RESET}")
        sleep(2)
        return

    show_banner()
    print(f"{GREEN}Starting process...{RESET}")

    asyncio.run(dump_channel_videos(profile, profileDump, videosCount))


def upload():
    profilesOptions = []
    profiles = get_profiles()

    profilesIndex = show_profiles(profiles, profilesOptions)

    if profilesIndex is None:
        return

    profile = profiles[profilesIndex][1]

    videosOptions = []
    videosAvailable = get_videos(profile)

    for video in videosAvailable:
        option = f"{video[1]} - {video[3]} - {video[4]}"
        videosOptions.append(option)

    chooseVideoTitle = f"Choose a video to upload:\nPress Q or Esc to quit. \n"
    chooseVideoMenu = TerminalMenu(
        menu_entries=videosOptions,
        title=chooseVideoTitle,
        menu_cursor=MENU_CURSOR,
        menu_cursor_style=MENU_CURSOR_STYLE,
        menu_highlight_style=MENU_HIGHLIGHT_STYLE,
        cycle_cursor=True,
        show_multi_select_hint=True,
        clear_screen=False,
    )

    chooseVideoIndex = chooseVideoMenu.show()

    if chooseVideoIndex is None:
        return

    videoId = videosAvailable[chooseVideoIndex][0]
    description = videosAvailable[chooseVideoIndex][2]
    song = videosAvailable[chooseVideoIndex][3]

    upload_video(f"videos/{videoId}.mp4", description=description,
                 song=song, profile=profile, cookies=f"cookies/{profile}.txt", headless=False, browser='chrome')

    os.remove(f"videos/{videoId}.mp4")
    update_uploaded_video(videoId)
    sleep(10)
    show_banner()


if __name__ == "__main__":
    setup()
    setup_database()
    main_menu()


# respectsofficial2
