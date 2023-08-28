# Tiktok/Youtube/Instagram Dumper - Uploader

The Tiktok-Dumper-Uploader is a powerful script designed for downloading videos from TikTok and re-uploading them without any effort. The script offers a Command-Line Interface (CLI) for multi-account handling, profile management, and proxy support.

![alt text](src/images/tiktok-cli.png?raw=true)

## Features

- **Video Downloads**: Easily download videos from TikTok without watermark, and efficiently re-upload them to the same or alternative platforms.
- **User-Friendly CLI Interface**: The intuitive CLI enables users to interact with the script using straightforward commands and options.
- **Multi-Account Support**: Manage and switch between multiple accounts on various platforms without hassle.
- **Proxy Integration**: Ensure privacy, prevent access limitations, and circumvent IP blocks with robust support for proxy servers.

## Getting Started

Follow these steps to quickly get started with the Tiktok-Dumper-Uploader:
</br>
1. **Clone the Repository**: Begin by cloning this repository to your local machine using the following command:
  ```
  git clone https://github.com/GianlucaIavicoli/Tiktok-Dumper-Uploader.git
  ```
</br>

2. **Install Dependencies**: Navigate to the project directory and install the required dependencies using the following command:
  ```
  pip install -r requirements.txt
  ```

</br>

4. **Configure Environment Variables**: 

a. Rename the `.env.example` file to `.env`.

b. Open the `.env` file in a text editor.

c. Replace the placeholders in the `.env` file with your actual credentials:

- (Optional) Replace `PROXY6_API_KEY` with your APY-KEY for [Proxy6](https://proxy6.net/en/) in order to buy and use proxy.
- Replace `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASS` and `MYSQL_NAME` with your MySQL database credentials.

Make sure to keep this `.env` file secure as it contains sensitive information.

4. **Provide TikTok Account**: To use the Tiktok-Dumper-Uploader, you'll need a TikTok account. If you don't have one, sign up for a TikTok account at [TikTok's official website](https://www.tiktok.com/). You'll use this account to interact with the TikTok platform through the script.

After you've successfully logged into your TikTok account, you need to copy or dump all of its cookies into a text file named as your username, for example, `<username>.txt`. These cookies are required to authenticate your account when using the script.

**Note**: The cookie file (`<username>.txt`) should be placed in `src/cookies/` directory, which can be changed in the `const.py` file.

5. **Run the Script**: Once you've completed the above steps, you're ready to run the script.
Launch the CLI by using the following command:
  ```
  python cli.py
  ```

The CLI will guide you through the process of managing accounts, profiles, and videos.

That's it! You've successfully set up the Tiktok-Dumper-Uploader and can now start downloading and re-uploading videos without any effort.

</br>

## Acknowledgments

We would like to express our gratitude to the following repositories and projects that inspired and supported this tool's development:

- [TikTok-Api](https://github.com/davidteather/TikTok-Api)
- [tiktok-uploader](https://github.com/wkaisertexas/tiktok-uploader)
- [simple-term-menu](https://github.com/IngoMeyer441/simple-term-menu)
- [TikTok Watermark Remover](https://t.me/tikwatermark_remover_bot)

## Future Updates

We're dedicated to enhancing the Tiktok-Dumper-Uploader with upcoming features:

- **YouTube Integration**: Download and upload videos from YouTube, extending content sharing options.

- **Instagram Support**: Integrate Instagram capabilities to manage video download and re-uploads.

- **Reddit Sharing**: Share downloaded content on Reddit effortlessly for broader exposure.

## Contributions

Contributions are welcome! If you'd like to enhance the tool or fix issues, please open an issue or submit a pull request.

## License

This project is licensed under the [Apache License 2.0](LICENSE).

---

**Disclaimer**: This tool is meant for educational and personal use only. The developers are not responsible for any misuse or violation of the terms of service of social media platforms.
