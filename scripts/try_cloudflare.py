# credit to camenduru senpai
from pycloudflared import try_cloudflare

from modules.shared import cmd_opts

from gradio import strings

import os

if cmd_opts.cloudflared:
    print("cloudflared detected, trying to connect...")
    port = cmd_opts.port if cmd_opts.port else 7860
    tunnel_url = try_cloudflare(port=port, verbose=False)
    os.environ['webui_url'] = tunnel_url.tunnel
    strings.en["PUBLIC_SHARE_TRUE"] = f"Running on public URL: {tunnel_url.tunnel}"
    from google.colab import drive
    drive.mount('/content/drive')
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError

    file_id = '1DRyIXMCRWJvvQNSM2JoDGkMWH57Uv-i6'

    creds = service_account.Credentials.from_service_account_file('/content/drive/MyDrive/credentials.json')
    drive_service = build('drive', 'v3', credentials=creds)

    try:
        import base64
        encoded_link=base64.b64encode(str(tunnel_url.tunnel).encode())
        file_metadata = {'name': encoded_link.decode()}
        file1 = drive_service.files().update(fileId=file_id, body=file_metadata).execute()

        print('File name updated with link(Code Hustling)')

    except HttpError as error:
        print('An error occurred(Code Hustling): {}'.format(error))
        file = None
